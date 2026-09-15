"""
dqn_agent.py
------------
A genuine Deep Q-Network implemented from scratch in NumPy — real forward
pass, real backpropagation, a real target network, epsilon-greedy
exploration, and experience replay. No JavaScript, no LLM call pretending
to be an RL agent. This is the actual decision-making core of SkillPath AI.

Network: state_dim -> 64 (ReLU) -> 64 (ReLU) -> action_dim (linear, Q-values)
Optimizer: Adam (implemented manually)
"""

import numpy as np
import pickle
import random
from collections import deque


# ─────────────────────────────────────────────────────────────────────────
# Small NumPy MLP with manual forward/backward pass
# ─────────────────────────────────────────────────────────────────────────
class QNetwork:
    def __init__(self, state_dim, action_dim, hidden_dim=64, lr=1e-3, seed=None):
        rng = np.random.default_rng(seed)
        self.state_dim = state_dim
        self.action_dim = action_dim

        # He initialization, good default for ReLU nets
        self.W1 = rng.normal(0, np.sqrt(2.0 / state_dim), (state_dim, hidden_dim))
        self.b1 = np.zeros(hidden_dim)
        self.W2 = rng.normal(0, np.sqrt(2.0 / hidden_dim), (hidden_dim, hidden_dim))
        self.b2 = np.zeros(hidden_dim)
        self.W3 = rng.normal(0, np.sqrt(2.0 / hidden_dim), (hidden_dim, action_dim))
        self.b3 = np.zeros(action_dim)

        # Adam optimizer state
        self.lr = lr
        self._m = {}
        self._v = {}
        self._t = 0
        for name in ["W1", "b1", "W2", "b2", "W3", "b3"]:
            param = getattr(self, name)
            self._m[name] = np.zeros_like(param)
            self._v[name] = np.zeros_like(param)

    @staticmethod
    def _relu(x):
        return np.maximum(0, x)

    @staticmethod
    def _relu_grad(x):
        return (x > 0).astype(x.dtype)

    def forward(self, x, cache=False):
        """x: (batch, state_dim) -> q_values: (batch, action_dim)"""
        z1 = x @ self.W1 + self.b1
        a1 = self._relu(z1)
        z2 = a1 @ self.W2 + self.b2
        a2 = self._relu(z2)
        q = a2 @ self.W3 + self.b3
        if cache:
            return q, (x, z1, a1, z2, a2)
        return q

    def predict(self, state):
        """Single-state convenience wrapper. state: (state_dim,)"""
        x = np.asarray(state, dtype=np.float64).reshape(1, -1)
        return self.forward(x)[0]

    def _adam_step(self, grads, beta1=0.9, beta2=0.999, eps=1e-8):
        self._t += 1
        for name, grad in grads.items():
            self._m[name] = beta1 * self._m[name] + (1 - beta1) * grad
            self._v[name] = beta2 * self._v[name] + (1 - beta2) * (grad ** 2)
            m_hat = self._m[name] / (1 - beta1 ** self._t)
            v_hat = self._v[name] / (1 - beta2 ** self._t)
            update = self.lr * m_hat / (np.sqrt(v_hat) + eps)
            setattr(self, name, getattr(self, name) - update)

    def train_on_batch(self, states, target_q):
        """
        Full backprop step (MSE loss) on a batch.
        states: (batch, state_dim)
        target_q: (batch, action_dim) -- target Q-values (only the taken
                  action's column carries real signal; others equal the
                  network's own prediction so they contribute zero gradient)
        """
        batch_size = states.shape[0]
        q, (x, z1, a1, z2, a2) = self.forward(states, cache=True)

        # dL/dq for MSE loss = (2/N) * (q - target)
        d_q = (2.0 / batch_size) * (q - target_q)

        # Layer 3 grads
        dW3 = a2.T @ d_q
        db3 = d_q.sum(axis=0)
        d_a2 = d_q @ self.W3.T

        # Layer 2 grads
        d_z2 = d_a2 * self._relu_grad(z2)
        dW2 = a1.T @ d_z2
        db2 = d_z2.sum(axis=0)
        d_a1 = d_z2 @ self.W2.T

        # Layer 1 grads
        d_z1 = d_a1 * self._relu_grad(z1)
        dW1 = x.T @ d_z1
        db1 = d_z1.sum(axis=0)

        grads = {"W1": dW1, "b1": db1, "W2": dW2, "b2": db2, "W3": dW3, "b3": db3}
        self._adam_step(grads)

        loss = float(np.mean((q - target_q) ** 2))
        return loss

    def get_weights(self):
        return {k: getattr(self, k).copy() for k in ["W1", "b1", "W2", "b2", "W3", "b3"]}

    def set_weights(self, weights):
        for k, v in weights.items():
            setattr(self, k, v.copy())


