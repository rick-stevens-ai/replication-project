"""
DRL agent for HPC job scheduling — simplified DRAS replication.

Implements:
  - DQN with ε-greedy exploration (DRAS-DQL style)
  - Policy Gradient (REINFORCE with baseline) (DRAS-PG style)

Uses the ClusterEnv simulator with Gym-like API.
"""

from __future__ import annotations
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import json
import os
from collections import deque
import random
from simulator import ClusterEnv, load_jobs, Job


# ---------------------------------------------------------------------------
# Network architectures
# ---------------------------------------------------------------------------
class DQN(nn.Module):
    """Simple DQN for job selection."""
    def __init__(self, obs_dim: int, action_dim: int, hidden1: int = 256, hidden2: int = 128):
        super().__init__()
        self.fc1 = nn.Linear(obs_dim, hidden1)
        self.fc2 = nn.Linear(hidden1, hidden2)
        self.fc3 = nn.Linear(hidden2, action_dim)

    def forward(self, x):
        x = F.leaky_relu(self.fc1(x))
        x = F.leaky_relu(self.fc2(x))
        return self.fc3(x)  # Q-values


class PolicyNet(nn.Module):
    """Actor-Critic network for PPO/PG."""
    def __init__(self, obs_dim: int, action_dim: int, hidden1: int = 256, hidden2: int = 128):
        super().__init__()
        self.shared1 = nn.Linear(obs_dim, hidden1)
        self.shared2 = nn.Linear(hidden1, hidden2)
        self.actor = nn.Linear(hidden2, action_dim)
        self.critic = nn.Linear(hidden2, 1)

    def forward(self, x):
        x = F.leaky_relu(self.shared1(x))
        x = F.leaky_relu(self.shared2(x))
        logits = self.actor(x)
        value = self.critic(x)
        return logits, value


# ---------------------------------------------------------------------------
# DQN Agent
# ---------------------------------------------------------------------------
class DQNAgent:
    def __init__(self, obs_dim: int, action_dim: int,
                 lr: float = 1e-3, gamma: float = 0.99,
                 eps_start: float = 1.0, eps_decay: float = 0.995, eps_min: float = 0.05,
                 buffer_size: int = 50000, batch_size: int = 64,
                 target_update: int = 100, hidden1: int = 256, hidden2: int = 128):
        self.obs_dim = obs_dim
        self.action_dim = action_dim
        self.gamma = gamma
        self.eps = eps_start
        self.eps_decay = eps_decay
        self.eps_min = eps_min
        self.batch_size = batch_size
        self.target_update = target_update
        self.learn_step = 0

        self.device = torch.device("cpu")  # CPU is fine for this scale

        self.policy_net = DQN(obs_dim, action_dim, hidden1, hidden2).to(self.device)
        self.target_net = DQN(obs_dim, action_dim, hidden1, hidden2).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.buffer = deque(maxlen=buffer_size)

    def select_action(self, obs: np.ndarray, mask: np.ndarray) -> int:
        """ε-greedy action selection with mask."""
        valid_actions = np.where(mask)[0]
        if len(valid_actions) == 0:
            return -1  # no valid action

        if random.random() < self.eps:
            return int(np.random.choice(valid_actions))

        with torch.no_grad():
            obs_t = torch.FloatTensor(obs).unsqueeze(0).to(self.device)
            q_values = self.policy_net(obs_t).squeeze(0).cpu().numpy()
            # Mask invalid actions
            masked_q = np.full(self.action_dim, -1e9)
            masked_q[valid_actions] = q_values[valid_actions]
            return int(np.argmax(masked_q))

    def store(self, obs, action, reward, next_obs, done):
        self.buffer.append((obs, action, reward, next_obs, done))

    def update(self):
        if len(self.buffer) < self.batch_size:
            return 0.0

        batch = random.sample(self.buffer, self.batch_size)
        obs, actions, rewards, next_obs, dones = zip(*batch)

        obs_t = torch.FloatTensor(np.array(obs)).to(self.device)
        actions_t = torch.LongTensor(actions).to(self.device)
        rewards_t = torch.FloatTensor(rewards).to(self.device)
        next_obs_t = torch.FloatTensor(np.array(next_obs)).to(self.device)
        dones_t = torch.FloatTensor(dones).to(self.device)

        # Current Q
        q_values = self.policy_net(obs_t).gather(1, actions_t.unsqueeze(1)).squeeze(1)
        # Target Q
        with torch.no_grad():
            next_q = self.target_net(next_obs_t).max(1)[0]
            target_q = rewards_t + self.gamma * next_q * (1 - dones_t)

        loss = F.mse_loss(q_values, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.policy_net.parameters(), 1.0)
        self.optimizer.step()

        self.learn_step += 1
        if self.learn_step % self.target_update == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())

        return loss.item()

    def decay_epsilon(self):
        self.eps = max(self.eps_min, self.eps * self.eps_decay)


