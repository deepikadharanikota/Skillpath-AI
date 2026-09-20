"""
dqn_agent_standard_dqn.py
-------------------------
Standard Deep Q-Network (Standard DQN) baseline, preserved for experimental comparison:
  1. Standard Q-Network Architecture:
     - Shared feature trunk:
         z1 = x @ W1 + b1, a1 = ReLU(z1)      (state_dim -> 64)
         z2 = a1 @ W2 + b2, a2 = ReLU(z2)     (64 -> 64)
     - Single direct Q-value output layer:
         Q(s, a) = a2 @ W3 + b3               (64 -> action_dim)
     - NO Value stream V(s)
     - NO Advantage stream A(s, a)
     - NO Dueling aggregation layer

  2. Standard DQN Target Calculation:
     - Target network maximum Q-value directly:
         y = r + gamma * (1 - done) * max_a' Q_target(s', a')
     - For terminal states:
         y = r
     - NO Double DQN decoupling (online network is NOT used to select next action)

  3. Uniform Experience Replay Buffer:
     - Uniform random batch sampling across stored transitions
     - NO Prioritized Experience Replay
     - NO TD-error priorities, NO alpha, NO beta, NO importance-sampling weights

  4. Epsilon-Greedy Exploration:
     - Uniform random exploration with rate epsilon
     - Greedy action exploitation: argmax_a Q(s, a)
     - Exponential epsilon decay per training step

  5. Target Network Synchronization:
     - Periodic hard copy of online network weights to target network
"""

import os
import pickle
import random
import logging
from typing import Dict, Tuple, List, Optional
import numpy as np

logger = logging.getLogger(__name__)

RL_ALGORITHM = "DQN"
ALGORITHM_VERSION = "Standard-DQN-v1"


