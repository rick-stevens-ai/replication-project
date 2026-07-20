"""
stoner.py — Claim: at u=1.08 the magnetic Stoner factor alpha_mag ~= 0.9 (paper, Fig 2 caption).
alpha_mag = max_q max_{magnetic IR} [ u * U0Q * chi0_Q(q) ]  (channel-diagonal approx).
The multipole order for channel Q appears when u*U0Q*chi0_Q(q) >= 1.

We scan magnetic channels over the Gamma-X-M-Gamma path (and offer full-BZ for Jz)
and report the largest eigenvalue (= Stoner factor) as a function of u.
"""
import numpy as np
from rpa import precompute_bands, chi0_Q, embed, U0Q
from model import normalized_multipoles
from qscan import qpath


def stoner_vs_u(nk=40, us=(0.9, 1.0, 1.08, 1.15), channels=None):
    ops = normalized_multipoles()
    if channels is None:
        channels = ["Jz", "Jx", "Jy", "Tza", "Tzb", "Txa", "Tya", "Txyz",  # magnetic
                    "Oxy", "Oyz", "Ozx", "O20", "O22"]                       # electric
    ks, Es, Vs, kmap = precompute_bands(nk)
    seg = qpath(nk)
    # precompute chi0 peak per channel over path (chi0 is u-independent)
    peak_c0 = {}
    for name in channels:
        Q6 = embed(ops[name][1])
        c0s = [chi0_Q(Q6, qi, qj, ks, Es, Vs, kmap) for (qi, qj) in seg]
        peak_c0[name] = max(c0s)
    mag = ["Jz", "Jx", "Jy", "Tza", "Tzb", "Txa", "Tya", "Txyz"]
    el = ["Oxy", "Oyz", "Ozx", "O20", "O22"]
    rows = []
    for u in us:
        a_all = {n: u * U0Q[n] * peak_c0[n] for n in channels}
        a_mag = max(a_all[n] for n in mag)
        a_el = max(a_all[n] for n in el)
        argmag = max(mag, key=lambda n: a_all[n])
        rows.append((u, a_mag, a_el, argmag))
    return peak_c0, rows


if __name__ == "__main__":
    import sys, json
    nk = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    peak_c0, rows = stoner_vs_u(nk=nk)
    print(f"# nk={nk}  channel-diagonal Stoner factors")
    print("# u      alpha_mag  alpha_el   (max mag channel)")
    out = []
    for u, am, ae, arg in rows:
        print(f"  {u:.3f}   {am:8.3f}  {ae:8.3f}   {arg}")
        out.append({"u": u, "alpha_mag": am, "alpha_el": ae, "argmax_mag": arg})
    print("\n# bare chi0 peak per channel:")
    for n, v in sorted(peak_c0.items(), key=lambda x: -x[1]):
        print(f"  {n:6s} {v:.3f}  (U0Q={U0Q[n]})")
    with open("stoner_summary.json", "w") as f:
        json.dump({"nk": nk, "rows": out,
                   "peak_chi0": peak_c0}, f, indent=2)
