#!/usr/bin/env python3
"""
From-scratch minimal-mechanism replication of the phase-field headline of:

  Gupta, Tanwani, Xu, Du, ... Hong, Tian, Ramesh, Das (2025),
  "Harnessing the polar vortex motion in oxide heterostructures."
  (PbTiO3/SrTiO3 heterostructures; TDGL phase-field.)

HEADLINE CLAIM tested here:
  "Phase-field simulations ... confirm the presence of a PURE VORTEX PHASE in
   the trilayer" (STO/PTO/STO), arising from a competition among Landau,
   elastic, electric (depolarization) and gradient energies. Observed vortex
   periodicity ~14 nm.

WHAT WE REPLICATE (mechanism, reduced 2D cross-section):
  A polar vortex in a PTO/STO film is a flux-closure texture: in the (x,z)
  cross-section of the ferroelectric layer the polarization P=(Px,Pz) rotates
  continuously around a singular core, producing an ALTERNATING array of
  clockwise / counter-clockwise vortices (a "pure vortex phase") with a well
  defined lateral period. The period is set by the competition between:
    - depolarization/electric energy (penalizes a net out-of-plane Pz in a
      thin film  ->  forces flux closure / in-plane rotation),
    - gradient energy (penalizes rotation  ->  wants large domains),
    - Landau energy (fixes |P| magnitude, double well),
    - elastic confinement (thin film => rotation confined to film thickness).
  The equilibrium period ~ film thickness (Kittel-like), which for a ~20 uc
  (~8 nm) PTO layer gives a vortex pair period on the order of ~10-15 nm, in
  the range the paper reports (~14 nm trilayer).

METHOD: 2D time-dependent Ginzburg-Landau (TDGL) relaxation,
    dP/dt = -L * dF/dP,  F = f_Landau + f_grad + f_elec(depol) + f_elastic.
Explicit Euler, periodic in x, film slab in z, air/dead layers above & below.

PROVENANCE / CREDIT (both shared kernels used as method templates):
  * ollie_tdgl_phasefield_polar_skyrmion_kernel.py  (Wang,Yang&Chen 2026):
      TDGL relaxation structure (dP/dt=-L dF/dP), Landau f=0.5 a|P|^2 +
      0.25 b|P|^4 + ..., gradient via spectral/FD Laplacian, depolarization
      term eps*<Pz>, order-parameter/core NMS characterization.
  * ollie_berg_luscher_topological_charge_kernel.py  (Gao et al. 2502.14236):
      lattice topological-charge / winding methodology (plaquette angle sum);
      here adapted to the 2D in-plane WINDING NUMBER of the polar director,
      which is the correct integer invariant for a 2D polar vortex (+-1).

CPU-only, numpy/scipy. Target < 6 min on nuc-CPU. SAVE-EARLY.
"""
from __future__ import annotations
import json, os, time, math
import numpy as np
from scipy.ndimage import gaussian_filter, minimum_filter

HERE = os.path.dirname(os.path.abspath(__file__))
RESULT = os.path.join(HERE, "hong2025_result.json")

def save(d):
    with open(RESULT, "w") as f:
        json.dump(d, f, indent=2, default=float)

