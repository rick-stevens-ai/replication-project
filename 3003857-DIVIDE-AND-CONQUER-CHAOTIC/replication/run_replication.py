#!/usr/bin/env python3
"""
Combined replication: OSTI 3003857 - Divide and Conquer MP-NODE
Vectorized/batched implementation for GPU efficiency.
"""

import torch
import torch.nn as nn
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import solve_ivp
from scipy.fft import fft, ifft, fftfreq
import json, os, time, sys

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}", flush=True)

SIGMA, BETA, RHO = 10.0, 8.0/3.0, 28.0

def lorenz_rhs(t, state):
    x, y, z = state
    return [SIGMA*(y-x), x*(RHO-z)-y, x*y-BETA*z]

def generate_lorenz_data(q0, T, dt, transient=100.0):
    sol = solve_ivp(lorenz_rhs, [0, transient], q0, method='DOP853', rtol=1e-12, atol=1e-14)
    q0a = sol.y[:, -1]
    t_eval = np.arange(0, T, dt)
    sol = solve_ivp(lorenz_rhs, [0, T], q0a, method='DOP853', t_eval=t_eval, rtol=1e-12, atol=1e-14)
    return sol.t, sol.y.T

# ============================================================
# Batched RK4 for Lorenz (parametric, for gradient demo)
# ============================================================
def rk4_step_lorenz(state, dt, rho):
    def f(s):
        x, y, z = s[...,0], s[...,1], s[...,2]
        return torch.stack([SIGMA*(y-x), x*(rho-z)-y, x*y-BETA*z], dim=-1)
    k1=f(state); k2=f(state+.5*dt*k1); k3=f(state+.5*dt*k2); k4=f(state+dt*k3)
    return state + (dt/6)*(k1+2*k2+2*k3+k4)

# ============================================================
# Batched Neural ODE Integration
# ============================================================
class LorenzNeuralODE(nn.Module):
    def __init__(self, hidden=64, layers=3):
        super().__init__()
        mods = [nn.Linear(3, hidden), nn.Tanh()]
        for _ in range(layers-1):
            mods += [nn.Linear(hidden, hidden), nn.Tanh()]
        mods.append(nn.Linear(hidden, 3))
        self.net = nn.Sequential(*mods)
        for m in self.net:
            if isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight, gain=0.1)
                nn.init.zeros_(m.bias)
    def forward(self, t, q):
        return self.net(q)

class KSNeuralODE(nn.Module):
    def __init__(self, N=64, hidden=32, layers=4):
        super().__init__()
        mods = [nn.Conv1d(1, hidden, 5, padding=2, padding_mode='circular'), nn.GELU()]
        for _ in range(layers-2):
            mods += [nn.Conv1d(hidden, hidden, 5, padding=2, padding_mode='circular'), nn.GELU()]
        mods.append(nn.Conv1d(hidden, 1, 5, padding=2, padding_mode='circular'))
        self.net = nn.Sequential(*mods)
        for m in self.net:
            if isinstance(m, nn.Conv1d):
                nn.init.xavier_normal_(m.weight, gain=0.1)
                if m.bias is not None: nn.init.zeros_(m.bias)
    def forward(self, t, q):
        # q: (batch, N) -> (batch, 1, N)
        if q.dim() == 1: q = q.unsqueeze(0)
        q3d = q.unsqueeze(1)
        return self.net(q3d).squeeze(1)  # (batch, N)

def rk4_integrate_batch(func, q0, n_steps, dt):
    """Batched RK4: q0 shape (B, D), returns (n_steps+1, B, D)"""
    traj = [q0]
    q = q0
    t = 0.0
    for _ in range(n_steps):
        k1 = func(t, q)
        k2 = func(t+.5*dt, q+.5*dt*k1)
        k3 = func(t+.5*dt, q+.5*dt*k2)
        k4 = func(t+dt, q+dt*k3)
        q = q + (dt/6)*(k1+2*k2+2*k3+k4)
        t += dt
        traj.append(q)
    return torch.stack(traj, dim=0)  # (T+1, B, D)

def rk4_integrate_single(func, q0, n_steps, dt):
    """Single trajectory: q0 shape (D,), returns (T+1, D)"""
    traj = [q0]
    q = q0
    t = 0.0
    for _ in range(n_steps):
        k1 = func(t, q.unsqueeze(0)).squeeze(0)
        k2 = func(t+.5*dt, (q+.5*dt*k1).unsqueeze(0)).squeeze(0)
        k3 = func(t+.5*dt, (q+.5*dt*k2).unsqueeze(0)).squeeze(0)
        k4 = func(t+dt, (q+dt*k3).unsqueeze(0)).squeeze(0)
        q = q + (dt/6)*(k1+2*k2+2*k3+k4)
        t += dt
        traj.append(q)
    return torch.stack(traj, dim=0)

