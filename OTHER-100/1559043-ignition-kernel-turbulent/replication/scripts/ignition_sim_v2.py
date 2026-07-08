#!/usr/bin/env python3
"""
2D simulation of post-discharge kernel ignition in a turbulent stratified crossflow.
Replicates Jaravel et al. (2019), OSTI 1559043.
Optimized version: coarser grid (1mm), reduced timesteps.
"""
import numpy as np
from scipy import ndimage
import os, json, time as timer

R_u = 8.314
SPECIES = ['CH4', 'O2', 'N2', 'CO2', 'H2O', 'NO', 'O']
N_SP = len(SPECIES)
SP = {sp: i for i, sp in enumerate(SPECIES)}
MW = np.array([16.04e-3, 32.0e-3, 28.0e-3, 44.01e-3, 18.015e-3, 30.01e-3, 16.0e-3])
CP0 = np.array([2226.0, 918.0, 1040.0, 846.0, 1864.0, 995.0, 1300.0])

Q_comb = 50.0e6; Ea_comb = 125.52e3; A_comb = 1.3e8
Ea_NO = 319.0e3; A_NO = 1.8e14

Lx, Lz = 0.073, 0.050
dx = dz = 0.001  # 1mm grid
Nx, Nz = int(Lx/dx), int(Lz/dz)  # 73 x 50 = 3650 cells

u_in = 20.0; T_in = 456.0; P_amb = 1.0e5; h_s = 6.4e-3
u_prime = 2.0; l_turb = 3.2e-3
U_ker = 2000.0; tau_pulse = 3e-6; D_ker = 5.0e-3; T_ker = 3300.0
x_ker_pos = 13.0e-3

dt = 1e-6; t_end = 0.002; Nt = int(t_end/dt)
mu_ref = 1.8e-5; D_diff = 2.0e-5; alpha_th = 2.5e-5

Y_ker = np.zeros(N_SP)
X_ker = {'N2': 0.74, 'O2': 0.14, 'NO': 0.054, 'O': 0.062}
Mmix_k = sum(X_ker.get(s, 0)*MW[SP[s]] for s in SPECIES)
for s, x in X_ker.items():
    Y_ker[SP[s]] = x * MW[SP[s]] / Mmix_k

print(f"Grid: {Nx}x{Nz}={Nx*Nz}, dt={dt*1e6:.1f}μs, Nt={Nt}")

def lap2d(f):
    L = np.zeros_like(f)
    L[1:-1,:] += (f[2:,:] - 2*f[1:-1,:] + f[:-2,:]) / dx**2
    L[:,1:-1] += (f[:,2:] - 2*f[:,1:-1] + f[:,:-2]) / dz**2
    return L

def advect(f, u, w):
    A = np.zeros_like(f)
    # x-direction upwind
    dfdx_fwd = np.zeros_like(f); dfdx_bwd = np.zeros_like(f)
    dfdx_fwd[:-1,:] = (f[1:,:] - f[:-1,:]) / dx
    dfdx_bwd[1:,:] = (f[1:,:] - f[:-1,:]) / dx
    A -= np.where(u > 0, u * dfdx_bwd, u * dfdx_fwd)
    # z-direction upwind
    dfdz_fwd = np.zeros_like(f); dfdz_bwd = np.zeros_like(f)
    dfdz_fwd[:,:-1] = (f[:,1:] - f[:,:-1]) / dz
    dfdz_bwd[:,1:] = (f[:,1:] - f[:,:-1]) / dz
    A -= np.where(w > 0, w * dfdz_bwd, w * dfdz_fwd)
    return A

