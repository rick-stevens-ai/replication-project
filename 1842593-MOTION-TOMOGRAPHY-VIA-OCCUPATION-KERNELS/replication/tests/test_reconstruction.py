"""Tests for flow field reconstruction."""

import sys
import numpy as np
import pytest

sys.path.insert(0, '.')
from src.flow_fields import flow_field_paper, flow_field_constant
from src.trajectories import generate_random_trajectories
from src.reconstruction import FlowReconstructor, compute_errors


class TestFlowReconstructor:
    def test_single_step_reduces_error(self):
        """Single-step reconstruction should reduce error vs zero estimate."""
        N = 10
        true_trajs, dr_trajs, times_list, disps, r0s, thetas = \
            generate_random_trajectories(N, flow_field_paper, 
                                         domain=(0.2, 0.8, 0.2, 0.8),
                                         T=1.0, n_steps=50, speed=1.0, seed=42)
        
        rec = FlowReconstructor(mu=1.0, lam=1e-6, n_steps=50)
        F_hat, _ = rec.fit_single_step(dr_trajs, times_list, disps)
        
        # Error with estimate should be less than error with zero
        zero_err = compute_errors(flow_field_paper, lambda x: np.zeros(2), nx=10, ny=10)
        est_err = compute_errors(flow_field_paper, F_hat, nx=10, ny=10)
        
        assert est_err['mean_error'] < zero_err['mean_error']
    
    def test_iterative_improves(self):
        """More iterations should generally reduce error."""
        N = 10
        true_trajs, dr_trajs, times_list, disps, r0s, thetas = \
            generate_random_trajectories(N, flow_field_paper,
                                         domain=(0.2, 0.8, 0.2, 0.8),
                                         T=1.0, n_steps=50, speed=1.0, seed=42)
        true_endpoints = np.array([t[-1] for t in true_trajs])
        
        rec = FlowReconstructor(mu=1.0, lam=1e-6, n_steps=50)
        F_hat, errors = rec.fit_iterative(
            r0s, np.full(N, 1.0), thetas, true_endpoints,
            T=1.0, n_iterations=5, verbose=False)
        
        # Displacement errors should decrease
        assert errors[-1] < errors[0]
    
    def test_constant_field_recovery(self):
        """Should recover constant field well."""
        N = 15
        true_trajs, dr_trajs, times_list, disps, r0s, thetas = \
            generate_random_trajectories(N, flow_field_constant,
                                         domain=(0.2, 0.8, 0.2, 0.8),
                                         T=1.0, n_steps=50, speed=1.0, seed=42)
        true_endpoints = np.array([t[-1] for t in true_trajs])
        
        rec = FlowReconstructor(mu=1.0, lam=1e-6, n_steps=50)
        F_hat, _ = rec.fit_iterative(
            r0s, np.full(N, 1.0), thetas, true_endpoints,
            T=1.0, n_iterations=5, verbose=False)
        
        errs = compute_errors(flow_field_constant, F_hat, nx=10, ny=10)
        assert errs['mean_error'] < 0.5  # Should be quite good


class TestComputeErrors:
    def test_zero_error(self):
        """Same function should give zero error."""
        errs = compute_errors(flow_field_paper, flow_field_paper, nx=10, ny=10)
        assert errs['rmse'] < 1e-10
        assert errs['mean_error'] < 1e-10
    
    def test_nonzero_error(self):
        errs = compute_errors(flow_field_paper, lambda x: np.zeros(2), nx=10, ny=10)
        assert errs['rmse'] > 0
        assert errs['mean_error'] > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
