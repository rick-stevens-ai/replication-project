#!/usr/bin/env python3
"""
Wang, Yang & Chen (2026) — arXiv:2604.26100
"Hidden Crossover and Relaxor-Like Response from Emerging Polar Skyrmion
Correlations in Ferroelectric Superlattices."

Minimal-mechanism replication (CPU, numpy/scipy).

Model
-----
Two coupled 2D layers, each with a 3-component polarization P=(Px,Py,Pz).
The Landau free energy (per site) is:

    f_L  = 0.5*a(T)*|P|^2 + 0.25*b*|P|^4 + (1/6)*c*|P|^6
           - K_z * Pz^2                (easy z-axis so Bloch cores are stable)
    f_G  = 0.5*g * sum_i |grad P_i|^2  (gradient / stiffness)
    f_E  = 0.5*eps * <Pz>^2  per layer (depolarization: penalize uniform Pz)
    f_int = -J * <P^(1).P^(2)>         (WEAK interlayer coupling, per site)
    a(T) = a0*(T - T0)                 (a<0 ferroelectric, a>0 paraelectric)

TDGL:  dP/dt = -L*(dF/dP) + sqrt(2*L*kT/dt)*eta

Interlayer correlation
    C(T) = Pearson correlation of the Gaussian-smoothed skyrmion-core
           density fields between the two layers (grows toward 1 when cores
           align vertically).

Susceptibility (CLAIM 2) from fluctuation-dissipation:
    chi(T) = V * Var(<Pz>) / kT           (V = N*N, per layer, averaged)

CLAIM 3 (stretch) uses AC field E(t)=E0*cos(w t) coupling to Pz.

Deliberately reduced: 2 layers x 32x32 for the temperature sweep + short chains.
The paper's 3D superlattice is out of scope; we only test the MECHANISM
signatures: correlation growth on cooling + broad chi(T) peak + direction of
AC-frequency dispersion.
"""
from __future__ import annotations
import json, os, time, math
import numpy as np
from numpy.fft import fft2, ifft2, fftfreq
from scipy.ndimage import gaussian_filter, maximum_filter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WORK = os.path.join(ROOT, "work")
FIGS = os.path.join(ROOT, "figs")
os.makedirs(WORK, exist_ok=True)
os.makedirs(FIGS, exist_ok=True)

def save_results(results):
    with open(os.path.join(WORK, "results.json"), "w") as f:
        json.dump(results, f, indent=2, default=float)