def chemistry(Y, T, rho):
    omega = np.zeros_like(Y)
    q = np.zeros_like(T)
    
    c_CH4 = rho * np.maximum(Y[SP['CH4']], 0) / MW[SP['CH4']]
    c_O2  = rho * np.maximum(Y[SP['O2']], 0)  / MW[SP['O2']]
    
    mask = (T > 800) & (Y[SP['CH4']] > 1e-6) & (Y[SP['O2']] > 1e-6)
    rate = np.where(mask,
        A_comb * np.power(np.maximum(c_CH4,1e-10), 0.2) *
        np.power(np.maximum(c_O2,1e-10), 1.3) *
        np.exp(-Ea_comb / (R_u * np.maximum(T, 300))), 0.0)
    maxr = rho * np.maximum(Y[SP['CH4']], 0) / (MW[SP['CH4']] * dt * 0.5 + 1e-30)
    rate = np.minimum(rate, maxr)
    
    omega[SP['CH4']] = -rate * MW[SP['CH4']]
    omega[SP['O2']]  = -rate * 2 * MW[SP['O2']]
    omega[SP['CO2']] = rate * MW[SP['CO2']]
    omega[SP['H2O']] = rate * 2 * MW[SP['H2O']]
    q = rate * MW[SP['CH4']] * Q_comb
    
    # O recombination
    Omask = Y[SP['O']] > 1e-6
    tau_r = np.where(Omask, 1e-4 * np.exp(10000.0 / np.maximum(T, 300)), 1e10)
    r_O = rho * np.maximum(Y[SP['O']], 0) / np.maximum(tau_r, dt)
    omega[SP['O']]  -= r_O
    omega[SP['O2']] += r_O * 0.5
    q += r_O * 2.5e6
    
    # Thermal NO
    c_N2 = rho * np.maximum(Y[SP['N2']], 0) / MW[SP['N2']]
    NO_m = (T > 1500) & (Y[SP['N2']] > 0.01)
    c_O_eq = c_O2 * 3.97e5 * np.exp(-31090.0 / np.maximum(T, 300))
    c_O_tot = rho * np.maximum(Y[SP['O']], 0) / MW[SP['O']] + c_O_eq
    r_NO = np.where(NO_m, A_NO * c_N2 * c_O_tot * np.exp(-Ea_NO / (R_u * np.maximum(T, 300))), 0.0)
    maxr_NO = rho * np.maximum(Y[SP['N2']], 0) / (MW[SP['N2']] * dt * 0.5 + 1e-30)
    r_NO = np.minimum(r_NO, maxr_NO)
    omega[SP['NO']] += r_NO * MW[SP['NO']]
    omega[SP['N2']] -= r_NO * 0.5 * MW[SP['N2']]
    
    return omega, q

