"""
Scipy L-BFGS-B wrapper for PyTorch models.
This provides a more robust L-BFGS implementation than PyTorch's built-in.
"""

import torch
import numpy as np
from scipy.optimize import minimize


class ScipyLBFGS:
    """
    Wrapper to use scipy's L-BFGS-B optimizer with PyTorch models.
    Converts between numpy flat arrays and PyTorch parameters.
    """

    def __init__(self, model, loss_fn, maxiter=20000, m=3, factr=1e-16, pgtol=1e-16):
        self.model = model
        self.loss_fn = loss_fn
        self.maxiter = maxiter
        self.m = m
        self.factr = factr
        self.pgtol = pgtol

        self.params = list(model.parameters())
        self.shapes = [p.shape for p in self.params]
        self.sizes = [p.numel() for p in self.params]
        self.n_params = sum(self.sizes)

        self.loss_history = []
        self._iter_count = 0

    def _params_to_vec(self):
        return np.concatenate([p.data.cpu().numpy().ravel() for p in self.params])

    def _vec_to_params(self, x):
        offset = 0
        for p, shape, size in zip(self.params, self.shapes, self.sizes):
            p.data = torch.tensor(
                x[offset:offset + size].reshape(shape),
                dtype=p.dtype, device=p.device
            )
            offset += size

    def _objective(self, x):
        self._vec_to_params(x)

        # Compute loss and gradient
        for p in self.params:
            if p.grad is not None:
                p.grad.zero_()

        loss = self.loss_fn()
        loss.backward()

        # Collect gradient
        grad = np.concatenate([
            p.grad.cpu().numpy().ravel() for p in self.params
        ])

        loss_val = loss.item()
        self.loss_history.append(loss_val)
        self._iter_count += 1

        return loss_val, grad.astype(np.float64)

    def _callback(self, x):
        """Called after each L-BFGS iteration."""
        pass

    def optimize(self, callback=None):
        x0 = self._params_to_vec().astype(np.float64)

        result = minimize(
            self._objective,
            x0,
            method='L-BFGS-B',
            jac=True,
            options={
                'maxiter': self.maxiter,
                'maxcor': self.m,  # history size
                'ftol': self.factr * np.finfo(float).eps,
                'gtol': self.pgtol,
                'disp': False,
            },
            callback=callback,
        )

        # Set final parameters
        self._vec_to_params(result.x)

        return result


class ScipyLBFGSSubset:
    """
    Scipy L-BFGS-B for optimizing a subset of parameters.
    Used for local subproblems in SPQN.
    """

    def __init__(self, model, subset_params, loss_fn, maxiter=50, m=3):
        self.model = model
        self.all_params = list(model.parameters())
        self.subset_params = subset_params
        self.loss_fn = loss_fn
        self.maxiter = maxiter
        self.m = m

        self.subset_ids = {id(p) for p in subset_params}
        self.shapes = [p.shape for p in subset_params]
        self.sizes = [p.numel() for p in subset_params]
        self.n_params = sum(self.sizes)

    def _params_to_vec(self):
        return np.concatenate([p.data.cpu().numpy().ravel() for p in self.subset_params])

    def _vec_to_params(self, x):
        offset = 0
        for p, shape, size in zip(self.subset_params, self.shapes, self.sizes):
            p.data = torch.tensor(
                x[offset:offset + size].reshape(shape),
                dtype=p.dtype, device=p.device
            )
            offset += size

    def _objective(self, x):
        self._vec_to_params(x)

        # Zero grads for subset only
        for p in self.subset_params:
            if p.grad is not None:
                p.grad.zero_()

        # Need to enable grad only for subset
        for p in self.all_params:
            p.requires_grad_(id(p) in self.subset_ids)

        loss = self.loss_fn()
        loss.backward()

        # Restore all grads
        for p in self.all_params:
            p.requires_grad_(True)

        grad = np.concatenate([
            p.grad.cpu().numpy().ravel() for p in self.subset_params
        ])

        return loss.item(), grad.astype(np.float64)

    def optimize(self):
        x0 = self._params_to_vec().astype(np.float64)

        result = minimize(
            self._objective,
            x0,
            method='L-BFGS-B',
            jac=True,
            options={
                'maxiter': self.maxiter,
                'maxcor': self.m,
                'ftol': 1e-16 * np.finfo(float).eps,
                'gtol': 1e-16,
                'disp': False,
            },
        )

        self._vec_to_params(result.x)
        return result
