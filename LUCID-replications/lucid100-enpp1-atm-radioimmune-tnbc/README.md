# LUCID100 — Slot 13 (Wave 2)

**Paper.** Ruiz-Fernández de Córdoba, Valencia, Welch, Moreno *et al.*
*Dual ENPP1/ATM depletion blunts DNA damage repair boosting radioimmune
efficacy to abrogate triple-negative breast cancer.*
**Signal Transduction and Targeted Therapy 10:185 (2025).**
DOI: [10.1038/s41392-025-02271-2](https://doi.org/10.1038/s41392-025-02271-2)
Open Access (CC BY 4.0).

**LUCID100 row.** Wave 2 / slot 13 / candidate_curated / tier A.
Themes: DNA repair / DDR; radiation quality / RBE; omics / signatures;
immune / inflammation / senescence.
Original LUCID task tag: *"omics/signature replication"*.

## Verdict (first pass)

**GREEN – partial signature replication achieved end-to-end on first pass.**

All six transcriptomic signature genes that the paper calls out by name in
Fig. 1c–d are recovered from GSE277249 with the correct direction in both
parental lineages (ANV5 family and 4T1 family), and 5 of 6 also pass
padj < 0.05 in *both* lineages with a vanilla PyDESeq2 contrast
(`CTC_in vs parental`). ENPP1 itself, the central gene of the paper,
shows log2FC = **+5.33** (padj ≈ 4e-31) in the ANV5 family and
log2FC = **+1.47** (padj ≈ 6e-5) in the 4T1 family. Pathway enrichment
on common up-DEGs cleanly recovers the inflammation / leukocyte-adhesion
GO categories that map onto Fig. 1b ("Regulation of inflammatory
response", "Tissue remodeling").

See `FIRST_PASS_REPORT.md` for the full hypothesis-by-hypothesis verdict.

## Layout

```
.
├── README.md                  # this file
├── PROGRESS.md                # change log
├── ARTIFACT_MANIFEST.md       # files + provenance + SHA-256
├── FIRST_PASS_REPORT.md       # verdict + scope + acceptance criteria
├── artifacts/                 # paper PDF + 2 supplementary files
│   ├── paper.pdf
│   ├── paper_layout.txt
│   ├── supp_MOESM1_ESM.docx   # Materials & Methods companion
│   ├── supp_MOESM1_ESM.txt
│   ├── supp_MOESM2_ESM.pdf    # Figures S1–S7 + Tables S1–S8 (DDR drug list, antibodies, shRNA)
│   └── supp_MOESM2_ESM.txt
├── data/                      # GEO GSE277249 (gene-level featureCounts)
│   ├── GSE277249_RAW.tar
│   ├── GSE277249_filelist.txt
│   ├── GSE277249_series_matrix.txt.gz
│   └── counts/                # 18 per-sample featureCounts TSVs
├── code/
│   ├── 01_build_matrix.py     # 18 featureCounts → matrix + sample sheet
│   └── 02_smoke_deg.py        # PyDESeq2 + Enrichr + hypothesis checks + figs
├── results/
│   ├── counts_matrix.tsv
│   ├── sample_sheet.tsv
│   ├── ensembl_symbol_mouse.tsv   # mygene cache
│   ├── deg_ANV5.tsv
│   ├── deg_4T1.tsv
│   ├── hypothesis_check.json
│   └── enrichr_common_up/         # GO BP enrichment (gseapy)
└── figures/
    ├── fig1_pca.png
    ├── fig2_enpp1_counts.png
    └── fig3_signature_heatmap.png
```

## Quick reproduction

```bash
cd lucid100-enpp1-atm-radioimmune-tnbc
python3 -m venv .venv
source .venv/bin/activate
pip install -U pandas numpy scipy matplotlib pydeseq2 gseapy statsmodels mygene
# data/ is already populated; if you wipe it, see ARTIFACT_MANIFEST.md
python code/01_build_matrix.py
python code/02_smoke_deg.py
```

Runtime on a 2024 M2/M3 MacBook: < 2 min total (featureCounts already
done upstream by the authors; we just run DESeq2 on ~57k genes × 18
samples).

## Honest limits of this pass

- Only the bulk RNA-seq pillar (Fig. 1, Supp. Fig. 1) was touched. The
  paper's functional claims (clonogenic D50, comet tail moment, γH2AX
  kinetics, in vivo tumor regression, abscopal effect, scRNA-seq panel)
  rely on **wet-lab data not deposited** — they cannot be replicated
  from public artifacts and were not attempted here.
- The drug-synergy screen (Fig. 3, Supp. Fig. 3) uses non-deposited
  plate readouts; only the drug list (Supp. Table S5/S6) is public.
- The scRNA-seq panel (Fig. 6) reuses **EGAD00001006608** (Bassez et al.
  *Nat. Med.* 2021), which is **EGA controlled-access** and was not
  retrieved here (would require a data-access committee request).

See `FIRST_PASS_REPORT.md` § 6 "Strict replication plan" for a clear
list of what is achievable vs. what is fundamentally blocked.