def run(phi, real=0):
    print(f"\n--- phi={phi}, real={real} ---")
    np.random.seed(42 + real*1000 + int(phi*100))
    
    u = np.full((Nx,Nz), u_in)
    w = np.zeros((Nx,Nz))
    T = np.full((Nx,Nz), T_in)
    Y = np.zeros((N_SP, Nx, Nz))
    
    f_s = 16.04 / (64.0/0.232)
    Y_f = phi * f_s / (1 + phi * f_s)
    Y_o = 0.232 * (1 - Y_f)
    Y_n = 1.0 - Y_f - Y_o
    
    z_arr = np.arange(Nz) * dz
    bl = 0.5 * (1 + np.tanh((z_arr - h_s)/1e-3))
    Y[SP['CH4'],:,:] = bl[None,:] * Y_f
    Y[SP['O2'],:,:]  = 0.232*(1-bl[None,:]) + Y_o*bl[None,:]
    Y[SP['N2'],:,:]  = 0.768*(1-bl[None,:]) + Y_n*bl[None,:]
    
    Mmix = 1.0 / np.maximum(np.sum(Y/MW[:,None,None], axis=0), 1e-10)
    rho = P_amb * Mmix / (R_u * T)
    
    i_k = int(x_ker_pos/dx)
    nk = int(D_ker/dx)
    i0, i1 = max(0,i_k-nk//2), min(Nx,i_k+nk//2)
    r_k = np.abs(np.arange(i0,i1)-i_k)*dx/(D_ker/2)
    kprof = np.sqrt(np.maximum(1-r_k**2, 0))
    
    th, Qh, Th = [], [], []
    snaps = {}
    t0w = timer.time()
    
    u_turb = ndimage.gaussian_filter1d(np.random.randn(Nz), l_turb/dz) * u_prime * 3
    w_turb = ndimage.gaussian_filter1d(np.random.randn(Nz), l_turb/dz) * u_prime * 3
    
    for n in range(Nt):
        t = n * dt
        
        # Advection + diffusion
        u += dt * (advect(u,u,w) + mu_ref/np.maximum(rho,0.1)*lap2d(u))
        w += dt * (advect(w,u,w) + mu_ref/np.maximum(rho,0.1)*lap2d(w))
        
        adv_T = advect(T,u,w)
        diff_T = alpha_th * lap2d(T)
        
        adv_Y = np.stack([advect(Y[s],u,w) for s in range(N_SP)])
        diff_Y = np.stack([D_diff * lap2d(Y[s]) for s in range(N_SP)])
        
        # Chemistry
        om, qd = chemistry(Y, T, rho)
        cp = np.sum(Y * CP0[:,None,None] * (1+2.5e-4*(T[None,:,:]-300)), axis=0)
        cp = np.maximum(cp, 500.0)
        
        T += dt * (adv_T + diff_T + qd / (rho*cp))
        Y += dt * (adv_Y + diff_Y + om / np.maximum(rho[None,:,:], 0.1))
        
        # Kernel injection
        if t < 2*tau_pulse:
            Mt = 1.0 if t < tau_pulse else max(0, 1-(t-tau_pulse)/tau_pulse)
            if Mt > 0:
                rho_k = P_amb * 0.028 / (R_u * T_ker)
                for idx, ii in enumerate(range(i0, i1)):
                    un = Mt * U_ker * kprof[idx] * (1 + 0.2*np.random.randn())
                    un = max(un, 0)
                    frac = np.minimum(dt*rho_k*un/(dz*np.maximum(rho[ii,:3],0.1)), 0.3)
                    w[ii,:3] += frac * un
                    T[ii,:3] = (1-frac)*T[ii,:3] + frac*T_ker
                    for s in range(N_SP):
                        Y[s,ii,:3] = (1-frac)*Y[s,ii,:3] + frac*Y_ker[s]
        
        # BC: inlet
        if n % 30 == 0:
            u_turb = ndimage.gaussian_filter1d(np.random.randn(Nz), l_turb/dz)*u_prime*3
            w_turb = ndimage.gaussian_filter1d(np.random.randn(Nz), l_turb/dz)*u_prime*3
        u[0,:] = u_in + u_turb
        w[0,:] = w_turb
        T[0,:] = T_in
        Y[SP['CH4'],0,:] = bl*Y_f
        Y[SP['O2'],0,:]  = 0.232*(1-bl) + Y_o*bl
        Y[SP['N2'],0,:]  = 0.768*(1-bl) + Y_n*bl
        for s in [SP['CO2'],SP['H2O'],SP['NO'],SP['O']]:
            Y[s,0,:] = 0
        
        # BC: outlet zero-gradient
        u[-1,:]=u[-2,:]; w[-1,:]=w[-2,:]; T[-1,:]=T[-2,:]
        Y[:,-1,:] = Y[:,-2,:]
        
        # BC: walls
        u[:,0]=0; w[:,0]=0; T[:,0]=T[:,1]; Y[:,:,0]=Y[:,:,1]
        u[:,-1]=0; w[:,-1]=0; T[:,-1]=T[:,-2]; Y[:,:,-1]=Y[:,:,-2]
        
        T = np.clip(T, 200, 4000)
        Y = np.clip(Y, 0, 1)
        
        Mmix = 1.0 / np.maximum(np.sum(Y/MW[:,None,None], axis=0), 1e-10)
        rho = P_amb * Mmix / (R_u * np.maximum(T, 200))
        
        if n % 20 == 0:
            Qt = float(np.sum(qd)*dx*dz)
            th.append(float(t*1e3))
            Qh.append(Qt)
            Th.append(float(np.max(T)))
        
        if n > 0 and n % 200 == 0:
            tk = f't_{t*1e3:.1f}ms'
            snaps[tk] = {
                'T': T.copy(), 'Y_CH4': Y[SP['CH4']].copy(),
                'Y_O2': Y[SP['O2']].copy(), 'Y_NO': Y[SP['NO']].copy(),
                'q_dot': qd.copy(), 'u': u.copy(), 'w': w.copy(),
            }
        
        if n > 0 and n % (Nt//10) == 0:
            el = timer.time()-t0w
            print(f"  {100*n/Nt:.0f}% t={t*1e3:.2f}ms Tmax={np.max(T):.0f}K "
                  f"Qdot={np.sum(qd)*dx*dz:.2e} [{el:.0f}s]")
    
    print(f"  Done. Tmax={np.max(T):.0f}K wall={timer.time()-t0w:.0f}s")
    return {
        'phi': phi, 'real': real,
        't': th, 'Qdot': Qh, 'Tmax': Th,
        'final_Qdot': Qh[-1] if Qh else 0,
        'final_Tmax': float(np.max(T)),
    }, snaps

def main():
    out = '/tmp/ignition_replication/results'
    os.makedirs(out, exist_ok=True)
    
    phis = [0.6, 0.8, 1.0, 1.2]
    nreal = 3
    all_r = {}
    
    for phi in phis:
        all_r[f'phi_{phi}'] = []
        for r in range(nreal):
            res, snaps = run(phi, r)
            all_r[f'phi_{phi}'].append(res)
            sd = os.path.join(out, f'snap_phi{phi}_r{r}')
            os.makedirs(sd, exist_ok=True)
            for k, v in snaps.items():
                np.savez_compressed(os.path.join(sd, f'{k}.npz'), **v)
    
    mQ = max(r['final_Qdot'] for v in all_r.values() for r in v)
    mQ = max(mQ, 1e-10)
    
    summary = {}
    print("\n" + "="*50)
    print("IGNITION PROPENSITY")
    print("="*50)
    for phi in phis:
        k = f'phi_{phi}'
        IPs = [r['final_Qdot']/mQ for r in all_r[k]]
        Ts = [r['final_Tmax'] for r in all_r[k]]
        summary[k] = {
            'IP_mean': float(np.mean(IPs)), 'IP_std': float(np.std(IPs)),
            'Tmax_mean': float(np.mean(Ts)), 'IPs': [float(x) for x in IPs],
        }
        print(f"  phi={phi}: IP={np.mean(IPs):.3f}+/-{np.std(IPs):.3f} Tmax={np.mean(Ts):.0f}K")
    
    with open(os.path.join(out, 'results.json'), 'w') as f:
        json.dump({'results': all_r, 'summary': summary}, f, indent=2, default=str)
    print(f"\nSaved to {out}/results.json")

if __name__ == '__main__':
    main()
