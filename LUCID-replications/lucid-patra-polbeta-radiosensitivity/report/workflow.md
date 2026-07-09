# Workflow — Patra 2022 POLβ Radiosensitivity Replication

## Inputs
- **Paper PDF:** `data/paper.pdf` (1.83 MB, open-access CC-BY-NC 4.0; DOI 10.3857/roj.2021.00689)
- **Supplementary PDFs:** `data/suppl1.pdf` (Western blot), `data/suppl2.pdf` (docking figures), `data/suppl3.pdf` (sequences — Table S1, key input), `data/suppl4.pdf` (ClusPro Table S2)
- **PDB downloads:** `data/pdb/` — 11 files pulled from RCSB (1TV9, 1DE8, 1EBM, 1TDH, 1WSR, 1XNA, 2BRF, 2FOZ, 2RCW, 3Q8K, 4ZZY)
- **Figure digitization:** two-pass visual read of Fig. 2 clonogenic survival curves (values hard-coded in `code/02_lq_fit.py`)

## Extraction
- `pdftotext` on paper + all 4 supplementary PDFs → `data/*.txt` companions
- No Nougat MMD extraction was performed for the original run (this backfill adds a stub — see `extraction/nougat.mmd`)
- Suppl. Table S1 sequences copy-pasted verbatim from suppl3.txt into `code/01_sequence_check.py` as inline FASTA strings

## Analysis pipeline

```
01_sequence_check.py  → results/{sequence_check.json, alignment.txt, wt_protein.fasta, del_protein.fasta, wt_nt.fasta, del_nt.fasta}
   Biopython translate WT + Δ cDNA; check frame; align proteins; verify 22 canonical residues in WT

02_lq_fit.py          → results/lq_fit.json, figures/fig2_replication.png
   scipy.optimize.curve_fit on SF(D) = exp(-αD - βD²); weighted least-squares; DMF calc

03_quantitative_audit.py → results/{quant_audit.json, quant_audit.txt}
   Internal-consistency checks on ROS, cell-cycle, Annexin V, docking scores

04_pdb_structural_check.py (added 2026-06-25) → results/{pdb_audit.json, pdb_audit.txt}
   Download 11 PDBs via urllib; parse with Bio.PDB.PDBParser
   Verify Polβ active-site residues in 1TV9 chain A
   Cross-check each partner PDB HEADER/COMPND vs paper label
```

## Environment
- Python 3.11 (system + Biopython, scipy, matplotlib, numpy)
- No GPU / no external services beyond RCSB downloads
- Everything runs on CherryRd or m1 in ~30 seconds total (excluding PDB downloads which take 1–2 min)

## Reproducibility
```bash
cd lucid-patra-polbeta-radiosensitivity
python3 code/01_sequence_check.py
python3 code/02_lq_fit.py
python3 code/03_quantitative_audit.py
python3 code/04_pdb_structural_check.py    # downloads ~3 MB from RCSB
```

All scripts are self-contained; no shared state or config.

## What Was NOT Run
- ClusPro (9 partner submissions × 1–12 h queue on public tier; AUP forbids parallel jobs)
- HDOCK (4 protein–DNA submissions; server rate-limited)
- SWISS-MODEL rebuild of ΔPolβ (blocked by cDNA inconsistency — deposited sequence encodes 198-aa frame-shifted pseudo-protein, not the 238-aa domain-truncated polymerase described)
- Any wet-lab work (clonogenic, Western, DAPI, AO/PI, DCFDA, cell-cycle PI, Annexin V) — LUCID scope

## Handoff
Reports live at top-level `REPORT.md` (verbose, canonical) and `report/REPORT.tex` (formal LaTeX summary). Open questions in `report/open_questions.json` + `report/open_questions_section.tex`. Failure analysis in `report/failure_analysis.md`. Artifact inventory in `report/artifacts_summary.md`.
