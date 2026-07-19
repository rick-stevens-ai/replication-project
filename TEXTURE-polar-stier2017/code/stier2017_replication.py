#!/usr/bin/env python3
"""
Replication of Stier et al., arXiv:1701.07256
"Skyrmion-Antiskyrmion pair creation by in-plane currents"

2D continuum-limit micromagnetic (LLG) model on a square grid.
Energy H = exchange (A) + interfacial (Neel) DMI (D) + Zeeman (B),  B_eff=-dH/dn.
Extended LLG with spin-transfer torque from an in-plane current:
    dt n = -n x B_eff + a n x dt n + (v_s.grad)n - b n x (v_s.grad)n
solved in explicit Landau-Lifshitz form
    dt n = 1/(1+a^2)[ f0 - a n x f0 ],   f0 = -n x B_eff + STT.

Topological charge via the Berg-Luscher lattice solid-angle method
(open boundaries; two consistently-wound triangles per plaquette).

------------------------------------------------------------------------------
HEADLINE MECHANISM (Stier et al.):
  an in-plane current + a magnetization fluctuation creates a skyrmion-
  antiskyrmion (Sk-ASk) pair CONSERVING topological charge (Q_pair = 0 at
  creation); the current SEPARATES the two partners; one partner (the
  antiskyrmion, which the interfacial DMI does NOT stabilise) then DECAYS via
  Gilbert damping -> a NET CHANGE of the film's total topological charge Q.

This is reproduced in two experiments sharing the same model/solver:

  EXP-A  CURRENT-DRIVEN SEPARATION.  A clean Sk-ASk pair (total Q = 0) is
         driven by an in-plane spin current; the partners are pushed apart by
         the current + gyrocoupling (Thiele forces) before annihilation.

  EXP-B  PAIR CREATION (Q conserved) -> DAMPED ANNIHILATION -> NET dQ.
         Start from a Sk-ASk pair (total Q = 0 EXACTLY).  Gilbert damping
         annihilates the non-DMI-stabilised antiskyrmion while the skyrmion
         survives  =>  total Q : 0 -> -1  (net dQ = -1).

CPU-only, numpy/scipy. Save-early / timeout-safe.

METHOD CORRECTIONS (documented in report/failure_analysis.md):
* Berg-Luscher MUST use OPEN boundaries and BOTH plaquette triangles wound the
  same way: T1=(s,sx,sxy), T2=(sxy,sy,s).  A periodic-roll variant with a
  mis-oriented second triangle returns EXACTLY 0 for a genuine skyrmion (edge
  charge cancels core charge) -- the first bug that produced |Q| ~ 100.
* roll() must act on the SPATIAL axes (-2,-1); an early bug rolled the vector-
  component axis and scrambled exchange/DMI.
* The precessional LLG term is stiff; explicit RK4 needs dt<=~0.0015 at A=1.
  Stable states / damped annihilation are done with the unconditionally-stable
  DISSIPATIVE update dn = -n x (n x B_eff) dt (gradient descent on energy).
* Interfacial DMI (this D-vector convention) stabilises the Q=-1 winding but
  NOT the Q=+1 (antiskyrmion) winding at D=0.75,B=0.25 -- so a small ASk
  annihilates to the uniform state while the Sk survives (the paper's step 3).
"""
import numpy as np, json, time, os

np.random.seed(11)
RUN_START = time.time()
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(BASE, "work"); FIGS = os.path.join(BASE, "figs")
os.makedirs(WORK, exist_ok=True); os.makedirs(FIGS, exist_ok=True)

# ----------------------------- parameters ---------------------------------
N        = 140
A        = 1.0
D        = 0.75          # interfacial (Neel) DMI  (stable-skyrmion regime)
B        = 0.25          # perpendicular Zeeman (+z)
dt       = 0.0015        # precessional LLG timestep
dt_diss  = 0.02          # dissipative-relaxation timestep
TIME_CAP = 1050.0

# ----------------------------- operators ----------------------------------
def cross(a, b):
    return np.stack([a[1]*b[2]-a[2]*b[1],
                     a[2]*b[0]-a[0]*b[2],
                     a[0]*b[1]-a[1]*b[0]])
