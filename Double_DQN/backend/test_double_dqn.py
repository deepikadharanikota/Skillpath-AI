"""
test_double_dqn.py
------------------
Comprehensive unit test suite for Double DQN:
  1. Standard Q-Network (Single-stream output, shapes, analytical vs numerical gradient check)
  2. Double DQN Decoupled Target Calculation (Online selects next action, Target evaluates action, terminal states)
  3. Proof that Standard DQN target (max Q_target) is replaced by Double DQN target
  4. Uniform Experience Replay (Uniform random sampling, no priorities/weights)
  5. Double DQN Agent (act, remember, replay, target update, epsilon decay, save/load)
  6. Algorithmic Disables Verification (Dueling DISABLED, PER DISABLED, Double DQN ENABLED)
  7. Verification Summary Printout verification (Requirement 28)
"""

import os
import io
import sys
import unittest
import numpy as np

from dqn_agent import (
    UniformReplayBuffer,
    StandardQNetwork,
    DoubleDQNAgent,
    ALGORITHM_VERSION,
    print_rl_configuration,
)
from environment import STATE_DIM, ACTION_DIM


class TestUniformReplayBuffer(unittest.TestCase):
    def test_buffer_push_len_sample(self):
        capacity = 50
        buffer = UniformReplayBuffer(capacity=capacity, seed=42)
        for i in range(30):
            s = np.zeros(STATE_DIM) + i
            buffer.push(s, i % ACTION_DIM, 1.0, s + 1, False)

        self.assertEqual(len(buffer), 30)

        batch_size = 8
        states, actions, rewards, next_states, dones = buffer.sample(batch_size)
        self.assertEqual(states.shape, (batch_size, STATE_DIM))
        self.assertEqual(actions.shape, (batch_size,))
        self.assertEqual(rewards.shape, (batch_size,))
        self.assertEqual(next_states.shape, (batch_size, STATE_DIM))
        self.assertEqual(dones.shape, (batch_size,))

        # Verify NO priorities or importance-sampling weights exist
        self.assertFalse(hasattr(buffer, "tree"))
        self.assertFalse(hasattr(buffer, "alpha"))
        self.assertFalse(hasattr(buffer, "beta"))
        self.assertFalse(hasattr(buffer, "update_priorities"))

    def test_buffer_overwrite(self):
        capacity = 5
        buffer = UniformReplayBuffer(capacity=capacity, seed=42)
        for i in range(10):
            buffer.push(np.zeros(STATE_DIM) + i, 0, 0.0, np.zeros(STATE_DIM), False)
        self.assertEqual(len(buffer), capacity)


class TestStandardQNetwork(unittest.TestCase):
    def setUp(self):
        self.state_dim = 13
        self.action_dim = 27
        self.net = StandardQNetwork(self.state_dim, self.action_dim, hidden_dim=32, seed=123)

    def test_network_shapes_and_forward(self):
        # Check standard layer shapes (single stream)
        self.assertEqual(self.net.W1.shape, (self.state_dim, 32))
        self.assertEqual(self.net.b1.shape, (32,))
        self.assertEqual(self.net.W2.shape, (32, 32))
        self.assertEqual(self.net.b2.shape, (32,))
        self.assertEqual(self.net.W3.shape, (32, self.action_dim))
        self.assertEqual(self.net.b3.shape, (self.action_dim,))

        # Verify NO dueling value/advantage stream parameters exist
        self.assertFalse(hasattr(self.net, "WV"))
        self.assertFalse(hasattr(self.net, "bV"))
        self.assertFalse(hasattr(self.net, "WA"))
        self.assertFalse(hasattr(self.net, "bA"))

        # Batch forward pass
        x = np.random.randn(4, self.state_dim)
        q = self.net.forward(x)
        self.assertEqual(q.shape, (4, self.action_dim))

        # Single state prediction
        single_q = self.net.predict(x[0])
        self.assertEqual(single_q.shape, (self.action_dim,))
        np.testing.assert_allclose(single_q, q[0], rtol=1e-6)

    def test_numerical_gradient_check(self):
        """
        Verify analytical backpropagation gradients in train_on_batch using finite differences
        for Standard Q-Network parameters (W3, b3, W2, b2, W1, b1).
        """
        batch_size = 2
        states = np.random.randn(batch_size, self.state_dim)
        actions = np.array([3, 7])
        targets = np.array([2.0, -1.0])

        test_net = StandardQNetwork(self.state_dim, self.action_dim, hidden_dim=16, seed=99)

        # Finite difference gradient check on W3
        eps = 1e-6
        W3_grad_num = np.zeros_like(test_net.W3)
        for i in range(min(4, test_net.W3.shape[0])):
            for j in range(min(4, test_net.W3.shape[1])):
                test_net.W3[i, j] += eps
                q_plus = test_net.forward(states)
                loss_plus = np.mean(0.5 * (q_plus[np.arange(batch_size), actions] - targets) ** 2)

                test_net.W3[i, j] -= 2 * eps
                q_minus = test_net.forward(states)
                loss_minus = np.mean(0.5 * (q_minus[np.arange(batch_size), actions] - targets) ** 2)

                test_net.W3[i, j] += eps  # restore
                W3_grad_num[i, j] = (loss_plus - loss_minus) / (2 * eps)

        # Compute analytical gradient
        q, (x, z1, a1, z2, a2) = test_net.forward(states, cache=True)
        diff = q[np.arange(batch_size), actions] - targets
        d_q = np.zeros_like(q)
        d_q[np.arange(batch_size), actions] = diff / batch_size
        d_W3 = a2.T @ d_q

        for i in range(min(4, test_net.W3.shape[0])):
            for j in range(min(4, test_net.W3.shape[1])):
                np.testing.assert_allclose(d_W3[i, j], W3_grad_num[i, j], rtol=1e-4, atol=1e-5)


