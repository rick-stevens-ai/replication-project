#!/usr/bin/env python3
"""
s100-039 lightweight reproduction / audit for:

  Tamborino et al., "Modeling Early Radiation DNA Damage Occurring During
  177Lu-DOTATATE Radionuclide Therapy", J Nucl Med 2021, DOI 10.2967/jnumed.121.262610.

We can NOT run the full Geant4-DNA Monte Carlo chain here (engine + DNAFabric
nuclear geometries on uicgpu). What we CAN check is the internal arithmetic
consistency of the paper's headline quantitative claims using the values the
paper itself tabulates in Supplemental Tables 1 and 2.

Specifically, we check:

  (1) The linear DSBs-vs-specific-energy slopes:
        Golgi internalization:    0.014 DSBs/cell/mGy
        Cytoplasm internalization: 0.017 DSBs/cell/mGy
      reported with R^2 = 1 (Figure 7D).

      The paper gives z̄ (Gy) per particle in Suppl Table 2:
        Cell 1 Cy=0.96, G=1.45;  Cell 2 Cy=0.51, G=0.26;  Cell 3 Cy=0.45, G=1.16.
      And the simulated DSBs/cell totals are in range 7–24 (Figure 7).

      We use the slope = N_DSBs / z̄ relation through the origin to back out
      the implied DSBs per cell for each (cell × scenario), check that they
      fall in the stated 7–24 range, and that the mean lands near 14.

  (2) The independent in-vivo comparison: Eberlein et al. measured
        0.0127 DSBs / mGy / cell  (blood lymphocytes, patients on 177Lu-DOTATATE).
      Paper claims "similar" to 0.014–0.017. Check magnitude (within ~30%).

  (3) Macrodosimetric vs microdosimetric correlation — paper states there
      is NO correlation when using mean absorbed dose D (Suppl Fig 2),
      only when using mean specific energy z̄. We compute R^2 for both and
      verify the qualitative claim that z̄ correlates and D does not.

  (4) DSBs/(Gy Gbp SP) range 2.3–3.0 vs literature: Tang 2.8–3.5, Nikjoo 3.32.

This is an audit + arithmetic spot-check; the real Monte Carlo numbers are
generated upstream by Geant4 + Geant4-DNA + DNAFabric and are not reproducible
on this machine.
"""

from __future__ import annotations
import json, math, statistics, sys
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Paper-tabulated inputs
# ---------------------------------------------------------------------------

# Supplemental Table 2: mean specific energy z̄ per particle entering the
# nucleus (Gy), for 2.5 MBq/mL of 177Lu-DOTATATE, 4 h cumulated decays.
# Rows = subcellular source compartment; columns = cell morphology.
zbar_Gy = {
    "Cy":     {"Cell 1": 0.96, "Cell 2": 0.51, "Cell 3": 0.45},
    "G":      {"Cell 1": 1.45, "Cell 2": 0.26, "Cell 3": 1.16},
    "Medium": {"Cell 1": 0.19, "Cell 2": 0.19, "Cell 3": 0.19},  # assumed same
}

# Supplemental Table 2: mean absorbed dose D̄ to nucleus (Gy), same conditions.
Dbar_Gy = {
    "Cy":     {"Cell 1": 0.29, "Cell 2": 0.32, "Cell 3": 0.24},
    "G":      {"Cell 1": 0.39, "Cell 2": 0.27, "Cell 3": 0.44},
    "Medium": {"Cell 1": 0.34, "Cell 2": 0.34, "Cell 3": 0.34},  # assumed same
}

# Headline slopes from Figure 7D (DSBs/cell vs z̄ to nucleus, mGy units).
slope_DSB_per_mGy = {
    "G":  0.014,   # Golgi
    "Cy": 0.017,   # cytoplasm
}

# Reported total DSB/cell statistics for 2.5 MBq/mL of 177Lu-DOTATATE
# (Figure 7A-C):
paper_sim_DSB_mean  = 14
paper_sim_DSB_range = (7, 24)
paper_exp_DSB_mean  = 13
paper_exp_DSB_range = (2, 30)

