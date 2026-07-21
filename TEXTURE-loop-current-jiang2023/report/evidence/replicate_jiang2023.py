#!/usr/bin/env python3
"""
Replication of the S-matrix / bipartite-crystalline-lattice (BCL) flat-band
counting theorem of Jiang et al., arXiv:2311.09290v2 (kagome 1:1/1:6:6/1:3:5
families; "hidden d-orbital decoupling of flat band sectors").

HEADLINE (Eqs. S10.1-S10.3):
  For a chiral bipartite Bloch Hamiltonian
      H(k) = [[0_{NL}, S(k)], [S(k)^dag, 0_{NLtilde}]],  NL >= NLtilde,
  there are AT LEAST NL - NLtilde flat bands pinned at E=0. If rank(S_k)=r_s
  (<= NLtilde) over the BZ, there are exactly NL + NLtilde - 2*r_s flat bands
  at zero energy. Concrete kagome instance: the d2(dx2-y2)/ptxy group forms a
  3+2 BCL -> N_d2 - N_p = 3-2 = 1 perfectly flat band.

We (1) reproduce the s-orbital kagome flat band at +2t using the shared kagome
kernel (baseline / "simple model"), and (2) verify the counting theorem from
scratch for several (NL, NLtilde, rank) configurations, including the paper's
3+2 case.

Kernel provenance:
  loop_current_kagome_kernel.py  (KagomeModel; Fernandes/Birol/Ye/Vanderbilt LC kernel)
  loop_current_meanfield_kernel.py (Ollie loop-current mean-field probe)
"""
from __future__ import annotations
import json, sys, time
import numpy as np

sys.path.insert(0, "/home/stevens/shared-kernels-cache")
import loop_current_kagome_kernel as kk  # provenance-credited shared kernel

RNG = np.random.default_rng(2311)
FLAT_TOL = 1e-6   # bandwidth below this = "perfectly flat"


def _jsafe(o):
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    raise TypeError(f"not serializable: {type(o)}")


def count_flat_bands(evals_over_k: np.ndarray, tol: float = FLAT_TOL,
                     e_target: float | None = None) -> tuple[int, list]:
    """evals_over_k: shape (Nk, Nbands) sorted ascending per k.
    A band index n is 'flat' if max-min over k < tol. If e_target given, also
    require the mean band energy within tol of e_target."""
    nb = evals_over_k.shape[1]
    flats = []
    for n in range(nb):
        col = evals_over_k[:, n]
        bw = float(col.max() - col.min())
        emean = float(col.mean())
        is_flat = bw < tol
        if e_target is not None:
            is_flat = is_flat and abs(emean - e_target) < 1e-4
        if is_flat:
            flats.append({"band": n, "bandwidth": bw, "energy": emean})
    return len(flats), flats


def bz_grid(nk: int) -> np.ndarray:
    f = np.linspace(0, 1, nk, endpoint=False)
    U, V = np.meshgrid(f, f, indexing="ij")
    return np.stack([U.ravel(), V.ravel()], axis=1)  # fractional (u,v)


# --- Part 1: s-orbital kagome baseline via shared kernel -------------------
def part1_kagome_baseline(nk: int = 24) -> dict:
    model = kk.KagomeModel(t=1.0, flux=0.0, flux_pattern="none")
    frac = bz_grid(nk)
    kcart = frac[:, [0]] * kk.B1 + frac[:, [1]] * kk.B2
    ev = np.array([np.sort(np.linalg.eigvalsh(model.hamiltonian(k[0], k[1])).real)
                   for k in kcart])
    nflat, flats = count_flat_bands(ev, tol=1e-6)
    # textbook: flat band at +2t (top band), Dirac touch of lower two at K
    top_bw = float(ev[:, 2].max() - ev[:, 2].min())
    return {
        "description": "s-orbital NN kagome (3 sites/cell), shared KagomeModel kernel",
        "n_flat_bands": nflat,
        "flat_bands": flats,
        "top_band_bandwidth": top_bw,
        "top_band_energy": float(ev[:, 2].mean()),
        "expected": "1 flat band at E=+2t=+2.0 (t=1 convention)",
        "match": (nflat == 1 and abs(ev[:, 2].mean() - 2.0) < 1e-3),
    }