# ------------------------------------------------------------------ #
class Skyrmion2Layer:
    def __init__(self, N=32, dx=1.0, seed=0,
                 a0=1.0, T0=0.9, b=1.0, c=0.5,
                 K_z=0.35, g=1.2, eps=0.6, J=0.05, L=1.0):
        # NB: J is now WEAK so interlayer alignment is a T-dependent effect,
        # not enforced from the start.
        self.N = N; self.dx = dx
        self.a0 = a0; self.T0 = T0; self.b = b; self.c = c
        self.K_z = K_z; self.g = g; self.eps = eps; self.J = J
        self.L = L
        self.rng = np.random.default_rng(seed)
        kx = 2*np.pi*fftfreq(N, d=dx); ky = 2*np.pi*fftfreq(N, d=dx)
        KX, KY = np.meshgrid(kx, ky, indexing="ij")
        self.k2 = KX**2 + KY**2
        self.P = 0.05 * self.rng.standard_normal((2, 3, N, N))

    def seed_skyrmions(self, n_per_layer=3, radius=4.0, chirality=+1):
        N = self.N
        for L in range(2):
            for _ in range(n_per_layer):
                cx = self.rng.uniform(0, N); cy = self.rng.uniform(0, N)
                xx, yy = np.meshgrid(np.arange(N), np.arange(N), indexing="ij")
                dx = ((xx - cx + N/2) % N) - N/2
                dy = ((yy - cy + N/2) % N) - N/2
                r = np.sqrt(dx**2 + dy**2) + 1e-6
                theta = np.arctan2(dy, dx)
                profile = np.tanh((r - radius) / 1.5)
                self.P[L, 2] += -profile
                self.P[L, 0] +=  0.6*(1-profile**2) * (-np.sin(theta)*chirality)
                self.P[L, 1] +=  0.6*(1-profile**2) * ( np.cos(theta)*chirality)

    def laplacian(self, f):
        F = fft2(f)
        return np.real(ifft2(-self.k2 * F))

    def dF_dP(self, T, E_z=0.0):
        a = self.a0 * (T - self.T0)
        P = self.P
        P2 = np.sum(P**2, axis=1, keepdims=True)
        dF = a*P + self.b*P*P2 + self.c*P*P2*P2
        dF[:, 2] += -2*self.K_z * P[:, 2]
        for Li in range(2):
            for ci in range(3):
                dF[Li, ci] += -self.g * self.laplacian(P[Li, ci])
        dF[0] += -self.J * P[1]
        dF[1] += -self.J * P[0]
        Pz_mean = P[:, 2].mean(axis=(1,2), keepdims=True)
        dF[:, 2] += self.eps * Pz_mean
        if E_z != 0.0:
            dF[:, 2] += -E_z
        return dF

    def step(self, T, dt, E_z=0.0, kT_noise=0.0):
        dF = self.dF_dP(T, E_z=E_z)
        self.P += -self.L * dt * dF
        if kT_noise > 0.0:
            sigma = math.sqrt(2.0 * self.L * kT_noise * dt)
            self.P += sigma * self.rng.standard_normal(self.P.shape)

    def pz_mean_per_layer(self):
        return self.P[:, 2].mean(axis=(1,2))  # (2,)

    def core_field(self, layer, sigma=2.0):
        """Bloch-core intensity field: high where Pz is deep-down and the
        in-plane polarization is large (skyrmion-like winding). Smoothed."""
        pz = self.P[layer, 2]
        pxy = np.sqrt(self.P[layer,0]**2 + self.P[layer,1]**2)
        # score = |P_xy| * relu(-Pz)   (only Pz-down places matter)
        core = pxy * np.clip(-pz, 0, None)
        return gaussian_filter(core, sigma=sigma, mode="wrap")

    def interlayer_correlation(self):
        a = self.core_field(0); b = self.core_field(1)
        a = a - a.mean(); b = b - b.mean()
        den = math.sqrt((a*a).sum() * (b*b).sum()) + 1e-12
        return float((a*b).sum() / den)

    def count_skyrmions(self, layer):
        """Count NMS local maxima of the smoothed core field above threshold."""
        c = self.core_field(layer, sigma=2.0)
        thr = c.mean() + 0.8 * c.std()
        mx = maximum_filter(c, size=5, mode="wrap")
        peaks = (c == mx) & (c > thr)
        return int(peaks.sum())

# ------------------------------------------------------------------ #
def equilibrate(model, T, n_steps, dt, kT_noise, E_z=0.0):
    for _ in range(n_steps):
        model.step(T, dt, E_z=E_z, kT_noise=kT_noise)

def measure_at_T(model, T, n_eq, n_meas, dt, kT_noise, sample_every=1):
    equilibrate(model, T, n_eq, dt, kT_noise)
    pz_series = []; corr_series = []; nsky_series = []
    for i in range(n_meas):
        model.step(T, dt, kT_noise=kT_noise)
        if i % sample_every == 0:
            # average of layer-mean Pz => scalar order-parameter fluctuation
            pz_series.append(float(model.pz_mean_per_layer().mean()))
            corr_series.append(model.interlayer_correlation())
            nsky_series.append(model.count_skyrmions(0) + model.count_skyrmions(1))
    pz_arr = np.array(pz_series)
    # V per layer = N*N; use per-layer volume for chi
    V = model.N * model.N
    var_pz = float(pz_arr.var())
    chi = V * var_pz / max(kT_noise, 1e-6)
    return {
        "chi_fluct": chi,
        "var_pz":    var_pz,
        "corr_mean": float(np.mean(corr_series)),
        "corr_std":  float(np.std(corr_series)),
        "pz_mean":   float(pz_arr.mean()),
        "n_sky_mean":float(np.mean(nsky_series)),
    }