# ---------------------------------------------------------------------------
# PPO Agent
# ---------------------------------------------------------------------------
class PPOAgent:
    def __init__(self, obs_dim: int, action_dim: int,
                 lr: float = 3e-4, gamma: float = 0.99, clip_eps: float = 0.2,
                 epochs: int = 4, batch_size: int = 64,
                 entropy_coef: float = 0.01, hidden1: int = 256, hidden2: int = 128):
        self.obs_dim = obs_dim
        self.action_dim = action_dim
        self.gamma = gamma
        self.clip_eps = clip_eps
        self.epochs = epochs
        self.batch_size = batch_size
        self.entropy_coef = entropy_coef

        self.device = torch.device("cpu")
        self.net = PolicyNet(obs_dim, action_dim, hidden1, hidden2).to(self.device)
        self.optimizer = optim.Adam(self.net.parameters(), lr=lr)

        # Trajectory buffer
        self.obs_buf = []
        self.act_buf = []
        self.rew_buf = []
        self.logp_buf = []
        self.val_buf = []
        self.mask_buf = []

    def select_action(self, obs: np.ndarray, mask: np.ndarray) -> tuple[int, float, float]:
        """Select action using policy, return (action, log_prob, value)."""
        valid_actions = np.where(mask)[0]
        if len(valid_actions) == 0:
            return -1, 0.0, 0.0

        with torch.no_grad():
            obs_t = torch.FloatTensor(obs).unsqueeze(0).to(self.device)
            logits, value = self.net(obs_t)
            logits = logits.squeeze(0)
            value = value.squeeze(0).item()

            # Mask invalid actions
            mask_t = torch.full((self.action_dim,), -1e9)
            mask_t[valid_actions] = 0.0
            logits = logits + mask_t

            probs = F.softmax(logits, dim=-1)
            dist = torch.distributions.Categorical(probs)
            action = dist.sample()
            log_prob = dist.log_prob(action)

        return action.item(), log_prob.item(), value

    def store(self, obs, action, reward, log_prob, value, mask):
        self.obs_buf.append(obs)
        self.act_buf.append(action)
        self.rew_buf.append(reward)
        self.logp_buf.append(log_prob)
        self.val_buf.append(value)
        self.mask_buf.append(mask)

    def update(self) -> float:
        """PPO update at end of episode."""
        if len(self.obs_buf) < 2:
            self._clear()
            return 0.0

        # Compute returns and advantages (GAE-lambda simplified)
        returns = []
        G = 0
        for r in reversed(self.rew_buf):
            G = r + self.gamma * G
            returns.insert(0, G)

        returns = np.array(returns, dtype=np.float32)
        values = np.array(self.val_buf, dtype=np.float32)
        advantages = returns - values
        # Normalize advantages
        adv_std = advantages.std()
        if adv_std > 1e-8:
            advantages = (advantages - advantages.mean()) / adv_std

        obs_t = torch.FloatTensor(np.array(self.obs_buf)).to(self.device)
        act_t = torch.LongTensor(self.act_buf).to(self.device)
        ret_t = torch.FloatTensor(returns).to(self.device)
        adv_t = torch.FloatTensor(advantages).to(self.device)
        old_logp_t = torch.FloatTensor(self.logp_buf).to(self.device)

        total_loss = 0.0
        n = len(self.obs_buf)

        for _ in range(self.epochs):
            # Shuffle indices
            indices = np.arange(n)
            np.random.shuffle(indices)

            for start in range(0, n, self.batch_size):
                end = min(start + self.batch_size, n)
                idx = indices[start:end]

                logits, values = self.net(obs_t[idx])

                # Apply mask
                for i, bi in enumerate(idx):
                    m = self.mask_buf[bi]
                    inv = ~m
                    if np.any(inv):
                        logits[i, torch.from_numpy(np.where(inv)[0])] = -1e9

                probs = F.softmax(logits, dim=-1)
                dist = torch.distributions.Categorical(probs)
                new_logp = dist.log_prob(act_t[idx])
                entropy = dist.entropy().mean()

                ratio = torch.exp(new_logp - old_logp_t[idx])
                surr1 = ratio * adv_t[idx]
                surr2 = torch.clamp(ratio, 1 - self.clip_eps, 1 + self.clip_eps) * adv_t[idx]

                actor_loss = -torch.min(surr1, surr2).mean()
                critic_loss = F.mse_loss(values.squeeze(-1), ret_t[idx])
                loss = actor_loss + 0.5 * critic_loss - self.entropy_coef * entropy

                self.optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.net.parameters(), 0.5)
                self.optimizer.step()
                total_loss += loss.item()

        self._clear()
        return total_loss

    def _clear(self):
        self.obs_buf.clear()
        self.act_buf.clear()
        self.rew_buf.clear()
        self.logp_buf.clear()
        self.val_buf.clear()
        self.mask_buf.clear()