# ============================================================
# EXPERIMENT 1: Gradient Explosion Demo
# ============================================================
def experiment_gradient_explosion():
    print("\n" + "="*60, flush=True)
    print("EXPERIMENT 1: Gradient Explosion Demo (Section 4.1.1)", flush=True)
    print("="*60, flush=True)
    
    q0 = torch.tensor([1.0, 1.0, 1.0], dtype=torch.float64, device=device)
    T, n_steps = 10.0, 500
    dt = T/n_steps
    n_opt, lr = 300, 0.05
    
    # Vanilla
    print("Vanilla optimization...", flush=True)
    rho_v = 28.0
    van_grads, van_objs = [], []
    for i in range(n_opt):
        rho = torch.tensor(rho_v, dtype=torch.float64, requires_grad=True, device=device)
        state = q0.clone()
        J = torch.tensor(0.0, dtype=torch.float64, device=device)
        for _ in range(n_steps):
            state = rk4_step_lorenz(state, dt, rho)
            J = J + torch.abs(state[2])*dt
        J = J/T
        try:
            J.backward(); g = rho.grad.item()
        except: g = 1e10
        van_grads.append(abs(g)); van_objs.append(J.item())
        rho_v -= lr * np.clip(g, -1, 1); rho_v = max(1.0, rho_v)
        if (i+1)%100==0: print(f"  Step {i+1}: |grad|={abs(g):.2e}, J={J.item():.4f}, rho={rho_v:.2f}", flush=True)
    
    # MP
    print("MP optimization...", flush=True)
    rho_m = 28.0
    n_win, spw = 10, n_steps//10
    mp_grads, mp_objs = [], []
    mu_vals = [1e-5]*60+[1e-4]*60+[1e-3]*60+[1e-2]*60+[1e-1]*60
    for i in range(n_opt):
        mu = mu_vals[min(i, len(mu_vals)-1)]
        rho = torch.tensor(rho_m, dtype=torch.float64, requires_grad=True, device=device)
        with torch.no_grad():
            ref = q0.clone()
            refs = [ref.clone()]
            for s in range(n_steps):
                ref = rk4_step_lorenz(ref, dt, rho_m)
                refs.append(ref.clone())
        J = torch.tensor(0., dtype=torch.float64, device=device)
        P = torch.tensor(0., dtype=torch.float64, device=device)
        for w in range(n_win):
            state = q0.clone() if w==0 else refs[w*spw].clone()
            for s in range(spw):
                state = rk4_step_lorenz(state, dt, rho)
                J = J + torch.abs(state[2])*dt
            if w < n_win-1:
                P = P + torch.sum((refs[(w+1)*spw]-state)**2)
        J=J/T; P=P/(n_win-1); loss=J+(mu/2)*P
        try:
            loss.backward(); g=rho.grad.item()
        except: g=0.0
        mp_grads.append(abs(g)); mp_objs.append(J.item())
        rho_m -= lr*np.clip(g,-1,1); rho_m = max(1.0, rho_m)
        if (i+1)%100==0: print(f"  Step {i+1}: |grad|={abs(g):.2e}, J={J.item():.4f}, rho={rho_m:.2f}, mu={mu:.1e}", flush=True)
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].semilogy(van_grads, alpha=.7, label='Vanilla'); axes[0].semilogy(mp_grads, alpha=.7, label='MP')
    for k in [60,120,180,240]: axes[0].axvline(x=k, color='gray', ls='--', alpha=.3)
    axes[0].set_xlabel('Steps'); axes[0].set_ylabel('|dJ/dρ|'); axes[0].set_title('(a) Gradient Magnitude'); axes[0].legend(); axes[0].grid(True, alpha=.3)
    axes[1].plot(van_objs, alpha=.7, label='Vanilla'); axes[1].plot(mp_objs, alpha=.7, label='MP')
    axes[1].set_xlabel('Steps'); axes[1].set_ylabel('J'); axes[1].set_title('(b) Objective'); axes[1].legend(); axes[1].grid(True, alpha=.3)
    plt.tight_layout(); plt.savefig('fig1_gradient_explosion.png', dpi=150, bbox_inches='tight'); plt.close()
    print("Saved fig1_gradient_explosion.png", flush=True)
    return {'van_max_grad': float(max(van_grads)), 'mp_max_grad': float(max(mp_grads)),
            'van_final_obj': float(van_objs[-1]), 'mp_final_obj': float(mp_objs[-1])}