# ─────────────────────────────────────────────────────────────────────────
# 1. Uniform Experience Replay Buffer
# ─────────────────────────────────────────────────────────────────────────
class UniformReplayBuffer:
    """
    Standard experience replay buffer with uniform random sampling:
      - Experiences are tuples of (state, action, reward, next_state, done)
      - Samples transitions uniformly with replacement/random indexing
      - No prioritization, no importance-sampling weights
    """
    def __init__(self, capacity: int = 10000, seed: Optional[int] = None):
        self.capacity = capacity
        self.data = [None] * capacity
        self.write = 0
        self.n_entries = 0
        self._rng = np.random.default_rng(seed)

    def push(self, state, action: int, reward: float, next_state, done: bool):
        """Insert new transition with uniform storage."""
        transition = (
            np.asarray(state, dtype=np.float64),
            int(action),
            float(reward),
            np.asarray(next_state, dtype=np.float64),
            bool(done),
        )
        self.data[self.write] = transition
        self.write = (self.write + 1) % self.capacity
        if self.n_entries < self.capacity:
            self.n_entries += 1

    def sample(self, batch_size: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Sample a batch of transitions uniformly at random."""
        if self.n_entries == 0:
            raise ValueError("Cannot sample from an empty replay buffer.")

        indices = self._rng.integers(0, self.n_entries, size=batch_size)
        batch = [self.data[idx] for idx in indices]
        states, actions, rewards, next_states, dones = zip(*batch)

        return (
            np.stack(states),
            np.array(actions, dtype=np.int64),
            np.array(rewards, dtype=np.float64),
            np.stack(next_states),
            np.array(dones, dtype=bool),
        )

    def __len__(self) -> int:
        return self.n_entries


# ─────────────────────────────────────────────────────────────────────────
# 2. Standard Deep Q-Network (Single-Stream Output)
# ─────────────────────────────────────────────────────────────────────────
class StandardQNetwork:
    """
    Standard Feedforward Deep Q-Network in pure NumPy:
      Layer 1: z1 = x @ W1 + b1, a1 = ReLU(z1)    (state_dim -> hidden_dim)
      Layer 2: z2 = a1 @ W2 + b2, a2 = ReLU(z2)   (hidden_dim -> hidden_dim)
      Output:  Q(s, a) = a2 @ W3 + b3             (hidden_dim -> action_dim)

    Directly predicts Q(s, a) for all actions without Value or Advantage streams.
    """
    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        hidden_dim: int = 64,
        lr: float = 1e-3,
        seed: Optional[int] = None
    ):
        rng = np.random.default_rng(seed)
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.hidden_dim = hidden_dim
        self.lr = lr

        # Layer 1
        self.W1 = rng.normal(0, np.sqrt(2.0 / state_dim), (state_dim, hidden_dim))
        self.b1 = np.zeros(hidden_dim)

        # Layer 2
        self.W2 = rng.normal(0, np.sqrt(2.0 / hidden_dim), (hidden_dim, hidden_dim))
        self.b2 = np.zeros(hidden_dim)

        # Output Layer: direct mapping to action_dim Q-values
        self.W3 = rng.normal(0, np.sqrt(2.0 / hidden_dim), (hidden_dim, action_dim))
        self.b3 = np.zeros(action_dim)

        # Adam optimizer parameters
        self._param_names = ["W1", "b1", "W2", "b2", "W3", "b3"]
        self._m = {k: np.zeros_like(getattr(self, k)) for k in self._param_names}
        self._v = {k: np.zeros_like(getattr(self, k)) for k in self._param_names}
        self._t = 0

    @staticmethod
    def _relu(x: np.ndarray) -> np.ndarray:
        return np.maximum(0, x)

    @staticmethod
    def _relu_grad(x: np.ndarray) -> np.ndarray:
        return (x > 0).astype(np.float64)

    def forward(self, x: np.ndarray, cache: bool = False):
        """
        Forward pass directly computing Q-values:
          x: (batch, state_dim)
        Returns:
          q_values: (batch, action_dim)
        """
        x = np.asarray(x, dtype=np.float64)
        z1 = x @ self.W1 + self.b1
        a1 = self._relu(z1)

        z2 = a1 @ self.W2 + self.b2
        a2 = self._relu(z2)

        q = a2 @ self.W3 + self.b3

        if cache:
            return q, (x, z1, a1, z2, a2)
        return q

    def predict(self, state: np.ndarray) -> np.ndarray:
        """Single state inference wrapper: (state_dim,) -> (action_dim,)"""
        x = np.asarray(state, dtype=np.float64).reshape(1, -1)
        return self.forward(x)[0]

    def _adam_step(self, grads: Dict[str, np.ndarray], beta1: float = 0.9, beta2: float = 0.999, eps: float = 1e-8):
        self._t += 1
        for name in self._param_names:
            grad = grads[name]
            self._m[name] = beta1 * self._m[name] + (1 - beta1) * grad
            self._v[name] = beta2 * self._v[name] + (1 - beta2) * (grad ** 2)
            m_hat = self._m[name] / (1.0 - beta1 ** self._t)
            v_hat = self._v[name] / (1.0 - beta2 ** self._t)
            update = self.lr * m_hat / (np.sqrt(v_hat) + eps)
            setattr(self, name, getattr(self, name) - update)

    def train_on_batch(self, states: np.ndarray, actions: np.ndarray, targets: np.ndarray, huber_delta: float = 1.0) -> float:
        """
        Backpropagation with standard Huber Loss:
          actions: (batch,) taken actions
          targets: (batch,) target Q values: r + gamma * max_a' Q_target(s', a')
        """
        batch_size = states.shape[0]
        q, (x, z1, a1, z2, a2) = self.forward(states, cache=True)

        # Compute TD error on taken actions: (Q(s, a) - target)
        current_q_taken = q[np.arange(batch_size), actions]
        diff = current_q_taken - targets  # shape (batch,)

        abs_diff = np.abs(diff)
        huber_grad = np.where(abs_diff <= huber_delta, diff, huber_delta * np.sign(diff))

        # Gradient with respect to Q-values: (batch, action_dim)
        d_q = np.zeros_like(q)
        d_q[np.arange(batch_size), actions] = huber_grad / batch_size

        # Output Layer Gradients (W3, b3)
        d_W3 = a2.T @ d_q  # (hidden_dim, action_dim)
        d_b3 = np.sum(d_q, axis=0)  # (action_dim,)

        # Backpropagation into Layer 2
        d_a2 = d_q @ self.W3.T  # (batch, hidden_dim)
        d_z2 = d_a2 * self._relu_grad(z2)
        d_W2 = a1.T @ d_z2  # (hidden_dim, hidden_dim)
        d_b2 = np.sum(d_z2, axis=0)  # (hidden_dim,)

        # Backpropagation into Layer 1
        d_a1 = d_z2 @ self.W2.T  # (batch, hidden_dim)
        d_z1 = d_a1 * self._relu_grad(z1)
        d_W1 = x.T @ d_z1  # (state_dim, hidden_dim)
        d_b1 = np.sum(d_z1, axis=0)  # (hidden_dim,)

        grads = {
            "W1": d_W1, "b1": d_b1,
            "W2": d_W2, "b2": d_b2,
            "W3": d_W3, "b3": d_b3,
        }
        self._adam_step(grads)

        # Compute scalar Huber loss for reporting
        huber_losses = np.where(
            abs_diff <= huber_delta,
            0.5 * (diff ** 2),
            huber_delta * (abs_diff - 0.5 * huber_delta)
        )
        total_loss = float(np.mean(huber_losses))
        return total_loss

    def get_weights(self) -> Dict[str, np.ndarray]:
        return {k: getattr(self, k).copy() for k in self._param_names}

    def set_weights(self, weights: Dict[str, np.ndarray]):
        for k in self._param_names:
            if k in weights:
                setattr(self, k, weights[k].copy())


# ─────────────────────────────────────────────────────────────────────────
# 3. Standard DQN Agent
# ─────────────────────────────────────────────────────────────────────────
class StandardDQNAgent:
    """
    Standard Deep Q-Network Agent (Standard DQN baseline):
      1. Standard Q-Network: Direct mapping from state to action Q-values
      2. Standard DQN Target: y = r + gamma * (1 - done) * max_a' Q_target(s', a')
      3. Uniform Experience Replay: Uniform random sampling
      4. Epsilon-Greedy: Epsilon exploration, argmax exploitation
      5. Periodic Target Network synchronization
    """
    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        hidden_dim: int = 64,
        lr: float = 1e-3,
        gamma: float = 0.95,
        epsilon_start: float = 1.0,
        epsilon_min: float = 0.05,
        epsilon_decay: float = 0.995,
        buffer_capacity: int = 10000,
        batch_size: int = 32,
        target_update_every: int = 25,
        seed: int = 42,
    ):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.target_update_every = target_update_every
        self._train_steps = 0
        self.algorithm_name = "Standard DQN"
        self.algorithm_version = ALGORITHM_VERSION

        # Standard Online and Target Networks
        self.online_net = StandardQNetwork(state_dim, action_dim, hidden_dim, lr, seed=seed)
        self.target_net = StandardQNetwork(state_dim, action_dim, hidden_dim, lr, seed=seed)
        self.target_net.set_weights(self.online_net.get_weights())

        # Uniform Experience Replay Buffer
        self.replay_buffer = UniformReplayBuffer(capacity=buffer_capacity, seed=seed)

    def act(self, state: np.ndarray, explore: bool = True) -> Tuple[int, np.ndarray]:
        """
        Epsilon-greedy action selection:
          - With probability epsilon: select random action (exploration)
          - Otherwise: select argmax_a Q(state, a) (exploitation)
        Returns:
          (action_index, q_values)
        """
        q_values = self.online_net.predict(state)
        if explore and random.random() < self.epsilon:
            action = random.randrange(self.action_dim)
        else:
            action = int(np.argmax(q_values))
        return action, q_values

    def remember(self, state, action: int, reward: float, next_state, done: bool):
        """Store experience transition into Uniform Experience Replay buffer."""
        self.replay_buffer.push(state, action, reward, next_state, done)

    def replay(self) -> Optional[float]:
        """
        One training step using Standard DQN:
          1. Uniform random sample of experiences from replay buffer
          2. Standard DQN target calculation:
               max_q' = max_a' Q_target(s', a')
               target = r + gamma * (1 - done) * max_q'
          3. Backpropagation with Huber Loss on online network
          4. Periodically synchronize target network
          5. Anneal epsilon
        """
        if len(self.replay_buffer) < self.batch_size:
            return None

        # 1. Uniform random sampling
        states, actions, rewards, next_states, dones = self.replay_buffer.sample(self.batch_size)

        # 2. Standard DQN Target Calculation
        next_q_target = self.target_net.forward(next_states)
        max_next_q = np.max(next_q_target, axis=1)
        targets = rewards + self.gamma * max_next_q * (1.0 - dones.astype(np.float64))

        # 3. Online Network Backpropagation
        loss = self.online_net.train_on_batch(states, actions, targets)

        # 4. Target network synchronization
        self._train_steps += 1
        if self._train_steps % self.target_update_every == 0:
            self.update_target()

        # 5. Anneal exploration rate
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

        return loss

    def update_target(self):
        """Hard copy online network weights to target network."""
        self.target_net.set_weights(self.online_net.get_weights())

    def save(self, path: str):
        """Save Standard DQN model and metadata."""
        data = {
            "algorithm_name": self.algorithm_name,
            "algorithm_version": self.algorithm_version,
            "online_weights": self.online_net.get_weights(),
            "target_weights": self.target_net.get_weights(),
            "epsilon": self.epsilon,
            "train_steps": self._train_steps,
            "state_dim": self.state_dim,
            "action_dim": self.action_dim,
        }
        with open(path, "wb") as f:
            pickle.dump(data, f)
        logger.info(f"Saved {self.algorithm_version} ({self.algorithm_name}) model to {path}")

    def load(self, path: str):
        """
        Load Standard DQN model weights and state.
        Gracefully handles loading standard weights [W1, b1, W2, b2, W3, b3].
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model file {path} does not exist.")

        with open(path, "rb") as f:
            data = pickle.load(f)

        version = data.get("algorithm_version", "legacy-standard-dqn")
        logger.info(f"Loading Standard DQN checkpoint: version={version}")

        online_w = data.get("online_weights", {})
        if "W3" in online_w and "b3" in online_w:
            self.online_net.set_weights(online_w)
            self.target_net.set_weights(data.get("target_weights", online_w))
            self.epsilon = data.get("epsilon", self.epsilon)
            self._train_steps = data.get("train_steps", 0)
            logger.info(f"Successfully loaded Standard DQN weights (step={self._train_steps}, epsilon={self.epsilon:.3f})")
        else:
            logger.warning(
                f"Checkpoint {path} contains non-standard DQN weights (incompatible shapes). "
                f"Initializing new Standard DQN architecture with random weights."
            )


# Drop-in Aliases
DQNAgent = StandardDQNAgent
QNetwork = StandardQNetwork
ReplayBuffer = UniformReplayBuffer


def print_rl_configuration():
    """Prints the clear RL Configuration summary as required."""
    print("=========================================")
    print("SkillPath AI RL Configuration")
    print("=========================================")
    print("")
    print("Algorithm:")
    print("Standard DQN")
    print("")
    print("Network:")
    print("Standard Q-Network")
    print("")
    print("Target:")
    print("Standard DQN target")
    print("")
    print("Replay:")
    print("Uniform Experience Replay")
    print("")
    print("Double DQN:")
    print("DISABLED")
    print("")
    print("Dueling Architecture:")
    print("DISABLED")
    print("")
    print("Prioritized Experience Replay:")
    print("DISABLED")
    print("")
    print("PER Importance Sampling:")
    print("DISABLED")
    print("")
    print("Epsilon-Greedy:")
    print("ENABLED")
    print("")
    print("=========================================")


if __name__ == "__main__":
    print_rl_configuration()