# ---------------------------------------------------------------------------
# Training loop
# ---------------------------------------------------------------------------
def train_dqn(env: ClusterEnv, train_jobs: list[Job], val_jobs: list[Job],
              num_episodes: int = 100, save_dir: str = "../data") -> list[dict]:
    """Train DQN agent and return per-episode metrics."""
    agent = DQNAgent(env.obs_dim, env.window_size, lr=1e-3, gamma=0.99,
                     eps_start=1.0, eps_decay=0.995, eps_min=0.05,
                     buffer_size=50000, batch_size=64, target_update=50)

    history = []

    for ep in range(num_episodes):
        obs, info = env.reset(train_jobs)
        mask = info["mask"]
        total_reward = 0.0
        steps = 0
        losses = []

        while True:
            action = agent.select_action(obs, mask)
            if action < 0:
                # No valid action — advance
                next_obs, reward, done, _, info = env.step(-1)
            else:
                next_obs, reward, done, _, info = env.step(action)
                agent.store(obs, action, reward, next_obs, float(done))
                loss = agent.update()
                if loss > 0:
                    losses.append(loss)

            total_reward += reward
            steps += 1
            obs = next_obs
            mask = info["mask"]

            if done:
                break

        agent.decay_epsilon()
        train_metrics = env.get_metrics()

        # Validation (greedy)
        val_metrics = evaluate_dqn(env, agent, val_jobs)

        record = {
            "episode": ep,
            "train_avg_wait": train_metrics["avg_wait"],
            "train_avg_slowdown": train_metrics["avg_slowdown"],
            "train_makespan": train_metrics["makespan"],
            "train_reward": total_reward,
            "val_avg_wait": val_metrics["avg_wait"],
            "val_avg_slowdown": val_metrics["avg_slowdown"],
            "val_makespan": val_metrics["makespan"],
            "epsilon": agent.eps,
            "avg_loss": float(np.mean(losses)) if losses else 0.0,
            "steps": steps,
        }
        history.append(record)

        if ep % 10 == 0 or ep == num_episodes - 1:
            print(f"[DQN] Ep {ep:3d} | ε={agent.eps:.3f} | "
                  f"train_wait={train_metrics['avg_wait']:.0f} | "
                  f"val_wait={val_metrics['avg_wait']:.0f} | "
                  f"reward={total_reward:.2f} | loss={record['avg_loss']:.4f}")

    # Save model
    torch.save(agent.policy_net.state_dict(), os.path.join(save_dir, "dqn_model.pt"))
    return history


