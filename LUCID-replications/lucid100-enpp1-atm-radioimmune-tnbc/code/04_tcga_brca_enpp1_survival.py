#!/usr/bin/env python3
"""
04_tcga_brca_enpp1_survival.py

Strict-replication item: paper claims (Fig. 1g + Supp. Fig. 1d) that
elevated ENPP1 in TNBC patients correlates with shorter recurrence-free
or overall survival.

Approach: pull TCGA-BRCA mRNA + clinical from the cBioPortal public REST
API (no auth, no key, free). Subset to triple-negative tumors using the
official TCGA IHC/PAM50 fields where available; otherwise approximate
via PAM50 = "Basal" (the standard TNBC proxy in TCGA-BRCA). Split
patients into ENPP1-high vs ENPP1-low by median, fit a Kaplan-Meier
curve for overall survival (OS_MONTHS / OS_STATUS), and report
log-rank p plus median survival per group.

Lifelines is small and pure-Python; we install it if missing.
"""

import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
FIG = ROOT / "figures"
RES.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

CBIO = "https://www.cbioportal.org/api"
STUDY = "brca_tcga_pan_can_atlas_2018"
PROFILE_MRNA = f"{STUDY}_rna_seq_v2_mrna_median_Zscores"
PROFILE_RSEM = f"{STUDY}_rna_seq_v2_mrna"
CLIN_LIST = f"{STUDY}_all"