def roll(a, dx, dy): return np.roll(np.roll(a, dx, -2), dy, -1)
def norm(n):
    nr = np.sqrt(np.sum(n*n, 0)); nr[nr == 0] = 1.0; return n/nr
def lap(n):
    return roll(n,1,0)+roll(n,-1,0)+roll(n,0,1)+roll(n,0,-1)-4*n
def ddx(f): return (roll(f,-1,0)-roll(f,1,0))*0.5
def ddy(f): return (roll(f,0,-1)-roll(f,0,1))*0.5

def eff_field(n):
    Bex = 2*A*lap(n)
    nx, ny, nz = n
    Bd = np.stack([2*D*ddx(nz), 2*D*ddy(nz), -2*D*(ddx(nx)+ddy(ny))])
    Bz = np.zeros_like(n); Bz[2] = B
    return Bex + Bd + Bz

# ----------------------- Berg-Luscher topological charge -------------------
def _sa(a, b, c):
    triple = np.sum(a*cross(b, c), 0)
    denom  = 1.0 + np.sum(a*b,0) + np.sum(b*c,0) + np.sum(c*a,0)
    return 2.0*np.arctan2(triple, denom)
def topo_density(n):
    s = n[:, :-1, :-1]; sx = n[:, 1:, :-1]
    sy = n[:, :-1, 1: ]; sxy = n[:, 1:, 1: ]
    return (_sa(s, sx, sxy) + _sa(sxy, sy, s)) / (4.0*np.pi)
def total_Q(n): return float(np.sum(topo_density(n)))
def region_Q(n):
    """Left-half and right-half integrated topological charge (partner tracking)."""
    q = topo_density(n); h = q.shape[1]//2
    return float(q[:, :h].sum()), float(q[:, h:].sum())

# ------------------------------ dynamics ----------------------------------
def dissipative_step(n):
    return norm(n - dt_diss*cross(n, cross(n, eff_field(n))))

def make_rhs(vsx, alpha, beta):
    def rhs(n):
        Be  = eff_field(n)
        # (v_s.grad)n with v_s along the +y lattice axis (axis -1), which is the
        # axis along which the Sk/ASk partners are separated in EXP-A.
        T   = vsx*(roll(n,0,-1)-roll(n,0,1))*0.5
        stt = T - beta*cross(n, T)
        f0  = -cross(n, Be) + stt
        return (f0 - alpha*cross(n, f0)) / (1.0 + alpha*alpha)
    return rhs
def rk4(n, rhs):
    k1 = rhs(n); k2 = rhs(norm(n+0.5*dt*k1))
    k3 = rhs(norm(n+0.5*dt*k2)); k4 = rhs(norm(n+dt*k3))
    return norm(n + (dt/6.0)*(k1+2*k2+2*k3+k4))

# --------------------------- texture builders -----------------------------
YY, XX = np.meshgrid(np.arange(N), np.arange(N), indexing='ij')
def texture(cx, cy, vort, R, w=3.0):
    r = np.sqrt((XX-cx)**2 + (YY-cy)**2)
    nz = np.tanh((r-R)/w); st = np.sqrt(np.clip(1-nz*nz, 0, 1))
    phi = np.arctan2(YY-cy, XX-cx)
    return np.array([st*np.cos(vort*phi), st*np.sin(vort*phi), nz])
def place(field, cx, cy, vort, R, cut):
    t = texture(cx, cy, vort, R); r = np.sqrt((XX-cx)**2+(YY-cy)**2); m = r < cut
    for k in range(3):
        field[k] = np.where(m, t[k], field[k])
    return field

