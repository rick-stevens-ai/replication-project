#!/usr/bin/env python3
"""
Tight-binding / k.p SURROGATE replication of oh2026:
  "p-wave orbital angular momentum texture in a chiral crystal" (TaSe4)2I
  Oh, Pacella, ... Di Sante, Comin, arXiv:2605.15544 (2026).

PAPER (tagged DFT: FPLO GGA-PBE + MLWF).  We build the reproducible MODEL CORE
(the minimal tight-binding model the paper itself invokes, Sec. III + Fig. S1)
WITHOUT running DFT.

PHYSICS (from paper Sec. III):
  - (TaSe4)2I is a 1D chiral chain along x. Low-energy bands = Ta-dx2 (which the
    paper states does NOT carry local OAM) hybridized with Se perpendicular
    p-orbitals (py, pz), which "act as orbital polarizers".
  - The chiral helix winding around x produces a SOC-FREE chiral coupling
    between py and pz that is ODD in kx (~ sin kx). In the {py,pz} subspace the
    imaginary antisymmetric coupling -i(|py><pz|-|pz><py|) IS the orbital
    angular-momentum operator L_x.  => eigenstates carry L_x ~ sign(sin kx):
    an ODD-PARITY (p-wave) OAM texture.
  - Enantiomer B = mirror image => opposite helicity => chiral couplings flip
    sign => L_x texture reverses sign (chirality control).
  - L_x is EVEN in ky (largely ky-independent), L_y weak, L_z absent.
  - Weak atomic SOC (xi L.S) splits bands by a tiny amount; the two split
    branches share the SAME OAM but carry OPPOSITE SAM => net SAM ~ 0 while OAM
    survives  => OAM polarization >> SAM polarization.

We REUSE the itinerant/atomic orbital-angular-momentum machinery convention
from the shared kernel:
  gobel2024_sd_skyrmion_kubo_Lz_kernel.py  (A. Goebel et al., arXiv:2410.00820)
  -- specifically the L_z = 1/2 (X v_y - Y v_x) itinerant-OAM construction and
  the "expectation of an angular-momentum operator over occupied Bloch states"
  workflow.  Here the relevant OAM is the ATOMIC (on-site) p-orbital L, which is
  the appropriate operator for a Wannier/atomic-orbital model (the paper's
  MLWF picture), so we use the p-orbital angular-momentum matrices directly;
  the summation-over-states expectation-value pattern is the same as the kernel.

Outputs work/oh2026_result.json  (SAVE-EARLY).
"""
import json, os, time
import numpy as np

t0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figs")
os.makedirs(FIGDIR, exist_ok=True)

# ----------------------------------------------------------------------------
# p-orbital angular-momentum matrices in the basis (px, py, pz).
#   (L_a)_{jk} = -i eps_{ajk}       (hbar = 1)
# ----------------------------------------------------------------------------
Lx = np.array([[0, 0, 0],
               [0, 0, -1j],
               [0, 1j, 0]], dtype=complex)
Ly = np.array([[0, 0, 1j],
               [0, 0, 0],
               [-1j, 0, 0]], dtype=complex)
Lz = np.array([[0, -1j, 0],
               [1j, 0, 0],
               [0, 0, 0]], dtype=complex)
I3 = np.eye(3, dtype=complex)

# Pauli (spin) matrices
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)


