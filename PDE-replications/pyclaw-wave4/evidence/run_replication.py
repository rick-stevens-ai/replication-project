#!/usr/bin/env python
"""
PyClaw replication — Wave 4
============================
Runs each test case in a subprocess so Fortran runtime errors
(e.g. SharpClaw allocation bug) don't kill the whole suite.
"""

import json, time, sys, os, subprocess, tempfile
import numpy as np

VENV_PYTHON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           '.venv', 'bin', 'python')
EDIR = os.path.dirname(os.path.abspath(__file__))

# ── subprocess runner for acoustics ──────────────────────────────────
ACOUSTICS_WORKER = r'''
import json, sys, numpy as np
from clawpack.pyclaw.examples.acoustics_1d_homogeneous import acoustics_1d

kwargs = json.loads(sys.argv[1])
claw = acoustics_1d.setup(disable_output=True, **kwargs)
claw.run()
q0 = claw.frames[0].state.get_q_global().reshape(-1)
qf = claw.frames[claw.num_output_times].state.get_q_global().reshape(-1)
dx = claw.solution.domain.grid.delta[0]
err = float(dx * np.sum(np.abs(qf - q0)))
# Also dump q0/qf for plotting if N is small
result = {"error": err}
if kwargs.get("num_cells", 100) <= 200:
    xc = claw.solution.domain.grid.x.centers.tolist()
    result["xc"] = xc
    result["q0_p"] = q0[:len(xc)].tolist()
    result["q0_u"] = q0[len(xc):].tolist()
    result["qf_p"] = qf[:len(xc)].tolist()
    result["qf_u"] = qf[len(xc):].tolist()
print(json.dumps(result))
'''

def run_acoustics_case(name, kwargs, timeout=120):
    """Run one acoustics case in a subprocess."""
    t0 = time.time()
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(ACOUSTICS_WORKER)
            worker_path = f.name
        result = subprocess.run(
            [VENV_PYTHON, worker_path, json.dumps(kwargs)],
            capture_output=True, text=True, timeout=timeout
        )
        os.unlink(worker_path)
        elapsed = time.time() - t0
        if result.returncode != 0:
            return dict(error=None, status="ERROR",
                        msg=result.stderr.strip()[-300:],
                        elapsed_s=round(elapsed, 2))
        # Parse last line as JSON (stdout may have CLAW log lines)
        lines = result.stdout.strip().split('\n')
        data = json.loads(lines[-1])
        return dict(error=data['error'], elapsed_s=round(elapsed, 2),
                    raw=data)
    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        return dict(error=None, status="TIMEOUT", elapsed_s=round(elapsed, 2))
    except Exception as exc:
        elapsed = time.time() - t0
        return dict(error=None, status="ERROR", msg=str(exc),
                    elapsed_s=round(elapsed, 2))


# ── Sod subprocess worker ───────────────────────────────────────────
SOD_WORKER = r'''
import json, numpy as np
from clawpack import pyclaw, riemann

try:
    rs = riemann.euler_with_efix_1D
except AttributeError:
    rs = riemann.euler_1D

solver = pyclaw.ClawSolver1D(rs)
solver.limiters = pyclaw.limiters.tvd.MC
solver.kernel_language = 'Fortran'
solver.bc_lower[0] = pyclaw.BC.extrap
solver.bc_upper[0] = pyclaw.BC.extrap

num_cells = 400
x = pyclaw.Dimension(0.0, 1.0, num_cells, name='x')
domain = pyclaw.Domain(x)
state = pyclaw.State(domain, solver.num_eqn)

gamma = 1.4
state.problem_data['gamma'] = gamma
state.problem_data['gamma1'] = gamma - 1.0

xc = domain.grid.x.centers
rho_L, u_L, p_L = 1.0, 0.0, 1.0
rho_R, u_R, p_R = 0.125, 0.0, 0.1
x0 = 0.5

state.q[0, :] = np.where(xc < x0, rho_L, rho_R)
state.q[1, :] = 0.0
state.q[2, :] = np.where(xc < x0, p_L/(gamma-1.), p_R/(gamma-1.))

claw = pyclaw.Controller()
claw.solution = pyclaw.Solution(state, domain)
claw.solver = solver
claw.tfinal = 0.2
claw.num_output_times = 1
claw.keep_copy = True
claw.output_format = None

claw.run()

qf = claw.frames[-1].state.get_q_global()
rho = qf[0, :]
mom = qf[1, :]
E   = qf[2, :]
u = mom / rho
p = (gamma - 1.) * (E - 0.5 * rho * u**2)

# Locate shock: steepest density drop in right half
drho = np.diff(rho)
idx_shock = np.argmin(drho[num_cells//2:]) + num_cells//2
x_shock = float(xc[idx_shock])

# Post-shock values (region between contact and shock, around x=0.58)
idx_post = np.argmin(np.abs(xc - 0.58))
rho_post = float(np.mean(rho[idx_post-2:idx_post+3]))
p_post   = float(np.mean(p[idx_post-2:idx_post+3]))
u_post   = float(np.mean(u[idx_post-2:idx_post+3]))

result = dict(
    x_shock=x_shock, rho_post=rho_post, p_post=p_post, u_post=u_post,
    xc=xc.tolist(), rho=rho.tolist(), u=u.tolist(), p=p.tolist()
)
print(json.dumps(result))
'''

