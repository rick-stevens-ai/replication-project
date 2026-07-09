"""
The per-replicate Day 1/2/3 data has up to 3 valid replicates per condition,
but the paper's summary means/SDs do not match the straight mean/SD of those
three values. Try to figure out what subset / weighting the paper used.

For each (timepoint, condition, phase), search:
  - all subsets of available replicates of size >= 2
  - report which subset reproduces the paper's reported mean & sd to high
    precision.

Also: maybe the paper accidentally swapped per-condition data, or used Day-1
replicates of one condition and Day-2 of another, etc. Check that too.
"""
import openpyxl, itertools, numpy as np, json

XLSX = "mendeley_data/Figure3Cell_Cycle_Analysis.xlsx"
wb = openpyxl.load_workbook(XLSX, data_only=True)
ws = wb["Sheet1"]
rows = [list(r) for r in ws.iter_rows(values_only=True)]

labels_groups = {
    "Control": [3, 4, 5, 6],
    "LDR":     [7, 8, 9, 10],
    "HDR":     [11, 12, 13, 14],
}
timepoints = {
    "12h":  (1, 2, 3),
    "Day1": (4, 5, 6),
    "Day2": (7, 8, 9),
    "Day3": (10, 11, 12),
}
phases = ["G0/G1", "S", "G2/M"]

def collect_with_labels(condition, tp):
    cols = timepoints[tp]
    out = []  # [(label, [G0/G1, S, G2/M]), ...]
    for ridx in labels_groups[condition]:
        r = rows[ridx]
        if not r or not isinstance(r[0], str):
            continue
        vals = [r[cols[0]], r[cols[1]], r[cols[2]]]
        if all(v is None for v in vals):
            continue
        if all((v == 0 or v is None) for v in vals):
            continue
        out.append((r[0], [float(v) if v is not None else None for v in vals]))
    return out

paper_summary = {
    "Day1": {
        "Control": {"G0/G1": (65.97, 1.559),  "S": (15.42, 3.132),  "G2/M": (17.97, 3.179)},
        "LDR":     {"G0/G1": (67.40, 1.240),  "S": (7.963, 2.221),  "G2/M": (24.44, 2.372)},
        "HDR":     {"G0/G1": (61.20, 1.838),  "S": (9.853, 0.4163), "G2/M": (28.70, 1.397)},
    },
    "Day2": {
        "Control": {"G0/G1": (67.28, 3.850),  "S": (5.943, 0.4827), "G2/M": (26.74, 3.467)},
        "LDR":     {"G0/G1": (63.32, 1.018),  "S": (3.783, 0.5320), "G2/M": (32.82, 1.477)},
        "HDR":     {"G0/G1": (59.28, 1.425),  "S": (5.837, 0.3755), "G2/M": (34.87, 1.107)},
    },
    "Day3": {
        "Control": {"G0/G1": (68.06, 3.632),  "S": (7.980, 1.520),  "G2/M": (23.94, 2.118)},
        "LDR":     {"G0/G1": (61.46, 0.9475), "S": (8.565, 0.7566), "G2/M": (29.95, 0.1909)},
        "HDR":     {"G0/G1": (57.06, 0.8402), "S": (8.000, 0.378),  "G2/M": (34.87, 1.132)},
    },
}

# Also check if the paper means *include the 12h Control/LDR/HDR rep4* somehow.
# The 12h block has 4 replicates per condition; Day1+ only 3.
# Try: combining the 12h replicate 4 row into Day1, Day2, or Day3.

def stats(vals):
    if len(vals) < 2:
        return None
    return float(np.mean(vals)), float(np.std(vals, ddof=1))

def close(ab, cd, tol_mean=0.05, tol_sd=0.05):
    if ab is None or cd is None: return False
    return abs(ab[0]-cd[0]) <= tol_mean and abs(ab[1]-cd[1]) <= tol_sd

# All available per-replicate values across both Day1..Day3 AND 12h rep4
# Note: 12h-rep4 row in the raw data only has 12h values; columns Day1..Day3 are blank
# So 12h-rep4 can't actually contribute to Day1..Day3 cell counts. Confirm.
print("=== 12h-rep4 row content (cols 1..12) ===")
for cond in labels_groups:
    ridx = labels_groups[cond][-1]
    print(cond, rows[ridx][:13])

# Try all subsets across (Control rep1..3, LDR rep1..3, HDR rep1..3) for each
# timepoint to see if any combination produces the paper's summary.
for tp in ("Day1", "Day2", "Day3"):
    print(f"\n--- {tp} subset search ---")
    for cond in labels_groups:
        data = collect_with_labels(cond, tp)  # list of (label, [g, s, g2m])
        # only Day1+ -> normally 3 entries
        n_avail = len(data)
        for size in range(2, n_avail+1):
            for combo in itertools.combinations(range(n_avail), size):
                labels = [data[i][0] for i in combo]
                g_vals = [data[i][1][0] for i in combo if data[i][1][0] is not None]
                s_vals = [data[i][1][1] for i in combo if data[i][1][1] is not None]
                m_vals = [data[i][1][2] for i in combo if data[i][1][2] is not None]
                if len(g_vals)<2 or len(s_vals)<2 or len(m_vals)<2: continue
                g_st, s_st, m_st = stats(g_vals), stats(s_vals), stats(m_vals)
                if (close(g_st, paper_summary[tp][cond]["G0/G1"]) and
                    close(s_st, paper_summary[tp][cond]["S"]) and
                    close(m_st, paper_summary[tp][cond]["G2/M"])):
                    print(f"  {cond}: MATCH using replicates {labels}")
                    print(f"     G0/G1 {g_st}   S {s_st}   G2/M {m_st}")
        # Also try cross-condition contamination: e.g., paper's "Control Day 1" stats
        # come from mixing one or two LDR/HDR replicates by mistake.
    # Try every cross-condition combination, size 3
    pool = []
    for cond in labels_groups:
        for label, vals in collect_with_labels(cond, tp):
            pool.append((cond, label, vals))
    for cond in labels_groups:
        target = paper_summary[tp][cond]
        n_pool = len(pool)
        for combo in itertools.combinations(range(n_pool), 3):
            labels = [(pool[i][0], pool[i][1]) for i in combo]
            g_vals = [pool[i][2][0] for i in combo if pool[i][2][0] is not None]
            s_vals = [pool[i][2][1] for i in combo if pool[i][2][1] is not None]
            m_vals = [pool[i][2][2] for i in combo if pool[i][2][2] is not None]
            if len(g_vals)<2 or len(s_vals)<2 or len(m_vals)<2: continue
            g_st, s_st, m_st = stats(g_vals), stats(s_vals), stats(m_vals)
            if (close(g_st, target["G0/G1"]) and
                close(s_st, target["S"]) and
                close(m_st, target["G2/M"])):
                print(f"  ** CROSS-COND match for paper-{cond}: {labels}")
                print(f"     G0/G1 {g_st}   S {s_st}   G2/M {m_st}")
