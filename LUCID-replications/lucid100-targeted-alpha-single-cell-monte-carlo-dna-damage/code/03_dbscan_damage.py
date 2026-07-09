"""Python re-implementation + unit test of the DBSCAN-based DNA damage
scorer described in Jolly & Fielding 2025 (Methods, 'Quantifying DNA
damage with DBSCAN').

Rules from the paper:
  - For each ionisation event with energy E (eV):
      P(direct DNA hit) = 0,                    E < 5  eV
                       = (E - 5)/(37.5 - 5),    5 <= E <= 37.5 eV  (linear ramp)
                       = 1,                     E > 37.5 eV
  - A second random filter: only 16% of ionisations interact with DNA
    (DNA occupies 16% of nucleus volume), so multiply the above by 0.16
    OR equivalently Bernoulli-sample with p_DNA=0.16. We follow the
    paper's order: first 'is this an SSB?' then 'does it occur on a DNA
    strand?'.
  - Surviving events are SSBs.
  - DBSCAN with eps = 3.2 nm, min_samples = 2: clusters are DSBs.
    sDSB = cluster with exactly 2 SSBs.
    cDSB = cluster with 3+ SSBs.

Without TOPAS-nBio we cannot generate physical ionisation tracks. The
unit test here exercises the scorer on synthetic, hand-built ionisation
clouds whose expected SSB/DSB counts are known a priori. This validates
that the algorithmic pipeline is faithful to the paper's description, so
that when real TOPAS-nBio phase spaces are available the same scorer can
be plugged in for offline cross-checks.
"""
from __future__ import annotations
import json, math, os, sys
import numpy as np

try:
    from sklearn.cluster import DBSCAN
except ImportError:
    DBSCAN = None

EPS_NM = 3.2
P_DNA_FRAC = 0.16
E_THRESH_LOW_eV = 5.0
E_THRESH_HIGH_eV = 37.5

def ssb_probability(E_eV: float) -> float:
    if E_eV < E_THRESH_LOW_eV: return 0.0
    if E_eV >= E_THRESH_HIGH_eV: return 1.0
    return (E_eV - E_THRESH_LOW_eV) / (E_THRESH_HIGH_eV - E_THRESH_LOW_eV)

def score_damage(ionisations, rng=None, eps_nm=EPS_NM, p_dna=P_DNA_FRAC):
    """ionisations: iterable of (x_nm, y_nm, z_nm, E_eV).
    Returns dict with SSB, sDSB, cDSB counts and the SSB site list.
    """
    rng = rng or np.random.default_rng(0)
    ssb_sites = []
    for x, y, z, E in ionisations:
        p_ion_to_ssb = ssb_probability(E)
        if rng.random() < p_ion_to_ssb and rng.random() < p_dna:
            ssb_sites.append((x, y, z))
    if not ssb_sites:
        return {"SSB": 0, "sDSB": 0, "cDSB": 0, "n_ssb_sites": 0}
    arr = np.asarray(ssb_sites, dtype=float)
    if len(arr) < 2 or DBSCAN is None:
        return {"SSB": len(arr), "sDSB": 0, "cDSB": 0, "n_ssb_sites": len(arr)}
    labels = DBSCAN(eps=eps_nm, min_samples=2).fit_predict(arr)
    sdsb = cdsb = 0
    isolated_ssb = int(np.sum(labels == -1))
    for lab in set(labels):
        if lab == -1: continue
        size = int(np.sum(labels == lab))
        if size == 2: sdsb += 1
        elif size >= 3: cdsb += 1
    return {"SSB": isolated_ssb, "sDSB": sdsb, "cDSB": cdsb,
            "n_ssb_sites": len(arr)}

# ---- unit tests ----
def _build_two_close_ions():
    # Two ionisations 1 nm apart, both high-energy -> almost certainly 1 sDSB
    return [(0, 0, 0, 100.0), (1.0, 0, 0, 100.0)]

def _build_cluster_of_three():
    # Three high-E ionisations within eps -> 1 cDSB
    return [(0, 0, 0, 100.0), (1.0, 0, 0, 100.0), (2.0, 0, 0, 100.0)]

def _build_two_far_ions():
    # Two high-E ionisations 10 nm apart -> 2 isolated SSBs, 0 DSBs
    return [(0, 0, 0, 100.0), (10.0, 0, 0, 100.0)]

def _build_subthreshold():
    # E < 5 eV -> 0 SSBs
    return [(0, 0, 0, 3.0), (1.0, 0, 0, 3.0)]

def _build_ramp_check():
    # E = 21.25 eV is the midpoint -> p_ssb = 0.5; over 200k trials with
    # p_dna=1.0 we expect SSB count ~ 100k (1-2% tolerance).
    return [(i*100.0, 0, 0, 21.25) for i in range(200_000)]

def run_unit_tests():
    out = {}
    rng = np.random.default_rng(42)

    # 1. Two close, high E, p_DNA=1 -> 1 sDSB
    r = score_damage(_build_two_close_ions(), rng=rng, p_dna=1.0)
    out["close_pair_high_E"] = r
    assert r["sDSB"] == 1 and r["cDSB"] == 0 and r["SSB"] == 0, r

    # 2. Three close, high E, p_DNA=1 -> 1 cDSB
    r = score_damage(_build_cluster_of_three(), rng=rng, p_dna=1.0)
    out["triplet_high_E"] = r
    assert r["cDSB"] == 1 and r["sDSB"] == 0 and r["SSB"] == 0, r

    # 3. Two far ions, high E, p_DNA=1 -> 2 isolated SSBs
    r = score_damage(_build_two_far_ions(), rng=rng, p_dna=1.0)
    out["far_pair_high_E"] = r
    assert r["sDSB"] == 0 and r["cDSB"] == 0 and r["SSB"] == 2, r

    # 4. Sub-threshold -> 0 SSBs
    r = score_damage(_build_subthreshold(), rng=rng, p_dna=1.0)
    out["subthreshold"] = r
    assert r["SSB"] == 0 and r["sDSB"] == 0 and r["cDSB"] == 0, r

    # 5. Ramp check at midpoint: ~50% SSB
    r = score_damage(_build_ramp_check(), rng=np.random.default_rng(7),
                     p_dna=1.0)
    out["ramp_midpoint_p_dna_1"] = r
    p_obs = r["n_ssb_sites"] / 200_000
    assert abs(p_obs - 0.5) < 0.01, f"ramp midpoint p_obs={p_obs}"
    out["ramp_midpoint_p_obs"] = p_obs

    # 6. p_DNA effect: same ramp but p_dna=0.16 -> ~8% SSBs
    r = score_damage(_build_ramp_check(), rng=np.random.default_rng(11),
                     p_dna=0.16)
    out["ramp_midpoint_p_dna_016"] = r
    p_obs2 = r["n_ssb_sites"] / 200_000
    assert abs(p_obs2 - 0.5*0.16) < 0.005, f"with p_dna 0.16 p_obs={p_obs2}"
    out["ramp_midpoint_p_dna_016_p_obs"] = p_obs2

    return out

def main():
    if DBSCAN is None:
        print("ERROR: scikit-learn not installed; install with `pip install scikit-learn numpy`", file=sys.stderr)
        sys.exit(1)
    out = run_unit_tests()
    print(json.dumps(out, indent=2, default=int))
    os.makedirs("results", exist_ok=True)
    with open("results/03_dbscan_unit_test.json", "w") as f:
        json.dump(out, f, indent=2, default=int)
    print("\nAll DBSCAN damage-model unit tests PASSED.")

if __name__ == "__main__":
    main()