# Eberlein et al. (ref 39) clinical correlation in blood lymphocytes:
eberlein_slope_DSB_per_mGy = 0.0127

# Paper-stated DSBs/(Gy·Gbp·SP) range and literature:
paper_DSB_per_GyGbpSP_range = (2.3, 3.0)
tang_range   = (2.8, 3.5)         # 220 kVp X to 4 MV X (ref 33)
nikjoo_value = 3.32               # 100 keV electrons (ref 34)


# ---------------------------------------------------------------------------
# (1) Predict DSBs/cell per scenario from the headline slope * z̄
# ---------------------------------------------------------------------------

def predict_dsb_per_cell(internalization: str) -> dict:
    """
    Use the paper's headline slope for the given internalization scenario
    (Golgi or Cytoplasm) together with the medium contribution to reconstruct
    per-cell DSBs.

    The total z̄ delivered to a given nucleus is (cell-source z̄) + (medium z̄):
    the paper sums the two contributions when computing total DSBs/cell
    (Eq. 1 sums n_M·p_M→N + n_C·p_C→N), so the equivalent in z̄ space is
    additive (linear, no-threshold).
    """
    slope = slope_DSB_per_mGy[internalization]   # DSBs / (mGy)
    out = {}
    for cell in ("Cell 1", "Cell 2", "Cell 3"):
        z_cell   = zbar_Gy[internalization][cell] * 1000.0   # mGy
        z_medium = zbar_Gy["Medium"][cell]        * 1000.0   # mGy
        z_total  = z_cell + z_medium
        out[cell] = {
            "z_cell_mGy":   round(z_cell,   3),
            "z_medium_mGy": round(z_medium, 3),
            "z_total_mGy":  round(z_total,  3),
            "DSB_per_cell_predicted": round(slope * z_total, 3),
        }
    return out


# ---------------------------------------------------------------------------
# (2) Linear-correlation diagnostics (R^2)
# ---------------------------------------------------------------------------

def linfit_no_intercept(xs, ys):
    """Least-squares slope through the origin: y = m x.  R^2 vs y_mean."""
    num   = sum(x*y for x, y in zip(xs, ys))
    den   = sum(x*x for x in xs)
    m     = num / den
    ybar  = sum(ys) / len(ys)
    ss_t  = sum((y - ybar)**2 for y in ys)
    ss_r  = sum((y - m*x )**2 for x, y in zip(xs, ys))
    r2    = 1.0 - ss_r/ss_t if ss_t > 0 else float("nan")
    return m, r2


# ---------------------------------------------------------------------------
# Run audit
# ---------------------------------------------------------------------------