# ============================================================
# EXPERIMENT 2: Loss Landscape
# ============================================================
def experiment_loss_landscape():
    print("\n" + "="*60, flush=True)
    print("EXPERIMENT 2: Loss Landscape (Section 4.1.2)", flush=True)
    print("="*60, flush=True)
    T, ns = 10.0, 500; dt = T/ns; ng = 30
    q0 = np.array([1.,1.,1.]); fb = np.zeros(ns); i1,i2 = 100,300; vals = np.linspace(-3,3,ng)
    
    def rk4_np(q0, fv, ns, dt):
        s=q0.copy()
        traj=[s.copy()]
        for i in range(ns):
            fi=fv[i]
            def d(s): return np.array([SIGMA*(s[1]-s[0]), s[0]*(RHO-s[2])-s[1], s[0]*s[1]-BETA*s[2]+fi])
            k1=d(s);k2=d(s+.5*dt*k1);k3=d(s+.5*dt*k2);k4=d(s+dt*k3)
            s=s+(dt/6)*(k1+2*k2+2*k3+k4); traj.append(s.copy())
        return np.array(traj)
    
    def obj_v(fv):
        t=rk4_np(q0,fv,ns,dt); J=0
        for i in range(1,len(t)):
            v=2*t[i,0]+t[i,1]
            if v>=0: J+=.5*v**2*dt
        return J/T
    
    def obj_mp(fv, nw=5, mu=.1):
        tr=rk4_np(q0,fv,ns,dt); spw=ns//nw; J=P=0
        for w in range(nw):
            si=w*spw; s=tr[si].copy()
            for ss in range(spw):
                fi=fv[si+ss]
                def d(st): return np.array([SIGMA*(st[1]-st[0]), st[0]*(RHO-st[2])-st[1], st[0]*st[1]-BETA*st[2]+fi])
                k1=d(s);k2=d(s+.5*dt*k1);k3=d(s+.5*dt*k2);k4=d(s+dt*k3)
                s=s+(dt/6)*(k1+2*k2+2*k3+k4)
                v=2*s[0]+s[1]
                if v>=0: J+=.5*v**2*dt
            if w<nw-1: P+=np.sum((tr[(w+1)*spw]-s)**2)
        return J/T+(mu/2)*P/(nw-1)
    
    print(f"Computing {ng}x{ng} landscape...", flush=True)
    Lv=np.zeros((ng,ng)); Lm=np.zeros((ng,ng))
    for i,v1 in enumerate(vals):
        for j,v2 in enumerate(vals):
            f=fb.copy(); f[i1]=v1; f[i2]=v2
            Lv[i,j]=obj_v(f); Lm[i,j]=obj_mp(f)
        if (i+1)%10==0: print(f"  Row {i+1}/{ng}", flush=True)
    
    fig, axes = plt.subplots(1,2,figsize=(14,5)); X,Y=np.meshgrid(vals,vals)
    for ax,L,t in [(axes[0],Lv,'Vanilla Loss'),(axes[1],Lm,'MP Loss')]:
        Lc=np.clip(L,np.percentile(L,2),np.percentile(L,98))
        c=ax.contourf(X,Y,Lc.T,levels=25,cmap='viridis'); plt.colorbar(c,ax=ax)
        ax.set_title(t); ax.set_xlabel(f'f[{i1}]'); ax.set_ylabel(f'f[{i2}]')
    plt.tight_layout(); plt.savefig('fig2_loss_landscape.png', dpi=150, bbox_inches='tight'); plt.close()
    print("Saved fig2_loss_landscape.png", flush=True)
    return {'van_std':float(Lv.std()),'mp_std':float(Lm.std())}

