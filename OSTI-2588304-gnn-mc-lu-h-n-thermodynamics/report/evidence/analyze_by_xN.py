"""
Parse the CGCNN test_results.csv and the dataset id_prop.csv + cifs to
compute MAE stratified by max xN/xLu (mimicking paper Fig 3b's curve).

Usage: python analyze_by_xN.py test_results.csv dataset_lu_h_n/
"""
import sys, os, csv
import numpy as np
from ase.io import read

def xN_ratio(cif_path):
    a = read(cif_path)
    syms = a.get_chemical_symbols()
    nl = sum(1 for x in syms if x == "Lu")
    nn = sum(1 for x in syms if x == "N")
    return nn / nl if nl else 0.0

def main():
    res_csv = sys.argv[1]
    ds = sys.argv[2]
    rows = []
    with open(res_csv) as f:
        for line in csv.reader(f):
            cid, y_true, y_pred = line[0], float(line[1]), float(line[2])
            xn = xN_ratio(os.path.join(ds, f"{cid}.cif"))
            rows.append((cid, y_true, y_pred, xn))

    y_true = np.array([r[1] for r in rows])
    y_pred = np.array([r[2] for r in rows])
    xN = np.array([r[3] for r in rows])
    ae = np.abs(y_true - y_pred)

    mae_all = ae.mean() * 1000  # meV/atom
    ss_res = ((y_true - y_pred) ** 2).sum()
    ss_tot = ((y_true - y_true.mean()) ** 2).sum()
    r2_all = 1 - ss_res / ss_tot

    print(f"[test set] N={len(rows)}")
    print(f"[test set] MAE = {mae_all:.2f} meV/atom")
    print(f"[test set] R^2 = {r2_all:.4f}")

    # Paper Fig 3b: <MAE>_K vs max xN/xLu (cumulative — include all configs
    # with xN/xLu <= threshold; error over that subset)
    thresholds = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0]
    print("\n[paper-style Fig 3b] MAE and R^2 as function of max xN/xLu:")
    print(f"{'max xN/xLu':>12}  {'N':>4}  {'MAE meV/atom':>14}  {'R^2':>8}")
    for t in thresholds:
        m = xN <= t
        if m.sum() < 5:
            continue
        yt, yp = y_true[m], y_pred[m]
        mae_t = np.abs(yt - yp).mean() * 1000
        ss_r = ((yt - yp) ** 2).sum()
        ss_t = ((yt - yt.mean()) ** 2).sum()
        r2 = 1 - ss_r / ss_t if ss_t > 0 else float("nan")
        print(f"{t:>12.2f}  {m.sum():>4d}  {mae_t:>14.2f}  {r2:>8.4f}")

    # Paper claim to check: MAE < 40 meV/atom AND R^2 > 0.9 for xN/xLu < 0.5
    m = xN < 0.5
    if m.sum() >= 5:
        yt, yp = y_true[m], y_pred[m]
        mae_c = np.abs(yt - yp).mean() * 1000
        ss_r = ((yt - yp) ** 2).sum()
        ss_t = ((yt - yt.mean()) ** 2).sum()
        r2 = 1 - ss_r / ss_t if ss_t > 0 else float("nan")
        ok = (mae_c < 40) and (r2 > 0.9)
        print(f"\n[paper-claim check]  xN/xLu < 0.5 subset (N={m.sum()}):")
        print(f"  MAE = {mae_c:.2f} meV/atom  (paper claim: < 40)   {'PASS' if mae_c<40 else 'FAIL'}")
        print(f"  R^2 = {r2:.4f}  (paper claim: > 0.9)              {'PASS' if r2>0.9 else 'FAIL'}")
        print(f"  Combined: {'PASS' if ok else 'FAIL'}")
    else:
        print(f"\n[paper-claim check] not enough configs with xN/xLu<0.5 in test set (only {m.sum()})")

if __name__ == "__main__":
    main()
