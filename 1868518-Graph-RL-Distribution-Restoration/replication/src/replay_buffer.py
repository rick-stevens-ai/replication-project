"""
Experience Replay Buffer for DQN Training
==========================================
Supports prioritized experience replay for multi-agent Graph-RL.
"""

import numpy as np
from collections import deque
import random
from typing import Dict, List, Tuple, Optional


class ReplayBuffer:
    """Standard replay buffer for DQN."""
    
    def __init__(self, capacity=100000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        batch = random.sample(self.buffer, min(batch_size, len(self.buffer)))
        states, actions, rewards, next_states, dones = zip(*batch)
        return states, actions, rewards, next_states, dones
    
    def __len__(self):
        return len(self.buffer)


class PrioritizedReplayBuffer:
    """
    Prioritized Experience Replay (PER) buffer.
    Samples transitions with probability proportional to their TD error.
    """
    
    def __init__(self, capacity=100000, alpha=0.6, beta=0.4, beta_increment=0.001):
        self.capacity = capacity
        self.alpha = alpha  # Priority exponent
        self.beta = beta    # Importance sampling exponent
        self.beta_increment = beta_increment
        
        self.buffer = []
        self.priorities = np.zeros(capacity, dtype=np.float32)
        self.position = 0
        self.size = 0
        self.max_priority = 1.0
    
    def push(self, state, action, reward, next_state, done):
        if self.size < self.capacity:
            self.buffer.append((state, action, reward, next_state, done))
        else:
            self.buffer[self.position] = (state, action, reward, next_state, done)
        
        self.priorities[self.position] = self.max_priority
        self.position = (self.position + 1) % self.capacity
        self.size = min(self.size + 1, self.capacity)
    
    def sample(self, batch_size):
        priorities = self.priorities[:self.size] ** self.alpha
        probabilities = priorities / priorities.sum()
        
        indices = np.random.choice(self.size, size=min(batch_size, self.size),
                                    p=probabilities, replace=False)
        
        # Importance sampling weights
        self.beta = min(1.0, self.beta + self.beta_increment)
        weights = (self.size * probabilities[indices]) ** (-self.beta)
        weights = weights / weights.max()
        
        batch = [self.buffer[i] for i in indices]
        states, actions, rewards, next_states, dones = zip(*batch)
        
        return states, actions, rewards, next_states, dones, indices, weights
    
    def update_priorities(self, indices, td_errors):
        for idx, td_error in zip(indices, td_errors):
            self.priorities[idx] = abs(td_error) + 1e-6
            self.max_priority = max(self.max_priority, self.priorities[idx])
    
    def __len__(self):
        return self.size


class MultiAgentReplayBuffer:
    """
    Replay buffer that stores multi-agent transitions.
    Each transition contains states, actions, and rewards for all agents.
    """
    
    def __init__(self, capacity=100000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state_dict, actions_dict, reward, next_state_dict, done):
        """
        Store a multi-agent transition.
        
        Args:
            state_dict: environment state dictionary
            actions_dict: {agent_id: action} mapping
            reward: shared team reward
            next_state_dict: next environment state
            done: episode termination flag
        """
        self.buffer.append((state_dict, actions_dict, reward, next_state_dict, done))
    
    def sample(self, batch_size):
        batch = random.sample(self.buffer, min(batch_size, len(self.buffer)))
        return list(zip(*batch))
    
    def __len__(self):
        return len(self.buffer)
