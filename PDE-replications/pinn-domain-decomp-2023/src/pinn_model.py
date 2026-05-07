"""
PINN Model with ResNet-style skip connections and adaptive tanh activation.
Implements the architecture from Kopaničáková et al. (2023).
"""

import torch
import torch.nn as nn
import numpy as np


class AdaptiveTanh(nn.Module):
    """Adaptive tanh activation: tanh(a * x) where a is learnable per layer."""
    def __init__(self, n_neurons):
        super().__init__()
        # One adaptive parameter per neuron (initialized to 1.0)
        self.a = nn.Parameter(torch.ones(n_neurons))

    def forward(self, x):
        return torch.tanh(self.a * x)


class ResNetPINN(nn.Module):
    """
    ResNet-style PINN: y_l = y_{l-1} + sigma(W_l y_{l-1} + b_l)
    
    Parameters:
        input_dim: dimension of input (e.g. 2 for (t,x))
        output_dim: dimension of output (e.g. 1)
        depth: number of hidden layers L-1 (total layers = depth + 2 for input/output)
        width: hidden layer width n_h
    """
    def __init__(self, input_dim, output_dim, depth, width):
        super().__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.depth = depth
        self.width = width

        # Input layer: W_0 x (no bias, maps d -> n_h)
        self.input_layer = nn.Linear(input_dim, width, bias=False)

        # Hidden layers with skip connections
        self.hidden_layers = nn.ModuleList()
        self.activations = nn.ModuleList()
        for l in range(depth):
            self.hidden_layers.append(nn.Linear(width, width))
            self.activations.append(AdaptiveTanh(width))

        # Output layer: W_L y_{L-1} + b_L
        self.output_layer = nn.Linear(width, output_dim)

        # Initialize weights using Xavier uniform
        self._init_weights()

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

    def forward(self, x):
        """
        Forward pass through the ResNet-style network.
        x: (batch_size, input_dim)
        Returns: (batch_size, output_dim) - the raw network output u_tilde
        """
        # Input layer
        y = self.input_layer(x)  # (batch, width)

        # Hidden layers with skip connections
        for layer, activation in zip(self.hidden_layers, self.activations):
            y = y + activation(layer(y))  # ResNet skip

        # Output layer
        y = self.output_layer(y)
        return y

    def get_layer_params(self):
        """
        Get parameter groups organized by layer for domain decomposition.
        Returns list of lists of parameters, one per layer.
        """
        layer_groups = []

        # Input layer params
        layer_groups.append(list(self.input_layer.parameters()))

        # Hidden layers (each: Linear weights+bias + AdaptiveTanh a)
        for l in range(self.depth):
            params = list(self.hidden_layers[l].parameters()) + \
                     list(self.activations[l].parameters())
            layer_groups.append(params)

        # Output layer params
        layer_groups.append(list(self.output_layer.parameters()))

        return layer_groups

    def get_layer_param_indices(self):
        """
        Get start/end indices for each layer's parameters in the flat parameter vector.
        Returns list of (start, end) tuples.
        """
        all_params = list(self.parameters())
        layer_groups = self.get_layer_params()

        indices = []
        param_to_idx = {}
        offset = 0
        for i, p in enumerate(all_params):
            n = p.numel()
            param_to_idx[id(p)] = (offset, offset + n)
            offset += n

        for group in layer_groups:
            group_start = float('inf')
            group_end = 0
            flat_indices = []
            for p in group:
                s, e = param_to_idx[id(p)]
                flat_indices.append((s, e))
                group_start = min(group_start, s)
                group_end = max(group_end, e)
            indices.append(flat_indices)

        return indices

    def count_parameters(self):
        return sum(p.numel() for p in self.parameters())
