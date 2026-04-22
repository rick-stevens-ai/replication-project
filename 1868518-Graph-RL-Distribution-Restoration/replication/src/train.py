"""
Training Script for Graph-RL Distribution System Restoration
=============================================================
Implements:
1. Multi-Agent GCN-DQN (paper's main method)
2. MLP-DQN baseline
3. Single-Agent GCN-DQN baseline
4. Pre-training paradigm (small network → large network transfer)

Zhao & Wang (2021): "Learning Sequential Distribution System Restoration 
via Graph-Reinforcement Learning" (OSTI 1868518)
"""

import os
import sys
import json
import time
import argparse
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import defaultdict
import copy

from environment import DistributionRestorationEnv, make_env
from models import GCN_DQN, MLP_DQN, SingleAgentGCN_DQN
from replay_buffer import MultiAgentReplayBuffer, ReplayBuffer


class GCN_DQN_Trainer:
    """
    Multi-Agent GCN Double DQN trainer.
    
    Key features (from paper):
    - Double DQN to reduce overestimation
    - Multi-agent with parameter sharing
    - Graph convolutional encoding of network topology
    - Epsilon-greedy exploration with decay
    - Target network soft update
    """
    
    def __init__(self, env, config=None, device='cpu'):
        self.env = env
        self.device = torch.device(device)
        
        # Default config
        self.config = {
            'lr': 1e-4,
            'gamma': 0.99,
            'batch_size': 64,
            'buffer_size': 50000,
            'epsilon_start': 1.0,
            'epsilon_end': 0.05,
            'epsilon_decay': 0.9995,
            'target_update_freq': 100,
            'tau': 0.005,  # Soft update parameter
            'hidden_dim': 64,
            'n_gcn_layers': 3,
            'graph_embed_dim': 128,
            'n_episodes': 5000,
            'max_steps': 30,
            'eval_interval': 100,
            'save_interval': 500,
            'log_interval': 50,
        }
        if config:
            self.config.update(config)
        
        # Initialize networks
        self.n_switches = len(env.switch_indices)
        self.n_dgs = env.n_dgs
        self.n_buses = len(env.net.bus)
        
        # Pad switch states to fixed size
        self.switch_state_dim = max(self.n_switches, 1)
        
        self.policy_net = GCN_DQN(
            node_feature_dim=8,
            n_switches=self.n_switches,
            n_dgs=self.n_dgs,
            hidden_dim=self.config['hidden_dim'],
            n_gcn_layers=self.config['n_gcn_layers'],
            graph_embed_dim=self.config['graph_embed_dim'],
            global_feature_dim=5,
            switch_state_dim=self.switch_state_dim,
            dueling=True
        ).to(self.device)
        
        self.target_net = copy.deepcopy(self.policy_net)
        self.target_net.eval()
        
        self.optimizer = optim.Adam(self.policy_net.parameters(), 
                                     lr=self.config['lr'])
        
        self.replay_buffer = MultiAgentReplayBuffer(
            capacity=self.config['buffer_size'])
        
        self.epsilon = self.config['epsilon_start']
        self.train_step = 0
        
        # DG bus indices (fixed for the network)
        self.agent_bus_indices = torch.tensor(
            env.dg_buses, dtype=torch.long).unsqueeze(0).to(self.device)
    
    def _state_to_tensors(self, state):
        """Convert state dict to tensors."""
        node_features = torch.FloatTensor(state['node_features']).unsqueeze(0).to(self.device)
        adjacency = torch.FloatTensor(state['adjacency']).unsqueeze(0).to(self.device)
        global_features = torch.FloatTensor(state['global_features']).unsqueeze(0).to(self.device)
        
        # Pad switch states
        sw = state['switch_states']
        if len(sw) < self.switch_state_dim:
            sw = np.pad(sw, (0, self.switch_state_dim - len(sw)))
        switch_states = torch.FloatTensor(sw[:self.switch_state_dim]).unsqueeze(0).to(self.device)
        
        return node_features, adjacency, global_features, switch_states
    
    def select_actions(self, state, evaluate=False):
        """
        Select actions for all agents using epsilon-greedy.
        
        Returns dict mapping agent_id → action
        """
        actions = {}
        n_actions = self.n_switches + 2
        
        if not evaluate and np.random.random() < self.epsilon:
            # Random actions
            for i in range(self.n_dgs):
                actions[i] = np.random.randint(0, n_actions)
        else:
            # Greedy actions from Q-network
            with torch.no_grad():
                node_features, adjacency, global_features, switch_states = \
                    self._state_to_tensors(state)
                
                q_values = self.policy_net(
                    node_features, adjacency, global_features, 
                    switch_states, self.agent_bus_indices
                )
                # q_values: (1, n_agents, n_actions)
                
                for i in range(self.n_dgs):
                    actions[i] = q_values[0, i].argmax().item()
        
        return actions
    
    def train_step_fn(self):
        """One training step: sample batch and update Q-network."""
        if len(self.replay_buffer) < self.config['batch_size']:
            return 0.0
        
        # Sample batch
        batch = self.replay_buffer.sample(self.config['batch_size'])
        states, actions_list, rewards, next_states, dones = batch
        
        batch_size = len(states)
        
        # Convert to tensors
        node_features = torch.stack([
            torch.FloatTensor(s['node_features']) for s in states
        ]).to(self.device)
        adjacencies = torch.stack([
            torch.FloatTensor(s['adjacency']) for s in states
        ]).to(self.device)
        global_feats = torch.stack([
            torch.FloatTensor(s['global_features']) for s in states
        ]).to(self.device)
        
        switch_states_batch = []
        for s in states:
            sw = s['switch_states']
            if len(sw) < self.switch_state_dim:
                sw = np.pad(sw, (0, self.switch_state_dim - len(sw)))
            switch_states_batch.append(torch.FloatTensor(sw[:self.switch_state_dim]))
        switch_states = torch.stack(switch_states_batch).to(self.device)
        
        # Next states
        next_node_features = torch.stack([
            torch.FloatTensor(s['node_features']) for s in next_states
        ]).to(self.device)
        next_adjacencies = torch.stack([
            torch.FloatTensor(s['adjacency']) for s in next_states
        ]).to(self.device)
        next_global_feats = torch.stack([
            torch.FloatTensor(s['global_features']) for s in next_states
        ]).to(self.device)
        
        next_switch_states_batch = []
        for s in next_states:
            sw = s['switch_states']
            if len(sw) < self.switch_state_dim:
                sw = np.pad(sw, (0, self.switch_state_dim - len(sw)))
            next_switch_states_batch.append(torch.FloatTensor(sw[:self.switch_state_dim]))
        next_switch_states = torch.stack(next_switch_states_batch).to(self.device)
        
        # Actions: (batch, n_agents)
        actions_tensor = torch.zeros(batch_size, self.n_dgs, dtype=torch.long).to(self.device)
        for b in range(batch_size):
            for agent_id, action in actions_list[b].items():
                if agent_id < self.n_dgs:
                    actions_tensor[b, agent_id] = action
        
        rewards_tensor = torch.FloatTensor(rewards).to(self.device)
        dones_tensor = torch.FloatTensor(dones).to(self.device)
        
        # Expand agent bus indices for batch
        agent_bus_idx = self.agent_bus_indices.expand(batch_size, -1)
        
        # Current Q-values
        current_q = self.policy_net(
            node_features, adjacencies, global_feats, 
            switch_states, agent_bus_idx
        )
        # (batch, n_agents, n_actions) → gather action Q-values
        current_q_gathered = current_q.gather(
            2, actions_tensor.unsqueeze(-1)
        ).squeeze(-1)
        # (batch, n_agents)
        
        # Double DQN: use policy net for action selection, target net for evaluation
        with torch.no_grad():
            next_q_policy = self.policy_net(
                next_node_features, next_adjacencies, next_global_feats,
                next_switch_states, agent_bus_idx
            )
            next_actions = next_q_policy.argmax(dim=-1)  # (batch, n_agents)
            
            next_q_target = self.target_net(
                next_node_features, next_adjacencies, next_global_feats,
                next_switch_states, agent_bus_idx
            )
            next_q_values = next_q_target.gather(
                2, next_actions.unsqueeze(-1)
            ).squeeze(-1)
            
            # TD target (shared reward for all agents)
            target_q = rewards_tensor.unsqueeze(1) + \
                       (1 - dones_tensor.unsqueeze(1)) * \
                       self.config['gamma'] * next_q_values
        
        # Loss: mean over agents and batch
        loss = F.smooth_l1_loss(current_q_gathered, target_q)
        
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.policy_net.parameters(), 10.0)
        self.optimizer.step()
        
        # Soft update target network
        self.train_step += 1
        if self.train_step % self.config['target_update_freq'] == 0:
            self._soft_update_target()
        
        return loss.item()
    
    def _soft_update_target(self):
        """Soft update target network parameters."""
        tau = self.config['tau']
        for target_param, policy_param in zip(
            self.target_net.parameters(), self.policy_net.parameters()):
            target_param.data.copy_(
                tau * policy_param.data + (1 - tau) * target_param.data)
    
    def train(self, save_dir='checkpoints'):
        """Main training loop."""
        os.makedirs(save_dir, exist_ok=True)
        
        history = {
            'episode_rewards': [],
            'episode_load_ratios': [],
            'losses': [],
            'epsilons': [],
            'eval_rewards': [],
            'eval_load_ratios': [],
        }
        
        best_eval_reward = -float('inf')
        
        for episode in range(self.config['n_episodes']):
            state = self.env.reset()
            episode_reward = 0.0
            episode_loss = 0.0
            n_steps = 0
            
            for step in range(self.config['max_steps']):
                actions = self.select_actions(state)
                next_state, reward, done, info = self.env.step(actions)
                
                self.replay_buffer.push(state, actions, reward, next_state, done)
                
                loss = self.train_step_fn()
                episode_loss += loss
                
                episode_reward += reward
                state = next_state
                n_steps += 1
                
                if done:
                    break
            
            # Decay epsilon
            self.epsilon = max(self.config['epsilon_end'],
                              self.epsilon * self.config['epsilon_decay'])
            
            history['episode_rewards'].append(episode_reward)
            history['episode_load_ratios'].append(
                self.env.restored_load / max(self.env.total_load, 1e-6))
            history['losses'].append(episode_loss / max(n_steps, 1))
            history['epsilons'].append(self.epsilon)
            
            # Logging
            if (episode + 1) % self.config['log_interval'] == 0:
                avg_reward = np.mean(history['episode_rewards'][-self.config['log_interval']:])
                avg_load = np.mean(history['episode_load_ratios'][-self.config['log_interval']:])
                avg_loss = np.mean(history['losses'][-self.config['log_interval']:])
                print(f"Episode {episode+1}/{self.config['n_episodes']} | "
                      f"Avg Reward: {avg_reward:.4f} | "
                      f"Avg Load Ratio: {avg_load:.4f} | "
                      f"Avg Loss: {avg_loss:.6f} | "
                      f"Epsilon: {self.epsilon:.4f}")
            
            # Evaluation
            if (episode + 1) % self.config['eval_interval'] == 0:
                eval_reward, eval_load = self.evaluate(n_episodes=20)
                history['eval_rewards'].append(eval_reward)
                history['eval_load_ratios'].append(eval_load)
                print(f"  [EVAL] Reward: {eval_reward:.4f} | Load Ratio: {eval_load:.4f}")
                
                if eval_reward > best_eval_reward:
                    best_eval_reward = eval_reward
                    self.save(os.path.join(save_dir, 'best_model.pt'))
                    print(f"  [EVAL] New best model saved!")
            
            # Periodic save
            if (episode + 1) % self.config['save_interval'] == 0:
                self.save(os.path.join(save_dir, f'model_ep{episode+1}.pt'))
        
        # Final save
        self.save(os.path.join(save_dir, 'final_model.pt'))
        
        # Save history
        with open(os.path.join(save_dir, 'training_history.json'), 'w') as f:
            json.dump({k: [float(v) for v in vs] for k, vs in history.items()}, f)
        
        return history
    
    def evaluate(self, n_episodes=50):
        """Evaluate current policy without exploration."""
        total_reward = 0.0
        total_load_ratio = 0.0
        
        for _ in range(n_episodes):
            state = self.env.reset()
            episode_reward = 0.0
            
            for step in range(self.config['max_steps']):
                actions = self.select_actions(state, evaluate=True)
                next_state, reward, done, info = self.env.step(actions)
                episode_reward += reward
                state = next_state
                if done:
                    break
            
            total_reward += episode_reward
            total_load_ratio += self.env.restored_load / max(self.env.total_load, 1e-6)
        
        return total_reward / n_episodes, total_load_ratio / n_episodes
    
    def save(self, path):
        """Save model checkpoint."""
        torch.save({
            'policy_net': self.policy_net.state_dict(),
            'target_net': self.target_net.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'epsilon': self.epsilon,
            'train_step': self.train_step,
            'config': self.config,
        }, path)
    
    def load(self, path):
        """Load model checkpoint."""
        checkpoint = torch.load(path, map_location=self.device)
        self.policy_net.load_state_dict(checkpoint['policy_net'])
        self.target_net.load_state_dict(checkpoint['target_net'])
        self.optimizer.load_state_dict(checkpoint['optimizer'])
        self.epsilon = checkpoint['epsilon']
        self.train_step = checkpoint['train_step']