# --- Part 2: BCL / S-matrix counting theorem from scratch ------------------
def make_S_of_k(NL: int, NLt: int, rank: int, kfrac) -> np.ndarray:
    """Build an S(k) of shape (NL, NLt) with a controlled BZ-wide rank.
    We construct S(k) = P(k) @ diag(sv) @ Q^dag where P (NL x rank) and
    Q (NLt x rank) carry smooth k-dependence and sv are nonzero singular
    values. rank <= min(NL,NLt) fixes rank(S_k) = rank for (generic) k."""
    u, v = kfrac
    phase = np.exp(2j * np.pi * (u + v))
    # deterministic-but-k-dependent orthonormal-ish columns
    P = RNG.standard_normal((NL, rank)) + 1j * RNG.standard_normal((NL, rank))
    Q = RNG.standard_normal((NLt, rank)) + 1j * RNG.standard_normal((NLt, rank))
    # inject k-dependence smoothly
    kmod = np.array([[np.cos(2*np.pi*u*(r+1)) + 1j*np.sin(2*np.pi*v*(r+1))
                      for r in range(rank)]])
    Pk = P * kmod
    Qk = Q * np.conj(kmod)
    sv = np.diag(1.0 + 0.5*np.arange(rank))  # distinct nonzero singular values
    return Pk @ sv @ Qk.conj().T


def bipartite_H(NL: int, NLt: int, rank: int, kfrac,
                A=None, B=None) -> np.ndarray:
    N = NL + NLt
    H = np.zeros((N, N), complex)
    S = make_S_of_k(NL, NLt, rank, kfrac)
    H[:NL, NL:] = S
    H[NL:, :NL] = S.conj().T
    if A is not None:
        H[:NL, :NL] = A
    if B is not None:
        H[NL:, NL:] = B
    return H


def part2_counting(nk: int = 12) -> dict:
    frac = bz_grid(nk)
    cases = []
    # (NL, NLt, rank, label). Note S must be reseeded per-config but frozen across k
    configs = [
        (3, 2, 2, "kagome d2/ptxy BCL (Nd2=3, Np=2): expect NL-NLt=1 flat"),
        (5, 3, 3, "generic 5+3 full-rank: expect 5-3=2 flat"),
        (4, 4, 2, "rank-deficient 4+4, rs=2: expect 4+4-2*2=4 flat"),
        (6, 2, 2, "1:6:6-like 6+2 full-rank: expect 6-2=4 flat"),
    ]
    for NL, NLt, rank, label in configs:
        # freeze random matrices for this config so only k varies
        global RNG
        RNG = np.random.default_rng(1000 + NL*10 + NLt + rank)
        # capture the frozen P,Q,sv by building once symbolically: rebuild helper
        _P = RNG.standard_normal((NL, rank)) + 1j*RNG.standard_normal((NL, rank))
        _Q = RNG.standard_normal((NLt, rank)) + 1j*RNG.standard_normal((NLt, rank))
        _sv = np.diag(1.0 + 0.5*np.arange(rank))
        def S_of(kf):
            u, v = kf
            kmod = np.array([[np.cos(2*np.pi*u*(r+1)) + 1j*np.sin(2*np.pi*v*(r+1))
                              for r in range(rank)]])
            Pk = _P * kmod; Qk = _Q * np.conj(kmod)
            return Pk @ _sv @ Qk.conj().T
        ev = []
        ranks = []
        for kf in frac:
            S = S_of(kf)
            N = NL + NLt
            H = np.zeros((N, N), complex)
            H[:NL, NL:] = S; H[NL:, :NL] = S.conj().T
            ev.append(np.sort(np.linalg.eigvalsh(H).real))
            ranks.append(np.linalg.matrix_rank(S, tol=1e-9))
        ev = np.array(ev)
        rs = int(np.median(ranks))
        nflat, flats = count_flat_bands(ev, tol=FLAT_TOL, e_target=0.0)
        predicted = NL + NLt - 2*rs
        cases.append({
            "label": label, "NL": NL, "NLtilde": NLt, "rank_S": rs,
            "predicted_flat_at_zero": predicted,
            "measured_flat_at_zero": nflat,
            "match": nflat == predicted,
            "flat_band_max_bandwidth": max((f["bandwidth"] for f in flats), default=0.0),
        })
    return {"description": "chiral bipartite H=[[0,S],[S^dag,0]] flat-band counting (Eq. S10.1-S10.2)",
            "cases": cases,
            "all_match": all(c["match"] for c in cases)}