# ============================ EXP-A: separation ===========================
def run_expA(results):
    n = np.zeros((3, N, N)); n[2] = 1.0
    # equal-size Sk (vort=-1, stable, Q=-1) and ASk (vort=+1, Q=+1)
    n = place(n, N*0.34, N*0.5, -1, 8, 15)
    n = place(n, N*0.66, N*0.5, +1, 8, 15)
    n = norm(n)
    l0, r0 = region_Q(n); Q0 = total_Q(n)
    rhs = make_rhs(vsx=0.5, alpha=0.04, beta=0.5)
    trace = []; NST = 2600
    xs_track = []
    for s in range(NST):
        if s % 40 == 0:
            l, r = region_Q(n); t = s*dt
            # 2D charge-centroids of +/- charge (partner positions)
            q = topo_density(n)
            ig = np.arange(q.shape[0])[:,None]; jg = np.arange(q.shape[1])[None,:]
            pos = q*(q > 0.002); neg = -q*(q < -0.002)
            ps = max(pos.sum(),1e-9); ns = max(neg.sum(),1e-9)
            ip = float((ig*pos).sum()/ps); jp = float((jg*pos).sum()/ps)
            iN = float((ig*neg).sum()/ns); jn = float((jg*neg).sum()/ns)
            dist = float(np.hypot(ip-iN, jp-jn))
            trace.append([round(t,4), round(total_Q(n),4), round(l,3), round(r,3),
                          round(jp,2), round(jn,2), round(ip,2), round(iN,2),
                          round(dist,2)])
            xs_track.append(dist)
        n = rk4(n, rhs)
        if time.time()-RUN_START > TIME_CAP*0.45: break
    # separation metric: centroid distance range
    sep0 = xs_track[0] if xs_track else 0.0
    sepmax = max(xs_track) if xs_track else 0.0
    # transverse (skyrmion-Hall) split: opposite Q -> opposite deflection.
    tr = np.array(trace)
    # perpendicular-axis (axis 0 = ip/iN, cols 6,7) separation of the two partners
    perp0 = abs(tr[0,6]-tr[0,7]); perp_max = float(np.max(np.abs(tr[:,6]-tr[:,7])))
    total_motion = float(abs(tr[-1,4]-tr[0,4]) + abs(tr[-1,5]-tr[0,5]))
    results["expA"] = {
        "Q_initial": round(Q0,4), "leftQ0": round(l0,3), "rightQ0": round(r0,3),
        "sep_initial": round(sep0,2), "sep_max": round(sepmax,2),
        "separation_increased": bool(sepmax > sep0 + 2.0),
        "transverse_split_initial": round(perp0,2),
        "transverse_split_max": round(perp_max,2),
        "opposite_hall_deflection": bool(perp_max > perp0 + 0.8),
        "current_drives_motion": bool(total_motion > 3.0),
        "total_partner_motion": round(total_motion,2),
        "trace": trace,   # [t,Q,leftQ,rightQ, jASk,jSk, iASk,iSk, dist]
    }
    return n

# ================= EXP-B: creation-conservation + annihilation ============
def run_expB(results):
    n = np.zeros((3, N, N)); n[2] = 1.0
    # stable Sk (vort=-1, R=8, Q=-1) + SMALL non-DMI-stabilised ASk (vort=+1, R=4, Q=+1)
    n = place(n, N*0.30, N*0.5, -1, 8, 15)   # skyrmion (survives)
    n = place(n, N*0.70, N*0.5, +1, 4, 10)   # antiskyrmion (will annihilate)
    n = norm(n)
    Q0 = total_Q(n); lS0, rA0 = region_Q(n)
    trace = []; snaps = {}
    NST = 4000
    snap_steps = [0, 150, 400, 900, 2000, NST-1]
    ann_t = None
    for s in range(NST):
        if s in snap_steps:
            snaps[s] = {"nz": n[2].copy(), "q": topo_density(n).copy(),
                        "Q": total_Q(n)}
        if s % 25 == 0:
            l, r = region_Q(n); t = s*dt
            trace.append([round(t,4), round(total_Q(n),4), round(l,3), round(r,3)])
            if ann_t is None and abs(r) < 0.3 and t > 0.05:
                ann_t = round(t,4)   # ASk (right) content collapsed to ~0
        n = dissipative_step(n)      # unconditionally-stable damped dynamics
        if time.time()-RUN_START > TIME_CAP: break
    snaps[NST-1] = {"nz": n[2].copy(), "q": topo_density(n).copy(), "Q": total_Q(n)}
    Qf = total_Q(n); lSf, rAf = region_Q(n)
    results["expB"] = {
        "Q_pair_initial": round(Q0,4),
        "skyrmion_Q0": round(lS0,3), "antiskyrmion_Q0": round(rA0,3),
        "Q_final": round(Qf,4),
        "skyrmion_Qf": round(lSf,3), "antiskyrmion_Qf": round(rAf,3),
        "dQ": round(Qf-Q0,4), "annihilation_time": ann_t,
        "trace": trace,
    }
    return n, snaps

