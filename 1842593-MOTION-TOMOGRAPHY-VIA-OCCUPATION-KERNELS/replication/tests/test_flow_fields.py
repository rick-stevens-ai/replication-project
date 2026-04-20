"""Tests for flow field implementations."""

import sys
import numpy as np
import pytest

sys.path.insert(0, '.')
from src.flow_fields import (flow_field_paper, flow_field_linear, 
                              flow_field_constant, evaluate_on_grid)


class TestFlowFieldPaper:
    def test_output_shape_scalar(self):
        x = np.array([0.5, 0.5])
        f = flow_field_paper(x)
        assert f.shape == (2,)
    
    def test_output_shape_batch(self):
        x = np.random.rand(10, 2)
        f = flow_field_paper(x)
        assert f.shape == (10, 2)
    
    def test_symmetry_properties(self):
        """The flow field should have approximate anti-symmetry."""
        # f1 at (0.25, 0.25) should be positive (5*exp term dominates)
        f = flow_field_paper(np.array([0.25, 0.25]))
        assert f[0] > 0  # f1 dominated by +5*exp term
    
    def test_nonzero(self):
        """Flow field should be nonzero at center."""
        f = flow_field_paper(np.array([0.5, 0.5]))
        assert np.linalg.norm(f) > 0.01


class TestFlowFieldLinear:
    def test_values(self):
        x = np.array([1.0, 2.0])
        f = flow_field_linear(x)
        np.testing.assert_allclose(f, [2.0, -0.2])
    
    def test_origin(self):
        f = flow_field_linear(np.array([0.0, 0.0]))
        np.testing.assert_allclose(f, [0.0, 0.0])


class TestFlowFieldConstant:
    def test_values(self):
        f = flow_field_constant(np.array([0.5, 0.5]))
        np.testing.assert_allclose(f, [0.2, 0.1])
    
    def test_constant_everywhere(self):
        pts = np.random.rand(5, 2)
        f = flow_field_constant(pts)
        for i in range(5):
            np.testing.assert_allclose(f[i], [0.2, 0.1])


class TestEvaluateOnGrid:
    def test_output_shapes(self):
        X, Y, U, V = evaluate_on_grid(flow_field_paper, nx=10, ny=10)
        assert X.shape == (10, 10)
        assert U.shape == (10, 10)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
