"""
PINN for solving RANS equations.
Replicates: Eivazi et al. (2022), Physics of Fluids 34, 075117

Architecture:
- FNN with 8 hidden layers, 20 neurons each, tanh activation
- Inputs: (x, y) spatial coordinates
- Outputs: U, V, P (+ Reynolds stresses for turbulent cases: uu, uv, vv)
- Loss: PDE residual (RANS eqs) + boundary data

Training: Adam optimizer -> L-BFGS

Author: Ollie (replication)
"""

import torch
import torch.nn as nn
import numpy as np
import time
import os
import json
from collections import OrderedDict


class PINN(nn.Module):
    """Physics-Informed Neural Network for RANS equations."""
    
    def __init__(self, n_inputs=2, n_outputs=3, n_hidden=8, n_neurons=20,
                 activation='tanh', lb=None, ub=None):
        """
        Args:
            n_inputs: number of input features (2 for x,y)
            n_outputs: number of outputs (3=U,V,P; 6=U,V,P,uu,uv,vv)
            n_hidden: number of hidden layers
            n_neurons: neurons per hidden layer
            activation: activation function
            lb: lower bounds for input normalization
            ub: upper bounds for input normalization
        """
        super().__init__()
        
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        
        # Input normalization bounds
        if lb is not None:
            self.register_buffer('lb', torch.tensor(lb, dtype=torch.float32))
            self.register_buffer('ub', torch.tensor(ub, dtype=torch.float32))
        else:
            self.lb = None
            self.ub = None
        
        # Build network
        layers = []
        layers.append(('input', nn.Linear(n_inputs, n_neurons)))
        layers.append(('input_act', nn.Tanh()))
        
        for i in range(n_hidden - 1):
            layers.append((f'hidden_{i}', nn.Linear(n_neurons, n_neurons)))
            layers.append((f'hidden_act_{i}', nn.Tanh()))
        
        layers.append(('output', nn.Linear(n_neurons, n_outputs)))
        
        self.net = nn.Sequential(OrderedDict(layers))
        
        # Xavier initialization
        self._initialize_weights()
    
    def _initialize_weights(self):
        for m in self.net.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight)
                nn.init.zeros_(m.bias)
    
    def forward(self, x):
        """Forward pass with input normalization."""
        if self.lb is not None:
            # Normalize to [-1, 1]
            x = 2.0 * (x - self.lb) / (self.ub - self.lb) - 1.0
        return self.net(x)


