#!/usr/bin/env python3
"""
Promotion-audit numerical checks for the structural NHEJ replication
(Friedland, Jacob, Kundrát, Radiat. Res. 173:677-688 (2010), DOI 10.1667/RR1965.1).

The target paper is paywalled (BioOne, no PMC, no preprint). These checks
therefore compare our re-implementation against OPEN-ACCESS sibling/anchor
papers and against the abstract's qualitative claims, instead of against
the target paper's own numerical tables.

Anchors used (all OA):
  * Henthorn et al. 2018 Sci Rep 8:2654, DOI 10.1038/s41598-018-21111-8.
    Cites RR1965, uses 25 nm synapsis radius, reports
    residual DSB fraction ~7.3% at 24 h (largely independent of LET).
  * Li, Reynolds, O'Neill 2014 PLoS One e85816, DOI 10.1371/journal.pone.0085816.
    Cites RR1965, fits sibling NHEJ scheme with rate constants in min^-1.
  * Literature consensus on biphasic kinetics:
    Rothkamm & Lobrich PNAS 2003, Karlsson & Stenerlow IJRB 2004.
    Fast component half-life ~10-30 min, slow component half-life
    ~2-4 h, ~5-10% residual at 24 h.

For each check we record PASS/FAIL/QUALITATIVE, the observed value,
the anchor value, and the tolerance used.

Output: results.json (machine-readable) plus stdout summary.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))


def load(name):
    with open(os.path.join(DATA, name)) as f:
        return json.load(f)


def first_dose(d, dose):
    for r in d["results"]:
        if abs(r["dose_gy"] - dose) < 1e-6:
            return r
    raise KeyError(dose)


def t_residual(rec, t_target):
    """Return residual fraction at the sample time nearest to t_target (min)."""
    times = rec["sample_times"]
    fracs = rec["mean_residual_fraction"]
    # require exact / nearest match
    best_i = min(range(len(times)), key=lambda i: abs(times[i] - t_target))
    return times[best_i], fracs[best_i]


def main():
    checks = []

    # --------------------------------------------------------------
    # Load all promotion-run datasets
    # --------------------------------------------------------------
    try:
        henth = load("promo_henthorn_anchor.json")          # tight geom
        loose30 = load("promo_loose_geom_pdirty30.json")    # loose geom, dirty 30%
        loose0 = load("promo_loose_geom_pdirty0.json")      # loose geom, no dirty
        ablation0 = load("promo_ablation_pdirty0.json")     # tight geom, no dirty
        dose_resp = load("dose_response.json")              # original tune2 sweep
        dose_mis = load("dose_response_misrejoin.json")     # original tune1 sweep
    except FileNotFoundError as e:
        print(f"missing input: {e}", file=sys.stderr)
        sys.exit(1)

    # --------------------------------------------------------------
    # C1 (abstract): biphasic (fast + slow) DSB rejoining curve.
    # Quantitative: at 5 min the residual fraction should already be
    # well below 1; at 24 h it should still be > 0 (a slow tail must
    # exist). Use the loose-geometry, p_dirty=0.30 run (closest to
    # the abstract's intended regime).
    # --------------------------------------------------------------
    rec = first_dose(loose30, 2.0)
    t5, f5 = t_residual(rec, 5.0)
    t60, f60 = t_residual(rec, 60.0)
    t240, f240 = t_residual(rec, 240.0)
    t1440, f1440 = t_residual(rec, 1440.0)
    biphasic = (f5 < 0.5) and (f60 > f240 * 1.5) and (f1440 > 0.001)
    # f60 > 1.5 * f240 means a meaningful slow phase between 1 h and 4 h
    checks.append(dict(
        id="C1_biphasic_shape",
        claim="Stochastic NHEJ reproduces biphasic (fast+slow) DSB rejoining curve",
        anchor="Rothkamm & Lobrich PNAS 2003 / Karlsson & Stenerlow IJRB 2004",
        condition="residual_5min < 0.5 AND residual_60min > 1.5 * residual_240min AND residual_24h > 0.1%",
        observed=dict(f5min=f5, f60min=f60, f240min=f240, f24h=f1440),
        verdict="PASS" if biphasic else "FAIL",
        kind="quantitative",
    ))

    # --------------------------------------------------------------
    # C1b: 24-h residual fraction within +-3x of Henthorn 2018 OA
    # anchor (~7.3%). Wide tolerance because we substituted PARTRAC
    # spatial input.
    # --------------------------------------------------------------
    anchor_henth = 0.073
    lo, hi = anchor_henth / 3.0, anchor_henth * 3.0
    match_henth = (lo <= f1440 <= hi)
    checks.append(dict(
        id="C1b_residual24h_vs_henthorn",
        claim="Residual DSB fraction at 24 h consistent with OA Henthorn 2018 (~7.3%)",
        anchor="Henthorn 2018 Sci Rep 8:2654 (~7.3% at 24h, largely LET-independent)",
        condition=f"{lo:.4f} <= residual_24h <= {hi:.4f}",
        observed=dict(f24h=f1440, anchor=anchor_henth),
        verdict="PASS" if match_henth else "FAIL",
        kind="quantitative",
    ))

    # --------------------------------------------------------------
    # C7 (abstract): dirty ends are the source of the slow rejoining
    # component. Test: with the same geometry, setting p_dirty=0 must
    # eliminate the slow tail (residual at 4 h drops by >= 10x AND
    # residual at 24 h drops by >= 5x).
    # Use the loose-geometry comparison (where geometry does not
    # confound).
    # --------------------------------------------------------------
    r30 = first_dose(loose30, 2.0)
    r0 = first_dose(loose0, 2.0)
    _, f4h_30 = t_residual(r30, 240.0)
    _, f4h_0 = t_residual(r0, 240.0)
    _, f24h_30 = t_residual(r30, 1440.0)
    _, f24h_0 = t_residual(r0, 1440.0)
    # avoid divide-by-zero: clip f4h_0, f24h_0 at 1e-4 (single-cell shot noise floor)
    fold_4h = f4h_30 / max(f4h_0, 1e-4)
    fold_24h = f24h_30 / max(f24h_0, 1e-4)
    dirty_drives_slow = (fold_4h >= 10.0) and (fold_24h >= 5.0)
    checks.append(dict(
        id="C7_dirty_drives_slow_tail",
        claim="Dirty (complex) DSBs are the source of the slow rejoining component",
        anchor="Abstract: 'three of four scenarios overestimate residual DSBs ... dirty-end processing is the multi-step slow contribution'",
        condition="residual_4h(dirty=30%)/residual_4h(dirty=0%) >= 10x AND ratio_24h >= 5x (loose-geometry regime)",
        observed=dict(
            f4h_pdirty30=f4h_30, f4h_pdirty0=f4h_0, fold_change_4h=fold_4h,
            f24h_pdirty30=f24h_30, f24h_pdirty0=f24h_0, fold_change_24h=fold_24h,
        ),
        verdict="PASS" if dirty_drives_slow else "FAIL",
        kind="quantitative",
    ))

    # --------------------------------------------------------------
    # C7-CONFOUND: under the tight-geometry (R_syn=25 nm, D=1e-4)
    # regime, the slow tail is dominated by FAILED SYNAPSIS, not by
    # dirty-end processing. This is a NEGATIVE FINDING that must be
    # surfaced honestly.
    # --------------------------------------------------------------
    rh30 = first_dose(henth, 2.0)
    ra0 = first_dose(ablation0, 2.0)
    _, f24h_henth30 = t_residual(rh30, 1440.0)
    _, f24h_abl0 = t_residual(ra0, 1440.0)
    diff = abs(f24h_henth30 - f24h_abl0)
    confound = (diff < 0.05)
    checks.append(dict(
        id="C7_confound_tight_geometry",
        claim="Under tight-geometry (R_syn=25nm, D=1e-4 um^2/min), the slow tail is dominated by failed synapsis, NOT by dirty-end processing",
        anchor="Negative control / internal consistency",
        condition="|residual_24h(dirty=30%) - residual_24h(dirty=0%)| < 0.05 (tight-geometry regime)",
        observed=dict(
            f24h_tight_pdirty30=f24h_henth30,
            f24h_tight_pdirty0=f24h_abl0,
            abs_difference=diff,
        ),
        verdict="PASS" if confound else "FAIL",
        kind="quantitative_negative_finding",
        note=("In the tight-geometry regime, dirty-end content does not affect "
              "long-time residual. This shows the structural replication's "
              "behavior is sensitive to the synapsis geometry parameters, "
              "which are exactly the parameters that the paper's 4 scenarios "
              "presumably vary - and which are inaccessible behind the paywall."),
    ))

    # --------------------------------------------------------------
    # C5 (abstract): mis-rejoined DSBs vs dose. Direction-of-effect:
    # mis-rejoin fraction should increase with dose (proximity-driven).
    # Use the original tune1 dose_response_misrejoin.json sweep.
    # --------------------------------------------------------------
    mis_pts = [(r["dose_gy"], r["misrejoin_fraction"]) for r in dose_mis["results"]]
    mis_pts.sort()
    # require monotone non-decreasing from 0.5 -> 10 Gy
    mono = all(mis_pts[i][1] <= mis_pts[i+1][1] + 0.02 for i in range(len(mis_pts)-1))
    # require >= 5x rise from 0.5 to 10 Gy
    rise = mis_pts[-1][1] / max(mis_pts[0][1], 1e-3)
    enough_rise = rise >= 5.0
    checks.append(dict(
        id="C5_misrejoin_rises_with_dose",
        claim="Mis-rejoin fraction increases with dose (proximity-driven misrepair)",
        anchor="Abstract; Forster 2019 HNSCC alpha_mr=0.02 Gy^-1, beta_mr=0.37 Gy^-2 (super-linear)",
        condition="monotone non-decreasing 0.5->10 Gy AND fold-change >= 5x",
        observed=dict(mis_fraction_curve=mis_pts, fold_change_05_to_10Gy=rise),
        verdict="PASS" if (mono and enough_rise) else "FAIL",
        kind="quantitative_trend",
    ))

    # --------------------------------------------------------------
    # C4 (abstract): three of four scenarios overestimate residual
    # DSBs at long times after low-dose IR. We have 2 scenarios; the
    # 'diffusive' scenario B (tune1 params) should overestimate
    # residuals vs the 'tethered' scenario A (tune2 params) at low dose.
    # --------------------------------------------------------------
    rA = first_dose(dose_resp, 0.5)
    rB = first_dose(dose_mis, 0.5)
    _, fA = t_residual(rA, 1440.0)
    _, fB = t_residual(rB, 1440.0)
    overest = fB > 5 * fA
    checks.append(dict(
        id="C4_scenarioB_overestimates_lowdose_residual",
        claim="At least one model scenario badly overestimates residual DSBs after low-dose IR",
        anchor="Abstract: 'three of the model scenarios obviously overestimate residual DSBs after long-term repair after low-dose irradiation'",
        condition="scenarioB_residual_24h(0.5 Gy) > 5 * scenarioA_residual_24h(0.5 Gy)",
        observed=dict(scenarioA_residual=fA, scenarioB_residual=fB, ratio=fB / max(fA, 1e-4)),
        verdict="PASS" if overest else "FAIL",
        kind="qualitative_with_quant_threshold",
    ))

    # --------------------------------------------------------------
    # Architecture self-consistency: DSB yield ~35/Gy/cell at 2 Gy.
    # --------------------------------------------------------------
    init_2gy = first_dose(loose30, 2.0)
    init_dsb = init_2gy["init_dsb"]
    expected = 35.0 * 2.0
    yield_ok = 0.85 * expected <= init_dsb <= 1.15 * expected
    checks.append(dict(
        id="A1_dsb_yield",
        claim="Initial DSB yield ~35/Gy/cell (low-LET gamma reference)",
        anchor="Karlsson & Stenerlow IJRB 2004 / Friedland group convention",
        condition=f"0.85*{expected} <= mean init_dsb <= 1.15*{expected}",
        observed=dict(mean_init_dsb=init_dsb, expected=expected),
        verdict="PASS" if yield_ok else "FAIL",
        kind="quantitative",
    ))

    # --------------------------------------------------------------
    # tally
    # --------------------------------------------------------------
    n_pass = sum(1 for c in checks if c["verdict"] == "PASS")
    n_total = len(checks)
    summary = dict(
        n_checks=n_total,
        n_pass=n_pass,
        pass_rate=n_pass / n_total,
        notes=(
            "Anchored to OA siblings (Henthorn 2018, Li 2014, Forster 2019) "
            "because target Friedland 2010 RR1965 paper is paywalled (BioOne, "
            "no PMC, no preprint). Cannot test paper's specific 4-scenario "
            "parameter table or per-dose numerical tables."
        ),
        access_status=dict(
            unpaywall="is_oa=False",
            europepmc="hasPDF=N, isOpenAccess=N, pmcid=null, inEPMC=N",
            scout_corpus="no hit for RR1965/Friedland 2010 (verified 2026-06-27)",
            bioone_html="returns 1161-byte challenge page (paywall, verified 2026-06-27)",
        ),
    )

    out = dict(summary=summary, checks=checks)
    with open(os.path.join(DATA, "..", "results.json"), "w") as f:
        json.dump(out, f, indent=2)

    print(f"Wrote results.json ({n_pass}/{n_total} PASS)\n")
    for c in checks:
        v = c["verdict"]
        marker = "✓" if v == "PASS" else ("✗" if v == "FAIL" else "?")
        print(f"  {marker} {c['id']}: {v}  ({c['kind']})")
        for k, val in c["observed"].items():
            if isinstance(val, float):
                print(f"      {k}={val:.4f}")
            elif isinstance(val, list):
                print(f"      {k}={val}")
            else:
                print(f"      {k}={val}")
        if "note" in c:
            print(f"      NOTE: {c['note']}")


if __name__ == "__main__":
    main()