def run_sod(timeout=120):
    t0 = time.time()
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(SOD_WORKER)
            worker_path = f.name
        result = subprocess.run(
            [VENV_PYTHON, worker_path],
            capture_output=True, text=True, timeout=timeout
        )
        os.unlink(worker_path)
        elapsed = time.time() - t0
        if result.returncode != 0:
            return dict(status="ERROR", msg=result.stderr.strip()[-500:],
                        elapsed_s=round(elapsed, 2))
        lines = result.stdout.strip().split('\n')
        data = json.loads(lines[-1])
        data['elapsed_s'] = round(elapsed, 2)
        return data
    except subprocess.TimeoutExpired:
        return dict(status="TIMEOUT", elapsed_s=round(time.time()-t0, 2))
    except Exception as exc:
        return dict(status="ERROR", msg=str(exc),
                    elapsed_s=round(time.time()-t0, 2))


# ── Plotting ─────────────────────────────────────────────────────────
def plot_acoustics(raw, outpath):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    xc = np.array(raw['xc'])
    fig, axes = plt.subplots(2, 1, figsize=(8, 6))
    axes[0].plot(xc, raw['q0_p'], 'b--', lw=1.5, label='t=0 (initial)')
    axes[0].plot(xc, raw['qf_p'], 'r-',  lw=1.5, label='t=1 (final)')
    axes[0].set_ylabel('Pressure')
    axes[0].legend()
    axes[0].set_title('1D Acoustics — Periodic wrap-around (N=100, Classic)')

    axes[1].plot(xc, raw['q0_u'], 'b--', lw=1.5, label='t=0')
    axes[1].plot(xc, raw['qf_u'], 'r-',  lw=1.5, label='t=1')
    axes[1].set_ylabel('Velocity')
    axes[1].set_xlabel('x')
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()
    print(f"  Saved {outpath}")


def plot_sod(sod, outpath):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    xc = np.array(sod['xc'])
    rho = np.array(sod['rho'])
    u   = np.array(sod['u'])
    p   = np.array(sod['p'])

    exact = dict(x_shock=0.6803, rho_post=0.26557, p_post=0.30313, u_post=0.92745)

    fig, axes = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
    axes[0].plot(xc, rho, 'b-', lw=1.2)
    axes[0].axhline(exact['rho_post'], color='r', ls='--', lw=1, label=f"exact ρ*={exact['rho_post']}")
    axes[0].axvline(exact['x_shock'], color='gray', ls=':', lw=1, label=f"exact shock x={exact['x_shock']}")
    axes[0].set_ylabel('Density')
    axes[0].legend(fontsize=8)
    axes[0].set_title('Sod Shock Tube — PyClaw Classic (N=400, t=0.2)')

    axes[1].plot(xc, u, 'b-', lw=1.2)
    axes[1].axhline(exact['u_post'], color='r', ls='--', lw=1, label=f"exact u*={exact['u_post']}")
    axes[1].set_ylabel('Velocity')
    axes[1].legend(fontsize=8)

    axes[2].plot(xc, p, 'b-', lw=1.2)
    axes[2].axhline(exact['p_post'], color='r', ls='--', lw=1, label=f"exact p*={exact['p_post']}")
    axes[2].set_ylabel('Pressure')
    axes[2].set_xlabel('x')
    axes[2].legend(fontsize=8)

    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()
    print(f"  Saved {outpath}")


def plot_convergence(conv, outpath):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    Ns = conv['Ns']
    errs = conv['errors']
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.loglog(Ns, errs, 'bo-', lw=2, label='Classic (MC limiter)')
    ax.loglog(Ns, [errs[0]*(Ns[0]/N)**2 for N in Ns], 'r--', label='O(Δx²)')
    ax.set_xlabel('Number of cells')
    ax.set_ylabel('L1 error (periodic return)')
    ax.set_title('1D Acoustics — Convergence')
    ax.legend()
    ax.grid(True, which='both', ls=':')
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()
    print(f"  Saved {outpath}")