# ============================================================
# EXPERIMENT 3: Lorenz NODE (Batched)
# ============================================================
def experiment_lorenz_node():
    print("\n" + "="*60, flush=True)
    print("EXPERIMENT 3: Lorenz-63 NODE Training (Batched)", flush=True)
    print("="*60, flush=True)
    
    dt = 0.02  # Larger dt for speed (paper doesn't specify exactly)
    print("Generating data...", flush=True)
    t_tr, d_tr = generate_lorenz_data([1.,1.,1.], 200., dt, transient=100.)
    t_te, d_te = generate_lorenz_data(d_tr[-1].tolist(), 50., dt, transient=50.)
    print(f"Train: {d_tr.shape}, Test: {d_te.shape}", flush=True)
    
    rollout = 50  # 50*0.02 = 1.0 time unit ~ 1 Lyapunov time
    n_epochs, bs = 2000, 32
    n_win = 5; spw = rollout//n_win  # 10 steps per window
    train_t = torch.tensor(d_tr, dtype=torch.float32, device=device)
    n_data = len(d_tr) - rollout
    
    def make_batch(bs):
        idx = np.random.randint(0, n_data, size=bs)
        q0s = torch.stack([train_t[i] for i in idx])  # (B, 3)
        targets = torch.stack([train_t[i:i+rollout+1] for i in idx])  # (B, T+1, 3)
        return q0s, targets
    
    # --- Vanilla ---
    print("\nTraining Vanilla NODE...", flush=True)
    van = LorenzNeuralODE().to(device)
    opt = torch.optim.Adam(van.parameters(), lr=1e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, n_epochs, eta_min=1e-5)
    van_losses = []
    t0 = time.time()
    for ep in range(n_epochs):
        q0s, targets = make_batch(bs)
        pred = rk4_integrate_batch(van, q0s, rollout, dt)  # (T+1, B, 3)
        pred = pred.permute(1, 0, 2)  # (B, T+1, 3)
        loss = torch.mean((pred - targets)**2)
        opt.zero_grad(); loss.backward()
        torch.nn.utils.clip_grad_norm_(van.parameters(), 1.0)
        opt.step(); sched.step()
        van_losses.append(loss.item())
        if (ep+1)%500==0: print(f"  Vanilla ep {ep+1}: loss={loss.item():.6f}", flush=True)
    van_time = time.time()-t0
    
    # --- MP-NODE ---
    print("\nTraining MP-NODE...", flush=True)
    mp = LorenzNeuralODE().to(device)
    opt = torch.optim.Adam(mp.parameters(), lr=1e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, n_epochs, eta_min=1e-5)
    mu_sched = {0:1e-6, 400:1e-4, 800:1e-2, 1200:1e0, 1600:1e2}
    mu = 1e-6
    mp_losses, mp_lgts, mp_lps = [], [], []
    t0 = time.time()
    for ep in range(n_epochs):
        if ep in mu_sched:
            mu = mu_sched[ep]
            print(f"  mu -> {mu:.1e} at ep {ep}", flush=True)
        q0s, targets = make_batch(bs)
        # targets: (B, T+1, 3)
        
        total_lgt = torch.tensor(0., device=device)
        total_lp = torch.tensor(0., device=device)
        
        # Window-based integration
        pred_parts = []
        for w in range(n_win):
            w_start = w * spw
            if w == 0:
                q_start = q0s  # (B, 3)
            else:
                # Use ground truth as IC for this window (re-initialized per Algorithm 1)
                q_start = targets[:, w_start, :]  # (B, 3) from GT
            
            pw = rk4_integrate_batch(mp, q_start, spw, dt)  # (spw+1, B, 3)
            pw = pw.permute(1, 0, 2)  # (B, spw+1, 3)
            pred_parts.append(pw)
            
            if w < n_win - 1:
                q_end = pw[:, -1, :]  # (B, 3)
                q_next = targets[:, (w+1)*spw, :]  # (B, 3)
                total_lp = total_lp + torch.mean((q_next - q_end)**2)
        
        # Assemble full prediction
        pred_full = torch.cat([p[:, :-1, :] for p in pred_parts[:-1]] + [pred_parts[-1]], dim=1)
        ml = min(pred_full.shape[1], targets.shape[1])
        total_lgt = torch.mean((pred_full[:, :ml, :] - targets[:, :ml, :])**2)
        total_lp = total_lp / max(n_win-1, 1)
        
        loss = total_lgt + (mu/2)*total_lp
        opt.zero_grad(); loss.backward()
        torch.nn.utils.clip_grad_norm_(mp.parameters(), 1.0)
        opt.step(); sched.step()
        
        mp_losses.append(loss.item()); mp_lgts.append(total_lgt.item()); mp_lps.append(total_lp.item())
        if (ep+1)%500==0: print(f"  MP ep {ep+1}: loss={loss.item():.6f}, LGT={total_lgt.item():.6f}, LP={total_lp.item():.6f}", flush=True)
    mp_time = time.time()-t0
    print(f"Times: Vanilla={van_time:.1f}s, MP={mp_time:.1f}s", flush=True)
    
    # --- Evaluate ---
    q0e = torch.tensor(d_te[0], dtype=torch.float32, device=device)
    T_short = 5.0; n_short = int(T_short/dt)
    
    with torch.no_grad():
        van_pred = rk4_integrate_single(van, q0e, n_short, dt).cpu().numpy()
        mp_pred = rk4_integrate_single(mp, q0e, n_short, dt).cpu().numpy()
    
    ml = min(len(van_pred), len(mp_pred), len(d_te))
    van_mse = np.mean((van_pred[:ml]-d_te[:ml])**2, axis=1)
    mp_mse = np.mean((mp_pred[:ml]-d_te[:ml])**2, axis=1)
    
    # Lyapunov
    print("Estimating Lyapunov exponents...", flush=True)
    def est_le(func, q0, dt, T=200., d0=1e-8, rnorm=50):
        pert = np.random.randn(3); pert = pert/np.linalg.norm(pert)*d0
        q1 = torch.tensor(q0, dtype=torch.float32, device=device)
        q2 = torch.tensor(q0+pert, dtype=torch.float32, device=device)
        ls, nr = 0., 0
        ns = int(T/dt)
        with torch.no_grad():
            for st in range(0, ns, rnorm):
                n = min(rnorm, ns-st)
                t1 = rk4_integrate_single(func, q1, n, dt)
                t2 = rk4_integrate_single(func, q2, n, dt)
                q1, q2 = t1[-1], t2[-1]
                d = torch.norm(q2-q1).item()
                if 0<d<1e10:
                    ls += np.log(d/d0); nr += 1
                    q2 = q1 + (q2-q1)/d*d0
        return ls/(nr*rnorm*dt) if nr>0 else float('nan')
    
    class TrueL:
        def __call__(self, t, q):
            if q.dim()==1: q=q.unsqueeze(0)
            x,y,z = q[...,0],q[...,1],q[...,2]
            r = torch.stack([SIGMA*(y-x),x*(RHO-z)-y,x*y-BETA*z],dim=-1)
            return r.squeeze(0) if r.shape[0]==1 else r
    
    true_le = est_le(TrueL(), d_te[0], dt, T=300.)
    van_le = est_le(van, d_te[0], dt, T=200.)
    mp_le = est_le(mp, d_te[0], dt, T=200.)
    print(f"  True LE: {true_le:.4f} (ref ~0.906)", flush=True)
    print(f"  Vanilla: {van_le:.4f}", flush=True)
    print(f"  MP-NODE: {mp_le:.4f}", flush=True)
    
    # Long-term stats
    print("Computing attractor statistics...", flush=True)
    _, true_long = generate_lorenz_data([1.,1.,1.], 500., dt, transient=200.)
    
    def gen_long(model, q0, T, dt):
        chunks = []
        q = torch.tensor(q0, dtype=torch.float32, device=device)
        with torch.no_grad():
            for s in range(0, int(T/dt), 5000):
                n = min(5000, int(T/dt)-s)
                t = rk4_integrate_single(model, q, n, dt)
                chunks.append(t[:-1].cpu().numpy())
                q = t[-1]
                if not torch.isfinite(q).all(): break
        return np.concatenate(chunks, axis=0) if chunks else np.zeros((1,3))
    
    van_long = gen_long(van, d_te[0], 500., dt)
    mp_long = gen_long(mp, d_te[0], 500., dt)
    
    skip = min(2500, len(true_long)//4)
    true_s = true_long[skip:]
    van_s = van_long[skip:] if len(van_long)>skip and np.isfinite(van_long).all() else van_long
    mp_s = mp_long[skip:] if len(mp_long)>skip and np.isfinite(mp_long).all() else mp_long
    
    stats = {}
    for name, arr in [('true',true_s),('vanilla',van_s),('mp_node',mp_s)]:
        if len(arr)>100 and np.isfinite(arr).all():
            stats[name] = {'mean':arr.mean(0).tolist(),'std':arr.std(0).tolist()}
        else:
            stats[name] = {'mean':[float('nan')]*3,'std':[float('nan')]*3}
    
    for k in stats:
        m = stats[k]['mean']
        print(f"  {k:10s} mean: [{m[0]:.2f}, {m[1]:.2f}, {m[2]:.2f}]", flush=True)
    
    # --- Plots ---
    fig, axes = plt.subplots(1,2,figsize=(14,5))
    axes[0].semilogy(van_losses, alpha=.5, label='Vanilla'); axes[0].semilogy(mp_losses, alpha=.5, label='MP-NODE')
    axes[0].set_xlabel('Epoch'); axes[0].set_ylabel('Loss'); axes[0].set_title('Training Loss'); axes[0].legend(); axes[0].grid(True,alpha=.3)
    axes[1].semilogy(mp_lgts, alpha=.5, label='$L_{GT}$'); axes[1].semilogy(mp_lps, alpha=.5, label='$L_P$')
    axes[1].set_xlabel('Epoch'); axes[1].set_ylabel('Loss'); axes[1].set_title('MP-NODE Components'); axes[1].legend(); axes[1].grid(True,alpha=.3)
    plt.tight_layout(); plt.savefig('fig3_lorenz_training.png',dpi=150,bbox_inches='tight'); plt.close()
    
    tp = np.arange(ml)*dt
    fig, axes = plt.subplots(3,1,figsize=(14,10),sharex=True)
    for d,l in enumerate(['x','y','z']):
        ax=axes[d]; ax.plot(tp,d_te[:ml,d],'k-',lw=1.5,label='True')
        ax.plot(tp,van_pred[:ml,d],'b--',alpha=.7,label='Vanilla'); ax.plot(tp,mp_pred[:ml,d],'r--',alpha=.7,label='MP-NODE')
        ax.set_ylabel(l); ax.legend(loc='upper right'); ax.grid(True,alpha=.3)
    axes[2].set_xlabel('Time'); axes[0].set_title('Lorenz-63 Trajectory Prediction')
    plt.tight_layout(); plt.savefig('fig4_lorenz_trajectory.png',dpi=150,bbox_inches='tight'); plt.close()
    
    fig, ax = plt.subplots(figsize=(10,5))
    ax.semilogy(tp, van_mse, label='Vanilla', alpha=.7); ax.semilogy(tp, mp_mse, label='MP-NODE', alpha=.7)
    ax.axvline(x=1/0.906, color='gray', ls='--', alpha=.5, label='1 Lyapunov time')
    ax.set_xlabel('Time'); ax.set_ylabel('MSE'); ax.set_title('Prediction Error'); ax.legend(); ax.grid(True,alpha=.3)
    plt.tight_layout(); plt.savefig('fig5_lorenz_mse.png',dpi=150,bbox_inches='tight'); plt.close()
    
    fig=plt.figure(figsize=(18,6))
    for i,(arr,t,c) in enumerate([(true_s,'True','k'),(van_s,'Vanilla','b'),(mp_s,'MP-NODE','r')]):
        ax=fig.add_subplot(1,3,i+1,projection='3d')
        if len(arr)>100 and np.isfinite(arr).all():
            ax.plot(arr[::10,0],arr[::10,1],arr[::10,2],c+'-',alpha=.3,lw=.3)
        ax.set_title(t); ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
    plt.tight_layout(); plt.savefig('fig6_lorenz_attractor.png',dpi=150,bbox_inches='tight'); plt.close()
    
    fig,axes=plt.subplots(1,3,figsize=(15,5))
    for d,l in enumerate(['x','y','z']):
        ax=axes[d]; ax.hist(true_s[:,d],bins=80,density=True,alpha=.5,color='k',label='True')
        if np.isfinite(van_s).all(): ax.hist(van_s[:,d],bins=80,density=True,alpha=.4,color='b',label='Vanilla')
        if np.isfinite(mp_s).all(): ax.hist(mp_s[:,d],bins=80,density=True,alpha=.4,color='r',label='MP-NODE')
        ax.set_xlabel(l); ax.legend(); ax.set_title(f'Dist of {l}')
    plt.tight_layout(); plt.savefig('fig7_lorenz_distributions.png',dpi=150,bbox_inches='tight'); plt.close()
    
    print("All Lorenz plots saved.", flush=True)
    return {
        'training': {'van_loss':float(van_losses[-1]),'mp_loss':float(mp_losses[-1]),'van_time':van_time,'mp_time':mp_time},
        'lyapunov': {'true':float(true_le),'vanilla':float(van_le),'mp_node':float(mp_le)},
        'stats': stats,
        'mse_1LT': {'van':float(np.mean(van_mse[:min(55,ml)])),'mp':float(np.mean(mp_mse[:min(55,ml)]))},
    }

# ============================================================
# EXPERIMENT 4: KS Equation
# ============================================================
class KSSolver:
    def __init__(self, L=22., N=64, dt=0.05):
        self.L,self.N,self.dt = L,N,dt
        self.k = 2*np.pi*fftfreq(N, d=L/N)
        self.L_op = -self.k**2 - self.k**4
    def integrate(self, q0, T, save_dt=0.25):
        se = max(1, int(save_dt/self.dt)); ns = int(T/self.dt)
        qh = fft(q0); E=np.exp(self.L_op*self.dt); E2=np.exp(self.L_op*self.dt/2)
        M=32; r=np.exp(1j*np.pi*(np.arange(1,M+1)-.5)/M)
        LR=self.dt*self.L_op[:,None]+r[None,:]
        Q=self.dt*np.real(np.mean((np.exp(LR/2)-1)/LR,1))
        f1=self.dt*np.real(np.mean((-4-LR+np.exp(LR)*(4-3*LR+LR**2))/LR**3,1))
        f2=self.dt*np.real(np.mean((2+LR+np.exp(LR)*(-2+LR))/LR**3,1))
        f3=self.dt*np.real(np.mean((-4-3*LR-LR**2+np.exp(LR)*(4-LR))/LR**3,1))
        traj=[np.real(ifft(qh)).copy()]
        for step in range(ns):
            Nv=-0.5*1j*self.k*fft(np.real(ifft(qh))**2)
            a=E2*qh+Q*Nv; Na=-0.5*1j*self.k*fft(np.real(ifft(a))**2)
            b=E2*qh+Q*Na; Nb=-0.5*1j*self.k*fft(np.real(ifft(b))**2)
            c=E2*a+Q*(2*Nb-Nv); Nc=-0.5*1j*self.k*fft(np.real(ifft(c))**2)
            qh=E*qh+Nv*f1+2*(Na+Nb)*f2+Nc*f3
            if (step+1)%se==0: traj.append(np.real(ifft(qh)).copy())
        return np.array(traj)

def experiment_ks():
    print("\n" + "="*60, flush=True)
    print("EXPERIMENT 4: Kuramoto-Sivashinsky", flush=True)
    print("="*60, flush=True)
    
    L,N = 22.,64; dt_save=0.25
    solver = KSSolver(L=L, N=N, dt=0.05)
    
    np.random.seed(42); q0=np.random.randn(N)*0.1
    print("KS transient...", flush=True)
    trans = solver.integrate(q0, T=500., save_dt=dt_save)
    
    print("KS training data (T=5000)...", flush=True)
    tr = solver.integrate(trans[-1], T=5000., save_dt=dt_save)
    tr = tr[:5000]
    print(f"Train: {tr.shape}", flush=True)
    
    print("KS test data...", flush=True)
    te = solver.integrate(tr[-1], T=2000., save_dt=dt_save)
    
    dmean,dstd = tr.mean(), tr.std()
    trn = (tr-dmean)/dstd; ten = (te-dmean)/dstd
    
    train_t = torch.tensor(trn, dtype=torch.float32, device=device)
    n_data_ks = len(trn)
    
    def make_ks_batch(bs, rollout):
        idx = np.random.randint(0, n_data_ks-rollout, size=bs)
        q0s = torch.stack([train_t[i] for i in idx])
        targets = torch.stack([train_t[i:i+rollout+1] for i in idx])
        return q0s, targets
    
    # Vanilla
    print("\nTraining Vanilla KS NODE...", flush=True)
    van_ks = KSNeuralODE(N=N).to(device)
    nparams = sum(p.numel() for p in van_ks.parameters())
    print(f"  Params: {nparams}", flush=True)
    opt = torch.optim.Adam(van_ks.parameters(), lr=1e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, 2000, eta_min=1e-5)
    van_ks_losses = []; t0=time.time()
    for ep in range(2000):
        q0s, targets = make_ks_batch(8, 10)
        pred = rk4_integrate_batch(van_ks, q0s, 10, dt_save).permute(1,0,2)
        loss = torch.mean((pred-targets)**2)
        opt.zero_grad(); loss.backward()
        torch.nn.utils.clip_grad_norm_(van_ks.parameters(), 1.0)
        opt.step(); sched.step()
        van_ks_losses.append(loss.item())
        if (ep+1)%500==0: print(f"  Vanilla KS ep {ep+1}: loss={loss.item():.6f}", flush=True)
    van_ks_time = time.time()-t0
    
    # MP
    print("\nTraining MP KS NODE...", flush=True)
    mp_ks = KSNeuralODE(N=N).to(device)
    opt = torch.optim.Adam(mp_ks.parameters(), lr=1e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, 2000, eta_min=1e-5)
    mu_s = {0:1e-4, 500:1e-2, 1000:1e0, 1500:1e2}; mu=1e-4
    rollout_mp = 50; n_win_ks = 5; spw_ks = rollout_mp//n_win_ks
    mp_ks_losses, mp_ks_lgts, mp_ks_lps = [],[],[]; t0=time.time()
    for ep in range(2000):
        if ep in mu_s: mu=mu_s[ep]; print(f"  mu -> {mu:.1e}", flush=True)
        q0s, targets = make_ks_batch(8, rollout_mp)
        
        total_lgt = torch.tensor(0., device=device)
        total_lp = torch.tensor(0., device=device)
        pred_parts = []
        for w in range(n_win_ks):
            ws = w*spw_ks
            q_start = q0s if w==0 else targets[:, ws, :]
            pw = rk4_integrate_batch(mp_ks, q_start, spw_ks, dt_save).permute(1,0,2)
            pred_parts.append(pw)
            if w < n_win_ks-1:
                total_lp += torch.mean((targets[:,(w+1)*spw_ks,:]-pw[:,-1,:])**2)
        
        pred_full = torch.cat([p[:,:-1,:] for p in pred_parts[:-1]]+[pred_parts[-1]], dim=1)
        ml = min(pred_full.shape[1], targets.shape[1])
        total_lgt = torch.mean((pred_full[:,:ml,:]-targets[:,:ml,:])**2)
        total_lp = total_lp / max(n_win_ks-1,1)
        loss = total_lgt + (mu/2)*total_lp
        
        opt.zero_grad(); loss.backward()
        torch.nn.utils.clip_grad_norm_(mp_ks.parameters(), 1.0)
        opt.step(); sched.step()
        mp_ks_losses.append(loss.item()); mp_ks_lgts.append(total_lgt.item()); mp_ks_lps.append(total_lp.item())
        if (ep+1)%500==0: print(f"  MP KS ep {ep+1}: loss={loss.item():.6f}", flush=True)
    mp_ks_time = time.time()-t0
    
    # Evaluate
    print("\nEvaluating KS...", flush=True)
    q0e = torch.tensor(ten[0], dtype=torch.float32, device=device)
    n_short, n_long = 200, 3000
    
    with torch.no_grad():
        vs = rk4_integrate_single(van_ks, q0e, n_short, dt_save).cpu().numpy()*dstd+dmean
        ms = rk4_integrate_single(mp_ks, q0e, n_short, dt_save).cpu().numpy()*dstd+dmean
        vl = rk4_integrate_single(van_ks, q0e, n_long, dt_save).cpu().numpy()*dstd+dmean
        ml_arr = rk4_integrate_single(mp_ks, q0e, n_long, dt_save).cpu().numpy()*dstd+dmean
    
    tes = te[:n_short+1]; tel = te[:n_long+1]
    
    # Joint PDF
    dx = L/N
    def get_d(a): qx=np.gradient(a,dx,axis=-1); return qx, np.gradient(qx,dx,axis=-1)
    def jpdf(qx,qxx,b=80): return np.histogram2d(qx.flatten(),qxx.flatten(),bins=b,density=True)
    def kld(P,Q,e=1e-12): P,Q=P+e,Q+e; P,Q=P/P.sum(),Q/Q.sum(); return float(np.sum(P*np.log(P/Q)))
    
    np_ = min(3000, len(tel), len(ml_arr))
    qxt,qxxt = get_d(tel[:np_]); pt,xe,ye = jpdf(qxt,qxxt)
    
    kl_v = kl_m = float('nan')
    if np.isfinite(vl[:np_]).all():
        qxv,qxxv = get_d(vl[:np_]); pv,_,_ = jpdf(qxv,qxxv); kl_v = kld(pv,pt)
    if np.isfinite(ml_arr[:np_]).all():
        qxm,qxxm = get_d(ml_arr[:np_]); pm,_,_ = jpdf(qxm,qxxm); kl_m = kld(pm,pt)
    
    print(f"  KL div: Vanilla={kl_v:.4f}, MP={kl_m:.4f} (paper: NODE=0.773, MP=0.029)", flush=True)
    
    # Plots
    x = np.linspace(0, L, N, endpoint=False)
    
    fig,axes=plt.subplots(2,3,figsize=(18,10))
    ns_=min(200,len(tes),len(vs),len(ms)); ts_=np.arange(ns_)*dt_save
    vmin,vmax = tes[:ns_].min(), tes[:ns_].max()
    for ax,a,t in [(axes[0,0],tes[:ns_],'True (Short)'),(axes[0,1],vs[:ns_],'NODE (Short)'),(axes[0,2],ms[:ns_],'MP-NODE (Short)')]:
        if np.isfinite(a).all(): ax.pcolormesh(x,ts_,a,cmap='RdBu_r',vmin=vmin,vmax=vmax)
        ax.set_title(t); ax.set_xlabel('x'); ax.set_ylabel('t')
    nl_=min(2000,len(tel),len(vl),len(ml_arr)); tl_=np.arange(nl_)*dt_save
    for ax,a,t in [(axes[1,0],tel[:nl_],'True (Long)'),(axes[1,1],vl[:nl_],'NODE (Long)'),(axes[1,2],ml_arr[:nl_],'MP-NODE (Long)')]:
        if np.isfinite(a).all(): ax.pcolormesh(x,tl_,a,cmap='RdBu_r')
        ax.set_title(t); ax.set_xlabel('x'); ax.set_ylabel('t')
    plt.tight_layout(); plt.savefig('fig8_ks_hovmoller.png',dpi=150,bbox_inches='tight'); plt.close()
    
    fig,axes=plt.subplots(1,3,figsize=(18,5))
    axes[0].pcolormesh(xe[:-1],ye[:-1],pt.T,cmap='hot_r'); axes[0].set_title('True')
    if not np.isnan(kl_v):
        axes[1].pcolormesh(xe[:-1],ye[:-1],pv.T,cmap='hot_r'); axes[1].set_title(f'NODE (KL={kl_v:.3f})')
    else: axes[1].set_title('NODE (diverged)')
    if not np.isnan(kl_m):
        axes[2].pcolormesh(xe[:-1],ye[:-1],pm.T,cmap='hot_r'); axes[2].set_title(f'MP-NODE (KL={kl_m:.3f})')
    else: axes[2].set_title('MP-NODE (diverged)')
    for ax in axes: ax.set_xlabel('$q_x$'); ax.set_ylabel('$q_{xx}$')
    plt.tight_layout(); plt.savefig('fig9_ks_joint_pdf.png',dpi=150,bbox_inches='tight'); plt.close()
    
    fig,ax=plt.subplots(figsize=(10,5))
    ax.semilogy(van_ks_losses,alpha=.5,label='NODE'); ax.semilogy(mp_ks_losses,alpha=.5,label='MP-NODE')
    ax.set_xlabel('Epoch'); ax.set_ylabel('Loss'); ax.set_title('KS Training'); ax.legend(); ax.grid(True,alpha=.3)
    plt.tight_layout(); plt.savefig('fig10_ks_training.png',dpi=150,bbox_inches='tight'); plt.close()
    
    # Return period
    def rp(traj, dt_s):
        mx=np.max(traj,axis=-1); th=np.linspace(np.percentile(mx,10),np.percentile(mx,99),40); rps=[]
        for t in th:
            ti=np.where(mx>t)[0]*dt_s
            if len(ti)>1: iv=np.diff(ti); iv=iv[iv>0]; rps.append(np.mean(iv) if len(iv)>0 else np.nan)
            else: rps.append(np.nan)
        return th, np.array(rps)
    
    fig,ax=plt.subplots(figsize=(8,6))
    th_t,rp_t = rp(tel[:np_],dt_save); ax.plot(th_t,rp_t,'k-',lw=2,label='True')
    if np.isfinite(vl[:np_]).all():
        th_v,rp_v = rp(vl[:np_],dt_save); ax.plot(th_v,rp_v,'b--',label='NODE')
    if np.isfinite(ml_arr[:np_]).all():
        th_m,rp_m = rp(ml_arr[:np_],dt_save); ax.plot(th_m,rp_m,'r--',label='MP-NODE')
    ax.set_xlabel('Max |q|'); ax.set_ylabel('Return Period'); ax.set_title('Return Period'); ax.legend(); ax.grid(True,alpha=.3)
    plt.tight_layout(); plt.savefig('fig11_ks_return_period.png',dpi=150,bbox_inches='tight'); plt.close()
    
    print("All KS plots saved.", flush=True)
    return {'training':{'van_loss':float(van_ks_losses[-1]),'mp_loss':float(mp_ks_losses[-1]),
            'van_time':van_ks_time,'mp_time':mp_ks_time},'kl':{'vanilla':kl_v,'mp':kl_m},'nparams':nparams}

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    R = {}; t_total = time.time()
    print(f"Starting replication | device={device} | PyTorch={torch.__version__}", flush=True)
    
    R['exp1_gradient'] = experiment_gradient_explosion()
    R['exp2_landscape'] = experiment_loss_landscape()
    R['exp3_lorenz'] = experiment_lorenz_node()
    R['exp4_ks'] = experiment_ks()
    
    R['total_time'] = time.time()-t_total
    R['device'] = str(device); R['torch'] = torch.__version__
    
    with open('all_results.json','w') as f:
        json.dump(R, f, indent=2, default=str)
    
    print(f"\n{'='*60}\nALL DONE in {R['total_time']:.1f}s\n{'='*60}", flush=True)
    print(json.dumps(R, indent=2, default=str), flush=True)
