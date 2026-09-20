"""
run_evaluation.py
-----------------
Fresh, rigorous, scientifically fair evaluation and comparison of:
  1. Standard DQN
  2. Double DQN
  3. Dueling DQN (+ PER)

Ensures 100% fair baseline:
  - Same environment (SimulatedLearner)
  - Same state space (13 dimensions)
  - Same action space (27 discrete actions)
  - Same reward function
  - Same training hyperparameters (lr=1e-3, gamma=0.95, batch=32, eps=1.0->0.05, 300 episodes)
  - Same evaluation protocol (200 episodes per seed, greedy exploration disabled)
  - Same 5 random seeds: [42, 101, 202, 303, 404]
  - Total: 1,000 evaluation episodes per algorithm (3,000 episodes overall)

Generates:
  - results/dqn_results.csv
  - results/double_dqn_results.csv
  - results/dueling_dqn_results.csv
  - results/combined_results.csv
  - results/summary_metrics.csv
  - config.json
  - graphs/*.png (separate graph for EVERY metric + training curves)
  - report/rl_comparison_report.md
"""

import os
import sys
import json
import time
import random
import importlib.util
from typing import Dict, List, Any, Tuple
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────────────────────
# Paths & Setup
# ─────────────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EVAL_DIR = os.path.join(BASE_DIR, "evaluation")
RESULTS_DIR = os.path.join(EVAL_DIR, "results")
GRAPHS_DIR = os.path.join(EVAL_DIR, "graphs")
REPORT_DIR = os.path.join(EVAL_DIR, "report")

for d in [RESULTS_DIR, GRAPHS_DIR, REPORT_DIR]:
    os.makedirs(d, exist_ok=True)

# Add DQN backend to sys.path for internal imports like 'environment'
dqn_backend_dir = os.path.join(BASE_DIR, "DQN", "backend")
if dqn_backend_dir not in sys.path:
    sys.path.insert(0, dqn_backend_dir)

