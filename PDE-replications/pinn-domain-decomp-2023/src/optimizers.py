"""
Optimizers for PINN training:
  - Standard L-BFGS (m=3, cubic backtracking, strong Wolfe)
  - Adam baseline
  - ASPQN (Additive Schwarz Preconditioned Quasi-Newton)
  - MSPQN (Multiplicative Schwarz Preconditioned Quasi-Newton)

Following Kopaničáková et al. (2023), arXiv:2306.17648
Key detail: L-BFGS uses memory m=3 (not the typical 20-100).
"""

import torch
import torch.nn as nn
import copy
import time
import numpy as np


def compute_loss(model, X_int, problem, bc_transform):
    """Compute PINN loss (PDE residual MSE with penalty-free BCs)."""
    residual = problem.pde_residual(model, X_int, bc_transform=bc_transform)
    loss = torch.mean(residual ** 2)
    return loss


def compute_relative_error(model, problem, bc_transform, n_test=10000, device='cpu',
                            ref_interp=None):
    """
    Compute relative L2 error.
    Paper formula: E_rel = ||u_NN - u*||_{L2} / ||u_NN||_{L2}
    """
    if problem.exact_solution_available():
        with torch.no_grad():
            X_test = problem.generate_collocation_points(n_int=n_test, device=device)
            u_raw = model(X_test)
            u_pred = bc_transform(u_raw, X_test)
            u_exact = problem.exact_solution(X_test)
            # Paper uses ||u_NN|| in denominator
            err = torch.norm(u_pred - u_exact) / (torch.norm(u_pred) + 1e-30)
        return err.item()
    elif ref_interp is not None:
        with torch.no_grad():
            X_test = problem.generate_collocation_points(n_int=n_test, device=device)
            u_raw = model(X_test)
            u_pred = bc_transform(u_raw, X_test)
            X_np = X_test.cpu().numpy()
            u_ref = torch.tensor(ref_interp(X_np), dtype=torch.float32,
                                 device=device).reshape(-1, 1)
            err = torch.norm(u_pred - u_ref) / (torch.norm(u_pred) + 1e-30)
        return err.item()
    return None


class LBFGSTrainer:
    """
    Standard L-BFGS training for PINN baseline.
    Uses m=3 history as specified in the paper.
    """

    def __init__(self, model, problem, bc_transform, X_int, device='cpu',
                 max_iter=20, history_size=3, lr=1.0,
                 line_search_fn='strong_wolfe', ref_interp=None):
        self.model = model
        self.problem = problem
        self.bc_transform = bc_transform
        self.X_int = X_int
        self.device = device
        self.ref_interp = ref_interp

        self.optimizer = torch.optim.LBFGS(
            model.parameters(),
            max_iter=max_iter,
            history_size=history_size,
            lr=lr,
            line_search_fn=line_search_fn,
            tolerance_grad=1e-16,
            tolerance_change=1e-16,
        )

        self.loss_history = []
        self.error_history = []
        self.time_history = []

    def train(self, n_epochs=1000, log_every=10, verbose=True):
        start_time = time.time()
        stagnation_count = 0
        prev_loss = float('inf')

        for epoch in range(n_epochs):
            loss_val = [0.0]

            def closure():
                self.optimizer.zero_grad()
                loss = compute_loss(self.model, self.X_int, self.problem, self.bc_transform)
                loss.backward()
                loss_val[0] = loss.item()
                return loss

            self.optimizer.step(closure)

            elapsed = time.time() - start_time
            self.loss_history.append(loss_val[0])
            self.time_history.append(elapsed)

            e_rel = compute_relative_error(self.model, self.problem, self.bc_transform,
                                           device=self.device, ref_interp=self.ref_interp)
            self.error_history.append(e_rel)

            # Check stagnation
            if abs(prev_loss - loss_val[0]) / (abs(prev_loss) + 1e-30) < 1e-10:
                stagnation_count += 1
            else:
                stagnation_count = 0
            prev_loss = loss_val[0]

            if verbose and (epoch % log_every == 0 or epoch == n_epochs - 1):
                err_str = f", E_rel={e_rel:.4e}" if e_rel is not None else ""
                print(f"  L-BFGS epoch {epoch:5d} | loss={loss_val[0]:.4e}{err_str} | time={elapsed:.1f}s")

            if loss_val[0] < 1e-14:
                if verbose:
                    print(f"  Converged at epoch {epoch}")
                break

            # If stagnated for 50 epochs, reinitialize L-BFGS state
            if stagnation_count >= 50:
                if verbose:
                    print(f"  L-BFGS stagnated, resetting optimizer state at epoch {epoch}")
                self.optimizer = torch.optim.LBFGS(
                    self.model.parameters(),
                    max_iter=20,
                    history_size=3,
                    lr=self.optimizer.defaults['lr'] * 0.5,
                    line_search_fn='strong_wolfe',
                    tolerance_grad=1e-16,
                    tolerance_change=1e-16,
                )
                stagnation_count = 0

        return self.loss_history, self.error_history, self.time_history