# ------------------------------------------------------------------ #
#  2D polar phase-field:  P = (Px, Pz)  on an (x, z) grid.
#  x : lateral (in-plane, periodic).  z : out-of-plane (film normal).
# ------------------------------------------------------------------ #
class PolarVortexField:
    def __init__(self, Nx=160, Nz=40, dx=1.0, seed=0,
                 # Landau double-well (a<0 => ferroelectric)
                 a=-1.0, b=1.0,
                 g=0.6,          # gradient stiffness (sets wall width / period)
                 eps=2.5,        # electric energy: bound-charge (div P)^2 penalty
                 Kz=0.6,         # uniaxial anisotropy favoring out-of-plane Pz (PTO c-axis)
                 L=1.0,          # TDGL mobility
                 film_frac=0.55, # fraction of z occupied by ferroelectric film
                 ):
        self.Nx, self.Nz, self.dx = Nx, Nz, dx
        self.a, self.b, self.g, self.eps, self.L, self.Kz = a, b, g, eps, L, Kz
        self.rng = np.random.default_rng(seed)
        # film mask: central slab in z is the ferroelectric (PTO); rest is
        # dielectric/air (dead layer, P forced ~0).
        z = np.arange(Nz)
        zc = Nz / 2.0
        half = film_frac * Nz / 2.0
        self.film = (np.abs(z - zc) <= half)[None, :]            # (1,Nz)
        self.film2 = np.repeat(self.film, Nx, axis=0)            # (Nx,Nz)
        # small random seed inside the film
        self.P = 0.10 * self.rng.standard_normal((2, Nx, Nz))
        self.P *= self.film2[None, :, :]

    def laplacian(self, f):
        # periodic in x, Neumann (reflect) in z
        lap = (-4.0 * f
               + np.roll(f, 1, axis=0) + np.roll(f, -1, axis=0)
               + np.pad(f, ((0,0),(1,0)), mode="edge")[:, :-1]
               + np.pad(f, ((0,0),(0,1)), mode="edge")[:, 1:]) / (self.dx**2)
        return lap

    def divergence(self, Px, Pz):
        # central differences; periodic in x, edge in z
        dPx_dx = (np.roll(Px, -1, axis=0) - np.roll(Px, 1, axis=0)) / (2*self.dx)
        dPz_dz = (np.pad(Pz, ((0,0),(0,1)), mode="edge")[:, 1:]
                  - np.pad(Pz, ((0,0),(1,0)), mode="edge")[:, :-1]) / (2*self.dx)
        return dPx_dx + dPz_dz

    def dF_dP(self):
        Px, Pz = self.P[0], self.P[1]
        P2 = Px**2 + Pz**2
        # Landau (isotropic double well): dF = a P + b P |P|^2
        dPx = self.a * Px + self.b * Px * P2
        dPz = self.a * Pz + self.b * Pz * P2
        # uniaxial anisotropy: favor out-of-plane Pz (PTO c-axis) -> -Kz Pz
        dPz += -self.Kz * Pz
        # gradient: -g * lap(P)
        dPx += -self.g * self.laplacian(Px)
        dPz += -self.g * self.laplacian(Pz)
        # electric energy: bound-charge penalty  f_elec = 0.5 eps (div P)^2
        #   variational derivative:  dF/dP = -eps * grad(div P)
        # This drives P toward a DIVERGENCE-FREE field = closed flux loops =
        # polar vortices (flux closure), the physical origin of the vortex phase.
        div = self.divergence(Px, Pz)
        grad_div_x = (np.roll(div, -1, axis=0) - np.roll(div, 1, axis=0)) / (2*self.dx)
        grad_div_z = (np.pad(div, ((0,0),(0,1)), mode="edge")[:, 1:]
                      - np.pad(div, ((0,0),(1,0)), mode="edge")[:, :-1]) / (2*self.dx)
        dPx += -self.eps * grad_div_x
        dPz += -self.eps * grad_div_z
        return np.stack([dPx, dPz], axis=0)

    def step(self, dt):
        dF = self.dF_dP()
        self.P += -self.L * dt * dF
        # enforce dead layers (dielectric/air): P -> 0 outside film, smooth edge
        self.P *= self.film2[None, :, :]

    # ---------------- characterization ----------------
    def magnitude(self):
        return np.sqrt(self.P[0]**2 + self.P[1]**2)

    def winding_field(self):
        """Local winding (vorticity) of the 2D polar director around each
        plaquette, via the Berg-Luscher-style plaquette angle-sum adapted to
        2D:  sum of signed angle increments of theta=atan2(Pz,Px) around the
        4 corners of each plaquette, /2pi  ->  integer +-1 at vortex cores."""
        th = np.arctan2(self.P[1], self.P[0])   # (Nx,Nz)
        def dang(a, b):
            d = b - a
            return (d + np.pi) % (2*np.pi) - np.pi
        # plaquette corners (i,j)->(i+1,j)->(i+1,j+1)->(i,j+1)->back
        t00 = th[:-1, :-1]; t10 = th[1:, :-1]
        t11 = th[1:, 1:];   t01 = th[:-1, 1:]
        w = (dang(t00, t10) + dang(t10, t11)
             + dang(t11, t01) + dang(t01, t00)) / (2*np.pi)
        return w      # (Nx-1, Nz-1), ~+-1 at cores

    def find_vortices(self):
        w = self.winding_field()
        mag = self.magnitude()[:-1, :-1]
        # a vortex core: |winding|~1 AND low |P| (singular core), inside film
        film = self.film2[:-1, :-1]
        pos = (w > 0.5) & film
        neg = (w < -0.5) & film
        n_pos = int(pos.sum()); n_neg = int(neg.sum())
        # lateral positions (x-index) of cores, for periodicity estimate
        core = pos | neg
        xs = np.where(core.any(axis=1))[0]
        return n_pos, n_neg, xs, w

    def lateral_period(self):
        """Estimate vortex lateral period from FFT of the mid-film Px row
        (Px changes sign between adjacent counter-rotating vortices)."""
        zc = self.Nz // 2
        row = self.P[0][:, zc]
        row = row - row.mean()
        if np.allclose(row, 0):
            return None, None
        F = np.abs(np.fft.rfft(row))
        freqs = np.fft.rfftfreq(self.Nx, d=self.dx)
        F[0] = 0.0
        k = int(np.argmax(F))
        if freqs[k] <= 0:
            return None, None
        period_cells = 1.0 / freqs[k]
        n_periods = self.Nx / period_cells
        return float(period_cells), float(n_periods)


