"""Tests for kernel functions and occupation kernel computations."""

import sys
import numpy as np
import pytest

sys.path.insert(0, '.')
from src.kernels import (gaussian_rbf, exponential_dot, occupation_kernel_eval,
                         gram_matrix_fast, gram_matrix_entry)


class TestGaussianRBF:
    def test_self_kernel(self):
        """K(x,x) = exp(0) = 1 for any x."""
        x = np.array([0.5, 0.3])
        assert np.isclose(gaussian_rbf(x, x, mu=1.0), 1.0)
    
    def test_symmetry(self):
        """K(x,y) = K(y,x)."""
        x = np.array([0.1, 0.2])
        y = np.array([0.8, 0.7])
        assert np.isclose(gaussian_rbf(x, y), gaussian_rbf(y, x))
    
    def test_decay(self):
        """Kernel decays with distance."""
        x = np.array([0.0, 0.0])
        y_near = np.array([0.1, 0.0])
        y_far = np.array([1.0, 0.0])
        assert gaussian_rbf(x, y_near) > gaussian_rbf(x, y_far)
    
    def test_mu_effect(self):
        """Larger mu => slower decay."""
        x = np.array([0.0, 0.0])
        y = np.array([1.0, 0.0])
        assert gaussian_rbf(x, y, mu=10.0) > gaussian_rbf(x, y, mu=0.1)
    
    def test_positive_definite(self):
        """Gram matrix should be positive semi-definite."""
        points = np.random.RandomState(42).rand(10, 2)
        G = np.array([[gaussian_rbf(points[i], points[j]) 
                       for j in range(10)] for i in range(10)])
        eigenvals = np.linalg.eigvalsh(G)
        assert np.all(eigenvals >= -1e-10)


class TestExponentialDot:
    def test_symmetry(self):
        x = np.array([0.1, 0.2])
        y = np.array([0.8, 0.7])
        assert np.isclose(exponential_dot(x, y), exponential_dot(y, x))
    
    def test_positive(self):
        x = np.array([0.5, 0.3])
        y = np.array([0.2, 0.8])
        assert exponential_dot(x, y) > 0


class TestOccupationKernel:
    def test_constant_trajectory(self):
        """For constant trajectory gamma(t)=x0, OK(x) = T * K(x, x0)."""
        x0 = np.array([0.5, 0.5])
        T = 1.0
        n = 100
        times = np.linspace(0, T, n+1)
        traj = np.tile(x0, (n+1, 1))
        
        x_eval = np.array([0.3, 0.4])
        ok_val = occupation_kernel_eval(x_eval, traj, times, gaussian_rbf, mu=1.0)
        expected = T * gaussian_rbf(x_eval, x0, mu=1.0)
        assert np.isclose(ok_val, expected, rtol=1e-4)
    
    def test_positivity(self):
        """Occupation kernel should be positive for Gaussian RBF."""
        traj = np.column_stack([np.linspace(0, 1, 51), np.linspace(0, 1, 51)])
        times = np.linspace(0, 1, 51)
        x = np.array([0.5, 0.5])
        val = occupation_kernel_eval(x, traj, times, gaussian_rbf, mu=1.0)
        assert val > 0


class TestGramMatrix:
    def test_symmetry(self):
        """Gram matrix should be symmetric."""
        rng = np.random.RandomState(42)
        trajs = [np.column_stack([np.linspace(0, 1, 21) + rng.randn(21)*0.1,
                                   np.linspace(0, 1, 21) + rng.randn(21)*0.1])
                 for _ in range(3)]
        times = [np.linspace(0, 1, 21)] * 3
        G = gram_matrix_fast(trajs, times, gaussian_rbf, mu=1.0)
        assert np.allclose(G, G.T, atol=1e-10)
    
    def test_positive_definite(self):
        """Gram matrix should be positive semi-definite."""
        rng = np.random.RandomState(42)
        trajs = [np.column_stack([np.linspace(0, 1, 21) * np.cos(a) + rng.randn(21)*0.01,
                                   np.linspace(0, 1, 21) * np.sin(a) + rng.randn(21)*0.01])
                 for a in np.linspace(0, np.pi, 5)]
        times = [np.linspace(0, 1, 21)] * 5
        G = gram_matrix_fast(trajs, times, gaussian_rbf, mu=1.0)
        eigenvals = np.linalg.eigvalsh(G)
        assert np.all(eigenvals >= -1e-10)
    
    def test_same_trajectory(self):
        """G_ii = ||Gamma_i||^2 should be positive."""
        traj = np.column_stack([np.linspace(0, 1, 51), np.zeros(51)])
        times = np.linspace(0, 1, 51)
        val = gram_matrix_entry(traj, times, traj, times, gaussian_rbf, mu=1.0)
        assert val > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