# ─────────────────────────────────────────────────────────────────────────────
# Import Agents and Environment Dynamically to Avoid Namespace Collision
# ─────────────────────────────────────────────────────────────────────────────
def load_module_from_path(module_name: str, file_path: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec for {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

dqn_module = load_module_from_path("dqn_pkg", os.path.join(BASE_DIR, "DQN", "backend", "dqn_agent.py"))
ddqn_module = load_module_from_path("ddqn_pkg", os.path.join(BASE_DIR, "Double_DQN", "backend", "dqn_agent.py"))
dueling_module = load_module_from_path("dueling_pkg", os.path.join(BASE_DIR, "Dueling_DQN", "backend", "dqn_agent.py"))

env_module = load_module_from_path("env_pkg", os.path.join(BASE_DIR, "DQN", "backend", "environment.py"))
sim_module = load_module_from_path("sim_pkg", os.path.join(BASE_DIR, "DQN", "backend", "simulated_learner.py"))

StandardDQNAgent = dqn_module.StandardDQNAgent
DoubleDQNAgent = ddqn_module.DoubleDQNAgent
DuelingDQNAgent = dueling_module.DoubleDQNAgent # Dueling Double DQN class
SimulatedLearner = sim_module.SimulatedLearner

STATE_DIM = env_module.STATE_DIM
ACTION_DIM = env_module.ACTION_DIM
TOPICS = env_module.TOPICS
DIFFICULTIES = env_module.DIFFICULTIES

# ─────────────────────────────────────────────────────────────────────────────
# Experiment Configuration
# ─────────────────────────────────────────────────────────────────────────────
SEEDS = [42, 101, 202, 303, 404]
TRAINING_EPISODES = 300
EVALUATION_EPISODES = 200
MAX_STEPS_PER_EPISODE = 12

HYPERPARAMETERS = {
    "state_dim": STATE_DIM,
    "action_dim": ACTION_DIM,
    "hidden_dim": 64,
    "learning_rate": 0.001,
    "gamma": 0.95,
    "epsilon_start": 1.0,
    "epsilon_min": 0.05,
    "epsilon_decay": 0.995,
    "replay_buffer_size": 10000,
    "batch_size": 32,
    "target_update_frequency": 25,
    "max_steps_per_episode": MAX_STEPS_PER_EPISODE,
    "training_episodes": TRAINING_EPISODES,
    "evaluation_episodes_per_seed": EVALUATION_EPISODES,
    "seeds": SEEDS,
    "total_evaluation_episodes_per_algo": len(SEEDS) * EVALUATION_EPISODES,
}

ALGORITHMS = {
    "DQN": {
        "class": StandardDQNAgent,
        "name": "Standard DQN",
        "color": "#2563EB",
        "description": "Standard Q-Network with direct single-stream mapping, standard max-target, uniform replay.",
    },
    "Double DQN": {
        "class": DoubleDQNAgent,
        "name": "Double DQN",
        "color": "#059669",
        "description": "Decoupled target network evaluation (argmax online, eval target), uniform replay.",
    },
    "Dueling DQN": {
        "class": DuelingDQNAgent,
        "name": "Dueling DQN",
        "color": "#7C3AED",
        "description": "Dueling network with separated Value and Advantage streams + PER.",
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# Helper: Train an Agent
# ─────────────────────────────────────────────────────────────────────────────
def train_agent(algo_name: str, agent_class, seed: int, episodes: int = TRAINING_EPISODES):
    random.seed(seed)
    np.random.seed(seed)

    agent = agent_class(
        state_dim=STATE_DIM,
        action_dim=ACTION_DIM,
        hidden_dim=64,
        lr=1e-3,
        gamma=0.95,
        epsilon_start=1.0,
        epsilon_min=0.05,
        epsilon_decay=0.995,
        buffer_capacity=10000,
        batch_size=32,
        target_update_every=25,
        seed=seed,
    )

    env = SimulatedLearner(seed=seed)
    train_log = {
        "episode": [],
        "reward": [],
        "loss": [],
        "epsilon": [],
    }

    for ep in range(1, episodes + 1):
        state = env.reset()
        ep_reward = 0.0
        step_losses = []

        for step in range(MAX_STEPS_PER_EPISODE):
            action, _ = agent.act(state, explore=True)
            next_state, reward, done, info = env.step(action)
            agent.remember(state, action, reward, next_state, done)
            loss = agent.replay()
            if loss is not None:
                step_losses.append(loss)
            state = next_state
            ep_reward += reward
            if done:
                break

        train_log["episode"].append(ep)
        train_log["reward"].append(ep_reward)
        train_log["loss"].append(float(np.mean(step_losses)) if step_losses else 0.0)
        train_log["epsilon"].append(agent.epsilon)

    return agent, train_log

# ─────────────────────────────────────────────────────────────────────────────
# Helper: Evaluate an Agent in Pure Greedy Evaluation Mode
# ─────────────────────────────────────────────────────────────────────────────
def evaluate_agent(
    algo_name: str,
    agent,
    seed: int,
    episodes: int = EVALUATION_EPISODES,
) -> List[Dict[str, Any]]:
    """
    Evaluates agent with exploration disabled (greedy), no training, no buffer push.
    Learner seed is deterministic (seed * 10000 + ep) so ALL ALGORITHMS face the
    EXACT SAME sequence of simulated learners.
    """
    records = []

    # Required target role skills for coverage evaluation (representative role: DevOps / Data / ML)
    target_role_topics = ["Python", "Machine Learning", "MLOps", "Data Engineering", "DevOps"]

    for ep in range(1, episodes + 1):
        eval_seed = seed * 10000 + ep
        env = SimulatedLearner(seed=eval_seed)
        state = env.reset()

        initial_mastery = dict(env.mastery)
        initial_skill_gap = float(np.mean([1.0 - initial_mastery[t] for t in target_role_topics]))
        initial_progress = float(np.mean(list(initial_mastery.values())))

        total_reward = 0.0
        q_values_collected = []
        quiz_scores = []
        code_scores = []
        successful_recs = 0
        step_count = 0
        step_to_goal = MAX_STEPS_PER_EPISODE # default if not reached

        for step in range(MAX_STEPS_PER_EPISODE):
            step_count += 1
            action, q_vals = agent.act(state, explore=False)
            q_values_collected.append(float(np.max(q_vals)))

            next_state, reward, done, info = env.step(action)
            total_reward += reward
            quiz_scores.append(info["quiz_score"])
            code_scores.append(info["code_score"])

            # Recommendation success condition: positive reward & passing quiz
            if reward > 0.0 and info["quiz_score"] >= 60.0:
                successful_recs += 1

            # Check if skill goal reached (mastery of target topics >= 0.70)
            cur_target_mastery = np.mean([env.mastery[t] for t in target_role_topics])
            if cur_target_mastery >= 0.70 and step_to_goal == MAX_STEPS_PER_EPISODE:
                step_to_goal = step_count

            state = next_state
            if done:
                break

        final_mastery = dict(env.mastery)
        final_skill_gap = float(np.mean([1.0 - final_mastery[t] for t in target_role_topics]))
        skill_gap_reduction = float(initial_skill_gap - final_skill_gap)
        skill_gap_reduction_pct = float(
            (skill_gap_reduction / initial_skill_gap * 100.0) if initial_skill_gap > 1e-6 else 0.0
        )

        initial_quiz = float(quiz_scores[0]) if quiz_scores else 0.0
        final_quiz = float(quiz_scores[-1]) if quiz_scores else 0.0
        quiz_improvement = float(final_quiz - initial_quiz)
        avg_quiz_score = float(np.mean(quiz_scores)) if quiz_scores else 0.0

        final_progress = float(np.mean(list(final_mastery.values())))
        learning_progress_improvement = float(final_progress - initial_progress)

        # Course completion: Topics reaching mastery >= 0.75
        completed_courses = sum(1 for m in final_mastery.values() if m >= 0.75)
        course_completion_rate = float((completed_courses / len(TOPICS)) * 100.0)

        # Video completion rate: steps completed relative to max session videos (4 per topic * 3 topics = 12 videos)
        video_completion_rate = float((step_count / MAX_STEPS_PER_EPISODE) * 100.0)

        # Target role skill coverage: Topics in target role reaching mastery >= 0.50
        covered_skills = sum(1 for t in target_role_topics if final_mastery[t] >= 0.50)
        target_skill_coverage = float((covered_skills / len(target_role_topics)) * 100.0)

        recommendation_success_rate = float((successful_recs / step_count) * 100.0) if step_count > 0 else 0.0

        # Success condition: Average quiz score >= 60% AND Net positive reward
        episode_success = bool(avg_quiz_score >= 60.0 and total_reward > 0.0)

        avg_q = float(np.mean(q_values_collected)) if q_values_collected else 0.0
        std_q = float(np.std(q_values_collected)) if q_values_collected else 0.0

        rec = {
            "algorithm": algo_name,
            "seed": seed,
            "episode": ep,
            "reward": float(total_reward),
            "episode_length": step_count,
            "success": int(episode_success),
            "skill_gap_initial": initial_skill_gap,
            "skill_gap_final": final_skill_gap,
            "skill_gap_reduction": skill_gap_reduction,
            "skill_gap_reduction_pct": skill_gap_reduction_pct,
            "quiz_initial": initial_quiz,
            "quiz_final": final_quiz,
            "quiz_improvement": quiz_improvement,
            "avg_quiz_score": avg_quiz_score,
            "course_completion": course_completion_rate,
            "video_completion": video_completion_rate,
            "learning_progress_initial": initial_progress,
            "learning_progress_final": final_progress,
            "learning_progress_improvement": learning_progress_improvement,
            "target_skill_coverage": target_skill_coverage,
            "recommendation_success": recommendation_success_rate,
            "steps_to_skill_goal": step_to_goal,
            "average_q_value": avg_q,
            "std_q_value": std_q,
        }
        records.append(rec)

    return records

# ─────────────────────────────────────────────────────────────────────────────
# Helper: Calculate Convergence Speed
# ─────────────────────────────────────────────────────────────────────────────
def calculate_convergence(moving_rewards: np.ndarray, threshold: float, window: int = 10, persist_len: int = 10) -> Any:
    """
    First episode where moving-average reward reaches and maintains at least
    90% of final eval performance for persist_len consecutive episodes.
    """
    for i in range(len(moving_rewards) - persist_len + 1):
        window_vals = moving_rewards[i : i + persist_len]
        if np.all(window_vals >= threshold):
            return int(i + window)
    return "Not reached"

# ─────────────────────────────────────────────────────────────────────────────
# Main Evaluation Orchestration
# ─────────────────────────────────────────────────────────────────────────────
def main():
    print("=" * 70)
    print("SKILLPATH AI — FRESH REINFORCEMENT LEARNING BENCHMARK EVALUATION")
    print("=" * 70)
    print(f"Algorithms: {list(ALGORITHMS.keys())}")
    print(f"Seeds: {SEEDS}")
    print(f"Training Episodes per run: {TRAINING_EPISODES}")
    print(f"Evaluation Episodes per run: {EVALUATION_EPISODES} (Greedy)")
    print(f"Total Evaluation Episodes: {len(SEEDS) * EVALUATION_EPISODES * len(ALGORITHMS):,}")
    print("=" * 70)

    start_total_time = time.time()

    all_eval_records = []
    training_histories = {algo: [] for algo in ALGORITHMS}
    trained_agents = {algo: [] for algo in ALGORITHMS}

    # 1. Execute Training & Evaluation
    for algo_key, algo_info in ALGORITHMS.items():
        print(f"\n>>> Running Benchmark for: {algo_key}")
        algo_class = algo_info["class"]

        for seed in SEEDS:
            t0 = time.time()
            print(f"  [Seed {seed}] Training {TRAINING_EPISODES} episodes...", end="", flush=True)
            agent, train_log = train_agent(algo_key, algo_class, seed, TRAINING_EPISODES)
            train_duration = time.time() - t0
            print(f" Done ({train_duration:.2f}s). Evaluating {EVALUATION_EPISODES} greedy episodes...", end="", flush=True)

            training_histories[algo_key].append(train_log)
            trained_agents[algo_key].append(agent)

            t1 = time.time()
            eval_records = evaluate_agent(algo_key, agent, seed, EVALUATION_EPISODES)
            eval_duration = time.time() - t1
            print(f" Done ({eval_duration:.2f}s). Mean Reward: {np.mean([r['reward'] for r in eval_records]):+.3f}")

            all_eval_records.extend(eval_records)

    # 2. Save Raw Evaluation Data CSVs
    print("\n>>> Exporting Raw Evaluation Datasets to CSV...")
    df_all = pd.DataFrame(all_eval_records)
    combined_csv_path = os.path.join(RESULTS_DIR, "combined_results.csv")
    df_all.to_csv(combined_csv_path, index=False)
    print(f"  Saved: {combined_csv_path} ({len(df_all)} rows)")

    for algo_key in ALGORITHMS:
        slug = algo_key.lower().replace(" ", "_")
        csv_path = os.path.join(RESULTS_DIR, f"{slug}_results.csv")
        df_algo = df_all[df_all["algorithm"] == algo_key]
        df_algo.to_csv(csv_path, index=False)
        print(f"  Saved: {csv_path} ({len(df_algo)} rows)")

    # 3. Compute Summary Statistics for All 24 Metrics
    print("\n>>> Computing Rigorous Statistical Metrics across Algorithms...")
    summary_rows = []
    stats_dict = {}

    for algo_key in ALGORITHMS:
        df_algo = df_all[df_all["algorithm"] == algo_key]
        rewards = df_algo["reward"].values
        cum_reward = float(np.sum(rewards))
        mean_reward = float(np.mean(rewards))
        std_reward = float(np.std(rewards))
        max_reward = float(np.max(rewards))
        min_reward = float(np.min(rewards))

        # Training loss & average training reward across seeds
        all_losses = [log["loss"] for log in training_histories[algo_key]]
        avg_loss_curve = np.mean(all_losses, axis=0)
        mean_final_loss = float(np.mean(avg_loss_curve[-20:]))

        all_train_rewards = [log["reward"] for log in training_histories[algo_key]]
        avg_train_curve = np.mean(all_train_rewards, axis=0)
        kernel = np.ones(10) / 10.0
        smoothed_train_rewards = np.convolve(avg_train_curve, kernel, mode="valid")

        # Convergence criterion: 90% of final mean reward
        conv_threshold = 0.90 * mean_reward
        conv_ep = calculate_convergence(smoothed_train_rewards, conv_threshold, window=10, persist_len=10)

        ep_len = df_algo["episode_length"].values
        mean_ep_len = float(np.mean(ep_len))
        std_ep_len = float(np.std(ep_len))

        success_rate = float(np.mean(df_algo["success"].values) * 100.0)

        skill_gap_red = df_algo["skill_gap_reduction"].values
        mean_gap_red = float(np.mean(skill_gap_red))
        std_gap_red = float(np.std(skill_gap_red))
        mean_gap_red_pct = float(np.mean(df_algo["skill_gap_reduction_pct"].values))

        quiz_imp = df_algo["quiz_improvement"].values
        mean_quiz_imp = float(np.mean(quiz_imp))
        std_quiz_imp = float(np.std(quiz_imp))
        mean_quiz_score = float(np.mean(df_algo["avg_quiz_score"].values))
        std_quiz_score = float(np.std(df_algo["avg_quiz_score"].values))

        course_comp = float(np.mean(df_algo["course_completion"].values))
        video_comp = float(np.mean(df_algo["video_completion"].values))
        learning_prog = float(np.mean(df_algo["learning_progress_improvement"].values))
        target_cov = float(np.mean(df_algo["target_skill_coverage"].values))
        rec_success = float(np.mean(df_algo["recommendation_success"].values))

        steps_goal = df_algo["steps_to_skill_goal"].values
        mean_steps_goal = float(np.mean(steps_goal))

        q_vals = df_algo["average_q_value"].values
        mean_q = float(np.mean(q_vals))
        std_q = float(np.mean(df_algo["std_q_value"].values))

        # 95% Confidence Interval for mean reward
        n = len(rewards)
        sem = std_reward / np.sqrt(n)
        ci_95 = stats.t.interval(0.95, df=n - 1, loc=mean_reward, scale=sem)

        stats_dict[algo_key] = {
            "mean_reward": mean_reward,
            "std_reward": std_reward,
            "ci_95_reward": [float(ci_95[0]), float(ci_95[1])],
            "cumulative_reward": cum_reward,
            "max_reward": max_reward,
            "min_reward": min_reward,
            "training_loss": mean_final_loss,
            "convergence_episode": conv_ep,
            "mean_episode_length": mean_ep_len,
            "std_episode_length": std_ep_len,
            "success_rate": success_rate,
            "skill_gap_reduction": mean_gap_red,
            "std_gap_reduction": std_gap_red,
            "skill_gap_reduction_pct": mean_gap_red_pct,
            "quiz_improvement": mean_quiz_imp,
            "std_quiz_imp": std_quiz_imp,
            "avg_quiz_score": mean_quiz_score,
            "std_quiz_score": std_quiz_score,
            "course_completion_rate": course_comp,
            "video_completion_rate": video_comp,
            "learning_progress_improvement": learning_prog,
            "target_role_skill_coverage": target_cov,
            "recommendation_success_rate": rec_success,
            "steps_to_skill_goal": mean_steps_goal,
            "average_q_value": mean_q,
            "std_q_value": std_q,
            "training_loss_curve": avg_loss_curve.tolist(),
            "training_reward_curve": avg_train_curve.tolist(),
            "smoothed_train_rewards": smoothed_train_rewards.tolist(),
        }

        summary_rows.append({
            "Algorithm": algo_key,
            "Mean Reward": f"{mean_reward:.4f}",
            "Reward Std": f"{std_reward:.4f}",
            "Cumulative Reward": f"{cum_reward:.2f}",
            "Max Reward": f"{max_reward:.4f}",
            "Min Reward": f"{min_reward:.4f}",
            "Training Loss": f"{mean_final_loss:.5f}",
            "Convergence Episode": str(conv_ep),
            "Average Episode Length": f"{mean_ep_len:.2f}",
            "Episode Length Std": f"{std_ep_len:.2f}",
            "Success Rate (%)": f"{success_rate:.2f}%",
            "Skill Gap Reduction": f"{mean_gap_red:.4f}",
            "Skill Gap Reduction %": f"{mean_gap_red_pct:.2f}%",
            "Quiz Improvement": f"{mean_quiz_imp:+.2f}",
            "Average Quiz Score": f"{mean_quiz_score:.2f}%",
            "Course Completion Rate": f"{course_comp:.2f}%",
            "Video Completion Rate": f"{video_comp:.2f}%",
            "Learning Progress Improvement": f"{learning_prog:.4f}",
            "Target Role Skill Coverage": f"{target_cov:.2f}%",
            "Recommendation Success Rate": f"{rec_success:.2f}%",
            "Steps to Skill Goal": f"{mean_steps_goal:.2f}",
            "Average Q-value": f"{mean_q:.4f}",
            "Q-value Std": f"{std_q:.4f}",
        })

    summary_df = pd.DataFrame(summary_rows)
    summary_csv_path = os.path.join(RESULTS_DIR, "summary_metrics.csv")
    summary_df.to_csv(summary_csv_path, index=False)
    print(f"  Saved: {summary_csv_path}")

    # 4. Perform Pairwise Statistical Hypothesis Testing
    print("\n>>> Performing Pairwise Statistical Tests (Welch's t-test, p-value, Cohen's d)...")
    pairwise_tests = {}
    pairs = [("DQN", "Double DQN"), ("DQN", "Dueling DQN"), ("Double DQN", "Dueling DQN")]

    for a1, a2 in pairs:
        r1 = df_all[df_all["algorithm"] == a1]["reward"].values
        r2 = df_all[df_all["algorithm"] == a2]["reward"].values

        # Welch's t-test (unequal variances assumed)
        t_stat, p_val = stats.ttest_ind(r1, r2, equal_var=False)

        # Cohen's d effect size
        n1, n2 = len(r1), len(r2)
        s1, s2 = np.var(r1, ddof=1), np.var(r2, ddof=1)
        s_pooled = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
        cohens_d = (np.mean(r2) - np.mean(r1)) / s_pooled if s_pooled > 0 else 0.0

        pairwise_tests[f"{a1} vs {a2}"] = {
            "t_statistic": float(t_stat),
            "p_value": float(p_val),
            "statistically_significant_p05": bool(p_val < 0.05),
            "cohens_d": float(cohens_d),
            "mean_diff": float(np.mean(r2) - np.mean(r1)),
            "sample_size_each": n1,
        }

    # 5. Save Experiment Config & Reproducibility Metadata
    config_data = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "python_version": sys.version,
        "platform": sys.platform,
        "experiment_configuration": HYPERPARAMETERS,
        "statistical_tests": pairwise_tests,
        "summary_statistics": {k: {sk: sv for sk, sv in v.items() if not sk.endswith("_curve") and sk != "smoothed_train_rewards"} for k, v in stats_dict.items()},
    }
    config_path = os.path.join(EVAL_DIR, "config.json")
    with open(config_path, "w") as f:
        json.dump(config_data, f, indent=2)
    print(f"  Saved: {config_path}")

    # 6. Generate SEPARATE Individual Graph for EVERY Single Metric (Minimum 24)
    print("\n>>> Generating 24 Individual Metric Graphs + Combined Training Curves...")
    algo_names = list(ALGORITHMS.keys())
    colors = [ALGORITHMS[a]["color"] for a in algo_names]

    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    def save_bar_chart(filename, title, ylabel, values, errors=None, fmt="%.3f", ylim=None):
        fig, ax = plt.subplots(figsize=(7, 5), dpi=150)
        bars = ax.bar(algo_names, values, yerr=errors, capsize=5, color=colors, edgecolor="black", alpha=0.88, width=0.55)
        ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
        ax.set_ylabel(ylabel, fontsize=12, labelpad=8)
        ax.set_xlabel("Algorithm", fontsize=12, labelpad=8)
        ax.grid(axis="y", linestyle="--", alpha=0.6)
        if ylim:
            ax.set_ylim(ylim)

        for bar in bars:
            height = bar.get_height()
            offset = (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.02
            y_pos = height + offset if height >= 0 else height - offset * 2
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                y_pos,
                fmt % height,
                ha="center",
                va="bottom" if height >= 0 else "top",
                fontsize=10,
                fontweight="bold",
            )

        fig.tight_layout()
        save_path = os.path.join(GRAPHS_DIR, filename)
        fig.savefig(save_path)
        plt.close(fig)
        print(f"    Graph saved: {filename}")

    # Graph 1: Average Episode Reward
    save_bar_chart(
        "average_episode_reward.png",
        "Metric 1: Average Episode Reward",
        "Average Episode Reward",
        [stats_dict[a]["mean_reward"] for a in algo_names],
        errors=[stats_dict[a]["std_reward"] for a in algo_names],
        fmt="%.3f",
    )

    # Graph 2: Cumulative Reward
    save_bar_chart(
        "cumulative_reward.png",
        "Metric 2: Cumulative Reward across Evaluation",
        "Total Cumulative Reward",
        [stats_dict[a]["cumulative_reward"] for a in algo_names],
        fmt="%.1f",
    )

    # Graph 3: Reward per Episode (Line Graph)
    fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
    for a in algo_names:
        # 20-episode moving average of evaluation reward across all seeds
        rewards_seq = df_all[df_all["algorithm"] == a]["reward"].values
        k = np.ones(20) / 20.0
        smooth_r = np.convolve(rewards_seq, k, mode="valid")
        ax.plot(smooth_r, label=f"{a} (20-ep rolling)", color=ALGORITHMS[a]["color"], linewidth=2)
    ax.set_title("Metric 3: Reward per Episode Trajectory (Greedy Evaluation)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Evaluation Episode Index", fontsize=12)
    ax.set_ylabel("Episode Reward", fontsize=12)
    ax.legend(frameon=True)
    ax.grid(True, linestyle="--", alpha=0.6)
    fig.tight_layout()
    fig.savefig(os.path.join(GRAPHS_DIR, "reward_per_episode.png"))
    plt.close(fig)
    print("    Graph saved: reward_per_episode.png")

    # Graph 4: Reward Standard Deviation
    save_bar_chart(
        "reward_std.png",
        "Metric 4: Reward Standard Deviation (Stability)",
        "Standard Deviation of Reward",
        [stats_dict[a]["std_reward"] for a in algo_names],
        fmt="%.3f",
    )

    # Graph 5: Maximum Episode Reward
    save_bar_chart(
        "max_reward.png",
        "Metric 5: Maximum Episode Reward",
        "Peak Reward",
        [stats_dict[a]["max_reward"] for a in algo_names],
        fmt="%.3f",
    )

    # Graph 6: Minimum Episode Reward
    save_bar_chart(
        "min_reward.png",
        "Metric 6: Minimum Episode Reward",
        "Minimum Reward",
        [stats_dict[a]["min_reward"] for a in algo_names],
        fmt="%.3f",
    )

    # Graph 7: Training Loss (Line Graph)
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
    for a in algo_names:
        loss_curve = stats_dict[a]["training_loss_curve"]
        ax.plot(range(1, len(loss_curve) + 1), loss_curve, label=a, color=ALGORITHMS[a]["color"], linewidth=2)
    ax.set_title("Metric 7: Training Loss Curve (Huber Loss)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Training Episode", fontsize=12)
    ax.set_ylabel("Huber Loss", fontsize=12)
    ax.legend(frameon=True)
    ax.grid(True, linestyle="--", alpha=0.6)
    fig.tight_layout()
    fig.savefig(os.path.join(GRAPHS_DIR, "training_loss.png"))
    plt.close(fig)
    print("    Graph saved: training_loss.png")

    # Graph 8: Average Training Reward (Line Graph)
    fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
    for a in algo_names:
        sm_rewards = stats_dict[a]["smoothed_train_rewards"]
        ax.plot(range(10, 10 + len(sm_rewards)), sm_rewards, label=a, color=ALGORITHMS[a]["color"], linewidth=2)
    ax.set_title("Metric 8: Average Training Reward (10-Episode Moving Average)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Training Episode", fontsize=12)
    ax.set_ylabel("10-Episode Moving Average Reward", fontsize=12)
    ax.legend(frameon=True)
    ax.grid(True, linestyle="--", alpha=0.6)
    fig.tight_layout()
    fig.savefig(os.path.join(GRAPHS_DIR, "average_training_reward.png"))
    plt.close(fig)
    print("    Graph saved: average_training_reward.png")

    # Graph 9: Convergence Speed
    conv_vals = [
        stats_dict[a]["convergence_episode"] if isinstance(stats_dict[a]["convergence_episode"], (int, float)) else 0
        for a in algo_names
    ]
    save_bar_chart(
        "convergence_speed.png",
        "Metric 9: Convergence Speed (Episodes to 90% Threshold)",
        "Convergence Episode",
        conv_vals,
        fmt="%d",
    )

    # Graph 10: Average Episode Length
    save_bar_chart(
        "episode_length.png",
        "Metric 10: Average Episode Length (Steps per Session)",
        "Steps per Episode",
        [stats_dict[a]["mean_episode_length"] for a in algo_names],
        errors=[stats_dict[a]["std_episode_length"] for a in algo_names],
        fmt="%.2f",
    )

    # Graph 11: Episode Length Standard Deviation
    save_bar_chart(
        "episode_length_std.png",
        "Metric 11: Episode Length Standard Deviation",
        "Standard Deviation of Steps",
        [stats_dict[a]["std_episode_length"] for a in algo_names],
        fmt="%.2f",
    )

    # Graph 12: Success Rate
    save_bar_chart(
        "success_rate.png",
        "Metric 12: Success Rate (Quiz >= 60% & Net Positive Reward)",
        "Success Rate (%)",
        [stats_dict[a]["success_rate"] for a in algo_names],
        fmt="%.2f%%",
        ylim=(0, 105),
    )

    # Graph 13: Skill Gap Reduction
    save_bar_chart(
        "skill_gap_reduction.png",
        "Metric 13: Skill Gap Reduction (Initial Gap - Final Gap)",
        "Mastery Units Reduced",
        [stats_dict[a]["skill_gap_reduction"] for a in algo_names],
        errors=[stats_dict[a]["std_gap_reduction"] for a in algo_names],
        fmt="%.3f",
    )

    # Graph 14: Skill Gap Reduction Percentage
    save_bar_chart(
        "skill_gap_reduction_percentage.png",
        "Metric 14: Skill Gap Reduction Percentage",
        "Skill Gap Reduction (%)",
        [stats_dict[a]["skill_gap_reduction_pct"] for a in algo_names],
        fmt="%.2f%%",
        ylim=(0, 100),
    )

    # Graph 15: Quiz Score Improvement
    save_bar_chart(
        "quiz_score_improvement.png",
        "Metric 15: Quiz Score Improvement (Final Quiz - Initial Quiz)",
        "Score Improvement (%)",
        [stats_dict[a]["quiz_improvement"] for a in algo_names],
        errors=[stats_dict[a]["std_quiz_imp"] for a in algo_names],
        fmt="%+.2f%%",
    )

    # Graph 16: Average Quiz Score
    save_bar_chart(
        "average_quiz_score.png",
        "Metric 16: Average Quiz Score Achieved",
        "Quiz Score (%)",
        [stats_dict[a]["avg_quiz_score"] for a in algo_names],
        errors=[stats_dict[a]["std_quiz_score"] for a in algo_names],
        fmt="%.2f%%",
        ylim=(0, 100),
    )

    # Graph 17: Course Completion Rate
    save_bar_chart(
        "course_completion_rate.png",
        "Metric 17: Course Completion Rate",
        "Courses Completed (%)",
        [stats_dict[a]["course_completion_rate"] for a in algo_names],
        fmt="%.2f%%",
        ylim=(0, 100),
    )

    # Graph 18: Video Completion Rate
    save_bar_chart(
        "video_completion_rate.png",
        "Metric 18: Video Completion Rate",
        "Videos Completed (%)",
        [stats_dict[a]["video_completion_rate"] for a in algo_names],
        fmt="%.2f%%",
        ylim=(0, 105),
    )

    # Graph 19: Learning Progress Improvement
    save_bar_chart(
        "learning_progress.png",
        "Metric 19: Overall Learning Progress Delta",
        "Mastery Delta",
        [stats_dict[a]["learning_progress_improvement"] for a in algo_names],
        fmt="%.4f",
    )

    # Graph 20: Target Role Skill Coverage
    save_bar_chart(
        "target_role_skill_coverage.png",
        "Metric 20: Target Role Skill Coverage",
        "Target Skill Coverage (%)",
        [stats_dict[a]["target_role_skill_coverage"] for a in algo_names],
        fmt="%.2f%%",
        ylim=(0, 100),
    )

    # Graph 21: Recommendation Success Rate
    save_bar_chart(
        "recommendation_success_rate.png",
        "Metric 21: Recommendation Success Rate",
        "Successful Recommendations (%)",
        [stats_dict[a]["recommendation_success_rate"] for a in algo_names],
        fmt="%.2f%%",
        ylim=(0, 100),
    )

    # Graph 22: Average Steps to Skill Goal
    save_bar_chart(
        "steps_to_skill_goal.png",
        "Metric 22: Average Steps to Reach Skill Goal",
        "Steps",
        [stats_dict[a]["steps_to_skill_goal"] for a in algo_names],
        fmt="%.2f",
    )

    # Graph 23: Average Q-value
    save_bar_chart(
        "average_q_value.png",
        "Metric 23: Average Predicted Q-Value (Greedy Evaluation)",
        "Predicted Q-Value",
        [stats_dict[a]["average_q_value"] for a in algo_names],
        fmt="%.3f",
    )

    # Graph 24: Q-value Standard Deviation
    save_bar_chart(
        "q_value_std.png",
        "Metric 24: Q-Value Standard Deviation",
        "Q-Value Std Dev",
        [stats_dict[a]["std_q_value"] for a in algo_names],
        fmt="%.3f",
    )

    # Combined 3-Panel Figure: Training Curves Comparison
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8), dpi=150)
    for a in algo_names:
        # Panel 1: Training Reward
        axes[0].plot(stats_dict[a]["training_reward_curve"], label=a, color=ALGORITHMS[a]["color"], alpha=0.35)
        sm = stats_dict[a]["smoothed_train_rewards"]
        axes[0].plot(range(9, 9 + len(sm)), sm, label=f"{a} (10-ep MA)", color=ALGORITHMS[a]["color"], linewidth=2)

        # Panel 2: Training Loss
        axes[1].plot(stats_dict[a]["training_loss_curve"], label=a, color=ALGORITHMS[a]["color"], linewidth=2)

        # Panel 3: Evaluation Reward Trajectory
        r_seq = df_all[df_all["algorithm"] == a]["reward"].values
        k = np.ones(30) / 30.0
        sm_eval = np.convolve(r_seq, k, mode="valid")
        axes[2].plot(sm_eval, label=a, color=ALGORITHMS[a]["color"], linewidth=2)

    axes[0].set_title("Training Reward Progression", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Episode")
    axes[0].set_ylabel("Reward")
    axes[0].legend(fontsize=8)
    axes[0].grid(True, linestyle="--", alpha=0.5)

    axes[1].set_title("Training Loss Progression (Huber)", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Episode")
    axes[1].set_ylabel("Loss")
    axes[1].legend(fontsize=8)
    axes[1].grid(True, linestyle="--", alpha=0.5)

    axes[2].set_title("Greedy Evaluation Reward (30-ep Rolling)", fontsize=12, fontweight="bold")
    axes[2].set_xlabel("Evaluation Episode Index")
    axes[2].set_ylabel("Reward")
    axes[2].legend(fontsize=8)
    axes[2].grid(True, linestyle="--", alpha=0.5)

    fig.tight_layout()
    combined_plot_path = os.path.join(GRAPHS_DIR, "training_curves_comparison.png")
    fig.savefig(combined_plot_path)
    plt.close(fig)
    print("    Graph saved: training_curves_comparison.png")

    total_duration = time.time() - start_total_time
    print("\n" + "=" * 70)
    print(f"BENCHMARK COMPLETED SUCCESSFULLY in {total_duration:.2f}s!")
    print(f"Results directory: {RESULTS_DIR}")
    print(f"Graphs directory:  {GRAPHS_DIR}")
    print("=" * 70)

if __name__ == "__main__":
    main()