def http_json(path: str, params: dict | None = None, method: str = "GET",
              body=None) -> object:
    url = f"{CBIO}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {"Accept": "application/json"}
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def main() -> None:
    # 1. Resolve ENPP1 -> Entrez id
    enpp1 = http_json("/genes/ENPP1")
    entrez = enpp1["entrezGeneId"]
    print(f"ENPP1 entrez={entrez}")

    # 2. Pull mRNA RSEM values for ENPP1 across all TCGA-BRCA samples
    rsem = http_json(
        f"/molecular-profiles/{PROFILE_RSEM}/molecular-data",
        params={"sampleListId": CLIN_LIST, "entrezGeneId": entrez},
    )
    print(f"RSEM rows: {len(rsem)}")
    if not rsem:
        # try z-score profile as a fallback
        rsem = http_json(
            f"/molecular-profiles/{PROFILE_MRNA}/molecular-data",
            params={"sampleListId": CLIN_LIST, "entrezGeneId": entrez},
        )
        print(f"Z-score fallback rows: {len(rsem)}")
    # rsem rows: sampleId, patientId, value

    # 3. Pull clinical data: PAM50 + OS_MONTHS + OS_STATUS for all patients
    clin = http_json(
        f"/studies/{STUDY}/clinical-data",
        params={"clinicalDataType": "PATIENT", "projection": "SUMMARY"},
    )
    print(f"Patient clinical rows (raw): {len(clin)}")

    sample_clin = http_json(
        f"/studies/{STUDY}/clinical-data",
        params={"clinicalDataType": "SAMPLE", "projection": "SUMMARY"},
    )
    print(f"Sample clinical rows (raw): {len(sample_clin)}")

    # Pivot to dicts
    pat = {}
    for row in clin:
        pid = row["patientId"]
        pat.setdefault(pid, {})[row["clinicalAttributeId"]] = row["value"]

    samp = {}
    for row in sample_clin:
        sid = row["sampleId"]
        samp.setdefault(sid, {
            "patientId": row["patientId"],
        })[row["clinicalAttributeId"]] = row["value"]

    # 4. Build dataframe
    import pandas as pd

    rows = []
    for r in rsem:
        sid = r["sampleId"]
        pid = r["patientId"]
        rows.append({
            "sampleId": sid,
            "patientId": pid,
            "ENPP1_rsem": r.get("value"),
            "PAM50": samp.get(sid, {}).get("SUBTYPE")
                     or pat.get(pid, {}).get("SUBTYPE"),
            "ER_STATUS": (samp.get(sid, {}).get("ER_STATUS_BY_IHC")
                          or pat.get(pid, {}).get("ER_STATUS_BY_IHC")),
            "PR_STATUS": (samp.get(sid, {}).get("PR_STATUS_BY_IHC")
                          or pat.get(pid, {}).get("PR_STATUS_BY_IHC")),
            "HER2_STATUS": (samp.get(sid, {}).get("IHC_HER2")
                            or pat.get(pid, {}).get("IHC_HER2")),
            "OS_MONTHS": pat.get(pid, {}).get("OS_MONTHS"),
            "OS_STATUS": pat.get(pid, {}).get("OS_STATUS"),
            "RFS_MONTHS": pat.get(pid, {}).get("DFS_MONTHS"),
            "RFS_STATUS": pat.get(pid, {}).get("DFS_STATUS"),
        })
    df = pd.DataFrame(rows)
    print(f"Joined rows: {len(df)}")
    print("PAM50 counts:")
    print(df["PAM50"].value_counts(dropna=False))
    print("ER counts:", df["ER_STATUS"].value_counts(dropna=False).to_dict())

    df.to_csv(RES / "tcga_brca_enpp1_table.tsv", sep="\t", index=False)

    # 5. Two TNBC definitions: PAM50=Basal, and ER-/PR-/HER2- by IHC
    df["is_basal"] = df["PAM50"].astype(str).str.lower().eq("brca_basal") | \
                     df["PAM50"].astype(str).str.lower().eq("basal")
    df["is_ihc_tnbc"] = (
        df["ER_STATUS"].astype(str).str.lower().eq("negative") &
        df["PR_STATUS"].astype(str).str.lower().eq("negative") &
        df["HER2_STATUS"].astype(str).str.lower().eq("negative")
    )

    results = {}

    def km(df_sub: "pd.DataFrame", time_col: str, status_col: str,
           label: str) -> dict:
        sub = df_sub.dropna(subset=["ENPP1_rsem", time_col, status_col]).copy()
        sub["ENPP1_rsem"] = sub["ENPP1_rsem"].astype(float)
        sub[time_col] = pd.to_numeric(sub[time_col], errors="coerce")
        sub = sub.dropna(subset=[time_col])
        if len(sub) < 20:
            return {"n": len(sub), "skip": "too few samples"}
        med = sub["ENPP1_rsem"].median()
        sub["enpp1_group"] = (sub["ENPP1_rsem"] > med).map(
            {True: "high", False: "low"})

        # status: "1:DECEASED" / "0:LIVING"  for OS; same shape for DFS
        sub["event"] = sub[status_col].astype(str).str.startswith("1")

        try:
            from lifelines import KaplanMeierFitter
            from lifelines.statistics import logrank_test
        except ImportError:
            return {"n": len(sub), "skip": "lifelines missing"}

        hi = sub[sub.enpp1_group == "high"]
        lo = sub[sub.enpp1_group == "low"]

        lr = logrank_test(hi[time_col], lo[time_col],
                          event_observed_A=hi.event,
                          event_observed_B=lo.event)

        # median survival
        def med_surv(s):
            kmf = KaplanMeierFitter().fit(s[time_col], s.event)
            return float(kmf.median_survival_time_)

        return {
            "label": label,
            "n_total": int(len(sub)),
            "n_high": int(len(hi)),
            "n_low": int(len(lo)),
            "median_ENPP1_rsem": float(med),
            "logrank_p": float(lr.p_value),
            "logrank_chi2": float(lr.test_statistic),
            "median_surv_high": med_surv(hi),
            "median_surv_low": med_surv(lo),
            "events_high": int(hi.event.sum()),
            "events_low": int(lo.event.sum()),
        }

    # Whole BRCA cohort (sanity baseline)
    results["BRCA_all_OS"] = km(df, "OS_MONTHS", "OS_STATUS", "all_BRCA_OS")
    results["BRCA_all_RFS"] = km(df, "RFS_MONTHS", "RFS_STATUS", "all_BRCA_RFS")

    # PAM50 basal
    results["PAM50_Basal_OS"] = km(df[df.is_basal], "OS_MONTHS", "OS_STATUS",
                                   "PAM50_Basal_OS")
    results["PAM50_Basal_RFS"] = km(df[df.is_basal], "RFS_MONTHS", "RFS_STATUS",
                                    "PAM50_Basal_RFS")

    # IHC-defined TNBC
    results["IHC_TNBC_OS"] = km(df[df.is_ihc_tnbc], "OS_MONTHS", "OS_STATUS",
                                "IHC_TNBC_OS")
    results["IHC_TNBC_RFS"] = km(df[df.is_ihc_tnbc], "RFS_MONTHS", "RFS_STATUS",
                                 "IHC_TNBC_RFS")

    (RES / "tcga_brca_enpp1_km.json").write_text(json.dumps(results, indent=2))

    print("\n=== KM results: ENPP1-high vs ENPP1-low (median split) ===")
    for k, v in results.items():
        if "skip" in v:
            print(f"{k}: skip ({v['skip']}, n={v.get('n')})")
        else:
            print(f"{k}: n={v['n_total']} (hi={v['n_high']} ev={v['events_high']} "
                  f"/ lo={v['n_low']} ev={v['events_low']}) "
                  f"med_surv hi={v['median_surv_high']} lo={v['median_surv_low']} "
                  f"logrank_p={v['logrank_p']:.3g}")

    # 6. KM plot for the IHC-TNBC OS cohort if it had enough events
    try:
        from lifelines import KaplanMeierFitter
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axs = plt.subplots(1, 2, figsize=(11, 4.5))
        for ax, (label, panel_df) in zip(
            axs,
            [("PAM50 Basal", df[df.is_basal]),
             ("IHC TNBC (ER-/PR-/HER2-)", df[df.is_ihc_tnbc])],
        ):
            sub = panel_df.dropna(subset=["ENPP1_rsem", "OS_MONTHS",
                                          "OS_STATUS"]).copy()
            sub["OS_MONTHS"] = pd.to_numeric(sub["OS_MONTHS"], errors="coerce")
            sub = sub.dropna(subset=["OS_MONTHS"])
            if len(sub) < 10:
                ax.set_title(f"{label} (too few; n={len(sub)})")
                continue
            sub["event"] = sub["OS_STATUS"].astype(str).str.startswith("1")
            med = sub["ENPP1_rsem"].astype(float).median()
            for grp, name in [(sub[sub.ENPP1_rsem > med], "ENPP1-high"),
                              (sub[sub.ENPP1_rsem <= med], "ENPP1-low")]:
                kmf = KaplanMeierFitter()
                kmf.fit(grp["OS_MONTHS"], grp["event"], label=name)
                kmf.plot_survival_function(ax=ax, ci_show=False)
            ax.set_title(f"{label} OS (n={len(sub)})")
            ax.set_xlabel("Months")
            ax.set_ylabel("Survival probability")
        fig.suptitle("TCGA-BRCA: ENPP1-high vs ENPP1-low overall survival")
        fig.tight_layout()
        fig.savefig(FIG / "fig5_tcga_brca_enpp1_km.png", dpi=140)
        plt.close(fig)
        print("Wrote", FIG / "fig5_tcga_brca_enpp1_km.png")
    except Exception as e:
        print(f"KM plot skipped: {e}")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.URLError as e:
        print(f"Network error talking to cBioPortal: {e}", file=sys.stderr)
        sys.exit(2)