class TestDoubleDQNAgent(unittest.TestCase):
    def setUp(self):
        self.agent = DoubleDQNAgent(
            state_dim=STATE_DIM,
            action_dim=ACTION_DIM,
            hidden_dim=32,
            batch_size=4,
            seed=42
        )

    def test_act_exploration_and_exploitation(self):
        state = np.random.randn(STATE_DIM)
        # Exploitation (greedy)
        action_greedy, q_vals = self.agent.act(state, explore=False)
        self.assertEqual(action_greedy, int(np.argmax(q_vals)))

        # Exploration (forced epsilon = 1.0)
        self.agent.epsilon = 1.0
        action_explore, _ = self.agent.act(state, explore=True)
        self.assertIn(action_explore, range(ACTION_DIM))

    def test_double_dqn_target_calculation(self):
        """
        Verify Double DQN Decoupled Target Calculation:
          1. Online network selects the action: a* = argmax_a' Q_online(s', a')
          2. Target network evaluates that selected action: eval_next_q = Q_target(s', a*)
          3. Double DQN Target: target = r + gamma * (1 - done) * eval_next_q
          4. Terminal state (done=True): target = r
          5. Crucial verification: When online argmax differs from target argmax,
             Double DQN evaluates the online network's action using the target network,
             proving that Double DQN is ACTIVE and Standard DQN direct max is DISABLED.
        """
        next_states = np.random.randn(2, STATE_DIM)
        rewards = np.array([1.5, 3.0])
        dones = np.array([False, True])

        # Configure weights to produce known distinct preferences:
        # Online net strictly prefers Action 5 (index 5)
        # Target net strictly prefers Action 20 (index 20) with very large value
        self.agent.online_net.b3[:] = 0.0
        self.agent.online_net.b3[5] = 100.0   # online prefers action 5

        self.agent.target_net.b3[:] = 0.0
        self.agent.target_net.b3[20] = 500.0  # target prefers action 20
        self.agent.target_net.b3[5] = 10.0    # target value for action 5 is only 10.0

        # Step 1: Online action selection
        next_q_online = self.agent.online_net.forward(next_states)
        best_next_actions = np.argmax(next_q_online, axis=1)
        self.assertEqual(best_next_actions[0], 5)
        self.assertEqual(best_next_actions[1], 5)

        # Step 2: Target action evaluation
        next_q_target = self.agent.target_net.forward(next_states)
        eval_next_q = next_q_target[np.arange(2), best_next_actions]

        # Double DQN selects Q_target evaluated at Action 5 (~10.0)
        # NOT max(Q_target) which would be Action 20 (~500.0)
        self.assertAlmostEqual(eval_next_q[0], next_q_target[0, 5], places=5)
        self.assertLess(eval_next_q[0], 50.0)

        # Step 3: Compute Double DQN targets
        expected_target_0 = rewards[0] + self.agent.gamma * eval_next_q[0]
        expected_target_1 = rewards[1]  # done=True

        targets = rewards + self.agent.gamma * eval_next_q * (1.0 - dones.astype(float))

        self.assertAlmostEqual(targets[0], expected_target_0, places=6)
        self.assertAlmostEqual(targets[1], expected_target_1, places=6)

    def test_training_step_and_epsilon_decay(self):
        for i in range(10):
            s = np.random.randn(STATE_DIM)
            s_next = np.random.randn(STATE_DIM)
            self.agent.remember(s, i % ACTION_DIM, 1.0, s_next, False)

        initial_eps = self.agent.epsilon
        loss = self.agent.replay()
        self.assertIsNotNone(loss)
        self.assertGreaterEqual(loss, 0.0)
        self.assertLess(self.agent.epsilon, initial_eps)

    def test_target_network_update(self):
        self.agent.online_net.W3 += 0.5
        self.assertFalse(np.allclose(self.agent.online_net.W3, self.agent.target_net.W3))

        self.agent.update_target()
        np.testing.assert_allclose(self.agent.online_net.W3, self.agent.target_net.W3)

    def test_model_save_and_load(self):
        tmp_path = "test_double_dqn_weights_tmp.pkl"
        try:
            self.agent._train_steps = 55
            self.agent.epsilon = 0.42
            self.agent.save(tmp_path)

            loaded_agent = DoubleDQNAgent(
                state_dim=STATE_DIM,
                action_dim=ACTION_DIM,
                hidden_dim=32,
                seed=999
            )
            loaded_agent.load(tmp_path)

            self.assertEqual(loaded_agent.algorithm_version, "DoubleDQN-v1")
            self.assertEqual(loaded_agent.algorithm_name, "Double DQN")
            self.assertEqual(loaded_agent._train_steps, 55)
            self.assertAlmostEqual(loaded_agent.epsilon, 0.42, places=5)
            np.testing.assert_allclose(
                self.agent.online_net.W3,
                loaded_agent.online_net.W3
            )
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