def run_temperature_sweep(Ts, N=32, seed=1, dt=0.02, n_eq=1200, n_meas=1500,
                          kT_scale=0.03, sample_every=1, verbose=True):
    model = Skyrmion2Layer(N=N, seed=seed, J=0.05)
    model.seed_skyrmions(n_per_layer=3, radius=4.0)
    # long anneal at the highest T
    equilibrate(model, T=Ts[0], n_steps=600, dt=dt, kT_noise=kT_scale*Ts[0])
    out = []
    for T in Ts:
        kT = kT_scale * T
        m = measure_at_T(model, T=T, n_eq=n_eq, n_meas=n_meas,
                         dt=dt, kT_noise=kT, sample_every=sample_every)
        m["T"] = float(T); m["kT_noise"] = float(kT)
        out.append(m)
        if verbose:
            print(f"  T={T:.3f}  chi={m['chi_fluct']:.3g}  "
                  f"corr={m['corr_mean']:+.3f}  Nsky={m['n_sky_mean']:.1f}  "
                  f"Pz={m['pz_mean']:+.3f}", flush=True)
    return out, model

# ------------------------------------------------------------------ #
def run_ac_susceptibility(Ts, omegas, N=32, seed=2, dt=0.02,
                          n_eq=500, n_cycles=5, E0=0.03, kT_scale=0.03):
    results = {"omegas": list(omegas), "Ts": list(Ts), "chi_ac": []}
    for om in omegas:
        row = []
        model = Skyrmion2Layer(N=N, seed=seed, J=0.05)
        model.seed_skyrmions(n_per_layer=3)
        equilibrate(model, T=Ts[0], n_steps=400, dt=dt, kT_noise=kT_scale*Ts[0])
        for T in Ts:
            kT = kT_scale * T
            equilibrate(model, T=T, n_steps=n_eq, dt=dt, kT_noise=kT)
            period = 2*math.pi/om
            n_steps = max(50, int(round(n_cycles * period / dt)))
            Pz = np.zeros(n_steps); cs = np.zeros(n_steps); sn = np.zeros(n_steps)
            for i in range(n_steps):
                t = i*dt
                Ez = E0 * math.cos(om * t)
                model.step(T, dt, E_z=Ez, kT_noise=kT)
                Pz[i] = float(model.pz_mean_per_layer().mean())
                cs[i] = math.cos(om*t); sn[i] = math.sin(om*t)
            skip = min(int(round(period/dt)), n_steps//2)
            Pz = Pz[skip:]; cs = cs[skip:]; sn = sn[skip:]
            chi_prime  =  2.0 * np.mean(Pz * cs) / E0
            chi_dprime = -2.0 * np.mean(Pz * sn) / E0
            row.append({"T": float(T), "chi_prime": float(chi_prime),
                        "chi_dprime": float(chi_dprime)})
            print(f"    om={om:.3f}  T={T:.3f}  chi'={chi_prime:+.3g}  "
                  f"chi''={chi_dprime:+.3g}", flush=True)
        results["chi_ac"].append(row)
    return results

# ------------------------------------------------------------------ #
def make_plots(sweep, model_final, ac=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    Ts   = np.array([m["T"] for m in sweep])
    chi  = np.array([m["chi_fluct"] for m in sweep])
    corr = np.array([m["corr_mean"] for m in sweep])
    err  = np.array([m["corr_std"]  for m in sweep])
    nsky = np.array([m["n_sky_mean"] for m in sweep])

    fig, ax = plt.subplots(figsize=(5.2,3.6))
    ax.plot(Ts, chi, "o-", color="C3")
    ax.set_xlabel("Temperature T (arb. units)")
    ax.set_ylabel(r"$\chi_{zz}\ \sim\ V\,\mathrm{Var}(\bar P_z)/k_BT$")
    ax.set_title("CLAIM 2: dielectric susceptibility vs T")
    ax.grid(alpha=0.3); fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "chi_vs_T.png"), dpi=140); plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.2,3.6))
    ax.errorbar(Ts, corr, yerr=err, fmt="s-", color="C0", capsize=3)
    ax.axhline(0, color="k", lw=0.6, alpha=0.4)
    ax.set_xlabel("Temperature T (arb. units)")
    ax.set_ylabel("Interlayer correlation of skyrmion-core density")
    ax.set_title("CLAIM 1: interlayer correlation grows on cooling")
    ax.grid(alpha=0.3); fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "corr_vs_T.png"), dpi=140); plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(8, 3.8))
    for L, ax in enumerate(axes):
        pz = model_final.P[L, 2]
        px = model_final.P[L, 0]; py = model_final.P[L, 1]
        im = ax.imshow(pz.T, origin="lower", cmap="RdBu_r",
                       vmin=-abs(pz).max(), vmax=abs(pz).max())
        step = max(1, model_final.N // 12)
        xs, ys = np.meshgrid(np.arange(0, model_final.N, step),
                             np.arange(0, model_final.N, step), indexing="ij")
        ax.quiver(xs, ys, px[::step, ::step], py[::step, ::step],
                  color="k", scale=15, width=0.006)
        ax.set_title(f"Layer {L+1}: $P_z$ + $(P_x,P_y)$")
        ax.set_xticks([]); ax.set_yticks([])
        fig.colorbar(im, ax=ax, shrink=0.85, label=r"$P_z$")
    fig.suptitle(f"Skyrmion snapshot at final T={sweep[-1]['T']:.2f}")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "skyrmion_snapshot.png"), dpi=140)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(5.2,3.4))
    ax.plot(Ts, nsky, "^-", color="C2")
    ax.set_xlabel("T"); ax.set_ylabel("mean total NMS core count (both layers)")
    ax.set_title("Skyrmion population vs T (informational)")
    ax.grid(alpha=0.3); fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "nsky_vs_T.png"), dpi=140); plt.close(fig)

    if ac is not None:
        fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.6))
        colors = ["C4","C1","C6","C2"]
        for i, om in enumerate(ac["omegas"]):
            row = ac["chi_ac"][i]
            Ts_ac = [r["T"] for r in row]
            xp    = [r["chi_prime"]  for r in row]
            xpp   = [r["chi_dprime"] for r in row]
            axes[0].plot(Ts_ac, xp,  "o-", color=colors[i%len(colors)],
                         label=f"$\\omega$={om:.2f}")
            axes[1].plot(Ts_ac, xpp, "s-", color=colors[i%len(colors)],
                         label=f"$\\omega$={om:.2f}")
        for ax, ylab, ttl in zip(axes,
                                 [r"$\chi'$", r"$\chi''$"],
                                 ["CLAIM 3: real part", "CLAIM 3: loss"]):
            ax.set_xlabel("T"); ax.set_ylabel(ylab); ax.set_title(ttl)
            ax.legend(fontsize=8); ax.grid(alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(FIGS, "chi_ac_vs_T.png"), dpi=140)
        plt.close(fig)

