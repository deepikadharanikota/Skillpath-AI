"""
train_offline.py
-----------------
Runs a full DQN training loop against the simulated learner and saves the
trained weights to dqn_weights.pkl, which api_server.py loads on startup.

Usage:
    python train_offline.py --episodes 300
"""

import argparse
import numpy as np

from dqn_agent import DQNAgent
from environment import STATE_DIM, ACTION_DIM
from simulated_learner import SimulatedLearner


def train(episodes=300, max_steps=12, seed=42, save_path="dqn_weights.pkl"):
    agent = DQNAgent(state_dim=STATE_DIM, action_dim=ACTION_DIM, seed=seed)
    env = SimulatedLearner(seed=seed)

    episode_rewards = []

    for ep in range(1, episodes + 1):
        state = env.reset()
        total_reward = 0.0
        losses = []

        for _ in range(max_steps):
            action, _ = agent.act(state, explore=True)
            next_state, reward, done, info = env.step(action)

            agent.remember(state, action, reward, next_state, done)
            loss = agent.replay()
            if loss is not None:
                losses.append(loss)

            state = next_state
            total_reward += reward
            if done:
                break

        episode_rewards.append(total_reward)

        if ep % 20 == 0 or ep == 1:
            avg_reward = float(np.mean(episode_rewards[-20:]))
            avg_loss = float(np.mean(losses)) if losses else 0.0
            print(f"episode {ep:4d} | avg_reward(last20)={avg_reward:+.3f} "
                  f"| loss={avg_loss:.4f} | epsilon={agent.epsilon:.3f} "
                  f"| buffer={len(agent.replay_buffer)}")

    agent.save(save_path)
    print(f"\nSaved trained weights to {save_path}")
    return agent


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=300)
    parser.add_argument("--save-path", type=str, default="dqn_weights.pkl")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    train(episodes=args.episodes, save_path=args.save_path, seed=args.seed)
