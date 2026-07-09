"""Parse SDD output files and summarize damage counts.
The 'Damage and primary count' header records 'N_damage, N_primary'."""
import os, glob, csv, statistics, re, sys

def parse_sdd(path):
    dose = primary = damage = None
    with open(path) as fh:
        for line in fh:
            if line.startswith("***EndOfHeader***"):
                break
            if line.startswith("Dose or fluence"):
                # "Dose or fluence, 1.5485..., 1e-12;"
                m = re.search(r",\s*([0-9.eE+-]+)", line)
                if m: dose = float(m.group(1))
            elif line.startswith("Damage and primary count"):
                parts = line.split(",")
                # "Damage and primary count, 2034, 4;"
                damage = int(parts[1].strip())
                primary = int(parts[2].strip().rstrip(";"))
    # Count DSBs by scanning DSB column. Easiest: count lines after header that contain
    # a non-trivial damage block. But SDD damage type tally is in damage spec field per row.
    # For smoke-level summary, treat "Damage and primary count" header as total damages.
    return dose, primary, damage

root = "code/SPT-SDD-Framework"
out_csv = "results/smoke_summary.csv"
os.makedirs("results", exist_ok=True)
with open(out_csv, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["particle", "cell", "dose_Gy", "primary_tracks", "damage_count"])
    for tag, sub in [("alpha","Alpha_Simulation"),("proton","Proton_Simulation"),("electron","Electron_Sim")]:
        files = sorted(glob.glob(os.path.join(root, sub, "cell_*.sdd")))
        for p in files:
            d, n, dmg = parse_sdd(p)
            w.writerow([tag, os.path.basename(p), d, n, dmg])

# print summary
print(f"{'particle':<10}{'cells':>6}{'mean_dose':>12}{'mean_tracks':>14}{'mean_damage':>14}")
import csv as _csv
rows = list(_csv.DictReader(open(out_csv)))
for tag in ("alpha","proton","electron"):
    sub = [r for r in rows if r["particle"]==tag]
    n = len(sub)
    md = statistics.mean(float(r["dose_Gy"]) for r in sub)
    mt = statistics.mean(int(r["primary_tracks"]) for r in sub)
    mdmg = statistics.mean(int(r["damage_count"]) for r in sub)
    print(f"{tag:<10}{n:>6}{md:>12.4f}{mt:>14.2f}{mdmg:>14.1f}")
print(f"\nWrote {out_csv}")
