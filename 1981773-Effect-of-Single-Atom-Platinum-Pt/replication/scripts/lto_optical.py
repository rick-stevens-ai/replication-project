"""LTO IPA absorption + Pt-induced shift, computed from existing QE eigenvalues.

Reads JDOS data files generated on uicgpu (slab_001/jdos.dat and slab_001_Pt/jdos.dat)
and produces:
  - paper-comparable α(ω)/ω² curves
  - quantitative table: gap, absorption-onset, peak position
  - Pt-induced red-shifts vs paper
"""
import numpy as np, json, sys, os

clean = "slab_001/jdos.dat"
pt = "slab_001_Pt/jdos.dat"
ROOT = sys.argv[1] if len(sys.argv)>1 else "."

def load(p):
    d = np.loadtxt(os.path.join(ROOT, p), comments="#")
    return d[:,0], d[:,1], d[:,2]  # om, jdos, alpha~jdos/w^2

def first_onset(om, j, thresh=10):
    mask = (om>0.05)
    cum = np.cumsum(j[mask])
    idx = np.argmax(cum>thresh) if (cum>thresh).any() else -1
    if idx<0: return None
    return om[mask][idx]

def peak(om, x, omin=0.3):
    mask = om>omin
    return om[mask][np.argmax(x[mask])], x[mask].max()

def main():
    om_c, j_c, a_c = load(clean)
    om_p, j_p, a_p = load(pt)

    # gaps (from extract_eigs runs):
    # clean: 2.254 eV ; Pt-doped 0.529 eV
    gap_c = 2.254
    gap_p = 0.529
    onset_c = first_onset(om_c, j_c)
    onset_p = first_onset(om_p, j_p)
    pk_c = peak(om_c, j_c, omin=0.3)
    pk_p = peak(om_p, j_p, omin=0.05)

    # paper-reported (Yan 2022, OSTI 1981773):
    # Bulk LTO PBE gap ~3.8 eV; clean (001) slab gap ~3.2 eV, Pt-doped ~1.0 eV (visualized
    # absorption onset shift from UV into visible). Paper's main quantitative claims:
    #   - Pt doping reduces band gap by ~70% (relative)
    #   - absorption edge shifts from 3.2 → 1.0 eV (i.e. red-shift ~2.2 eV)
    paper = {
        "bulk_gap_paper_eV": 3.8,
        "001_clean_gap_paper_eV": 3.2,
        "001_Pt_gap_paper_eV": 1.0,
        "rel_reduction_paper": (3.2-1.0)/3.2,  # 0.687
        "abs_onset_redshift_paper_eV": 3.2-1.0,  # 2.2
    }
    rel = (gap_c - gap_p) / gap_c
    out = {
        "ours": {
            "001_clean_gap_eV": gap_c,
            "001_Pt_gap_eV": gap_p,
            "relative_gap_reduction": rel,
            "absolute_gap_reduction_eV": gap_c-gap_p,
            "jdos_onset_clean_eV": float(onset_c) if onset_c else None,
            "jdos_onset_Pt_eV": float(onset_p) if onset_p else None,
            "jdos_peak_clean_eV": float(pk_c[0]),
            "jdos_peak_Pt_eV": float(pk_p[0]),
        },
        "paper": paper,
        "agreement_relative_reduction_pct": float(100*abs(rel - paper["rel_reduction_paper"]) / paper["rel_reduction_paper"]),
        "agreement_redshift_pct": float(100*abs((gap_c-gap_p) - paper["abs_onset_redshift_paper_eV"]) / paper["abs_onset_redshift_paper_eV"]),
    }
    print(json.dumps(out, indent=2))
    json.dump(out, open(os.path.join(ROOT,"lto_optical_summary.json"),"w"), indent=2)
    return out

if __name__=="__main__":
    main()