# --- Part 3: intra-sublattice case (A(k) with k-indep multiplicity) --------
def part3_intra(nk: int = 12) -> dict:
    """Eq. S10.3: add A(k)=mu*I_{NL}. Then na=NL k-indep eigenvalue mult;
    expect na - NLtilde flat bands at energy != 0 (pinned near mu)."""
    frac = bz_grid(nk)
    NL, NLt, rank = 3, 2, 2
    mu = 0.7
    RNGl = np.random.default_rng(555)
    _P = RNGl.standard_normal((NL, rank)) + 1j*RNGl.standard_normal((NL, rank))
    _Q = RNGl.standard_normal((NLt, rank)) + 1j*RNGl.standard_normal((NLt, rank))
    _sv = np.diag(1.0 + 0.5*np.arange(rank))
    ev = []
    for kf in frac:
        u, v = kf
        kmod = np.array([[np.cos(2*np.pi*u*(r+1)) + 1j*np.sin(2*np.pi*v*(r+1))
                          for r in range(rank)]])
        S = (_P*kmod) @ _sv @ (_Q*np.conj(kmod)).conj().T
        N = NL + NLt
        H = np.zeros((N, N), complex)
        H[:NL, :NL] = mu*np.eye(NL)
        H[:NL, NL:] = S; H[NL:, :NL] = S.conj().T
        ev.append(np.sort(np.linalg.eigvalsh(H).real))
    ev = np.array(ev)
    nflat, flats = count_flat_bands(ev, tol=FLAT_TOL)
    predicted = NL - NLt  # = 1, at energy mu
    return {"description": "intra-sublattice A=mu*I (Eq. S10.3): flat band at nonzero energy",
            "NL": NL, "NLtilde": NLt, "mu": mu,
            "predicted_flat": predicted, "measured_flat": nflat,
            "flat_bands": flats,
            "match": nflat == predicted and any(abs(f["energy"]-mu) < 1e-3 for f in flats)}


# --- Part 4: loop-current cross-check via shared mean-field kernel ---------
def part4_loopcurrent() -> dict:
    import loop_current_meanfield_kernel as lc
    r = lc.probe(Lx=4, Ly=4, t=1.0, filling=1.0/3.0, phi=1e-3, mass=0.0)
    return {"description": "shared loop-current mean-field probe (context/provenance)",
            "loop_current_susceptibility": r["loop_current_susceptibility"],
            "loop_order_phi0": r["loop_order_phi0"],
            "note": "paper is flat-band-framework, not spontaneous LC; probe included for class provenance only"}


def main():
    t0 = time.time()
    out = {"paper": "jiang2023 arXiv:2311.09290v2",
           "headline": "S-matrix/BCL flat-band counting: NL-NLtilde (or NL+NLtilde-2rs) flat bands",
           "kernel_provenance": ["loop_current_kagome_kernel.py", "loop_current_meanfield_kernel.py"]}
    # SAVE-EARLY skeleton
    outpath = "/home/stevens/textures-100/corpus/textures-loop-current-jiang2023/work/jiang2023_result.json"
    with open(outpath, "w") as f:
        json.dump(out, f, indent=2, default=_jsafe)

    out["part1_kagome_baseline"] = part1_kagome_baseline()
    with open(outpath, "w") as f: json.dump(out, f, indent=2, default=_jsafe)  # save-early

    out["part2_counting_theorem"] = part2_counting()
    with open(outpath, "w") as f: json.dump(out, f, indent=2, default=_jsafe)

    out["part3_intra_sublattice"] = part3_intra()
    out["part4_loopcurrent_context"] = part4_loopcurrent()

    overall = (out["part1_kagome_baseline"]["match"]
               and out["part2_counting_theorem"]["all_match"]
               and out["part3_intra_sublattice"]["match"])
    out["overall_headline_reproduced"] = bool(overall)
    out["runtime_sec"] = round(time.time() - t0, 2)
    with open(outpath, "w") as f:
        json.dump(out, f, indent=2, default=_jsafe)
    print(json.dumps(out, indent=2, default=_jsafe))


if __name__ == "__main__":
    main()