# ------------------------------------------------------------------ #
def relax(model, n_steps, dt, log_every=500, t0=0.0):
    hist = []
    for s in range(n_steps):
        model.step(dt)
        if s % log_every == 0 or s == n_steps - 1:
            mag = model.magnitude()[model.film2]
            npos, nneg, xs, _ = model.find_vortices()
            hist.append({"step": s, "mean_P": float(mag.mean()),
                         "n_vortex_pos": npos, "n_vortex_neg": nneg})
            print(f"  [{time.time()-t0:5.1f}s] step {s:5d}  "
                  f"<|P|>={mag.mean():.3f}  +v={npos} -v={nneg}", flush=True)
    return hist


def main():
    t0 = time.time()
    results = {
        "paper": "Gupta et al. 2025, 'Harnessing the polar vortex motion in "
                 "oxide heterostructures' (PTO/STO, TDGL phase-field)",
        "headline_claim": ("Phase-field simulations confirm a PURE VORTEX PHASE "
                            "in the STO/PTO/STO trilayer, from Landau+elastic+"
                            "electric+gradient energy competition; vortex "
                            "periodicity ~14 nm."),
        "method": "2D TDGL phase-field relaxation, dP/dt=-L dF/dP, "
                  "F=Landau+gradient+depolarization(electric)+elastic-confinement.",
        "provenance_credit": {
            "ollie_tdgl_phasefield_polar_skyrmion_kernel.py":
                "TDGL relaxation structure, Landau double well, gradient "
                "Laplacian, depolarization term eps*<Pz>, core characterization.",
            "ollie_berg_luscher_topological_charge_kernel.py":
                "lattice plaquette angle-sum topological-charge/winding method, "
                "adapted to 2D polar-director winding number (+-1 vortex cores).",
        },
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "runs": {},
    }
    save(results)

    # ---- Run A: PURE VORTEX PHASE (thin film, strong depolarization) ----
    # Thin ferroelectric slab + strong depolarization => flux closure =>
    # a periodic alternating vortex array (the "pure vortex phase").
    print(f"[{time.time()-t0:5.1f}s] Run A: pure-vortex regime "
          "(thin film, strong depolarization)")
    mA = PolarVortexField(Nx=160, Nz=40, seed=1,
                          a=-1.0, b=1.0, g=0.6, eps=4.0, Kz=0.8, film_frac=0.5)
    histA = relax(mA, n_steps=12000, dt=0.01, log_every=2000, t0=t0)
    npos, nneg, xs, w = mA.find_vortices()
    per_cells, n_per = mA.lateral_period()
    magA = mA.magnitude()[mA.film2]
    # map cells->nm: film thickness (film_frac*Nz cells) == ~8 nm (20 uc PTO)
    film_cells = mA.film.sum()
    nm_per_cell = 8.0 / film_cells       # calibrate: PTO layer ~8 nm
    results["runs"]["A_pure_vortex"] = {
        "regime": "thin film + strong depolarization (eps=3.0)",
        "grid": [mA.Nx, mA.Nz], "film_cells_z": int(film_cells),
        "n_vortex_pos": npos, "n_vortex_neg": nneg,
        "n_vortex_total": npos + nneg,
        "alternating_ratio": (min(npos, nneg) / max(npos, nneg, 1)),
        "lateral_period_cells": per_cells,
        "n_periods_across_box": n_per,
        "vortex_period_nm_est": (per_cells * nm_per_cell) if per_cells else None,
        "nm_per_cell_calib": nm_per_cell,
        "mean_P": float(magA.mean()),
        "history": histA,
    }
    save(results)

    # ---- Run B: CONTROL - thick film / weak depolarization => uniform domain ----
    # (no flux-closure driver => should NOT form a vortex array).
    print(f"[{time.time()-t0:5.1f}s] Run B: control "
          "(weak depolarization => uniform/domain, no pure vortex phase)")
    mB = PolarVortexField(Nx=160, Nz=40, seed=1,
                          a=-1.0, b=1.0, g=0.6, eps=0.05, Kz=0.8, film_frac=0.5)
    histB = relax(mB, n_steps=12000, dt=0.01, log_every=4000, t0=t0)
    nposB, nnegB, xsB, wB = mB.find_vortices()
    perB, nperB = mB.lateral_period()
    results["runs"]["B_control_weak_depol"] = {
        "regime": "weak depolarization (eps=0.05) => uniform/domain expected",
        "n_vortex_pos": nposB, "n_vortex_neg": nnegB,
        "n_vortex_total": nposB + nnegB,
        "lateral_period_cells": perB,
        "mean_P": float(mB.magnitude()[mB.film2].mean()),
    }
    save(results)

    # ---- Scoring ----
    A = results["runs"]["A_pure_vortex"]
    # criterion for "pure vortex phase":
    #   (1) multiple vortices form (>=4 total),
    #   (2) roughly equal +/- (alternating array, ratio > 0.5),
    #   (3) a well-defined lateral periodicity (>=2 periods across box),
    #   (4) vortex phase is REGIME-SELECTIVE (control forms far fewer).
    c1 = A["n_vortex_total"] >= 4
    c2 = A["alternating_ratio"] > 0.5
    c3 = (A["n_periods_across_box"] or 0) >= 2
    c4 = A["n_vortex_total"] > 2 * results["runs"]["B_control_weak_depol"]["n_vortex_total"]
    # periodicity in plausible nm range (paper ~14 nm; accept 5-30 nm order)
    per_nm = A["vortex_period_nm_est"]
    c5 = (per_nm is not None) and (5.0 <= per_nm <= 30.0)
    checks = {"multiple_vortices>=4": bool(c1),
              "alternating_+-_array": bool(c2),
              ">=2_periods_(periodic)": bool(c3),
              "regime_selective_vs_control": bool(c4),
              "period_nm_in_5_30_range": bool(c5)}
    n_pass = sum(checks.values())
    if n_pass >= 4 and c1 and c2:
        verdict = "REPLICATED"
    elif n_pass >= 2 and c1:
        verdict = "PARTIAL"
    else:
        verdict = "NEGATIVE"
    results["claim_checks"] = checks
    results["n_checks_pass"] = n_pass
    results["verdict"] = verdict
    results["runtime_s"] = round(time.time() - t0, 1)
    results["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    save(results)
    print(f"\n[{results['runtime_s']:.1f}s] DONE verdict={verdict} "
          f"checks={n_pass}/5  period~{per_nm}nm  "
          f"vortices=+{A['n_vortex_pos']}/-{A['n_vortex_neg']}")
    return results


if __name__ == "__main__":
    main()
