# SkillPath AI — 100% Python

An adaptive learning coach that uses a real, from-scratch Deep Q-Network
(implemented in NumPy) to decide what a learner should study next and at
what difficulty. **The entire project is now Python** — the old React /
JavaScript frontend (`my-app/`) has been removed and replaced with a
[Streamlit](https://streamlit.io) app that runs the same core RL logic
directly, in-process.


## Run it

```bash
pip install -r requirements.txt
streamlit run main.py
```

Then open the URL Streamlit prints (usually `http://localhost:8501`).

## Project layout

| File | Purpose |
|---|---|
| `main.py` | **Entry point.** The Streamlit app — resume upload, learning modules, quizzes, results, and the dashboard. Ties everything below together. |
| `data.py` | Static content: skills database, topics, roles, module structure, curated video library (per topic/difficulty/module, watched in order), and the 15-question leveled quiz bank per topic (5 easy/5 medium/5 hard). |
| `agent_utils.py` | Skill extraction from resume text, module-progress helpers, and topic-knowledge estimation for the dashboard. Direct Python port of `agentUtils.js`. |
| `recommender.py` | Decision layer that asks the trained `DQNAgent` what to recommend next and turns its output into a friendly explanation. Replaces `apiUtils.js` — no external LLM call is required to run the app. |
| `dqn_agent.py` | The DQN itself: `QNetwork` (manual forward pass + backprop + Adam), `ReplayBuffer`, `DQNAgent` (epsilon-greedy `act`, `remember`, `replay`, target-network sync, save/load). |
| `environment.py` | Defines the MDP: state encoding (12-dim: 8 topic-mastery values + 3 recent scores + fatigue), action space (24 = 8 topics × 3 difficulties), and the reward function. |
| `simulated_learner.py` | A simulated student used to pretrain the agent offline before it meets a real user. |
| `train_offline.py` | Runs the full training loop against the simulator and saves `dqn_weights.pkl`. |
| `dqn_weights.pkl` | Pretrained weights, loaded automatically by `main.py` on startup (falls back to an untrained agent if missing). |



## Learning flow (videos + quiz)

**Videos — one at a time, in order.** Each module (Introduction / Core
Content / Final Review) has its own video list, watched strictly in
sequence: `intro` has 1 video, `core` has **at least 2 detailed videos**
(the "excluding introduction and conclusion" requirement), `summary` has
1 recap video. The next video only unlocks once the current one is
marked "✅ I've watched this." The quiz button itself stays locked until
every video in the module is done.

**Quiz — 15 questions, timed, no skipping.** Every topic has a bank of
**15 leveled questions — exactly 5 easy, 5 medium, 5 hard** — used for
that topic's intro/core/summary quizzes (shuffled fresh each attempt).
Questions are shown **one at a time**: you must select an answer and
wait a **minimum of 60 seconds** before "Confirm Answer & Continue"
unlocks, there's no back button and no way to jump ahead, and the top
navigation is hidden for the duration so you can't leave mid-quiz.
After the 15th question, you get a full review (your answer, the
correct one, and an explanation for each question) before moving on to
the optional coding challenge.

This lives in `data.py` (`VIDEO_DB[topic][difficulty][module]`,
`QUIZ_BANK[topic]`) and `main.py` (`render_learning()` for video gating,
`render_quiz()` for the timed one-by-one flow). It only touches content
and UI flow — the DQN, the environment/reward, and `agent.remember()` /
`agent.replay()` are untouched; a module's aggregate quiz/code score
(0–100%) still feeds the same reward function regardless of how many
questions produced it.

*Note on the 60-second timer:* it's enforced server-side against a real
timestamp, so it can't be bypassed by clicking fast. The visual
countdown is a self-contained JS clock (via Streamlit's built-in
`components.html`, no extra package) that ticks independently in the
browser; if you leave the tab idle rather than interacting, the
"Confirm" button's enabled state only re-evaluates on the next
Streamlit rerun (any click, including the "🔄 Check timer" button next
to it) — a small, documented limitation of doing this without adding a
JS-autorefresh dependency.

## (Optional) Retraining the agent

```bash
python train_offline.py --episodes 300
```

This runs the DQN against `SimulatedLearner` and overwrites
`dqn_weights.pkl`. `main.py` will pick up the new weights the next time
it starts.

## Evaluating the agent (`evaluate.py`)

`train_offline.py`'s printout tells you the loss went down. It doesn't
tell you whether the resulting policy is actually *good*. `evaluate.py`
answers that by comparing the trained DQN against sane baselines on the
same simulator, using matched random seeds so every policy faces an
identical sequence of simulated learners (fair, paired comparison).

```bash
# Evaluate the existing dqn_weights.pkl
python evaluate.py

# Retrain from scratch with full logging (reward/loss/epsilon curves), then evaluate
python evaluate.py --retrain --episodes 1000 --eval-episodes 200
```

**Baselines compared:**
| Policy | Description |
|---|---|
| `dqn_greedy` | The trained agent, greedy (`explore=False`) |
| `random` | Uniform random action every step |
| `round_robin_beginner` | Cycles through all 8 topics in order, always "beginner" — no adaptation at all |
| `rule_based_weakest_topic` | Always recommends the topic with the lowest current mastery, difficulty matched to mastery level via simple thresholds |

**Metrics reported, per policy:** average episode reward (± std), average
simulated quiz/code score, average number of distinct topics recommended
per episode, and a **95% bootstrap confidence interval on the paired
reward difference** against `dqn_greedy` (so you can tell a real gap from
noise, not just eyeball two averages).

**Outputs:** `metrics/training_curves.png` (reward/loss/epsilon/quiz-score
over training, only with `--retrain`), `metrics/policy_comparison.png`,
and `metrics/summary.json`.

### Current honest result

Running `evaluate.py` against the shipped `dqn_weights.pkl` (and again
after retraining for 1000 episodes — loss fully converges to ~0.0001 by
episode 1000, so this isn't an undertraining issue):

```
dqn_greedy                | reward=+5.30 ± 0.26 | quiz=83.4% | topics/ep=4.5/8
random                    | reward=+3.44 ± 0.47 | quiz=43.4% | topics/ep=6.3/8
round_robin_beginner      | reward=+5.48 ± 0.14 | quiz=85.2% | topics/ep=8.0/8
rule_based_weakest_topic  | reward=+5.62 ± 0.14 | quiz=86.0% | topics/ep=5.6/8

dqn_greedy vs round_robin_beginner      | diff=-0.18  95% CI=[-0.22, -0.15] -> DQN worse
dqn_greedy vs rule_based_weakest_topic  | diff=-0.32  95% CI=[-0.36, -0.29] -> DQN worse
```

**The DQN reliably beats random, but loses to both simple baselines —
and the gap is statistically significant (CI excludes zero), not noise.**
Likely explanation: the reward function's `topic_alignment` term is
`1 - mastery(topic)`, which makes "recommend whatever topic has the
lowest mastery" very close to reward-optimal by construction — exactly
what `rule_based_weakest_topic` does directly. A function approximator
trained via epsilon-greedy TD-learning has to *discover* that rule
through trial and error across a 24-action space, and 1000 episodes of a
2-hidden-layer MLP hasn't fully closed that gap. This is a genuine,
reproducible finding (not a bug) — it means either the reward shaping
makes this task close to a contextual-bandit problem a simpler method
would solve more directly, or the DQN needs more training / tuning
(larger buffer warm-up, slower epsilon decay, or a larger network) to
match a rule it should in principle be able to exceed. Re-run
`evaluate.py` after any changes to see whether the gap closes.

## Why this is a genuine RL system, not a rebrand

- **Function approximation**: Q-values come from a trained neural net, not a lookup table or if/else ladder.
- **Backpropagation**: `QNetwork.train_on_batch` computes real gradients layer by layer and updates weights with Adam.
- **Experience replay**: transitions are stored and sampled in random mini-batches, breaking correlation between consecutive updates.
- **Target network**: a separate slow-moving copy of the weights is used to compute bootstrapped targets, updated every `target_update_every` steps — this is what makes DQN stable (Mnih et al., 2015).
- **Epsilon-greedy exploration with decay**: the agent explores early and exploits more as `epsilon` decays.
- **Bellman update**: `target = reward + gamma * max_a' Q_target(s', a')`, the actual DQN objective, not a heuristic.
- **Live training**: every time a learner finishes a quiz, `main.py` calls `agent.remember(...)` and `agent.replay()` — a real gradient step happens on the spot, in the same process serving the UI.