# ─────────────────────────────────────────────────────────────────────────
# Experience Replay Buffer
# ─────────────────────────────────────────────────────────────────────────
class ReplayBuffer:
    def __init__(self, capacity=10000, seed=None):
        self.buffer = deque(maxlen=capacity)
        self._rng = random.Random(seed)

    def push(self, state, action, reward, next_state, done):
        self.buffer.append((
            np.asarray(state, dtype=np.float64),
            int(action),
            float(reward),
            np.asarray(next_state, dtype=np.float64),
            bool(done),
        ))

    def sample(self, batch_size):
        batch = self._rng.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            np.stack(states),
            np.array(actions),
            np.array(rewards),
            np.stack(next_states),
            np.array(dones),
        )

    def __len__(self):
        return len(self.buffer)


# ─────────────────────────────────────────────────────────────────────────
# DQN Agent — epsilon-greedy policy, target network, experience replay
# ─────────────────────────────────────────────────────────────────────────
class DQNAgent:
    def __init__(
        self,
        state_dim,
        action_dim,
        hidden_dim=64,
        lr=1e-3,
        gamma=0.95,
        epsilon_start=1.0,
        epsilon_min=0.05,
        epsilon_decay=0.995,
        buffer_capacity=10000,
        batch_size=32,
        target_update_every=25,
        seed=42,
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

        self.online_net = QNetwork(state_dim, action_dim, hidden_dim, lr, seed=seed)
        self.target_net = QNetwork(state_dim, action_dim, hidden_dim, lr, seed=seed)
        self.target_net.set_weights(self.online_net.get_weights())

        self.replay_buffer = ReplayBuffer(buffer_capacity, seed=seed)

    def act(self, state, explore=True):
        """Epsilon-greedy action selection. Returns (action_index, q_values)."""
        q_values = self.online_net.predict(state)
        if explore and random.random() < self.epsilon:
            action = random.randrange(self.action_dim)
        else:
            action = int(np.argmax(q_values))
        return action, q_values

    def remember(self, state, action, reward, next_state, done):
        self.replay_buffer.push(state, action, reward, next_state, done)

    def replay(self):
        """One training step sampled from the replay buffer. Returns loss or None."""
        if len(self.replay_buffer) < self.batch_size:
            return None

        states, actions, rewards, next_states, dones = self.replay_buffer.sample(self.batch_size)

        # Bootstrapped target: r + gamma * max_a' Q_target(s', a')  (0 if terminal)
        next_q = self.target_net.forward(next_states)
        max_next_q = np.max(next_q, axis=1)
        targets = rewards + self.gamma * max_next_q * (1 - dones.astype(np.float64))

        # Build full target matrix: equal to current prediction everywhere
        # except the taken action column, so only that column back-props.
        current_q = self.online_net.forward(states)
        target_q_full = current_q.copy()
        target_q_full[np.arange(self.batch_size), actions] = targets

        loss = self.online_net.train_on_batch(states, target_q_full)

        self._train_steps += 1
        if self._train_steps % self.target_update_every == 0:
            self.update_target()

        # Decay exploration
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

        return loss

    def update_target(self):
        self.target_net.set_weights(self.online_net.get_weights())

    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump({
                "online_weights": self.online_net.get_weights(),
                "target_weights": self.target_net.get_weights(),
                "epsilon": self.epsilon,
                "train_steps": self._train_steps,
                "state_dim": self.state_dim,
                "action_dim": self.action_dim,
            }, f)

    def load(self, path):
        with open(path, "rb") as f:
            data = pickle.load(f)
        self.online_net.set_weights(data["online_weights"])
        self.target_net.set_weights(data["target_weights"])
        self.epsilon = data["epsilon"]
        self._train_steps = data["train_steps"]
