"""
Apoptosis (Fig 4) replication.
Per-replicate %population in {Healthy, Early-apoptotic, Mid-apoptotic, Late-apoptotic}
for 12h, Day 1, Day 2, Day 3 from Figure4Apoptosis.xlsx 'Results' sheet.
Cross-check our recomputed means/SDs against the embedded summary block, then
run Welch t-tests and compare to the paper's reported significance pattern.
"""
import openpyxl, numpy as np
from scipy import stats
import json

wb = openpyxl.load_workbook("mendeley_data/Figure4Apoptosis.xlsx", data_only=True)
ws = wb["Results"]
rows = [list(r) for r in ws.iter_rows(values_only=True)]

# Block layout per timepoint:
#   header_row, label_row, then 9 rows of replicates (Control 1..3, LDR 1..3, HDR 1..3)
# 12h block:   rows 2..10
# Day1 block:  rows 15..23
# Day2 block:  rows 28..36
# Day3 block:  rows 41..49
blocks = {
    "12h":  (2, 5),    # control_start_row, then +3 LDR, +6 HDR
    "Day1": (15, 5),
    "Day2": (28, 5),
    "Day3": (41, 5),
}
phases = ["Healthy", "Early", "Mid", "Late"]

# Per-replicate value extraction (cols 1..4)
def block_data(tp):
    c_start, _ = blocks[tp]
    out = {"Control": [], "LDR": [], "HDR": []}
    for k, cond in enumerate(["Control", "LDR", "HDR"]):
        for j in range(3):
            r = rows[c_start + k*3 + j]
            out[cond].append([float(r[1]), float(r[2]), float(r[3]), float(r[4])])
    return out

# Paper's embedded summary block (cols 8 mean / 9 early_mean / etc) — extract
# rather than retype: rows c_start+0 and c_start+2 and c_start+4 hold "Mean" lines,
# cols 8..11 hold means (Healthy, Early, Mid, Late).
def block_summary(tp):
    c_start, _ = blocks[tp]
    out = {}
    for k, cond in enumerate(["Control", "LDR", "HDR"]):
        mean_row = rows[c_start + k*2]
        sd_row   = rows[c_start + k*2 + 1]
        means = [float(mean_row[8 + i]) for i in range(4)]
        sds   = [float(sd_row[8 + i])   for i in range(4)]
        out[cond] = {ph: (means[i], sds[i]) for i, ph in enumerate(phases)}
    return out

# Paper expected significance pattern from Results section, Fig 4:
# "HDR samples 12h after exposure were significantly different from control and LDR samples"
#   -> 12h Healthy: Control-vs-HDR sig, LDR-vs-HDR sig, Control-vs-LDR ns
# "Both LDR and HDR samples were significantly different from control on day 2 for early
#  apoptotic cells"
#   -> Day2 Early: Control-vs-LDR sig, Control-vs-HDR sig
# "HDR samples showed significant differences from both LDR and control samples
#  12 hours and 2 days after irradiation" (context: late apoptotic ~or full pattern)
#   -> 12h Late: Control-vs-HDR sig, LDR-vs-HDR sig
#   -> Day2 Late: Control-vs-HDR sig, LDR-vs-HDR sig
# We will print all and mark agreement only on these explicitly listed contrasts.

paper_expected = {
    ("12h",  "Healthy"): {("Control","HDR"): True,  ("LDR","HDR"): True,  ("Control","LDR"): False},
    ("Day2", "Early"):   {("Control","LDR"): True,  ("Control","HDR"): True},
    ("12h",  "Late"):    {("Control","HDR"): True,  ("LDR","HDR"): True},
    ("Day2", "Late"):    {("Control","HDR"): True,  ("LDR","HDR"): True},
}

print("=== Apoptosis: re-derived vs paper summary block ===")
tol_mean = 0.05; tol_sd = 0.05
matched = 0; total = 0; mismatches = []
recomp = {}
for tp in ("12h","Day1","Day2","Day3"):
    data = block_data(tp)
    summ = block_summary(tp)
    recomp[tp] = {}
    for cond in ("Control","LDR","HDR"):
        recomp[tp][cond] = {}
        arr = np.array(data[cond])  # (3,4)
        for i, ph in enumerate(phases):
            vals = arr[:, i].tolist()
            m = float(np.mean(vals))
            s = float(np.std(vals, ddof=1))
            pm, ps = summ[cond][ph]
            total += 1
            ok = abs(m-pm)<=tol_mean and abs(s-ps)<=tol_sd
            if ok: matched += 1
            else: mismatches.append((tp,cond,ph,pm,ps,m,s))
            recomp[tp][cond][ph] = {"mean": m, "sd": s, "values": vals, "paper_mean": pm, "paper_sd": ps, "ok": ok}
            print(f"  {tp:5s} {cond:7s} {ph:6s}  paper=({pm:.3f},{ps:.3f})  repl=({m:.3f},{s:.3f})  {'OK' if ok else 'DIFF'}")
print(f"\nApoptosis summary match: {matched}/{total}")

print("\n=== Apoptosis: t-tests (Welch) ===")
contrasts = [("Control","LDR"),("Control","HDR"),("LDR","HDR")]
agree = 0; checked = 0
for tp in ("12h","Day1","Day2","Day3"):
    data = block_data(tp)
    arr = {c: np.array(data[c]) for c in ("Control","LDR","HDR")}
    for i, ph in enumerate(phases):
        for c in contrasts:
            a = arr[c[0]][:,i]; b = arr[c[1]][:,i]
            p = stats.ttest_ind(a,b,equal_var=False).pvalue
            sig = p < 0.05
            exp = paper_expected.get((tp,ph),{}).get(c, None)
            if exp is not None:
                checked += 1
                if sig == exp: agree += 1
                mark = ("OK" if sig==exp else "DIFF")
                print(f"  {tp:5s} {ph:6s} {c[0]:>7}-vs-{c[1]:<7}  p={p:.4f}  sig={'Y' if sig else 'n'}  paper={'Y' if exp else 'n'}  {mark}")
print(f"\nApoptosis stat-pattern agreement: {agree}/{checked} on explicitly-stated contrasts")

with open("replication_apoptosis_results.json","w") as f:
    json.dump({"recomputed": recomp, "summary_matches": [matched, total],
               "stat_matches": [agree, checked]}, f, indent=2)
print("\nWrote replication_apoptosis_results.json")