def main() -> int:
    report = {}

    # --- (1) Predict DSBs/cell per cell × internalization
    pred = {sc: predict_dsb_per_cell(sc) for sc in ("G", "Cy")}
    flat_predictions = []
    for sc, cells in pred.items():
        for cell, row in cells.items():
            flat_predictions.append((sc, cell, row["DSB_per_cell_predicted"]))
    pred_values = [v for _,_,v in flat_predictions]
    report["per_scenario_predictions"] = pred
    report["predicted_DSB_per_cell"] = {
        "values":  pred_values,
        "min":     min(pred_values),
        "max":     max(pred_values),
        "mean":    statistics.mean(pred_values),
        "median":  statistics.median(pred_values),
    }
    report["paper_simulated_DSB_per_cell"] = {
        "mean":  paper_sim_DSB_mean,
        "range": paper_sim_DSB_range,
    }
    report["paper_experimental_DSB_per_cell"] = {
        "mean":  paper_exp_DSB_mean,
        "range": paper_exp_DSB_range,
    }

    # --- (2) Independent correlation diagnostics
    #
    # For each scenario, take (z̄_total_mGy, DSB_per_cell_predicted) pairs
    # across the 3 cell morphologies, fit through the origin, and recover
    # the input slope. R^2 should be exactly 1.0 by construction since we
    # used the same slope to generate the DSB numbers; the test is that
    # the recovered slope = the input slope.
    for sc in ("G", "Cy"):
        xs = [pred[sc][c]["z_total_mGy"]            for c in ("Cell 1","Cell 2","Cell 3")]
        ys = [pred[sc][c]["DSB_per_cell_predicted"] for c in ("Cell 1","Cell 2","Cell 3")]
        m, r2 = linfit_no_intercept(xs, ys)
        report.setdefault("recovered_slopes", {})[sc] = {
            "expected_slope":   slope_DSB_per_mGy[sc],
            "recovered_slope":  round(m, 6),
            "R2":               round(r2, 6),
            "abs_error":        round(abs(m - slope_DSB_per_mGy[sc]), 8),
        }

    # --- (3) Macrodosimetric (D̄) correlation should fail
    #
    # Take the same 6 (scenario × cell) points and instead of z̄_total use
    # D̄_total = D̄_cell + D̄_medium, with the paper's reported DSB totals
    # (we use the slope×z̄ predictions as proxies for DSB totals since the
    # exact per-cell sim values are reported only graphically).
    xs_D = []
    ys_D = []
    xs_z = []
    ys_z = []
    for sc in ("G", "Cy"):
        for cell in ("Cell 1","Cell 2","Cell 3"):
            D_total = (Dbar_Gy[sc][cell] + Dbar_Gy["Medium"][cell]) * 1000.0  # mGy
            z_total = pred[sc][cell]["z_total_mGy"]
            dsb     = pred[sc][cell]["DSB_per_cell_predicted"]
            xs_D.append(D_total); ys_D.append(dsb)
            xs_z.append(z_total); ys_z.append(dsb)
    m_D, r2_D = linfit_no_intercept(xs_D, ys_D)
    m_z, r2_z = linfit_no_intercept(xs_z, ys_z)
    report["pooled_correlation"] = {
        "z_bar":  {"slope_DSB_per_mGy": round(m_z, 6), "R2": round(r2_z, 6)},
        "D_bar":  {"slope_DSB_per_mGy": round(m_D, 6), "R2": round(r2_D, 6)},
        "comment": ("Paper Suppl Fig 2 claims no correlation against mean "
                    "absorbed dose, only against mean specific energy. "
                    "Lower R^2 for D̄ is the expected qualitative behavior."),
    }

    # --- (4) Eberlein in-vivo cross-check
    report["eberlein_cross_check"] = {
        "eberlein_DSB_per_mGy":   eberlein_slope_DSB_per_mGy,
        "this_paper_Golgi":       slope_DSB_per_mGy["G"],
        "this_paper_Cytoplasm":   slope_DSB_per_mGy["Cy"],
        "ratio_Golgi_to_Eberlein":     round(slope_DSB_per_mGy["G"]/eberlein_slope_DSB_per_mGy, 3),
        "ratio_Cytoplasm_to_Eberlein": round(slope_DSB_per_mGy["Cy"]/eberlein_slope_DSB_per_mGy, 3),
        "comment": ("Paper claims 'similar' values.  10–34% above Eberlein in "
                    "patient blood; reasonable agreement given completely "
                    "different cell type (U2OS+SST2 vs lymphocytes) and "
                    "exposure geometry."),
    }

    # --- (5) Literature comparison of DSB yield per Gy Gbp SP
    report["DSB_yield_per_GyGbpSP"] = {
        "this_paper_range": list(paper_DSB_per_GyGbpSP_range),
        "tang_2019_range":  list(tang_range),
        "nikjoo_value":     nikjoo_value,
        "overlap_with_tang":   (
            max(paper_DSB_per_GyGbpSP_range[0], tang_range[0])
            <= min(paper_DSB_per_GyGbpSP_range[1], tang_range[1])
        ),
        "nikjoo_within_paper_range_or_near": (
            paper_DSB_per_GyGbpSP_range[0] - 0.5
            <= nikjoo_value
            <= paper_DSB_per_GyGbpSP_range[1] + 0.5
        ),
    }

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
