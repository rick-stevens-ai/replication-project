"""
GNN + RL Models for Distribution System Restoration
====================================================
Replication of Zhao & Wang (2021): Graph-Reinforcement Learning

This module implements:
1. GCN-DQN: Graph Convolutional Network + Double DQN (paper's main approach)
2. MLP-DQN: Feedforward network baseline
3. Single-agent DQN: Non-multi-agent baseline
4. Multi-Agent GCN-DQN with parameter sharing
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, List, Optional, Tuple


class GCNLayer(nn.Module):
    """
    Graph Convolutional Layer following Kipf & Welling (2017).
    
    H^{l+1} = sigma(D^{-1/2} A_hat D^{-1/2} H^l W^l)
    where A_hat = A + I (adjacency with self-loops)
    """
    
    def __init__(self, in_features, out_features, bias=True):
        super().__init__()
        self.weight = nn.Parameter(torch.FloatTensor(in_features, out_features))
        if bias:
            self.bias = nn.Parameter(torch.FloatTensor(out_features))
        else:
            self.bias = None
        self.reset_parameters()
    
    def reset_parameters(self):
        nn.init.xavier_uniform_(self.weight)
        if self.bias is not None:
            nn.init.zeros_(self.bias)
    
    def forward(self, x, adj):
        """
        Args:
            x: Node features (batch, n_nodes, in_features)
            adj: Normalized adjacency matrix (batch, n_nodes, n_nodes)
        Returns:
            Updated node features (batch, n_nodes, out_features)
        """
        # x @ W
        support = torch.matmul(x, self.weight)
        # A_hat @ (x @ W)
        output = torch.bmm(adj, support)
        
        if self.bias is not None:
            output = output + self.bias
        return output


class GraphEncoder(nn.Module):
    """
    Multi-layer GCN encoder for distribution network topology.
    
    Encodes the power network graph into node embeddings and a graph-level
    embedding that captures the spatial structure and inter-device interactions.
    """
    
    def __init__(self, node_feature_dim=8, hidden_dim=64, n_gcn_layers=3,
                 graph_embed_dim=128, dropout=0.1):
        super().__init__()
        
        self.node_feature_dim = node_feature_dim
        self.hidden_dim = hidden_dim
        self.graph_embed_dim = graph_embed_dim
        
        # Input projection
        self.input_proj = nn.Linear(node_feature_dim, hidden_dim)
        
        # GCN layers
        self.gcn_layers = nn.ModuleList()
        self.gcn_norms = nn.ModuleList()
        for i in range(n_gcn_layers):
            self.gcn_layers.append(GCNLayer(hidden_dim, hidden_dim))
            self.gcn_norms.append(nn.LayerNorm(hidden_dim))
        
        self.dropout = nn.Dropout(dropout)
        
        # Graph-level readout
        self.graph_readout = nn.Sequential(
            nn.Linear(hidden_dim, graph_embed_dim),
            nn.ReLU(),
            nn.Linear(graph_embed_dim, graph_embed_dim)
        )
        
        # Node-level output
        self.node_output = nn.Sequential(
            nn.Linear(hidden_dim, graph_embed_dim),
            nn.ReLU()
        )
    
    def normalize_adjacency(self, adj):
        """
        Compute D^{-1/2} A_hat D^{-1/2} normalization.
        A_hat already includes self-loops.
        """
        # Degree matrix
        degree = adj.sum(dim=-1, keepdim=True)
        degree = degree.clamp(min=1e-6)
        # D^{-1/2}
        d_inv_sqrt = 1.0 / torch.sqrt(degree)
        # D^{-1/2} A D^{-1/2}
        adj_normalized = adj * d_inv_sqrt * d_inv_sqrt.transpose(-1, -2)
        return adj_normalized
    
    def forward(self, node_features, adjacency):
        """
        Args:
            node_features: (batch, n_nodes, node_feature_dim)
            adjacency: (batch, n_nodes, n_nodes) - with self-loops
        
        Returns:
            node_embeddings: (batch, n_nodes, graph_embed_dim)
            graph_embedding: (batch, graph_embed_dim)
        """
        # Normalize adjacency
        adj_norm = self.normalize_adjacency(adjacency)
        
        # Initial projection
        h = self.input_proj(node_features)
        h = F.relu(h)
        
        # GCN layers with residual connections
        for i, (gcn, norm) in enumerate(zip(self.gcn_layers, self.gcn_norms)):
            h_new = gcn(h, adj_norm)
            h_new = norm(h_new)
            h_new = F.relu(h_new)
            h_new = self.dropout(h_new)
            h = h + h_new  # Residual connection
        
        # Node embeddings
        node_embeddings = self.node_output(h)
        
        # Graph-level embedding via mean pooling
        graph_embedding = self.graph_readout(h.mean(dim=1))
        
        return node_embeddings, graph_embedding


class GCN_DQN(nn.Module):
    """
    Graph Convolutional Network + Double DQN for multi-agent restoration.
    
    Architecture (following the paper):
    1. GCN encodes network topology → node embeddings + graph embedding
    2. Agent-specific features extracted from node embedding at DG bus
    3. Combined with global features → Q-value for each action
    
    Multi-agent with parameter sharing: all agents share the same network
    but receive different observations (their local node embedding).
    """
    
    def __init__(self, node_feature_dim=8, n_switches=20, n_dgs=5,
                 hidden_dim=64, n_gcn_layers=3, graph_embed_dim=128,
                 global_feature_dim=5, switch_state_dim=20,
                 dueling=True, dropout=0.1):
        super().__init__()
        
        self.n_switches = n_switches
        self.n_dgs = n_dgs
        self.n_actions = n_switches + 2  # switches + DG toggle + no-op
        self.dueling = dueling
        
        # Graph encoder
        self.graph_encoder = GraphEncoder(
            node_feature_dim=node_feature_dim,
            hidden_dim=hidden_dim,
            n_gcn_layers=n_gcn_layers,
            graph_embed_dim=graph_embed_dim,
            dropout=dropout
        )
        
        # Context encoder for global features
        self.context_encoder = nn.Sequential(
            nn.Linear(global_feature_dim + switch_state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, graph_embed_dim),
            nn.ReLU()
        )
        
        # Q-network (combines graph embedding + agent's node embedding + context)
        q_input_dim = graph_embed_dim * 3  # graph + agent node + context
        
        if dueling:
            # Dueling architecture
            self.value_stream = nn.Sequential(
                nn.Linear(q_input_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, hidden_dim // 2),
                nn.ReLU(),
                nn.Linear(hidden_dim // 2, 1)
            )
            self.advantage_stream = nn.Sequential(
                nn.Linear(q_input_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, hidden_dim // 2),
                nn.ReLU(),
                nn.Linear(hidden_dim // 2, self.n_actions)
            )
        else:
            self.q_network = nn.Sequential(
                nn.Linear(q_input_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, self.n_actions)
            )
    
    def forward(self, node_features, adjacency, global_features, 
                switch_states, agent_bus_indices):
        """
        Compute Q-values for all agents.
        
        Args:
            node_features: (batch, n_nodes, node_feat_dim)
            adjacency: (batch, n_nodes, n_nodes)
            global_features: (batch, global_feat_dim)
            switch_states: (batch, n_switches)
            agent_bus_indices: (batch, n_agents) - bus index for each agent
        
        Returns:
            q_values: (batch, n_agents, n_actions)
        """
        batch_size = node_features.shape[0]
        
        # Encode graph
        node_embeddings, graph_embedding = self.graph_encoder(
            node_features, adjacency)
        
        # Encode context
        context_input = torch.cat([global_features, switch_states], dim=-1)
        context_embedding = self.context_encoder(context_input)
        
        # Extract agent-specific node embeddings
        # agent_bus_indices: (batch, n_agents)
        n_agents = agent_bus_indices.shape[1]
        
        # Gather node embeddings at agent bus positions
        idx = agent_bus_indices.unsqueeze(-1).expand(-1, -1, node_embeddings.shape[-1])
        agent_node_embeddings = torch.gather(node_embeddings, 1, idx)
        # (batch, n_agents, graph_embed_dim)
        
        # Expand graph and context embeddings for each agent
        graph_emb_expanded = graph_embedding.unsqueeze(1).expand(-1, n_agents, -1)
        context_emb_expanded = context_embedding.unsqueeze(1).expand(-1, n_agents, -1)
        
        # Concatenate
        combined = torch.cat([
            graph_emb_expanded, 
            agent_node_embeddings, 
            context_emb_expanded
        ], dim=-1)
        # (batch, n_agents, q_input_dim)
        
        # Reshape for Q-network
        combined_flat = combined.view(batch_size * n_agents, -1)
        
        if self.dueling:
            value = self.value_stream(combined_flat)
            advantage = self.advantage_stream(combined_flat)
            q_values = value + advantage - advantage.mean(dim=-1, keepdim=True)
        else:
            q_values = self.q_network(combined_flat)
        
        q_values = q_values.view(batch_size, n_agents, self.n_actions)
        
        return q_values


class MLP_DQN(nn.Module):
    """
    Feedforward MLP DQN baseline (no graph structure).
    Used for comparison to show GCN's advantage.
    """
    
    def __init__(self, state_dim, n_actions, hidden_dim=256, n_layers=3):
        super().__init__()
        
        layers = []
        layers.append(nn.Linear(state_dim, hidden_dim))
        layers.append(nn.ReLU())
        
        for _ in range(n_layers - 1):
            layers.append(nn.Linear(hidden_dim, hidden_dim))
            layers.append(nn.ReLU())
        
        layers.append(nn.Linear(hidden_dim, n_actions))
        self.network = nn.Sequential(*layers)
    
    def forward(self, state):
        """
        Args:
            state: (batch, state_dim) flattened state vector
        Returns:
            q_values: (batch, n_actions)
        """
        return self.network(state)


class SingleAgentGCN_DQN(nn.Module):
    """
    Single-agent GCN-DQN baseline.
    One agent controls all switches and DGs.
    Action space is the Cartesian product (simplified to sequential).
    """
    
    def __init__(self, node_feature_dim=8, n_actions=50,
                 hidden_dim=64, n_gcn_layers=3, graph_embed_dim=128,
                 global_feature_dim=5, switch_state_dim=20):
        super().__init__()
        
        self.graph_encoder = GraphEncoder(
            node_feature_dim=node_feature_dim,
            hidden_dim=hidden_dim,
            n_gcn_layers=n_gcn_layers,
            graph_embed_dim=graph_embed_dim
        )
        
        self.context_encoder = nn.Sequential(
            nn.Linear(global_feature_dim + switch_state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, graph_embed_dim),
            nn.ReLU()
        )
        
        self.q_network = nn.Sequential(
            nn.Linear(graph_embed_dim * 2, hidden_dim * 2),
            nn.ReLU(),
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, n_actions)
        )
    
    def forward(self, node_features, adjacency, global_features, switch_states):
        """Single agent Q-values."""
        _, graph_embedding = self.graph_encoder(node_features, adjacency)
        context = self.context_encoder(
            torch.cat([global_features, switch_states], dim=-1))
        combined = torch.cat([graph_embedding, context], dim=-1)
        return self.q_network(combined)