# ----------------------------------------------------------------------------
# 3-orbital chiral tight-binding Hamiltonian (orbital only, no spin).
# basis: (px, py, pz).  px = the chain-axis "dx2-like" primary orbital that the
# paper says is OAM-inert; py,pz = Se perpendicular orbital polarizers.
#   chi = +1 for enantiomer A, -1 for enantiomer B (opposite helicity).
# ----------------------------------------------------------------------------
def H_orbital(kx, ky, chi=+1,
              tx=1.0, ty=0.15, epx=0.8, epy=-0.6, delta=0.35,
              A=0.6, B=0.12, Cz=0.0):
    """
    basis (px, py, pz).  px = Ta-dx2-like PRIMARY orbital; the paper states it
    is OAM-INERT, so we place it ABOVE the low-energy manifold as a spectator.
    The low-energy DOUBLET is {py, pz} -- the Se perpendicular "orbital
    polarizers" that the paper says carry the finite Lx.

    tx,ty : intra-chain / weak inter-chain hopping (dispersion, orbital-diagonal)
    epx   : on-site energy of px (spectator), pushed UP (OAM-inert)
    epy   : on-site energy of the py/pz doublet (low-energy manifold)
    delta : small py/pz on-site splitting -> Lx=0 baseline at kx=0 so that the
            chiral term turns on a SMOOTH p-wave Lx ~ sin(kx) (linear form
            factor, matching the paper's linearly-dispersing +Lx bands)
    A     : CHIRAL py<->pz coupling  A*sin(kx)*Lx  (the p-wave OAM generator)
    B     : weak chiral px<->pz coupling  B*sin(kx)*Ly -> WEAK Ly (px far away)
    Cz    : px<->py term  Cz*sin(ky)*Lz ; default 0 => Lz ABSENT (paper).
    """
    disp = (-2 * tx * np.cos(kx) - 2 * ty * np.cos(ky))
    H = disp * I3
    H = H + np.diag([epx, epy, epy + delta]).astype(complex)
    H = H + chi * A * np.sin(kx) * Lx      # p-wave OAM (dominant, in py/pz)
    H = H + chi * B * np.sin(kx) * Ly      # weak p-wave Ly (px spectator)
    H = H + chi * Cz * np.sin(ky) * Lz     # 0 by default -> Lz absent
    return H


def band_OAM(kx, ky, chi=+1, band=0, **kw):
    """Return (energy, <Lx>,<Ly>,<Lz>) for the `band`-th eigenstate (0=lowest)."""
    H = H_orbital(kx, ky, chi=chi, **kw)
    E, V = np.linalg.eigh(H)
    psi = V[:, band]
    lx = np.real(psi.conj() @ Lx @ psi)
    ly = np.real(psi.conj() @ Ly @ psi)
    lz = np.real(psi.conj() @ Lz @ psi)
    return E[band], lx, ly, lz


# ----------------------------------------------------------------------------
# Spinful 6-orbital model with weak atomic SOC (xi L.S) for the SAM check.
# ----------------------------------------------------------------------------
def H_spinful(kx, ky, chi=+1, xi=0.02, **kw):
    Ho = H_orbital(kx, ky, chi=chi, **kw)               # 3x3
    H = np.kron(Ho, I2)                                  # 6x6 (orbital x spin)
    LS = (np.kron(Lx, sx) + np.kron(Ly, sy) + np.kron(Lz, sz)) / 2.0
    H = H + xi * LS
    return H


def spin_orbital_expect(psi):
    """<Lx>,<Sx> for a 6-vector state (orbital(3) x spin(2))."""
    LxS = np.kron(Lx, I2)
    SxO = np.kron(I3, sx / 2.0)
    lx = np.real(psi.conj() @ LxS @ psi)
    sx_ = np.real(psi.conj() @ SxO @ psi)
    return lx, sx_


