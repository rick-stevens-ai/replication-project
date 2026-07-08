#!/usr/bin/env python3
"""
FRONT 1 — Standard-of-care survival baselines for pediatric medulloblastoma.

Cohorts:
  A. mbl_icgc (Northcott 2017 ICGC, n=125) — has SUBGROUP + OS + PFS + M_STAGE + AGE + SEX + WGS mutation_count
  B. mbl_sickkids_2016 (n=46) — has SUBGROUP + OS_MONTHS for those with data
  C. Pooled (intersection of common fields)

For each cohort, compute C-index / HR / log-rank for the canonical MB prognostic
markers:
  - SUBGROUP (Group3 worst, Group4/SHH intermediate, WNT best)
  - SUBGROUP binary (Group3 vs others ; Group3 vs Group4)
  - METASTATIC (M+ stage)
  - AGE (≥10y vs <10y, and continuous)
  - SEX

Output JSON to /data/stevens/alter-pediatric-mb/results/f1_baseline.json

This is the bar the GSVD predictor must beat (analog to NBL Path-B FRONT 1).
"""
from __future__ import annotations
import json, sys
from pathlib import Path
import numpy as np

sys.path.insert(0, "/data/stevens/alter-pediatric-mb/code")
from survival_stats import (kaplan_meier_medians, log_rank, cox_univariate,
                             concordance_index)

DATA = Path("/data/stevens/alter-pediatric-mb/data")
RES  = Path("/data/stevens/alter-pediatric-mb/results")
RES.mkdir(parents=True, exist_ok=True)


def load_clinical(study_id: str) -> dict:
    with open(DATA / f"{study_id}_clinical.json") as f:
        return json.load(f)


def os_months_to_days(months):
    # NBL pipeline used days; here we keep months but use days conversion if needed.
    # survival_stats uses arbitrary time units; we'll use months directly.
    return months


def parse_os(rec):
    """Return (time_months, event) or (nan, nan) if missing."""
    t = rec.get("OS_MONTHS")
    s = rec.get("OS_STATUS", "")
    if t is None or t == "" or s == "":
        return np.nan, np.nan
    try:
        tm = float(t)
    except ValueError:
        return np.nan, np.nan
    # cBioPortal convention: "0:LIVING" / "1:DECEASED"
    if s.startswith("1") or "DECEASED" in s.upper():
        return tm, 1
    elif s.startswith("0") or "LIVING" in s.upper():
        return tm, 0
    return tm, np.nan


def normalize_subgroup(sg: str | None) -> str | None:
    if sg is None:
        return None
    s = sg.strip().upper().replace(" ", "")
    # variants we saw: 'SHH','Grp4','GRP 4','Group4','Group4 6','WNT','WNT 2'
    if s.startswith("SHH"):
        return "SHH"
    if s.startswith("WNT"):
        return "WNT"
    if "GRP3" in s or "GROUP3" in s:
        return "Group3"
    if "GRP4" in s or "GROUP4" in s:
        return "Group4"
    return None


def build_cohort(study_id: str):
    """Load study, parse OS+SUBGROUP+METASTATIC+AGE+SEX into numpy arrays."""
    cl = load_clinical(study_id)
    rows = []
    for pid, rec in cl.items():
        t, e = parse_os(rec)
        sg = normalize_subgroup(rec.get("SUBGROUP"))
        age = rec.get("AGE")
        try:
            age = float(age) if age not in (None, "") else np.nan
        except (TypeError, ValueError):
            age = np.nan
        sex = rec.get("SEX", "").strip().upper()
        sex_code = 0 if sex.startswith("M") else (1 if sex.startswith("F") else np.nan)
        m_raw = rec.get("CLIN_M_STAGE", rec.get("M_STAGE", ""))
        m_raw = str(m_raw).strip().upper()
        if m_raw.startswith("M0"):
            m_code = 0
        elif m_raw.startswith("M") and len(m_raw) > 1:  # M1..M4
            m_code = 1
        else:
            m_code = np.nan
        rows.append({"patient": pid, "t": t, "e": e, "subgroup": sg,
                     "age": age, "sex": sex_code, "m_stage": m_code})
    return rows


