"""
qscan.py — q-dependence of RPA multipole susceptibilities along Gamma-X-M-Gamma
and a coarse full-BZ map, to test:
  (C2) magnetic Jz channel is the largest in RPA, peaking near q=0 and q=Q=(pi,pi)
  (C3) quadrupole Oxy stays small relative to magnetic channels in RPA

Uses the channel-diagonal RPA from rpa.py with reported U0Q (TABLE II).
Also reports the RPA-vs-bare "magnetic dominance ratio" max(chi_mag)/max(chi_quad).
"""
import numpy as np
from rpa import (precompute_bands, chi0_Q, embed, U0Q, fermi)
from model import normalized_multipoles


def qpath(nk):
    """Gamma(0,0)->X(pi,0)->M(pi,pi)->Gamma, in mesh-index steps."""
    h = nk // 2
    seg = []
    labels = []
    # Gamma->X
    for i in range(h + 1):
        seg.append((i, 0)); 
    # X->M
    for j in range(1, h + 1):
        seg.append((h, j))
    # M->Gamma (diagonal)
    for d in range(1, h + 1):
        seg.append((h - d, h - d))
    return seg


def full_map(name, nk, u):
    ops = normalized_multipoles()
    ks, Es, Vs, kmap = precompute_bands(nk)
    Q6 = embed(ops[name][1])
    C0 = np.zeros((nk, nk))
    CR = np.zeros((nk, nk))
    for qi in range(nk):
        for qj in range(nk):
            c0 = chi0_Q(Q6, qi, qj, ks, Es, Vs, kmap)
            den = 1 - u * U0Q[name] * c0
            C0[qi, qj] = c0
            CR[qi, qj] = c0 / den if den > 0 else np.inf
    return C0, CR


def scan_channels(nk, u, channels):
    ops = normalized_multipoles()
    ks, Es, Vs, kmap = precompute_bands(nk)
    seg = qpath(nk)
    out = {}
    for name in channels:
        Q6 = embed(ops[name][1])
        c0s, crs = [], []
        for (qi, qj) in seg:
            c0 = chi0_Q(Q6, qi, qj, ks, Es, Vs, kmap)
            den = 1 - u * U0Q[name] * c0
            c0s.append(c0)
            crs.append(c0 / den if den > 0 else np.inf)
        out[name] = (np.array(c0s), np.array(crs))
    return seg, out


if __name__ == "__main__":
    import sys, json
    nk = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    u = float(sys.argv[2]) if len(sys.argv) > 2 else 1.08
    mag = ["Jz", "Jx", "Jy", "Txa", "Tya", "Tza", "Tzb", "Txyz"]
    quad = ["Oxy", "Oyz", "Ozx", "O20", "O22"]
    seg, out = scan_channels(nk, u, mag + quad)
    # summarize peak values (bare and RPA)
    print(f"# nk={nk} u={u} — peak chi0 and chiRPA over Gamma-X-M-Gamma path")
    summary = {}
    for name in mag + quad:
        c0, cr = out[name]
        finite = cr[np.isfinite(cr)]
        peak_rpa = float(np.max(finite)) if finite.size else float("inf")
        argp = int(np.argmax(c0))
        qp = seg[argp]
        summary[name] = {
            "peak_chi0": float(np.max(c0)),
            "peak_rpa": peak_rpa,
            "arg_chi0_qidx": list(qp),
            "grp": "mag" if name in mag else "quad",
        }
        print(f"{name:6s} [{'M' if name in mag else 'Q'}] peak_chi0={np.max(c0):6.3f} "
              f"at q-idx={qp}  peak_rpa={peak_rpa:8.3f}")
    mag_peak0 = max(summary[n]["peak_chi0"] for n in mag)
    quad_peak0 = max(summary[n]["peak_chi0"] for n in quad)
    top_mag = max(mag, key=lambda n: summary[n]["peak_chi0"])
    top_quad = max(quad, key=lambda n: summary[n]["peak_chi0"])
    print(f"\nLargest MAGNETIC channel (bare): {top_mag} = {mag_peak0:.3f}")
    print(f"Largest QUADRUPOLE channel (bare): {top_quad} = {quad_peak0:.3f}")
    print(f"magnetic/quadrupole bare peak ratio = {mag_peak0/quad_peak0:.3f}")
    # save
    with open("qscan_summary.json", "w") as f:
        json.dump({"nk": nk, "u": u, "summary": summary,
                   "top_mag": top_mag, "top_quad": top_quad,
                   "mag_over_quad_bare": mag_peak0/quad_peak0}, f, indent=2)
    # save Jz and Oxy full path for plotting/report
    np.savez("qscan_paths.npz", seg=np.array(seg),
             Jz0=out["Jz"][0], JzR=out["Jz"][1],
             Oxy0=out["Oxy"][0], OxyR=out["Oxy"][1],
             Jx0=out["Jx"][0], JxR=out["Jx"][1])
