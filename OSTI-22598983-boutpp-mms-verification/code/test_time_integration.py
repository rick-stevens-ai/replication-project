#!/usr/bin/env python3
"""
Independent replication of BOUT++ MMS time-integration verification (Sec 4.1).

Paper claim (Fig 2): integrating df/dt = f from t=0 to t=1, error norm vs dt.
Measured convergence rates (two highest-res cases):
    Euler   0.995   (expected 1)
    RK3-SSP 3.00    (expected 3)
    RK4     3.99    (expected 4)
    Karniadakis 2.13 (expected 3; degraded by Euler startup) -- BOUT++-specific, skipped.

We do NOT use BOUT++. We implement Euler, RK3-SSP (Shu-Osher/Gottlieb-Shu), RK4 from
scratch and integrate the scalar ODE df/dt = f, f(0)=1, exact f(1)=e.
Error = |f_num(1) - e|. Convergence rate = log2(err[k]/err[k+1]) as dt halves.
"""
import numpy as np

def rhs(f, t):
    return f  # df/dt = f

def euler(f0, dt, nsteps):
    f = f0
    t = 0.0
    for _ in range(nsteps):
        f = f + dt * rhs(f, t)
        t += dt
    return f

def rk4(f0, dt, nsteps):
    f = f0
    t = 0.0
    for _ in range(nsteps):
        k1 = rhs(f, t)
        k2 = rhs(f + 0.5*dt*k1, t + 0.5*dt)
        k3 = rhs(f + 0.5*dt*k2, t + 0.5*dt)
        k4 = rhs(f + dt*k3, t + dt)
        f = f + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)
        t += dt
    return f

def rk3_ssp(f0, dt, nsteps):
    # Third-order Strong Stability Preserving RK (Gottlieb & Shu 1998), the
    # scheme cited by the paper [ref 23].
    f = f0
    t = 0.0
    for _ in range(nsteps):
        u1 = f + dt*rhs(f, t)
        u2 = 0.75*f + 0.25*u1 + 0.25*dt*rhs(u1, t+dt)
        f  = (1.0/3.0)*f + (2.0/3.0)*u2 + (2.0/3.0)*dt*rhs(u2, t+0.5*dt)
        t += dt
    return f

def convergence(method, name, expected):
    exact = np.e
    # choose dt values matching paper's decades (dt from ~1 down to ~1e-3)
    nsteps_list = [8, 16, 32, 64, 128, 256, 512, 1024]
    errs = []
    dts = []
    for n in nsteps_list:
        dt = 1.0 / n
        fnum = method(1.0, dt, n)
        errs.append(abs(fnum - exact))
        dts.append(dt)
    print(f"\n== {name} (expected order {expected}) ==")
    print(f"{'dt':>12} {'error':>14} {'rate':>8}")
    rates = []
    for i in range(len(errs)):
        if i == 0:
            print(f"{dts[i]:12.5e} {errs[i]:14.5e} {'--':>8}")
        else:
            r = np.log(errs[i-1]/errs[i]) / np.log(dts[i-1]/dts[i])
            rates.append(r)
            print(f"{dts[i]:12.5e} {errs[i]:14.5e} {r:8.3f}")
    # paper uses "two highest resolution cases" -> last rate
    final = rates[-1]
    print(f"  -> convergence rate (finest pair): {final:.3f}   [paper: see below]")
    return final

if __name__ == "__main__":
    results = {}
    results['Euler']   = convergence(euler,   'Euler',   1)
    results['RK3-SSP'] = convergence(rk3_ssp, 'RK3-SSP', 3)
    results['RK4']     = convergence(rk4,     'RK4',     4)
    print("\n=== SUMMARY (my rate vs paper) ===")
    paper = {'Euler': 0.995, 'RK3-SSP': 3.00, 'RK4': 3.99}
    for k in results:
        print(f"  {k:10s}: mine={results[k]:.3f}  paper={paper[k]:.3f}  diff={abs(results[k]-paper[k]):.3f}")
