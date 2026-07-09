"""
Paper-faithful experiments reproducing Hiptmair-Moiola-Perugia 2011, §4.

Reproduces:
  - Fig 4.2: regular solution xi=1, omega=10; L2 / brokenH1 / jumpL2 vs p
  - Fig 4.3: singular xi=2/3 and 3/2, omega=10; L2 vs p/log(p)
  - Fig 4.4: singular xi=2/3 and 3/2, omega=10; brokenH1 vs p/log(p)
  - Fig 4.5: singular xi=2/3 and 3/2, omega=10; jumpL2 vs p/log(p)
  - Fig 4.6 left: regular xi=1, omega in {0.25, 1, 4, 16, 64}, L2 vs p
  - Fig 4.6 right: singular xi=2/3, same omega sweep, L2 vs p/log(p)
  - Algebraic order extraction for singular cases (slope in log(error) vs log(p/log p))
  - Conditioning observation (record cond(A) vs p)

The paper uses two flux choices: UWVF (alpha=beta=delta=1/2) and PWDG with
parameter a0=10. Our solver uses the LS-Trefftz-DG variant with alpha=k/2,
delta=1/(2k). This shares the same plane-wave trial space and produces a
positive-semidefinite normal-equation system. We document the deviation
honestly: the curve labelled "Trefftz-DG-LS" in our results is the
reproduction of the paper's PWDG curves at the level of approximation theory
(same trial space, same kind of skeleton penalty) but uses a least-squares
discretization. The paper's "proj." curve (best L^2 projection onto the
plane-wave space) is reproduced exactly.

Output:
  results/paper_fig42_regular.json
  results/paper_fig43_45_singular.json    (combines 4.3, 4.4, 4.5)
  results/paper_fig46_omega_sweep.json
  results/paper_conditioning.json
"""
import sys, os, json, time
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from paper_mesh import make_paper_mesh
from pwdg_dirichlet import TrefftzDGLS
from bessel_solution import make_bessel_solution
from paper_errors import (
    l2_error_omega,
    broken_h1_seminorm_error,
    jump_l2_skeleton,
    l2_projection_errors,
    l2_norm_omega,
)

RESULTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'results'))
os.makedirs(RESULTS_DIR, exist_ok=True)


def run_one(mesh, omega, p, u_exact, want_proj=True):
    """Solve PWDG at given p and return error dict."""
    solver = TrefftzDGLS(mesh, k=omega, p=p)
    out = {'p': p}
    t0 = time.time()
    try:
        c, A, b = solver.solve(u_exact)
        out['solve_time_s'] = time.time() - t0
        out['cond_A'] = float(np.linalg.cond(A))
    except Exception as e:
        out['solve_failed'] = str(e); return out

    out['L2_omega'] = float(l2_error_omega(mesh, solver, c, u_exact))
    out['brokenH1'] = float(broken_h1_seminorm_error(mesh, solver, c, u_exact))
    out['jumpL2']  = float(jump_l2_skeleton(mesh, solver, c))
    if want_proj:
        e_pr, _ = l2_projection_errors(mesh, solver, u_exact)
        out['proj_L2'] = float(e_pr)
    return out


def experiment_fig42_regular():
    mesh = make_paper_mesh()
    omega = 10.0
    u = make_bessel_solution(1.0, omega)
    u_norm = float(l2_norm_omega(mesh, u))
    p_list = list(range(3, 22, 2))  # 3..21 to keep things light
    rows = []
    for p in p_list:
        r = run_one(mesh, omega, p, u)
        rows.append(r)
        print(f"[fig4.2 xi=1 om=10] p={p:2d}  L2={r.get('L2_omega'):.3e}  "
              f"H1={r.get('brokenH1'):.3e}  jp={r.get('jumpL2'):.3e}  "
              f"proj={r.get('proj_L2'):.3e}  cond={r.get('cond_A'):.2e}")
    out = {
        'experiment': 'fig4.2_regular_xi1_omega10',
        'paper_ref': 'Hiptmair-Moiola-Perugia 2011 Fig 4.2',
        'description': 'Regular solution u=J_1(omega r)cos(theta); L^2, broken H^1, jump norms vs p',
        'mesh': '8 triangles on [0,1]x[-1/2,1/2], h=1/sqrt(2)',
        'omega': omega, 'xi': 1.0,
        'u_L2_norm': u_norm,
        'rows': rows,
    }
    with open(os.path.join(RESULTS_DIR, 'paper_fig42_regular.json'), 'w') as f:
        json.dump(out, f, indent=2)
    return out