# ------------------------------------------------------------------ #
def main():
    t0 = time.time()
    results = {
        "paper": "arXiv:2604.26100 (Wang, Yang, Chen 2026)",
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": {
            "kind": "2-layer 2D phase-field (TDGL), reduced-mechanism",
            "grid": "2 x 32 x 32 with 3-component P",
            "params": dict(a0=1.0, T0=0.9, b=1.0, c=0.5,
                           K_z=0.35, g=1.2, eps=0.6, J=0.05, L=1.0,
                           dt=0.02, kT_scale=0.03),
            "notes": ("Weak J=0.05 so interlayer alignment is emergent, not "
                      "enforced. Fluctuation-dissipation for chi. Cores found "
                      "by NMS on Gaussian-smoothed |P_xy|*max(-Pz,0) field."),
        },
        "claims": {},
    }
    save_results(results)

    # ---- Temperature sweep ----
    # Ts spans well above and below T0=0.9. Cool slowly.
    Ts = np.array([1.60, 1.40, 1.20, 1.05, 0.95, 0.85, 0.75, 0.60, 0.45, 0.30])
    print(f"[{time.time()-t0:6.1f}s] T sweep: {list(Ts)}")
    sweep, model_final = run_temperature_sweep(
        Ts, N=32, seed=1, dt=0.02, n_eq=1000, n_meas=1200,
        kT_scale=0.03, sample_every=1)
    results["sweep"] = sweep
    save_results(results)

    Ts_a  = np.array([m["T"] for m in sweep])
    chi_a = np.array([m["chi_fluct"] for m in sweep])
    cor_a = np.array([m["corr_mean"] for m in sweep])

    # CLAIM 1
    corr_high = float(np.mean(cor_a[:2]))
    corr_low  = float(np.mean(cor_a[-2:]))
    claim1_pass = bool(corr_low > corr_high + 0.03)
    results["claims"]["claim1_interlayer_corr"] = {
        "description": "Interlayer correlation of skyrmion cores grows on cooling",
        "corr_high_T_mean": corr_high,
        "corr_low_T_mean":  corr_low,
        "delta_corr":       corr_low - corr_high,
        "pass_criterion":   "corr(low T) > corr(high T) + 0.03",
        "pass":             claim1_pass,
    }

    # CLAIM 2
    peak_i   = int(np.argmax(chi_a))
    peak_T   = float(Ts_a[peak_i]); peak_chi = float(chi_a[peak_i])
    half = 0.5 * peak_chi
    above = chi_a >= half
    T_above = Ts_a[above]
    fwhm = float(T_above.max() - T_above.min()) if T_above.size >= 2 else 0.0
    interior = peak_i not in (0, len(chi_a)-1)
    endpoints_low = (chi_a[0] < peak_chi) and (chi_a[-1] < peak_chi)
    claim2_pass = bool(interior and endpoints_low)
    results["claims"]["claim2_chi_peak"] = {
        "description": "Broad peak in dielectric susceptibility vs T",
        "peak_T": peak_T, "peak_chi": peak_chi,
        "fwhm_T": fwhm,
        "broadness_fwhm_over_Tpeak": fwhm/peak_T if peak_T>0 else 0.0,
        "chi_at_low_T":  float(chi_a[-1]),
        "chi_at_high_T": float(chi_a[0]),
        "pass_criterion":"interior peak with both endpoints below peak",
        "pass": claim2_pass,
    }
    save_results(results)

    # ---- Stretch: CLAIM 3 ----
    ac = None
    elapsed = time.time() - t0
    remaining = 1200 - elapsed
    print(f"[{elapsed:6.1f}s] main sweep done; ~{remaining:.0f}s left")
    if remaining > 300:
        try:
            Ts_ac = np.array([1.30, 1.10, 0.95, 0.80, 0.65, 0.45])
            omegas = [0.10, 0.30, 0.90]
            print(f"[{time.time()-t0:6.1f}s] AC: omegas={omegas}")
            ac = run_ac_susceptibility(
                Ts_ac, omegas, N=32, seed=2, dt=0.02, n_eq=400,
                n_cycles=4, E0=0.03, kT_scale=0.03)
            results["ac"] = ac
            peak_Ts = []
            for i, om in enumerate(omegas):
                row = ac["chi_ac"][i]
                xp = np.abs(np.array([r["chi_prime"] for r in row]))
                Tvals = np.array([r["T"] for r in row])
                peak_Ts.append(float(Tvals[int(np.argmax(xp))]))
            direction_ok = bool(peak_Ts[-1] >= peak_Ts[0])
            results["claims"]["claim3_relaxor_dispersion"] = {
                "description": "chi'(T) peak shifts to higher T with omega",
                "omegas": omegas,
                "peak_T_at_omega": peak_Ts,
                "direction_reproduced": direction_ok,
                "pass_criterion":"peak_T(omega_max) >= peak_T(omega_min)",
                "pass": direction_ok,
                "note": "Minimal 2-layer model: direction only, not magnitude.",
            }
            save_results(results)
        except Exception as e:
            results["claims"]["claim3_relaxor_dispersion"] = {
                "pass": False, "error": repr(e)}
            save_results(results)

    make_plots(sweep, model_final, ac=ac)

    passed = [k for k,v in results["claims"].items() if v.get("pass")]
    n_pass = len(passed); n_tot = len(results["claims"])
    if n_tot == 0:
        verdict = "NO_TESTS"
    elif n_pass == n_tot:
        verdict = "PARTIAL (mechanism-only; not a full-superlattice match)"
    elif n_pass >= 2:
        verdict = "PARTIAL"
    elif n_pass == 1:
        verdict = "WEAK_PARTIAL"
    else:
        verdict = "NEGATIVE"

    results["verdict"] = verdict
    results["claims_passed"] = passed
    results["runtime_s"] = round(time.time()-t0, 1)
    results["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    save_results(results)
    print(f"\n[{results['runtime_s']:.1f}s] DONE  verdict={verdict}  "
          f"passed={passed}")
    return results

if __name__ == "__main__":
    main()