class MLPDQNTrainer:
    """MLP-DQN Baseline Trainer (no graph structure)."""
    
    def __init__(self, env, config=None, device='cpu'):
        self.env = env
        self.device = torch.device(device)
        
        self.config = {
            'lr': 1e-4,
            'gamma': 0.99,
            'batch_size': 64,
            'buffer_size': 50000,
            'epsilon_start': 1.0,
            'epsilon_end': 0.05,
            'epsilon_decay': 0.9995,
            'target_update_freq': 100,
            'hidden_dim': 256,
            'n_episodes': 5000,
            'max_steps': 30,
            'eval_interval': 100,
            'log_interval': 50,
        }
        if config:
            self.config.update(config)
        
        # Flatten state: node features + global features + switch states
        self.n_buses = len(env.net.bus)
        self.state_dim = self.n_buses * 8 + 5 + len(env.switch_indices)
        self.n_actions = len(env.switch_indices) + 2  # Per agent (but single-agent here)
        # Total actions: all possible combinations simplified to sequential
        # Each step: choose one action from union of all agent actions
        self.total_actions = self.n_actions * env.n_dgs + 1  # +1 for global no-op
        
        self.policy_net = MLP_DQN(
            self.state_dim, self.total_actions, 
            hidden_dim=self.config['hidden_dim']
        ).to(self.device)
        
        self.target_net = copy.deepcopy(self.policy_net)
        self.target_net.eval()
        
        self.optimizer = optim.Adam(self.policy_net.parameters(), 
                                     lr=self.config['lr'])
        self.replay_buffer = ReplayBuffer(capacity=self.config['buffer_size'])
        self.epsilon = self.config['epsilon_start']
        self.train_step = 0
    
    def _state_to_flat(self, state):
        """Flatten state dictionary to vector."""
        flat = np.concatenate([
            state['node_features'].flatten(),
            state['global_features'],
            state['switch_states']
        ])
        # Pad/truncate to fixed size
        if len(flat) < self.state_dim:
            flat = np.pad(flat, (0, self.state_dim - len(flat)))
        else:
            flat = flat[:self.state_dim]
        return flat
    
    def _action_to_multi_agent(self, action):
        """Convert flat action index to multi-agent actions dict."""
        if action >= self.n_actions * self.env.n_dgs:
            # Global no-op
            return {i: self.n_actions - 1 for i in range(self.env.n_dgs)}
        
        agent_id = action // self.n_actions
        agent_action = action % self.n_actions
        
        actions = {i: self.n_actions - 1 for i in range(self.env.n_dgs)}  # Default no-op
        if agent_id < self.env.n_dgs:
            actions[agent_id] = agent_action
        return actions
    
    def select_action(self, state, evaluate=False):
        if not evaluate and np.random.random() < self.epsilon:
            return np.random.randint(0, self.total_actions)
        
        with torch.no_grad():
            flat_state = self._state_to_flat(state)
            state_tensor = torch.FloatTensor(flat_state).unsqueeze(0).to(self.device)
            q_values = self.policy_net(state_tensor)
            return q_values.argmax().item()
    
    def train(self, save_dir='checkpoints_mlp'):
        os.makedirs(save_dir, exist_ok=True)
        history = defaultdict(list)
        best_eval_reward = -float('inf')
        
        for episode in range(self.config['n_episodes']):
            state = self.env.reset()
            episode_reward = 0.0
            
            for step in range(self.config['max_steps']):
                action = self.select_action(state)
                multi_actions = self._action_to_multi_agent(action)
                next_state, reward, done, info = self.env.step(multi_actions)
                
                self.replay_buffer.push(
                    self._state_to_flat(state), action, reward,
                    self._state_to_flat(next_state), done)
                
                # Train
                if len(self.replay_buffer) >= self.config['batch_size']:
                    self._train_step()
                
                episode_reward += reward
                state = next_state
                if done:
                    break
            
            self.epsilon = max(self.config['epsilon_end'],
                              self.epsilon * self.config['epsilon_decay'])
            
            history['episode_rewards'].append(episode_reward)
            history['episode_load_ratios'].append(
                self.env.restored_load / max(self.env.total_load, 1e-6))
            
            if (episode + 1) % self.config['log_interval'] == 0:
                avg_r = np.mean(history['episode_rewards'][-self.config['log_interval']:])
                avg_l = np.mean(history['episode_load_ratios'][-self.config['log_interval']:])
                print(f"[MLP] Ep {episode+1} | Avg R: {avg_r:.4f} | Load: {avg_l:.4f}")
            
            if (episode + 1) % self.config['eval_interval'] == 0:
                eval_r, eval_l = self.evaluate()
                history['eval_rewards'].append(eval_r)
                history['eval_load_ratios'].append(eval_l)
                print(f"  [MLP EVAL] R: {eval_r:.4f} | Load: {eval_l:.4f}")
                if eval_r > best_eval_reward:
                    best_eval_reward = eval_r
                    torch.save(self.policy_net.state_dict(), 
                              os.path.join(save_dir, 'best_model.pt'))
        
        with open(os.path.join(save_dir, 'training_history.json'), 'w') as f:
            json.dump({k: [float(v) for v in vs] for k, vs in history.items()}, f)
        
        return dict(history)
    
    def _train_step(self):
        states, actions, rewards, next_states, dones = \
            self.replay_buffer.sample(self.config['batch_size'])
        
        states = torch.FloatTensor(np.array(states)).to(self.device)
        actions = torch.LongTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        next_states = torch.FloatTensor(np.array(next_states)).to(self.device)
        dones = torch.FloatTensor(dones).to(self.device)
        
        current_q = self.policy_net(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        
        with torch.no_grad():
            next_actions = self.policy_net(next_states).argmax(dim=1)
            next_q = self.target_net(next_states).gather(
                1, next_actions.unsqueeze(1)).squeeze(1)
            target_q = rewards + (1 - dones) * self.config['gamma'] * next_q
        
        loss = F.smooth_l1_loss(current_q, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        self.train_step += 1
        if self.train_step % self.config['target_update_freq'] == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())
    
    def evaluate(self, n_episodes=20):
        total_r, total_l = 0.0, 0.0
        for _ in range(n_episodes):
            state = self.env.reset()
            ep_r = 0.0
            for step in range(self.config['max_steps']):
                action = self.select_action(state, evaluate=True)
                multi_actions = self._action_to_multi_agent(action)
                state, reward, done, _ = self.env.step(multi_actions)
                ep_r += reward
                if done:
                    break
            total_r += ep_r
            total_l += self.env.restored_load / max(self.env.total_load, 1e-6)
        return total_r / n_episodes, total_l / n_episodes


def run_experiment(args):
    """Run a complete training experiment."""
    
    print(f"\n{'='*60}")
    print(f"Distribution System Restoration - Graph RL Replication")
    print(f"Network: {args.network}")
    print(f"Method: {args.method}")
    print(f"Device: {args.device}")
    print(f"{'='*60}\n")
    
    # Create environment
    env = make_env(
        network_case=args.network,
        max_steps=args.max_steps,
        n_dgs=args.n_dgs,
        seed=args.seed
    )
    
    # Base save directory
    save_dir = os.path.join(args.output_dir, f'{args.method}_{args.network}')
    os.makedirs(save_dir, exist_ok=True)
    
    # Config overrides
    config = {
        'n_episodes': args.n_episodes,
        'max_steps': args.max_steps,
        'lr': args.lr,
        'batch_size': args.batch_size,
    }
    
    if args.method == 'gcn_dqn':
        trainer = GCN_DQN_Trainer(env, config=config, device=args.device)
    elif args.method == 'mlp_dqn':
        trainer = MLPDQNTrainer(env, config=config, device=args.device)
    else:
        raise ValueError(f"Unknown method: {args.method}")
    
    # Train
    start_time = time.time()
    history = trainer.train(save_dir=save_dir)
    train_time = time.time() - start_time
    
    print(f"\nTraining completed in {train_time:.1f}s")
    print(f"Results saved to {save_dir}")
    
    # Save experiment metadata
    metadata = {
        'network': args.network,
        'method': args.method,
        'n_episodes': args.n_episodes,
        'training_time_s': train_time,
        'n_buses': len(env.net.bus),
        'n_switches': len(env.switch_indices),
        'n_dgs': env.n_dgs,
        'device': args.device,
        'seed': args.seed,
    }
    with open(os.path.join(save_dir, 'metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return history


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--network', type=str, default='ieee33',
                       choices=['ieee33', 'ieee123', 'ieee8500'])
    parser.add_argument('--method', type=str, default='gcn_dqn',
                       choices=['gcn_dqn', 'mlp_dqn'])
    parser.add_argument('--n_episodes', type=int, default=3000)
    parser.add_argument('--max_steps', type=int, default=30)
    parser.add_argument('--n_dgs', type=int, default=5)
    parser.add_argument('--lr', type=float, default=1e-4)
    parser.add_argument('--batch_size', type=int, default=64)
    parser.add_argument('--device', type=str, default='cpu')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--output_dir', type=str, default='../results')
    
    args = parser.parse_args()
    run_experiment(args)