def front1_for_cohort(study_id: str, label: str) -> dict:
    rows = build_cohort(study_id)
    print(f"\n=== {label} (study={study_id}, n={len(rows)}) ===")
    out = {"study": study_id, "label": label, "n_total": len(rows)}

    # Subgroup distribution
    from collections import Counter
    sg_count = Counter([r["subgroup"] for r in rows])
    print(f"  subgroup distribution: {dict(sg_count)}")
    out["subgroup_distribution"] = dict(sg_count)

    # Filter for survival analyses
    surv = [r for r in rows if not np.isnan(r["t"]) and not np.isnan(r["e"]) and r["t"] > 0]
    print(f"  with valid OS: {len(surv)}")
    out["n_with_os"] = len(surv)
    if len(surv) < 10:
        print("  too few for survival analysis")
        return out

    t = np.array([r["t"] for r in surv], dtype=float)
    e = np.array([r["e"] for r in surv], dtype=int)

    # ------ Indicator 1: subgroup ordered prognostic score ------
    sg_vec = [r["subgroup"] for r in surv]
    # Established MB prognostic ordering (worst -> best):
    # Group3 > Group4 > SHH > WNT (lower score = better prognosis)
    sg_order = {"WNT": 0, "SHH": 1, "Group4": 2, "Group3": 3}
    sg_known = [i for i, s in enumerate(sg_vec) if s in sg_order]
    if len(sg_known) >= 10:
        ti = t[sg_known]; ei = e[sg_known]
        score = np.array([sg_order[sg_vec[i]] for i in sg_known], dtype=float)
        try:
            cox = cox_univariate(ti, ei, score)
            ci  = concordance_index(ti, ei, score)
            out["subgroup_ordered"] = {
                "n": int(len(sg_known)),
                "cox_hr": round(cox.hr, 4),
                "cox_ci": [round(cox.ci_lower, 4), round(cox.ci_upper, 4)],
                "cox_wald_p": cox.wald_p,
                "concordance": round(ci, 4),
            }
            print(f"  subgroup ordered (Grp3>Grp4>SHH>WNT): HR={cox.hr:.3f} ({cox.ci_lower:.2f}-{cox.ci_upper:.2f}) P={cox.wald_p:.3g} C={ci:.3f}")
        except Exception as ex:
            out["subgroup_ordered"] = {"error": str(ex)}

    # ------ Indicator 2: subgroup Group3 binary ------
    sg_g3 = np.array([1 if s == "Group3" else 0 for s in sg_vec], dtype=int)
    try:
        lr = log_rank(t, e, sg_g3)
        cox = cox_univariate(t, e, sg_g3.astype(float))
        ci  = concordance_index(t, e, sg_g3.astype(float))
        out["group3_binary"] = {
            "n": int(len(surv)),
            "n_g3": int(sg_g3.sum()),
            "cox_hr": round(cox.hr, 4),
            "cox_ci": [round(cox.ci_lower, 4), round(cox.ci_upper, 4)],
            "cox_wald_p": cox.wald_p,
            "logrank_p": lr.p_value,
            "concordance": round(ci, 4),
        }
        print(f"  Group3 vs rest: n={len(surv)} (G3={sg_g3.sum()}) HR={cox.hr:.3f} logrank P={lr.p_value:.3g} C={ci:.3f}")
    except Exception as ex:
        out["group3_binary"] = {"error": str(ex)}

    # ------ Indicator 3: Group3 vs Group4 only (the CN-driven pair) ------
    g3g4 = [i for i, s in enumerate(sg_vec) if s in ("Group3", "Group4")]
    if len(g3g4) >= 10:
        ti = t[g3g4]; ei = e[g3g4]
        sg34 = np.array([1 if sg_vec[i] == "Group3" else 0 for i in g3g4], dtype=int)
        try:
            lr = log_rank(ti, ei, sg34)
            cox = cox_univariate(ti, ei, sg34.astype(float))
            ci  = concordance_index(ti, ei, sg34.astype(float))
            out["group3_vs_group4"] = {
                "n": int(len(g3g4)),
                "n_g3": int(sg34.sum()),
                "n_g4": int(len(g3g4) - sg34.sum()),
                "cox_hr": round(cox.hr, 4),
                "cox_ci": [round(cox.ci_lower, 4), round(cox.ci_upper, 4)],
                "cox_wald_p": cox.wald_p,
                "logrank_p": lr.p_value,
                "concordance": round(ci, 4),
            }
            print(f"  Group3 vs Group4 only: n={len(g3g4)} HR={cox.hr:.3f} logrank P={lr.p_value:.3g} C={ci:.3f}")
        except Exception as ex:
            out["group3_vs_group4"] = {"error": str(ex)}

    # ------ Indicator 4: M-stage ------
    mvec = np.array([r["m_stage"] for r in surv], dtype=float)
    valid = ~np.isnan(mvec)
    if valid.sum() >= 10 and len(np.unique(mvec[valid])) > 1:
        ti = t[valid]; ei = e[valid]; m = mvec[valid].astype(int)
        try:
            lr = log_rank(ti, ei, m)
            cox = cox_univariate(ti, ei, m.astype(float))
            ci  = concordance_index(ti, ei, m.astype(float))
            out["m_stage_binary"] = {
                "n": int(valid.sum()),
                "n_metastatic": int(m.sum()),
                "cox_hr": round(cox.hr, 4),
                "cox_ci": [round(cox.ci_lower, 4), round(cox.ci_upper, 4)],
                "cox_wald_p": cox.wald_p,
                "logrank_p": lr.p_value,
                "concordance": round(ci, 4),
            }
            print(f"  M+ vs M0: n={valid.sum()} HR={cox.hr:.3f} P={lr.p_value:.3g} C={ci:.3f}")
        except Exception as ex:
            out["m_stage_binary"] = {"error": str(ex)}

    # ------ Indicator 5: AGE ------
    age = np.array([r["age"] for r in surv], dtype=float)
    valid = ~np.isnan(age)
    if valid.sum() >= 10:
        ti = t[valid]; ei = e[valid]; a = age[valid]
        # continuous
        try:
            cox = cox_univariate(ti, ei, a)
            ci  = concordance_index(ti, ei, a)
            out["age_continuous"] = {
                "n": int(valid.sum()),
                "cox_hr": round(cox.hr, 4),
                "cox_ci": [round(cox.ci_lower, 4), round(cox.ci_upper, 4)],
                "cox_wald_p": cox.wald_p,
                "concordance": round(ci, 4),
            }
            print(f"  AGE continuous: n={valid.sum()} HR={cox.hr:.3f} per yr P={cox.wald_p:.3g} C={ci:.3f}")
        except Exception as ex:
            out["age_continuous"] = {"error": str(ex)}
        # binary (≥10 yr — adult-like)
        ab = (a >= 10).astype(int)
        if 5 <= ab.sum() <= len(ab) - 5:
            try:
                lr = log_rank(ti, ei, ab)
                cox = cox_univariate(ti, ei, ab.astype(float))
                ci  = concordance_index(ti, ei, ab.astype(float))
                out["age_ge10"] = {
                    "n": int(valid.sum()),
                    "n_ge10": int(ab.sum()),
                    "cox_hr": round(cox.hr, 4),
                    "cox_ci": [round(cox.ci_lower, 4), round(cox.ci_upper, 4)],
                    "cox_wald_p": cox.wald_p,
                    "logrank_p": lr.p_value,
                    "concordance": round(ci, 4),
                }
                print(f"  AGE≥10y: n={valid.sum()} ({ab.sum()} ≥10) HR={cox.hr:.3f} P={lr.p_value:.3g} C={ci:.3f}")
            except Exception as ex:
                out["age_ge10"] = {"error": str(ex)}

    # ------ Indicator 6: SEX ------
    sx = np.array([r["sex"] for r in surv], dtype=float)
    valid = ~np.isnan(sx)
    if valid.sum() >= 10:
        ti = t[valid]; ei = e[valid]; s = sx[valid].astype(int)
        try:
            lr = log_rank(ti, ei, s)
            cox = cox_univariate(ti, ei, s.astype(float))
            ci  = concordance_index(ti, ei, s.astype(float))
            out["sex_female"] = {
                "n": int(valid.sum()),
                "n_female": int(s.sum()),
                "cox_hr": round(cox.hr, 4),
                "cox_ci": [round(cox.ci_lower, 4), round(cox.ci_upper, 4)],
                "cox_wald_p": cox.wald_p,
                "logrank_p": lr.p_value,
                "concordance": round(ci, 4),
            }
            print(f"  Female vs male: n={valid.sum()} HR={cox.hr:.3f} P={lr.p_value:.3g} C={ci:.3f}")
        except Exception as ex:
            out["sex_female"] = {"error": str(ex)}

    return out


def main():
    results = {
        "engine": "scipy fallback (lifelines not installed)",
        "time_unit": "months",
        "subgroup_ordering": "WNT(0) < SHH(1) < Group4(2) < Group3(3)  (worse OS = higher)",
    }
    for sid, label in [("mbl_icgc", "ICGC Northcott 2017"),
                       ("mbl_sickkids_2016", "SickKids 2016")]:
        results[sid] = front1_for_cohort(sid, label)
    out_path = RES / "f1_baseline.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nwrote {out_path}")
    return results


if __name__ == "__main__":
    main()