class SPQNTrainer:
    """
    Schwarz Preconditioned Quasi-Newton trainer.
    Implements ASPQN (additive) and MSPQN (multiplicative) variants.
    
    Algorithm per outer iteration:
    1. Preconditioning step: solve local subproblems (layer-wise decomposition)
    2. Global L-BFGS step from the preconditioned iterate
    
    Local and global L-BFGS both use m=3 history.
    """

    def __init__(self, model, problem, bc_transform, X_int, device='cpu',
                 mode='multiplicative',
                 n_subdomains=None,
                 k_s=50,
                 local_lr=1.0,
                 local_history=3,
                 global_lr=1.0,
                 global_history=3,
                 alpha=1.0,
                 ref_interp=None):
        self.model = model
        self.problem = problem
        self.bc_transform = bc_transform
        self.X_int = X_int
        self.device = device
        self.mode = mode
        self.k_s = k_s
        self.local_lr = local_lr
        self.local_history = local_history
        self.global_lr = global_lr
        self.global_history = global_history
        self.alpha = alpha
        self.ref_interp = ref_interp

        # Build layer groups
        layer_groups = model.get_layer_params()
        n_layers = len(layer_groups)

        if n_subdomains is None or n_subdomains >= n_layers:
            self.subdomains = layer_groups
        else:
            self.subdomains = []
            layers_per_sd = n_layers // n_subdomains
            remainder = n_layers % n_subdomains
            idx = 0
            for s in range(n_subdomains):
                n_this = layers_per_sd + (1 if s < remainder else 0)
                group = []
                for _ in range(n_this):
                    if idx < n_layers:
                        group.extend(layer_groups[idx])
                        idx += 1
                self.subdomains.append(group)

        self.n_sd = len(self.subdomains)

        # Global L-BFGS
        self.global_optimizer = torch.optim.LBFGS(
            model.parameters(),
            max_iter=20,
            history_size=global_history,
            lr=global_lr,
            line_search_fn='strong_wolfe',
            tolerance_grad=1e-16,
            tolerance_change=1e-16,
        )

        self.loss_history = []
        self.error_history = []
        self.time_history = []

    def _solve_local_subproblem(self, subdomain_params):
        """Solve local subproblem: minimize L w.r.t. subdomain_params only."""
        all_params = list(self.model.parameters())
        sd_param_ids = {id(p) for p in subdomain_params}

        # Freeze non-subdomain params
        for p in all_params:
            p.requires_grad_(id(p) in sd_param_ids)

        active_params = [p for p in subdomain_params if p.requires_grad]
        if not active_params:
            for p in all_params:
                p.requires_grad_(True)
            return

        local_opt = torch.optim.LBFGS(
            active_params,
            max_iter=self.k_s,
            history_size=self.local_history,
            lr=self.local_lr,
            line_search_fn='strong_wolfe',
            tolerance_grad=1e-16,
            tolerance_change=1e-16,
        )

        def closure():
            local_opt.zero_grad()
            loss = compute_loss(self.model, self.X_int, self.problem, self.bc_transform)
            loss.backward()
            return loss

        local_opt.step(closure)

        # Unfreeze all
        for p in all_params:
            p.requires_grad_(True)

    def _precondition_step(self):
        """Apply nonlinear preconditioning."""
        if self.mode == 'additive':
            saved_params = [p.data.clone() for p in self.model.parameters()]
            all_updates = []

            for sd_params in self.subdomains:
                # Reset to saved
                for p, sp in zip(self.model.parameters(), saved_params):
                    p.data.copy_(sp)

                self._solve_local_subproblem(sd_params)

                update = [(p.data - sp).clone()
                          for p, sp in zip(self.model.parameters(), saved_params)]
                all_updates.append(update)

            # Apply combined additive update
            for p, sp in zip(self.model.parameters(), saved_params):
                p.data.copy_(sp)

            for update in all_updates:
                for p, du in zip(self.model.parameters(), update):
                    p.data.add_(du, alpha=self.alpha)

        elif self.mode == 'multiplicative':
            for sd_params in self.subdomains:
                self._solve_local_subproblem(sd_params)

    def train(self, n_epochs=200, log_every=10, verbose=True):
        start_time = time.time()

        for epoch in range(n_epochs):
            # Preconditioning step
            self._precondition_step()

            # Global L-BFGS from preconditioned iterate
            loss_val = [0.0]

            def closure():
                self.global_optimizer.zero_grad()
                loss = compute_loss(self.model, self.X_int, self.problem, self.bc_transform)
                loss.backward()
                loss_val[0] = loss.item()
                return loss

            self.global_optimizer.step(closure)

            elapsed = time.time() - start_time
            self.loss_history.append(loss_val[0])
            self.time_history.append(elapsed)

            e_rel = compute_relative_error(self.model, self.problem, self.bc_transform,
                                           device=self.device, ref_interp=self.ref_interp)
            self.error_history.append(e_rel)

            if verbose and (epoch % log_every == 0 or epoch == n_epochs - 1):
                err_str = f", E_rel={e_rel:.4e}" if e_rel is not None else ""
                mname = "ASPQN" if self.mode == 'additive' else "MSPQN"
                print(f"  {mname} epoch {epoch:5d} | loss={loss_val[0]:.4e}{err_str} | time={elapsed:.1f}s")

            if loss_val[0] < 1e-14:
                if verbose:
                    print(f"  Converged at epoch {epoch}")
                break

        return self.loss_history, self.error_history, self.time_history