# ============================================================================
def main():
    res = {
        "paper": "Oh et al., p-wave OAM texture in chiral (TaSe4)2I, arXiv:2605.15544 (2026)",
        "method_paper": "DFT (FPLO GGA-PBE) + maximally-localized Wannier functions",
        "method_here": "tight-binding / k.p MODEL SURROGATE of the paper's minimal "
                       "chiral p-orbital model (Sec. III, Fig. S1); NO DFT run.",
        "kernel_credit": "OAM expectation-over-states workflow adapted from "
                         "gobel2024_sd_skyrmion_kubo_Lz_kernel.py "
                         "(A. Goebel et al., arXiv:2410.00820).",
        "headline_claim": "A p-wave (odd-parity) OAM texture Lx(k) with "
                          "enantiomer-dependent sign reversal; OAM polarization "
                          ">> SAM polarization at low energy.",
        "checks": {},
    }

    params = dict(tx=1.0, ty=0.15, epx=0.8, epy=-0.6, delta=0.35, A=0.6, B=0.12, Cz=0.0)
    res["params"] = params

    # ---- k-grid over the BZ ----
    nk = 121
    ks = np.linspace(-np.pi, np.pi, nk)
    KX, KY = np.meshgrid(ks, ks, indexing="ij")

    def texture(chi):
        Lxg = np.zeros_like(KX); Lyg = np.zeros_like(KX); Lzg = np.zeros_like(KX)
        Eg = np.zeros_like(KX)
        for i in range(nk):
            for j in range(nk):
                E, lx, ly, lz = band_OAM(KX[i, j], KY[i, j], chi=chi, band=0, **params)
                Eg[i, j] = E; Lxg[i, j] = lx; Lyg[i, j] = ly; Lzg[i, j] = lz
        return Eg, Lxg, Lyg, Lzg

    EA, LxA, LyA, LzA = texture(+1)   # enantiomer A
    EB, LxB, LyB, LzB = texture(-1)   # enantiomer B

    # ---------- CHECK 1: p-wave (odd-parity in kx) OAM texture ----------
    # Lx(+kx) = -Lx(-kx): antisymmetric under kx -> -kx
    Lx_flip = LxA[::-1, :]                       # kx -> -kx
    odd_resid = np.max(np.abs(LxA + Lx_flip)) / (np.max(np.abs(LxA)) + 1e-12)
    # sign at +kx vs -kx region (average over ky, exclude kx~0 and BZ boundary)
    mid = nk // 2
    q = nk // 6
    lx_pos = float(np.mean(LxA[mid + q:mid + 3 * q, :]))   # +kx region
    lx_neg = float(np.mean(LxA[mid - 3 * q:mid - q, :]))   # -kx region
    pwave_ok = (odd_resid < 1e-6) and (np.sign(lx_pos) == -np.sign(lx_neg)) and abs(lx_pos) > 0.1
    res["checks"]["C1_pwave_odd_parity_Lx"] = {
        "claim": "Lx(k) is odd-parity (p-wave): +Lx for +kx, -Lx for -kx",
        "odd_parity_residual_kx": float(odd_resid),
        "mean_Lx_pos_kx": lx_pos, "mean_Lx_neg_kx": lx_neg,
        "match": bool(pwave_ok),
    }

    # ---------- CHECK 2: enantiomer sign reversal ----------
    ent_resid = np.max(np.abs(LxA + LxB)) / (np.max(np.abs(LxA)) + 1e-12)
    ent_ok = ent_resid < 1e-6
    res["checks"]["C2_enantiomer_sign_reversal"] = {
        "claim": "Enantiomer B has opposite-sign Lx texture vs A (chirality control)",
        "max_|LxA+LxB|_over_max|LxA|": float(ent_resid),
        "match": bool(ent_ok),
    }

    # ---------- CHECK 3: mirror symmetry relations A<->B ----------
    # Mx (kx->-kx): maps A->B with Lx unchanged:  LxB(-kx,ky) == LxA(kx,ky)
    Mx_resid = np.max(np.abs(LxB[::-1, :] - LxA)) / (np.max(np.abs(LxA)) + 1e-12)
    # My (ky->-ky): maps A->B with Lx->-Lx:  LxB(kx,-ky) == -LxA(kx,ky)
    My_resid = np.max(np.abs(LxB[:, ::-1] + LxA)) / (np.max(np.abs(LxA)) + 1e-12)
    mirror_ok = (Mx_resid < 1e-6) and (My_resid < 1e-6)
    res["checks"]["C3_mirror_relations"] = {
        "claim": "Mx maps A->B (Lx unchanged, kx->-kx); My maps A->B (Lx->-Lx, ky->-ky)",
        "Mx_residual": float(Mx_resid), "My_residual": float(My_resid),
        "match": bool(mirror_ok),
    }

    # ---------- CHECK 4: Lx even in ky, Ly weak, Lz absent ----------
    ky_even_resid = np.max(np.abs(LxA - LxA[:, ::-1])) / (np.max(np.abs(LxA)) + 1e-12)
    ly_over_lx = float(np.max(np.abs(LyA)) / (np.max(np.abs(LxA)) + 1e-12))
    lz_over_lx = float(np.max(np.abs(LzA)) / (np.max(np.abs(LxA)) + 1e-12))
    comp_ok = (ky_even_resid < 1e-6) and (ly_over_lx < 0.5) and (lz_over_lx < 0.05)
    res["checks"]["C4_Lx_even_ky__Ly_weak__Lz_absent"] = {
        "claim": "Lx even in ky (~ky-independent); Ly weak; Lz absent",
        "Lx_ky_even_residual": float(ky_even_resid),
        "max|Ly|/max|Lx|": ly_over_lx,
        "max|Lz|/max|Lx|": lz_over_lx,
        "match": bool(comp_ok),
    }

    # ---------- CHECK 5: p-wave harmonic dominance on a constant-|k| loop ----------
    # decompose Lx(phi) on a circle radius k0 into angular harmonics cos(m phi)
    k0 = 1.0
    phis = np.linspace(0, 2 * np.pi, 720, endpoint=False)
    lx_loop = np.array([band_OAM(k0 * np.cos(p), k0 * np.sin(p), chi=+1, band=0, **params)[1]
                        for p in phis])
    # angular Fourier amplitudes a_m = <Lx, cos(m phi)>, b_m = <Lx, sin(m phi)>
    amps = {}
    for m in range(0, 5):
        am = 2 * np.mean(lx_loop * np.cos(m * phis))
        bm = 2 * np.mean(lx_loop * np.sin(m * phis))
        amps[m] = float(np.hypot(am, bm))
    amps[0] = float(np.mean(lx_loop))  # s-wave = mean
    m1 = amps[1]
    others = max(amps[0], amps[2], amps[3], amps[4])
    pwave_dom = m1 > 3.0 * (others + 1e-12)
    # sign changes around the loop = 2 for a clean p-wave (2 nodes)
    sgn = np.sign(lx_loop); sgn = sgn[sgn != 0]
    nodes = int(np.sum(np.abs(np.diff(sgn)) > 0))
    res["checks"]["C5_pwave_harmonic_dominance"] = {
        "claim": "OAM texture on a constant-|k| loop is dominated by the m=1 "
                 "(p-wave) angular harmonic, with 2 nodes (dipolar)",
        "harmonic_amplitudes_m0..m4": amps,
        "m1_over_max_others": float(m1 / (others + 1e-12)),
        "sign_nodes_around_loop": nodes,
        "match": bool(pwave_dom and nodes == 2),
    }

    # ---------- CHECK 6: OAM >> SAM (weak-SOC spin story) ----------
    # pick a representative k on the +kx band, small SOC
    kx0, ky0 = 0.4 * np.pi, 0.0
    xi = 0.02                    # weak atomic SOC
    Hs = H_spinful(kx0, ky0, chi=+1, xi=xi, **params)
    Es, Vs = np.linalg.eigh(Hs)
    # the two lowest (spin-split) branches
    order = np.argsort(Es)
    b0, b1 = order[0], order[1]
    lx0, sx0 = spin_orbital_expect(Vs[:, b0])
    lx1, sx1 = spin_orbital_expect(Vs[:, b1])
    split = float(Es[b1] - Es[b0])              # SOC splitting (energy units)
    net_sam = abs(sx0 + sx1)                     # net SAM of the pair
    net_oam = abs(lx0 + lx1)                     # net OAM of the pair
    same_oam_sign = (np.sign(lx0) == np.sign(lx1)) and abs(lx0) > 0.1
    opp_sam_sign = (np.sign(sx0) == -np.sign(sx1)) or net_sam < 0.1
    oam_over_sam = float(net_oam / (net_sam + 1e-9))
    c6_ok = same_oam_sign and (net_sam < 0.1) and (net_oam > 0.3)
    res["checks"]["C6_OAM_gg_SAM_weak_SOC"] = {
        "claim": "Weak SOC: two split branches share OAM sign but carry opposite "
                 "SAM => net SAM~0 while OAM survives; OAM polarization >> SAM.",
        "soc_xi": xi, "band_splitting": split,
        "branch0_Lx": float(lx0), "branch0_Sx": float(sx0),
        "branch1_Lx": float(lx1), "branch1_Sx": float(sx1),
        "net_OAM_pair": float(net_oam), "net_SAM_pair": float(net_sam),
        "net_OAM_over_net_SAM": oam_over_sam,
        "match": bool(c6_ok),
    }

    # ----------------- overall verdict -----------------
    checks = res["checks"]
    passed = [k for k, v in checks.items() if v["match"]]
    failed = [k for k, v in checks.items() if not v["match"]]
    res["n_checks"] = len(checks)
    res["n_passed"] = len(passed)
    res["passed"] = passed
    res["failed"] = failed
    res["verdict"] = "REPLICATED" if len(failed) == 0 else (
        "PARTIAL" if len(passed) >= len(failed) else "BLOCKED")
    res["runtime_sec"] = round(time.time() - t0, 1)

    # ----------------- figures -----------------
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(2, 3, figsize=(15, 9))
        ext = [-np.pi, np.pi, -np.pi, np.pi]
        vlim = np.max(np.abs(LxA))
        for a, (dat, ttl) in zip(
            ax[0], [(LxA, "Enantiomer A: $L_x(k)$ (p-wave)"),
                    (LxB, "Enantiomer B: $L_x(k)$ (sign-flipped)"),
                    (LyA, "Enantiomer A: $L_y(k)$ (weak)")]):
            im = a.imshow(dat.T, origin="lower", extent=ext, cmap="RdBu_r",
                          vmin=-vlim, vmax=vlim, aspect="auto")
            a.set_title(ttl); a.set_xlabel("$k_x$"); a.set_ylabel("$k_y$")
            plt.colorbar(im, ax=a, fraction=0.046)
        # Lz
        im = ax[1, 0].imshow(LzA.T, origin="lower", extent=ext, cmap="RdBu_r",
                             vmin=-vlim, vmax=vlim, aspect="auto")
        ax[1, 0].set_title("Enantiomer A: $L_z(k)$ (~absent)")
        ax[1, 0].set_xlabel("$k_x$"); ax[1, 0].set_ylabel("$k_y$")
        plt.colorbar(im, ax=ax[1, 0], fraction=0.046)
        # Lx along ky=0 cut
        ax[1, 1].plot(ks, LxA[:, mid], "b-", label="Enantiomer A")
        ax[1, 1].plot(ks, LxB[:, mid], "r--", label="Enantiomer B")
        ax[1, 1].axhline(0, color="k", lw=0.5)
        ax[1, 1].set_title("$L_x(k_x, k_y{=}0)$: odd-parity + enantiomer flip")
        ax[1, 1].set_xlabel("$k_x$"); ax[1, 1].set_ylabel("$L_x$"); ax[1, 1].legend()
        # harmonic bar
        ax[1, 2].bar(list(amps.keys()), list(amps.values()),
                     color=["gray", "crimson", "gray", "gray", "gray"])
        ax[1, 2].set_title("Angular harmonics of $L_x$ on |k| loop\n(m=1 = p-wave)")
        ax[1, 2].set_xlabel("harmonic m"); ax[1, 2].set_ylabel("amplitude")
        fig.tight_layout()
        fp = os.path.join(FIGDIR, "oh2026_pwave_oam.png")
        fig.savefig(fp, dpi=110)
        res["figures"] = ["figs/oh2026_pwave_oam.png"]
        print("wrote", fp)
    except Exception as e:
        res["figures_error"] = str(e)
        print("fig error:", e)

    outp = os.path.join(HERE, "oh2026_result.json")
    with open(outp, "w") as f:
        json.dump(res, f, indent=2)
    print("\n===== oh2026_result.json =====")
    print(json.dumps({k: res[k] for k in
                      ["verdict", "n_passed", "n_checks", "passed", "failed", "runtime_sec"]},
                     indent=2))
    for k, v in checks.items():
        print(f"  [{'PASS' if v['match'] else 'FAIL'}] {k}")
    return res


if __name__ == "__main__":
    main()