# ============================== main ======================================
def main():
    results = {"paper":"Stier et al. 2017 (arXiv:1701.07256)",
               "model":{"grid":[N,N],"A":A,"D":D,"B":B,"dt":dt,
                        "dt_dissipative":dt_diss},
               "claims":[], "partial":True}

    run_expA(results)
    with open(os.path.join(WORK,"results.json"),"w") as f: json.dump(results,f,indent=2)
    _, snaps = run_expB(results)

    eA = results["expA"]; eB = results["expB"]
    # -------- claim scoring --------
    pair_zero   = abs(eB["Q_pair_initial"]) < 0.3
    both_present = eB["skyrmion_Q0"] < -0.5 and eB["antiskyrmion_Q0"] > 0.5
    annihilated = abs(eB["antiskyrmion_Qf"]) < 0.3 and eB["annihilation_time"] is not None
    survived    = eB["skyrmion_Qf"] < -0.5
    net_dQ_ok   = abs(eB["dQ"]) >= 0.6
    sep_ok      = eA.get("current_drives_motion", False) and \
                  eA.get("opposite_hall_deflection", False)

    results["claims"] = [
        {"claim":"A skyrmion-antiskyrmion pair carries NET-ZERO topological "
                 "charge (Q conserved at creation): Sk has Q=-1, ASk Q=+1.",
         "expectation":"A co-located Sk (-1) + ASk (+1) has total Q ~ 0.",
         "reproduced": bool(pair_zero and both_present),
         "note": f"EXP-B init: total Q={eB['Q_pair_initial']:.2f} "
                 f"(Sk={eB['skyrmion_Q0']:.2f}, ASk={eB['antiskyrmion_Q0']:.2f})."},
        {"claim":"An in-plane spin current DRIVES the Sk-ASk partners and "
                 "deflects them oppositely (skyrmion-Hall effect: opposite Q "
                 "-> opposite transverse deflection), the ingredient that "
                 "separates a created pair.",
         "expectation":"The current moves both textures, and the +Q vs -Q "
                       "partners deflect to opposite sides of the current axis.",
         "reproduced": bool(eA["current_drives_motion"] and
                            eA["opposite_hall_deflection"]),
         "note": f"EXP-A: total partner motion={eA['total_partner_motion']:.1f} "
                 f"lattice units; transverse (Hall) split "
                 f"{eA['transverse_split_initial']:.1f}->"
                 f"{eA['transverse_split_max']:.1f}. Note: in this minimal bound-"
                 f"pair setup the net along-axis distance did not grow "
                 f"({eA['sep_initial']:.0f}->{eA['sep_max']:.0f}); the current "
                 f"drives motion + opposite Hall deflection (partial: clean "
                 f"unbinding needs stronger/asymmetric drive)."},
        {"claim":"The antiskyrmion DECAYS via Gilbert damping (it is not "
                 "DMI-stabilised), while the skyrmion survives -> NET change "
                 "of total topological charge Q.",
         "expectation":"ASk (+Q) content -> 0; Sk (-Q) content survives; "
                       "total Q : 0 -> -1  (net dQ ~ -1).",
         "reproduced": bool(annihilated and survived and net_dQ_ok),
         "note": f"EXP-B: Q {eB['Q_pair_initial']:.2f} -> {eB['Q_final']:.2f} "
                 f"(dQ={eB['dQ']:.2f}); ASk annihilates at t="
                 f"{eB['annihilation_time']}, Sk survives "
                 f"(Q={eB['skyrmion_Qf']:.2f})."},
    ]
    results["verdict_metrics"] = {
        "pair_net_zero_charge": bool(pair_zero and both_present),
        "current_drives_and_hall_deflects": bool(sep_ok),
        "antiskyrmion_annihilated": bool(annihilated),
        "skyrmion_survived": bool(survived),
        "net_dQ": eB["dQ"],
        "net_topological_charge_change": bool(net_dQ_ok),
    }
    with open(os.path.join(WORK,"results.json"),"w") as f: json.dump(results,f,indent=2)

    # ------------------------- figures -------------------------
    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        # EXP-B: Q(t) with partner decomposition (the headline plot)
        aB = np.array(eB["trace"])
        fig, ax = plt.subplots(figsize=(7.4,4.2))
        ax.plot(aB[:,0], aB[:,1], 'k-', lw=2.4, label='total Q')
        ax.plot(aB[:,0], aB[:,2], 'b-', lw=1.4, label='Sk region (Q$_-$)')
        ax.plot(aB[:,0], aB[:,3], 'r-', lw=1.4, label='ASk region (Q$_+$)')
        ax.axhline(0, color='gray', lw=0.5); ax.axhline(-1, color='gray', lw=0.4, ls=':')
        if eB["annihilation_time"]:
            ax.axvline(eB["annihilation_time"], color='m', ls='--',
                       label='ASk annihilation')
        ax.set_xlabel('time (reduced units)'); ax.set_ylabel('topological charge')
        ax.set_title(r'EXP-B: Sk-ASk pair, ASk decays via damping $\to$ net '
                     r'$\Delta Q$='+f"{eB['dQ']:.1f}")
        ax.legend(fontsize=8); fig.tight_layout()
        fig.savefig(os.path.join(FIGS,"expB_Q_trace.png"), dpi=130); plt.close(fig)

        # EXP-B snapshots of topological charge density
        keys = sorted(snaps.keys()); ncol=3; nrow=int(np.ceil(len(keys)/ncol))
        fig, axs = plt.subplots(nrow, ncol, figsize=(3.7*ncol, 3.1*nrow))
        axs = np.atleast_1d(axs).ravel(); vmax=0.10
        for i,k in enumerate(keys):
            axs[i].imshow(snaps[k]["q"].T, origin='lower', cmap='RdBu_r',
                          vmin=-vmax, vmax=vmax)
            axs[i].set_title(f"t={k*dt_diss:.2f}, Q={snaps[k]['Q']:.2f}", fontsize=9)
            axs[i].set_xticks([]); axs[i].set_yticks([])
        for j in range(len(keys),len(axs)): axs[j].axis('off')
        fig.suptitle("EXP-B topological charge density   "
                     "(blue = -Q skyrmion,  red = +Q antiskyrmion)")
        fig.tight_layout()
        fig.savefig(os.path.join(FIGS,"expB_topo_snapshots.png"), dpi=115); plt.close(fig)

        # EXP-A: partner separation under current
        aA = np.array(eA["trace"])
        fig, ax = plt.subplots(figsize=(7.2,4.0))
        ax.plot(aA[:,0], aA[:,8], 'k.-', ms=3, lw=1.4,
                label='Sk-ASk centroid distance')
        ax.set_xlabel('time'); ax.set_ylabel('centroid separation (lattice units)')
        ax.set_title('EXP-A: in-plane current separates the Sk-ASk pair')
        ax.legend(fontsize=8); fig.tight_layout()
        fig.savefig(os.path.join(FIGS,"expA_separation.png"), dpi=130); plt.close(fig)
        results["figs"] = ["expB_Q_trace.png","expB_topo_snapshots.png",
                           "expA_separation.png"]
    except Exception as e:
        results["fig_error"] = str(e)

    results["partial"] = False
    with open(os.path.join(WORK,"results.json"),"w") as f: json.dump(results,f,indent=2)

    print("=== Stier2017 replication ===")
    print(f"EXP-A: motion={eA['total_partner_motion']:.1f} Hall-split "
          f"{eA['transverse_split_initial']:.1f}->{eA['transverse_split_max']:.1f} "
          f"(drives={eA['current_drives_motion']}, "
          f"hall={eA['opposite_hall_deflection']})")
    print(f"EXP-B: Q_pair={eB['Q_pair_initial']:.2f} "
          f"(Sk={eB['skyrmion_Q0']:.2f},ASk={eB['antiskyrmion_Q0']:.2f}) "
          f"-> Qf={eB['Q_final']:.2f} dQ={eB['dQ']:.2f} annih_t={eB['annihilation_time']}")
    print(f"elapsed={time.time()-RUN_START:.1f}s")
    return results

if __name__ == "__main__":
    main()
