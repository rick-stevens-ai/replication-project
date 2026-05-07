"""
Neural network architectures for NN-DO/BO methods.
Zhang et al. 2019 - Learning in Modal Space.
"""
import torch
import torch.nn as nn
import numpy as np


class FeedForwardNet(nn.Module):
    """Standard feed-forward neural network with tanh activation."""
    def __init__(self, input_dim, output_dim, hidden_layers, hidden_neurons):
        super().__init__()
        layers = []
        prev = input_dim
        for _ in range(hidden_layers):
            layers.append(nn.Linear(prev, hidden_neurons))
            layers.append(nn.Tanh())
            prev = hidden_neurons
        layers.append(nn.Linear(prev, output_dim))
        self.net = nn.Sequential(*layers)
        self._init_weights()

    def _init_weights(self):
        for m in self.net:
            if isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight)
                nn.init.zeros_(m.bias)

    def forward(self, x):
        return self.net(x)


def gauss_legendre_points(n, a=0.0, b=1.0):
    """Gauss-Legendre quadrature points and weights on [a, b]."""
    nodes, weights = np.polynomial.legendre.leggauss(n)
    # Map from [-1, 1] to [a, b]
    nodes = 0.5 * (b - a) * nodes + 0.5 * (a + b)
    weights = 0.5 * (b - a) * weights
    return nodes, weights


def inverse_normal_cdf_gl(n):
    """Generate stochastic collocation points for N(0,1) using GL + inverse CDF."""
    from scipy.stats import norm
    nodes, weights = gauss_legendre_points(n, a=0.0, b=1.0)
    # Map uniform [0,1] -> N(0,1) via inverse CDF
    xi_points = norm.ppf(nodes)
    return xi_points, weights