def experiment_fig43_45_singular():
    mesh = make_paper_mesh()
    omega = 10.0
    p_list = list(range(3, 22, 2))
    out_all = {}
    for xi in [2/3, 3/2]:
        u = make_bessel_solution(xi, omega)
        u_norm = float(l2_norm_omega(mesh, u))
        rows = []
        for p in p_list:
            r = run_one(mesh, omega, p, u)
            r['p_over_log_p'] = p / np.log(p)
            rows.append(r)
            print(f"[fig4.3-5 xi={xi:.3f} om=10] p={p:2d}  L2={r.get('L2_omega'):.3e}  "
                  f"H1={r.get('brokenH1'):.3e}  jp={r.get('jumpL2'):.3e}  "
                  f"proj={r.get('proj_L2'):.3e}")
        out_all[f'xi_{xi:.4f}'] = {
            'xi': xi, 'omega': omega, 'u_L2_norm': u_norm, 'rows': rows,
        }
        # Algebraic-order estimate: slope of log(error) vs log(p/log p)
        # using the central window where convergence is "clean"
        good = [r for r in rows if r.get('L2_omega', 1.0) > 0 and r.get('p_over_log_p') and r['p'] >= 5 and r['p'] <= 17]
        if len(good) >= 3:
            x = np.log([r['p_over_log_p'] for r in good])
            for key in ['L2_omega', 'brokenH1', 'jumpL2']:
                y = np.log([r[key] for r in good])
                # slope = d log err / d log (p/log p)
                slope, intercept = np.polyfit(x, y, 1)
                out_all[f'xi_{xi:.4f}'][f'algebraic_slope_{key}'] = float(slope)
                print(f"  fit slope log({key}) vs log(p/log p) = {slope:.2f}")
    final = {
        'experiment': 'fig4.3-4.5_singular_xi_2over3_and_3over2',
        'paper_ref': 'Hiptmair-Moiola-Perugia 2011 Fig 4.3, 4.4, 4.5',
        'description': 'Singular solutions u=J_xi(omega r)cos(xi theta), xi=2/3, 3/2; L2/H1/jump vs p/log(p)',
        'mesh': '8 triangles on [0,1]x[-1/2,1/2], h=1/sqrt(2)',
        'expected': 'algebraic convergence in p/log(p); paper says xi=3/2 (u in H^2) converges faster than xi=2/3',
        'cases': out_all,
    }
    with open(os.path.join(RESULTS_DIR, 'paper_fig43_45_singular.json'), 'w') as f:
        json.dump(final, f, indent=2)
    return final


def experiment_fig46_omega_sweep():
    mesh = make_paper_mesh()
    p_list = list(range(3, 22, 2))
    out_all = {}
    # Fig 4.6 left: regular xi=1
    print("\n--- Fig 4.6 left: regular xi=1, omega sweep ---")
    out_all['regular_xi_1'] = {'rows_by_omega': {}}
    for omega in [0.25, 1.0, 4.0, 16.0, 64.0]:
        u = make_bessel_solution(1.0, omega)
        rows = []
        for p in p_list:
            r = run_one(mesh, omega, p, u, want_proj=False)
            rows.append(r)
        out_all['regular_xi_1']['rows_by_omega'][f'omega_{omega}'] = rows
        print(f"  omega={omega:>5g}: L2 at p=21 = {rows[-1].get('L2_omega'):.2e}")
    # Fig 4.6 right: singular xi=2/3
    print("\n--- Fig 4.6 right: singular xi=2/3, omega sweep ---")
    out_all['singular_xi_2_3'] = {'rows_by_omega': {}}
    for omega in [0.25, 1.0, 4.0, 16.0, 64.0]:
        u = make_bessel_solution(2/3, omega)
        rows = []
        for p in p_list:
            r = run_one(mesh, omega, p, u, want_proj=False)
            r['p_over_log_p'] = p / np.log(p)
            rows.append(r)
        out_all['singular_xi_2_3']['rows_by_omega'][f'omega_{omega}'] = rows
        print(f"  omega={omega:>5g}: L2 at p=21 = {rows[-1].get('L2_omega'):.2e}")
    final = {
        'experiment': 'fig4.6_omega_sweep',
        'paper_ref': 'Hiptmair-Moiola-Perugia 2011 Fig 4.6',
        'description': 'Vary omega in {0.25,1,4,16,64} with fixed mesh; preasymptotic region grows with omega, instability appears sooner for small omega',
        'cases': out_all,
    }
    with open(os.path.join(RESULTS_DIR, 'paper_fig46_omega_sweep.json'), 'w') as f:
        json.dump(final, f, indent=2)
    return final


def experiment_conditioning():
    """Document the conditioning growth — paper §4 notes ill-conditioning blocks convergence."""
    mesh = make_paper_mesh()
    omega = 10.0
    u = make_bessel_solution(1.0, omega)
    rows = []
    for p in list(range(3, 22, 2)) + [23, 25]:
        try:
            solver = TrefftzDGLS(mesh, k=omega, p=p)
            c, A, b = solver.solve(u)
            cn = float(np.linalg.cond(A))
            err = float(l2_error_omega(mesh, solver, c, u))
            rows.append({'p': p, 'cond_A': cn, 'L2_omega': err})
            print(f"[cond] p={p:2d}  cond={cn:.2e}  L2={err:.2e}")
        except Exception as e:
            rows.append({'p': p, 'solve_failed': str(e)})
            print(f"[cond] p={p:2d}  FAILED: {e}")
    out = {
        'experiment': 'conditioning_growth',
        'paper_ref': 'Hiptmair-Moiola-Perugia 2011 §4, last paragraph: ill-conditioning blocks high p',
        'rows': rows,
    }
    with open(os.path.join(RESULTS_DIR, 'paper_conditioning.json'), 'w') as f:
        json.dump(out, f, indent=2)
    return out


if __name__ == '__main__':
    print("\n========== Fig 4.2 (regular xi=1) ==========")
    experiment_fig42_regular()
    print("\n========== Fig 4.3-4.5 (singular xi=2/3, 3/2) ==========")
    experiment_fig43_45_singular()
    print("\n========== Fig 4.6 (omega sweep) ==========")
    experiment_fig46_omega_sweep()
    print("\n========== Conditioning ==========")
    experiment_conditioning()
    print("\nAll experiments complete. See results/paper_*.json")
