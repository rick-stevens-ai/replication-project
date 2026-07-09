"""
Abstract claim: "DNA DSBs were observed in 30% of the hiPSC-DCHs overall,
and in 60% after high-dose (>2 Gy) IR. ... reduced the DSBs over time until
it reached 30%."

This is a quantitative claim that should be reproducible from Fig 2 if we
had the underlying gH2AX MFI / %positive data. Without the figure values
we cannot recompute, but we CAN check:
  - Internal narrative consistency with the supplementary p-value pattern.
  - The expected dose-response monotonicity in significance.

For hiPSC-DCHs (per S1) — significance "vs. HC-402-05a" anchored on hiPSCs
gives 12 comparisons (3 doses * 4 times). Check the trend across dose and
time for the hiPSCs row (proxy: increasing damage with dose).
"""
import csv
RANK = {"ns":0, "*":1, "**":2, "***":3, "****":4}
rows = list(csv.DictReader(open("parsed_supp/all_supp_significance.csv")))

# Pull S1 rows: cell_line=hiPSCs, comparison="vs. hiPSC-DCHs"
# This tells us how DIFFERENT the irradiated hiPSCs are from hiPSC-DCHs at each
# dose * time — proxy for "DCHs damage similar to hiPSCs at low dose, diverges
# at high dose because DCHs repair better".
print("S1 gH2AX: hiPSCs vs. hiPSC-DCHs significance (proxy for DCH-vs-iPSC divergence)")
print("dose       1h    5h    9h    24h")
for dose in ["0 Gy","1 Gy","2 Gy","5 Gy"]:
    line = [dose.ljust(10)]
    for t in ["1h","5h","9h","24h"]:
        sig = next((r['sig'] for r in rows
                    if r['panel']=='S1_gH2AX' and r['cell_line']=='hiPSCs'
                    and r['dose_Gy']==dose and r['time']==t
                    and r['comparison']=='vs. hiPSC-DCHs'), '-')
        line.append(sig.ljust(5))
    print(" ".join(line))

print()
print("S1 gH2AX: hiPSCs vs. HC-402-05a significance")
print("dose       1h    5h    9h    24h")
for dose in ["0 Gy","1 Gy","2 Gy","5 Gy"]:
    line = [dose.ljust(10)]
    for t in ["1h","5h","9h","24h"]:
        sig = next((r['sig'] for r in rows
                    if r['panel']=='S1_gH2AX' and r['cell_line']=='hiPSCs'
                    and r['dose_Gy']==dose and r['time']==t
                    and r['comparison']=='vs. HC-402-05a'), '-')
        line.append(sig.ljust(5))
    print(" ".join(line))

# Claim component A: "DNA DSBs were observed in 30% of the hiPSC-DCHs overall"
# Cannot recompute (no underlying data). NOT TESTED.

# Claim component B: hiPSC-DCHs repair efficiently (DSBs decrease over time):
# Look for evidence in the significance pattern.
# At 5 Gy, the divergence between hiPSCs and hiPSC-DCHs should become significant
# as time increases (DCHs repair, iPSCs don't).
print()
print("Time-course of hiPSCs vs hiPSC-DCHs divergence at 5 Gy:")
for t in ["1h","5h","9h","24h"]:
    sig = next((r['sig'] for r in rows
                if r['panel']=='S1_gH2AX' and r['cell_line']=='hiPSCs'
                and r['dose_Gy']=='5 Gy' and r['time']==t
                and r['comparison']=='vs. hiPSC-DCHs'), '-')
    print(f"  {t}: {sig}  (rank {RANK.get(sig,-1)})")

# Dose-response: at 24h, divergence iPSC-vs-DCH should increase with dose
print()
print("Dose-response of hiPSCs vs hiPSC-DCHs at 24h:")
for dose in ["0 Gy","1 Gy","2 Gy","5 Gy"]:
    sig = next((r['sig'] for r in rows
                if r['panel']=='S1_gH2AX' and r['cell_line']=='hiPSCs'
                and r['dose_Gy']==dose and r['time']=='24h'
                and r['comparison']=='vs. hiPSC-DCHs'), '-')
    print(f"  {dose}: {sig}  (rank {RANK.get(sig,-1)})")