# ── MAIN ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 60)
    print("PyClaw Replication — Wave 4")
    print("=" * 60)

    # Reference values from upstream test_acoustics.py
    refs = {
        "classic_Fortran_N100": 0.001981,
        "classic_Python_N100":  0.001981,
        "sharpclaw_weno5_N100": 0.001540,
        "sharpclaw_weno11_N100": 0.000521,
        "sharpclaw_LMM_N100":   0.001545,
    }
    thresholds_reg = 1e-5  # for regression tests
    accuracy_thresholds = {
        "classic_Fortran_N2000": 1e-5,
        "classic_Fortran_N4000": 2e-6,
        "sharpclaw_N2000":       1e-8,
    }

    cases = [
        ("classic_Fortran_N100",  dict(kernel_language='Fortran', solver_type='classic', num_cells=100)),
        ("classic_Python_N100",   dict(kernel_language='Python',  solver_type='classic', num_cells=100)),
        ("sharpclaw_weno5_N100",  dict(kernel_language='Fortran', solver_type='sharpclaw', num_cells=100)),
        ("sharpclaw_weno11_N100", dict(kernel_language='Fortran', solver_type='sharpclaw', num_cells=100, weno_order=11)),
        ("sharpclaw_LMM_N100",   dict(kernel_language='Fortran', solver_type='sharpclaw', num_cells=100, time_integrator='SSPLMMk3')),
        ("classic_Fortran_N2000", dict(kernel_language='Fortran', solver_type='classic', num_cells=2000)),
        ("classic_Fortran_N4000", dict(kernel_language='Fortran', solver_type='classic', num_cells=4000)),
        ("sharpclaw_N2000",       dict(kernel_language='Fortran', solver_type='sharpclaw', num_cells=2000)),
    ]

    # ── 1. Acoustics regression ──
    print("\n[1] Acoustics regression suite")
    results = {}
    plot_raw = None
    for name, kw in cases:
        r = run_acoustics_case(name, kw)
        err = r.get('error')
        if err is not None:
            if name in refs:
                match = abs(err - refs[name]) < thresholds_reg
                r['status'] = "PASS" if match else "FAIL"
                r['ref'] = refs[name]
            elif name in accuracy_thresholds:
                match = err < accuracy_thresholds[name]
                r['status'] = "PASS" if match else "FAIL"
                r['threshold'] = accuracy_thresholds[name]
            else:
                r['status'] = "OK"
            print(f"  {name}: err={err:.6e}  {r['status']}  ({r['elapsed_s']}s)")
            if name == "classic_Fortran_N100" and 'raw' in r:
                plot_raw = r['raw']
        else:
            status = r.get('status', 'ERROR')
            msg = r.get('msg', '')[:120]
            print(f"  {name}: {status}  ({r['elapsed_s']}s)  {msg}")
        # Don't store huge arrays in summary
        if 'raw' in r:
            del r['raw']
        results[name] = r

    # Plot acoustics
    if plot_raw:
        print("\n  Plotting acoustics...")
        plot_acoustics(plot_raw, os.path.join(EDIR, 'acoustics_solution.png'))

    # ── 2. Convergence study ──
    print("\n[2] Convergence study (Classic, Fortran)")
    Ns = [50, 100, 200, 400, 800, 1600]
    conv_errors = []
    for N in Ns:
        r = run_acoustics_case(f"conv_N{N}", dict(kernel_language='Fortran',
                                                    solver_type='classic', num_cells=N))
        err = r.get('error')
        conv_errors.append(err)
        if err is not None:
            print(f"  N={N:5d}  L1_err={err:.6e}")
        else:
            print(f"  N={N:5d}  {r.get('status','ERROR')}")

    orders = []
    if all(e is not None for e in conv_errors):
        for i in range(1, len(Ns)):
            o = np.log(conv_errors[i-1]/conv_errors[i]) / np.log(Ns[i]/Ns[i-1])
            orders.append(round(float(o), 3))
            print(f"    order({Ns[i-1]}→{Ns[i]}) = {o:.3f}")
        conv = dict(Ns=Ns, errors=conv_errors, orders=orders)
        plot_convergence(conv, os.path.join(EDIR, 'convergence.png'))
    else:
        conv = dict(Ns=Ns, errors=conv_errors, orders=[], status="incomplete")

    # ── 3. Sod shock tube ──
    print("\n[3] Sod shock tube")
    sod = run_sod()
    exact_sod = dict(x_shock=0.6803, rho_post=0.26557, p_post=0.30313, u_post=0.92745)
    sod_ok = 'xc' in sod
    if sod_ok:
        for k in exact_sod:
            e = exact_sod[k]; c = sod[k]
            rel = abs(c-e)/abs(e) if e != 0 else abs(c-e)
            print(f"  {k}: computed={c:.5f}  exact={e:.5f}  rel_err={rel:.4e}")
        plot_sod(sod, os.path.join(EDIR, 'sod_shock_tube.png'))
    else:
        print(f"  Sod: {sod.get('status','ERROR')}")
        print(f"  {sod.get('msg','')[:200]}")

    # ── 4. Save results ──
    summary = dict(
        acoustics_regression=results,
        convergence=conv,
        sod_shock_tube={k: v for k, v in sod.items()
                        if k not in ('xc','rho','u','p')},
        sod_exact=exact_sod,
    )
    outfile = os.path.join(EDIR, 'results.json')
    with open(outfile, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\n  Results → {outfile}")

    # ── 5. Summary ──
    print("\n" + "=" * 60)
    n_pass = sum(1 for v in results.values() if v.get('status') == 'PASS')
    n_total = len(results)
    print(f"Acoustics: {n_pass}/{n_total} PASS")
    if sod_ok:
        print("Sod: computed successfully")
    else:
        print(f"Sod: {sod.get('status', 'ERROR')}")
    if orders:
        avg_order = np.mean(orders)
        print(f"Convergence: avg order = {avg_order:.2f} (expected ≈ 2.0 for classic)")
    print("=" * 60)