class RANSSolver:
    """
    RANS equation solver using PINNs.
    
    Supports multiple flow configurations:
    - 'laminar': Navier-Stokes (no Reynolds stresses), outputs U, V, P
    - 'rans_uv': RANS with only shear stress uv, outputs U, V, uv
    - 'rans_full': Full RANS with all stresses, outputs U, V, P, uu, uv, vv
    """
    
    def __init__(self, config):
        """
        Args:
            config: dict with keys:
                mode: 'laminar', 'rans_uv', 'rans_full'
                Re: Reynolds number
                n_hidden: number of hidden layers (default 8)
                n_neurons: neurons per layer (default 20)
                adam_lr: Adam learning rate (default 1e-3)
                adam_epochs: Adam training epochs (default 10000)
                lbfgs_epochs: L-BFGS iterations (default 5000)
                device: 'cuda' or 'cpu'
        """
        self.config = config
        self.mode = config.get('mode', 'laminar')
        self.Re = config['Re']
        self.nu = 1.0 / self.Re  # kinematic viscosity (non-dim)
        self.device = torch.device(config.get('device', 'cuda' if torch.cuda.is_available() else 'cpu'))
        
        # Determine number of outputs based on mode
        if self.mode == 'laminar':
            self.n_outputs = 3  # U, V, P
        elif self.mode == 'rans_uv':
            self.n_outputs = 3  # U, V, uv (no P, no normal stresses)
        elif self.mode == 'rans_full':
            self.n_outputs = 6  # U, V, P, uu, uv, vv
        else:
            raise ValueError(f"Unknown mode: {self.mode}")
        
        self.model = None
        self.loss_history = []
    
    def setup_model(self, lb, ub):
        """Initialize the PINN model."""
        self.model = PINN(
            n_inputs=2,
            n_outputs=self.n_outputs,
            n_hidden=self.config.get('n_hidden', 8),
            n_neurons=self.config.get('n_neurons', 20),
            lb=lb, ub=ub
        ).to(self.device)
        
        print(f"Model on {self.device}, params: {sum(p.numel() for p in self.model.parameters())}")
    
    def set_data(self, x_bc, y_bc, u_bc, x_pde, y_pde):
        """
        Set training data.
        
        Args:
            x_bc, y_bc: boundary point coordinates [N_bc]
            u_bc: boundary values [N_bc, n_outputs] — columns depend on mode
            x_pde, y_pde: collocation points for PDE residual [N_pde]
        """
        self.x_bc = torch.tensor(x_bc, dtype=torch.float32, device=self.device).reshape(-1, 1)
        self.y_bc = torch.tensor(y_bc, dtype=torch.float32, device=self.device).reshape(-1, 1)
        self.u_bc = torch.tensor(u_bc, dtype=torch.float32, device=self.device)
        if self.u_bc.dim() == 1:
            self.u_bc = self.u_bc.reshape(-1, 1)
        
        self.x_pde = torch.tensor(x_pde, dtype=torch.float32, device=self.device).reshape(-1, 1)
        self.y_pde = torch.tensor(y_pde, dtype=torch.float32, device=self.device).reshape(-1, 1)
        
        self.x_pde.requires_grad_(True)
        self.y_pde.requires_grad_(True)
        
        # Combine PDE points (include boundary points in PDE loss too)
        x_all = torch.cat([self.x_pde, self.x_bc], dim=0)
        y_all = torch.cat([self.y_pde, self.y_bc], dim=0)
        self.xy_pde = torch.cat([x_all, y_all], dim=1)
        self.xy_pde.requires_grad_(True)
        
        self.xy_bc = torch.cat([self.x_bc, self.y_bc], dim=1)
        
        self.n_bc = self.x_bc.shape[0]
        self.n_pde = self.xy_pde.shape[0]
        
        print(f"Data: {self.n_bc} boundary points, {self.n_pde} PDE collocation points")
    
    def compute_pde_residual(self, xy):
        """
        Compute RANS/NS PDE residuals using automatic differentiation.
        
        Returns tensor of residuals [N, n_eqs]
        """
        xy = xy.requires_grad_(True)
        out = self.model(xy)
        
        if self.mode == 'laminar':
            U, V, P = out[:, 0:1], out[:, 1:2], out[:, 2:3]
            
            # Gradients
            U_g = torch.autograd.grad(U, xy, torch.ones_like(U), create_graph=True)[0]
            V_g = torch.autograd.grad(V, xy, torch.ones_like(V), create_graph=True)[0]
            P_g = torch.autograd.grad(P, xy, torch.ones_like(P), create_graph=True)[0]
            
            U_x, U_y = U_g[:, 0:1], U_g[:, 1:2]
            V_x, V_y = V_g[:, 0:1], V_g[:, 1:2]
            P_x, P_y = P_g[:, 0:1], P_g[:, 1:2]
            
            # Second derivatives
            U_xx = torch.autograd.grad(U_x, xy, torch.ones_like(U_x), create_graph=True)[0][:, 0:1]
            U_yy = torch.autograd.grad(U_y, xy, torch.ones_like(U_y), create_graph=True)[0][:, 1:2]
            V_xx = torch.autograd.grad(V_x, xy, torch.ones_like(V_x), create_graph=True)[0][:, 0:1]
            V_yy = torch.autograd.grad(V_y, xy, torch.ones_like(V_y), create_graph=True)[0][:, 1:2]
            
            # NS residuals
            # Continuity: dU/dx + dV/dy = 0
            res_cont = U_x + V_y
            # x-momentum: U*dU/dx + V*dU/dy + (1/rho)*dP/dx - nu*(d2U/dx2 + d2U/dy2) = 0
            res_mom_x = U * U_x + V * U_y + P_x - self.nu * (U_xx + U_yy)
            # y-momentum: U*dV/dx + V*dV/dy + (1/rho)*dP/dy - nu*(d2V/dx2 + d2V/dy2) = 0
            res_mom_y = U * V_x + V * V_y + P_y - self.nu * (V_xx + V_yy)
            
            return torch.cat([res_cont, res_mom_x, res_mom_y], dim=1)
        
        elif self.mode == 'rans_uv':
            # Outputs: U, V, uv
            U, V, uv = out[:, 0:1], out[:, 1:2], out[:, 2:3]
            
            # Gradients
            U_g = torch.autograd.grad(U, xy, torch.ones_like(U), create_graph=True)[0]
            V_g = torch.autograd.grad(V, xy, torch.ones_like(V), create_graph=True)[0]
            uv_g = torch.autograd.grad(uv, xy, torch.ones_like(uv), create_graph=True)[0]
            
            U_x, U_y = U_g[:, 0:1], U_g[:, 1:2]
            V_x, V_y = V_g[:, 0:1], V_g[:, 1:2]
            uv_x, uv_y = uv_g[:, 0:1], uv_g[:, 1:2]
            
            # Second derivatives
            U_xx = torch.autograd.grad(U_x, xy, torch.ones_like(U_x), create_graph=True)[0][:, 0:1]
            U_yy = torch.autograd.grad(U_y, xy, torch.ones_like(U_y), create_graph=True)[0][:, 1:2]
            
            # Continuity: dU/dx + dV/dy = 0
            res_cont = U_x + V_y
            # x-momentum (RANS, simplified for BL without P, with uv only):
            # U*dU/dx + V*dU/dy - nu*(d2U/dx2 + d2U/dy2) + duv/dy = 0
            # Note: for ZPG BL the streamwise Reynolds stress gradient is often neglected
            res_mom_x = U * U_x + V * U_y - self.nu * (U_xx + U_yy) + uv_y
            
            return torch.cat([res_cont, res_mom_x], dim=1)
        
        elif self.mode == 'rans_full':
            # Outputs: U, V, P, uu, uv, vv
            U, V, P = out[:, 0:1], out[:, 1:2], out[:, 2:3]
            uu, uv, vv = out[:, 3:4], out[:, 4:5], out[:, 5:6]
            
            # Gradients
            U_g = torch.autograd.grad(U, xy, torch.ones_like(U), create_graph=True)[0]
            V_g = torch.autograd.grad(V, xy, torch.ones_like(V), create_graph=True)[0]
            P_g = torch.autograd.grad(P, xy, torch.ones_like(P), create_graph=True)[0]
            uu_g = torch.autograd.grad(uu, xy, torch.ones_like(uu), create_graph=True)[0]
            uv_g = torch.autograd.grad(uv, xy, torch.ones_like(uv), create_graph=True)[0]
            vv_g = torch.autograd.grad(vv, xy, torch.ones_like(vv), create_graph=True)[0]
            
            U_x, U_y = U_g[:, 0:1], U_g[:, 1:2]
            V_x, V_y = V_g[:, 0:1], V_g[:, 1:2]
            P_x, P_y = P_g[:, 0:1], P_g[:, 1:2]
            uu_x = uu_g[:, 0:1]
            uv_x, uv_y = uv_g[:, 0:1], uv_g[:, 1:2]
            vv_y = vv_g[:, 1:2]
            
            # Second derivatives
            U_xx = torch.autograd.grad(U_x, xy, torch.ones_like(U_x), create_graph=True)[0][:, 0:1]
            U_yy = torch.autograd.grad(U_y, xy, torch.ones_like(U_y), create_graph=True)[0][:, 1:2]
            V_xx = torch.autograd.grad(V_x, xy, torch.ones_like(V_x), create_graph=True)[0][:, 0:1]
            V_yy = torch.autograd.grad(V_y, xy, torch.ones_like(V_y), create_graph=True)[0][:, 1:2]
            
            # RANS residuals
            # Continuity: dU/dx + dV/dy = 0
            res_cont = U_x + V_y
            
            # x-momentum: U*dU/dx + V*dU/dy + (1/rho)*dP/dx - nu*(d2U/dx2 + d2U/dy2) + duu/dx + duv/dy = 0
            res_mom_x = U * U_x + V * U_y + P_x - self.nu * (U_xx + U_yy) + uu_x + uv_y
            
            # y-momentum: U*dV/dx + V*dV/dy + (1/rho)*dP/dy - nu*(d2V/dx2 + d2V/dy2) + duv/dx + dvv/dy = 0
            res_mom_y = U * V_x + V * V_y + P_y - self.nu * (V_xx + V_yy) + uv_x + vv_y
            
            return torch.cat([res_cont, res_mom_x, res_mom_y], dim=1)
    
    def compute_loss(self):
        """Compute total loss = PDE residual loss + boundary data loss."""
        # PDE residual loss
        residuals = self.compute_pde_residual(self.xy_pde)
        loss_pde = torch.mean(residuals**2)
        
        # Boundary data loss
        pred_bc = self.model(self.xy_bc)
        
        # Create mask for available data (non-NaN)
        mask = ~torch.isnan(self.u_bc)
        if mask.any():
            loss_bc = torch.mean((pred_bc[mask] - self.u_bc[mask])**2)
        else:
            loss_bc = torch.tensor(0.0, device=self.device)
        
        loss_total = loss_pde + loss_bc
        
        return loss_total, loss_pde.item(), loss_bc.item()
    
    def train_adam(self, n_epochs=None, lr=None, print_every=500):
        """Train with Adam optimizer."""
        n_epochs = n_epochs or self.config.get('adam_epochs', 10000)
        lr = lr or self.config.get('adam_lr', 1e-3)
        
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, patience=1000, factor=0.5, min_lr=1e-6
        )
        
        print(f"\n--- Adam Training ({n_epochs} epochs, lr={lr}) ---")
        t0 = time.time()
        
        for epoch in range(1, n_epochs + 1):
            optimizer.zero_grad()
            loss, loss_pde, loss_bc = self.compute_loss()
            loss.backward()
            optimizer.step()
            scheduler.step(loss)
            
            self.loss_history.append({
                'epoch': epoch, 'loss': loss.item(),
                'loss_pde': loss_pde, 'loss_bc': loss_bc,
                'phase': 'adam'
            })
            
            if epoch % print_every == 0 or epoch == 1:
                elapsed = time.time() - t0
                print(f"  Epoch {epoch:6d} | Loss: {loss.item():.6e} "
                      f"(PDE: {loss_pde:.6e}, BC: {loss_bc:.6e}) | "
                      f"Time: {elapsed:.1f}s")
        
        print(f"Adam done in {time.time()-t0:.1f}s, final loss: {loss.item():.6e}")
    
    def train_lbfgs(self, max_iter=None, print_every=100):
        """Train with L-BFGS optimizer."""
        max_iter = max_iter or self.config.get('lbfgs_epochs', 5000)
        
        optimizer = torch.optim.LBFGS(
            self.model.parameters(),
            lr=1.0,
            max_iter=20,
            max_eval=25,
            history_size=50,
            tolerance_grad=1e-9,
            tolerance_change=1e-11,
            line_search_fn='strong_wolfe'
        )
        
        print(f"\n--- L-BFGS Training (max {max_iter} iterations) ---")
        t0 = time.time()
        self._lbfgs_iter = 0
        self._lbfgs_loss = None
        
        def closure():
            optimizer.zero_grad()
            loss, loss_pde, loss_bc = self.compute_loss()
            loss.backward()
            self._lbfgs_iter += 1
            self._lbfgs_loss = (loss.item(), loss_pde, loss_bc)
            
            self.loss_history.append({
                'epoch': len(self.loss_history) + 1,
                'loss': loss.item(),
                'loss_pde': loss_pde, 'loss_bc': loss_bc,
                'phase': 'lbfgs'
            })
            
            if self._lbfgs_iter % print_every == 0:
                elapsed = time.time() - t0
                print(f"  Iter {self._lbfgs_iter:6d} | Loss: {loss.item():.6e} "
                      f"(PDE: {loss_pde:.6e}, BC: {loss_bc:.6e}) | "
                      f"Time: {elapsed:.1f}s")
            
            return loss
        
        for _ in range(max_iter):
            optimizer.step(closure)
            if self._lbfgs_iter >= max_iter:
                break
        
        final = self._lbfgs_loss
        print(f"L-BFGS done in {time.time()-t0:.1f}s, final loss: {final[0]:.6e}")
    
    def predict(self, x, y):
        """Predict at given (x, y) points."""
        self.model.eval()
        with torch.no_grad():
            xy = torch.tensor(np.column_stack([x.ravel(), y.ravel()]),
                            dtype=torch.float32, device=self.device)
            pred = self.model(xy).cpu().numpy()
        return pred
    
    def compute_errors(self, x, y, u_ref):
        """
        Compute relative L2 errors as defined in the paper:
        E_i = ||U_i - U_i_pred||_2 / ||U_i||_2 * 100
        """
        pred = self.predict(x, y)
        errors = {}
        
        if self.mode == 'laminar':
            names = ['U', 'V', 'P']
        elif self.mode == 'rans_uv':
            names = ['U', 'V', 'uv']
        elif self.mode == 'rans_full':
            names = ['U', 'V', 'P', 'uu', 'uv', 'vv']
        
        for i, name in enumerate(names):
            if i < u_ref.shape[1]:
                ref = u_ref[:, i]
                pre = pred[:, i]
                norm_ref = np.linalg.norm(ref)
                if norm_ref > 1e-10:
                    err = np.linalg.norm(ref - pre) / norm_ref * 100
                else:
                    err = np.linalg.norm(ref - pre) * 100
                errors[name] = err
        
        return errors
    
    def save(self, path):
        """Save model and training history."""
        torch.save({
            'model_state': self.model.state_dict(),
            'config': self.config,
            'loss_history': self.loss_history,
        }, path)
        print(f"Model saved to {path}")
    
    def load(self, path):
        """Load model."""
        ckpt = torch.load(path, map_location=self.device)
        self.model.load_state_dict(ckpt['model_state'])
        self.loss_history = ckpt.get('loss_history', [])
        print(f"Model loaded from {path}")


def relative_l2_error(ref, pred):
    """Compute relative L2 error: ||ref - pred||_2 / ||ref||_2 * 100"""
    norm = np.linalg.norm(ref)
    if norm < 1e-10:
        return np.linalg.norm(ref - pred) * 100
    return np.linalg.norm(ref - pred) / norm * 100