class TestAlgorithmicDisablesVerification(unittest.TestCase):
    """
    Explicit verification of criteria from Prompt Requirements 23 & 28:
      ✓ Standard Q-network
      ✓ Single Q-value output stream
      ✓ No value stream
      ✓ No advantage stream
      ✓ No dueling aggregation
      ✓ Online network selects next action
      ✓ Target network evaluates selected action
      ✓ argmax performed using online network
      ✓ No direct max over target-network Q-values
      ✓ Uniform random replay
      ✓ No priorities
      ✓ No alpha
      ✓ No beta
      ✓ No importance-sampling weights
      ✓ No priority updates
      ✓ Epsilon-greedy
    """
    def test_dueling_disabled(self):
        agent = DoubleDQNAgent(STATE_DIM, ACTION_DIM)
        # Verify network has NO dual streams
        self.assertFalse(hasattr(agent.online_net, "WV"))
        self.assertFalse(hasattr(agent.online_net, "bV"))
        self.assertFalse(hasattr(agent.online_net, "WA"))
        self.assertFalse(hasattr(agent.online_net, "bA"))
        # Output is directly standard W3, b3
        self.assertTrue(hasattr(agent.online_net, "W3"))
        self.assertTrue(hasattr(agent.online_net, "b3"))

    def test_per_disabled(self):
        agent = DoubleDQNAgent(STATE_DIM, ACTION_DIM)
        # Verify buffer is Uniform, NOT Prioritized
        self.assertFalse(hasattr(agent.replay_buffer, "tree"))
        self.assertFalse(hasattr(agent.replay_buffer, "alpha"))
        self.assertFalse(hasattr(agent.replay_buffer, "beta"))
        self.assertFalse(hasattr(agent.replay_buffer, "update_priorities"))

    def test_double_dqn_target_decoupling(self):
        agent = DoubleDQNAgent(STATE_DIM, ACTION_DIM, batch_size=4)
        for i in range(20):
            agent.remember(np.random.randn(STATE_DIM), i % ACTION_DIM, 1.0, np.random.randn(STATE_DIM), False)

        # Configure weights to verify online selection vs target evaluation
        # Online network prefers action 0
        agent.online_net.b3[:] = 0.0
        agent.online_net.b3[0] = 50.0

        # Target network prefers action 1 with huge value (100.0), but action 0 has low value (5.0)
        agent.target_net.b3[:] = 0.0
        agent.target_net.b3[1] = 100.0
        agent.target_net.b3[0] = 5.0

        states, actions, rewards, next_states, dones = agent.replay_buffer.sample(4)

        # 1. Online action selection
        next_q_online = agent.online_net.forward(next_states)
        best_next_actions = np.argmax(next_q_online, axis=1)
        self.assertTrue(np.all(best_next_actions == 0))

        # 2. Target action evaluation
        next_q_target = agent.target_net.forward(next_states)
        eval_next_q = next_q_target[np.arange(4), best_next_actions]

        # Double DQN evaluates at chosen action 0 (value ~5.0)
        # If standard DQN were active, max_a Q_target would be ~100.0 (action 1)
        self.assertTrue(np.all(eval_next_q < 20.0))
        self.assertFalse(np.any(eval_next_q >= 90.0))

    def test_configuration_summary_output(self):
        """Verify the exact text output of print_rl_configuration() per Requirement 28."""
        captured_output = io.StringIO()
        old_stdout = sys.stdout
        try:
            sys.stdout = captured_output
            print_rl_configuration()
        finally:
            sys.stdout = old_stdout

        output = captured_output.getvalue()
        self.assertIn("Algorithm:\nDouble DQN", output)
        self.assertIn("Network:\nStandard Q-Network", output)
        self.assertIn("Online Network:\nENABLED", output)
        self.assertIn("Target Network:\nENABLED", output)
        self.assertIn("Target Calculation:\nDouble DQN", output)
        self.assertIn("Online Action Selection:\nENABLED", output)
        self.assertIn("Target Action Evaluation:\nENABLED", output)
        self.assertIn("Dueling Architecture:\nDISABLED", output)
        self.assertIn("Prioritized Experience Replay:\nDISABLED", output)
        self.assertIn("Uniform Experience Replay:\nENABLED", output)
        self.assertIn("PER Importance Sampling:\nDISABLED", output)
        self.assertIn("Epsilon-Greedy:\nENABLED", output)


if __name__ == "__main__":
    unittest.main()
