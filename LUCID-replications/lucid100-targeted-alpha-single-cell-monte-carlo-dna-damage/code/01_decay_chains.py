"""Decay-chain alpha spectra for the 4 TαT radionuclides in
Jolly & Fielding 2025 (doi:10.1007/s13246-025-01605-2).

Source data: NNDC/ENSDF and ICRP-107 published values. We list, for each
parent, all alpha-emitting members of the decay chain (paper's Appendix 1
red-coloured nodes) with mean alpha energy and per-parent yield (alphas
per primary parent decay, accounting for branching).

This script reproduces the spectra used by the paper to drive 'isotropic
alpha-only discrete energy' sources (the Fig.3 / Fig.5 / Table 2 bottom
rows config). The energies and branchings come from public ENSDF data;
the per-parent yields use steady-state branching assumptions stated in
the paper (each daughter is allowed to decay to stability before the
next parent simulation primary).
"""
from __future__ import annotations
import json, sys
from dataclasses import dataclass, asdict

@dataclass
class AlphaEmission:
    parent_chain: str
    emitter: str          # nuclide emitting the alpha
    energy_MeV: float     # mean alpha energy (intensity-weighted, dominant line)
    branching: float      # probability that this alpha is emitted per primary parent decay

# References:
#  Ac-225 chain: NNDC ENSDF, ICRP-107. 4 alphas to stable Pb-209 then Bi-209 (stable for our window).
#  Ra-223 chain: 4 alphas (Ra-223, Rn-219, Po-215, Bi-211*/Po-211*) to Pb-207. We use the dominant alpha branch at Bi-211: 99.7% alpha to Tl-207, balance via Po-211 alpha 7.45 MeV.
#  Pb-212 chain: pure beta to Bi-212; Bi-212 branches 35.94% alpha (6.05 MeV avg) + 64.06% beta to Po-212 (alpha 8.785 MeV). So per Pb-212 decay: 0.3594 alphas at ~6.05 MeV + 0.6406 alphas at 8.785 MeV.
#  At-211 chain: 41.8% alpha 5.870 MeV to Bi-207 (stable for our timescale); 58.2% EC to Po-211 then alpha 7.450 MeV. So per At-211 decay: 1.0 alpha total (one branch or the other).

CHAINS = [
    # Ac-225 -> Fr-221 -> At-217 -> Bi-213 (-> Po-213 or Tl-209) -> Pb-209
    AlphaEmission("Ac-225", "Ac-225", 5.830, 1.000),
    AlphaEmission("Ac-225", "Fr-221", 6.341, 1.000),
    AlphaEmission("Ac-225", "At-217", 7.067, 1.000),
    AlphaEmission("Ac-225", "Bi-213", 5.870, 0.0214),   # 2.14% direct alpha to Tl-209
    AlphaEmission("Ac-225", "Po-213", 8.376, 0.9786),   # 97.86% Bi-213 -> beta -> Po-213 -> alpha

    # Ra-223 -> Rn-219 -> Po-215 -> Pb-211 (beta) -> Bi-211 -> Tl-207 (beta) -> Pb-207
    AlphaEmission("Ra-223", "Ra-223", 5.716, 1.000),
    AlphaEmission("Ra-223", "Rn-219", 6.819, 1.000),
    AlphaEmission("Ra-223", "Po-215", 7.386, 1.000),
    AlphaEmission("Ra-223", "Bi-211", 6.623, 0.99724),  # 99.724% alpha to Tl-207
    AlphaEmission("Ra-223", "Po-211", 7.450, 0.00276),  # 0.276% beta -> Po-211 -> alpha

    # Pb-212 (beta) -> Bi-212 (35.94% alpha or 64.06% beta) -> Po-212 (alpha) or Tl-208 (beta) -> Pb-208
    AlphaEmission("Pb-212", "Bi-212", 6.051, 0.3594),
    AlphaEmission("Pb-212", "Po-212", 8.785, 0.6406),

    # At-211: 41.8% alpha 5.870 MeV -> Bi-207 (stable on our timescale);
    #         58.2% EC -> Po-211 -> alpha 7.450 MeV (T1/2 0.516 s)
    AlphaEmission("At-211", "At-211", 5.870, 0.418),
    AlphaEmission("At-211", "Po-211", 7.450, 0.582),
]

def summarize(chains):
    out = {}
    for c in chains:
        d = out.setdefault(c.parent_chain, {"alphas_per_decay": 0.0, "mean_E_MeV": 0.0,
                                            "emissions": []})
        d["alphas_per_decay"] += c.branching
        d["emissions"].append(asdict(c))
    for parent, d in out.items():
        E_weighted = sum(e["energy_MeV"]*e["branching"] for e in d["emissions"])
        d["mean_E_MeV"] = E_weighted / d["alphas_per_decay"] if d["alphas_per_decay"] else 0.0
    return out

def main():
    summary = summarize(CHAINS)
    print("Per-parent-decay alpha spectra (from NNDC/ENSDF):")
    print(f"{'Parent':<8} {'<alphas/decay>':>14} {'<E_alpha> MeV':>14}")
    for parent, d in summary.items():
        print(f"{parent:<8} {d['alphas_per_decay']:>14.4f} {d['mean_E_MeV']:>14.3f}")
    print()
    print("Individual emissions:")
    print(f"{'Parent':<8} {'Emitter':<8} {'E_MeV':>8} {'Branch':>10}")
    for c in CHAINS:
        print(f"{c.parent_chain:<8} {c.emitter:<8} {c.energy_MeV:>8.3f} {c.branching:>10.4f}")
    # Save as JSON for downstream scripts
    with open("results/01_decay_chains.json", "w") as f:
        json.dump({"summary": summary,
                   "emissions": [asdict(c) for c in CHAINS]}, f, indent=2)
    print("\nWrote results/01_decay_chains.json")

if __name__ == "__main__":
    main()