def evaluate_dqn(env: ClusterEnv, agent: DQNAgent, jobs: list[Job]) -> dict:
    """Evaluate DQN greedily (no exploration)."""
    old_eps = agent.eps
    agent.eps = 0.0
    obs, info = env.reset(jobs)
    mask = info["mask"]

    while True:
        action = agent.select_action(obs, mask)
        obs, reward, done, _, info = env.step(action if action >= 0 else -1)
        mask = info["mask"]
        if done:
            break

    agent.eps = old_eps
    return env.get_metrics()


def train_ppo(env: ClusterEnv, train_jobs: list[Job], val_jobs: list[Job],
              num_episodes: int = 100, save_dir: str = "../data") -> list[dict]:
    """Train PPO agent and return per-episode metrics."""
    agent = PPOAgent(env.obs_dim, env.window_size, lr=3e-4, gamma=0.99,
                     clip_eps=0.2, epochs=4, batch_size=64,
                     entropy_coef=0.01)

    history = []

    for ep in range(num_episodes):
        obs, info = env.reset(train_jobs)
        mask = info["mask"]
        total_reward = 0.0
        steps = 0

        while True:
            action, log_prob, value = agent.select_action(obs, mask)
            if action < 0:
                next_obs, reward, done, _, info = env.step(-1)
            else:
                next_obs, reward, done, _, info = env.step(action)
                agent.store(obs, action, reward, log_prob, value, mask)

            total_reward += reward
            steps += 1
            obs = next_obs
            mask = info["mask"]

            if done:
                break

        loss = agent.update()
        train_metrics = env.get_metrics()

        # Validation
        val_metrics = evaluate_ppo(env, agent, val_jobs)

        record = {
            "episode": ep,
            "train_avg_wait": train_metrics["avg_wait"],
            "train_avg_slowdown": train_metrics["avg_slowdown"],
            "train_makespan": train_metrics["makespan"],
            "train_reward": total_reward,
            "val_avg_wait": val_metrics["avg_wait"],
            "val_avg_slowdown": val_metrics["avg_slowdown"],
            "val_makespan": val_metrics["makespan"],
            "loss": loss,
            "steps": steps,
        }
        history.append(record)

        if ep % 10 == 0 or ep == num_episodes - 1:
            print(f"[PPO] Ep {ep:3d} | "
                  f"train_wait={train_metrics['avg_wait']:.0f} | "
                  f"val_wait={val_metrics['avg_wait']:.0f} | "
                  f"reward={total_reward:.2f} | loss={loss:.4f}")

    # Save model
    torch.save(agent.net.state_dict(), os.path.join(save_dir, "ppo_model.pt"))
    return history


def evaluate_ppo(env: ClusterEnv, agent: PPOAgent, jobs: list[Job]) -> dict:
    """Evaluate PPO greedily."""
    obs, info = env.reset(jobs)
    mask = info["mask"]

    while True:
        valid_actions = np.where(mask)[0]
        if len(valid_actions) == 0:
            obs, reward, done, _, info = env.step(-1)
        else:
            with torch.no_grad():
                obs_t = torch.FloatTensor(obs).unsqueeze(0)
                logits, _ = agent.net(obs_t)
                logits = logits.squeeze(0)
                mask_t = torch.full((agent.action_dim,), -1e9)
                mask_t[valid_actions] = 0.0
                logits = logits + mask_t
                action = torch.argmax(logits).item()
            obs, reward, done, _, info = env.step(action)
        mask = info["mask"]
        if done:
            break

    return env.get_metrics()