class AdamTrainer:
    """Adam optimizer baseline."""

    def __init__(self, model, problem, bc_transform, X_int, device='cpu',
                 lr=1e-3, ref_interp=None):
        self.model = model
        self.problem = problem
        self.bc_transform = bc_transform
        self.X_int = X_int
        self.device = device
        self.ref_interp = ref_interp

        self.optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        self.scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            self.optimizer, patience=500, factor=0.5, min_lr=1e-6)

        self.loss_history = []
        self.error_history = []
        self.time_history = []

    def train(self, n_epochs=50000, log_every=1000, verbose=True):
        start_time = time.time()

        for epoch in range(n_epochs):
            self.optimizer.zero_grad()
            loss = compute_loss(self.model, self.X_int, self.problem, self.bc_transform)
            loss.backward()
            self.optimizer.step()
            self.scheduler.step(loss.item())

            elapsed = time.time() - start_time
            self.loss_history.append(loss.item())
            self.time_history.append(elapsed)

            e_rel = compute_relative_error(self.model, self.problem, self.bc_transform,
                                           device=self.device, ref_interp=self.ref_interp)
            self.error_history.append(e_rel)

            if verbose and (epoch % log_every == 0 or epoch == n_epochs - 1):
                err_str = f", E_rel={e_rel:.4e}" if e_rel is not None else ""
                print(f"  Adam epoch {epoch:5d} | loss={loss.item():.4e}{err_str} | time={elapsed:.1f}s")

            if loss.item() < 1e-14:
                if verbose:
                    print(f"  Converged at epoch {epoch}")
                break

        return self.loss_history, self.error_history, self.time_history
