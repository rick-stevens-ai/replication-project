# Progress — LUCID100 W2-#16 (Zhu 2020 TOPAS-nBio proton)

All timestamps America/Chicago.

## 2026-06-09 13:06 — Launch

Subagent spawned by main agent for max-rate Wave-2 backfill slot 16.
Source of truth: `~/.openclaw/workspace/lucid-replications/LUCID100_SOLID_MASTER_QA.tsv`
(row 48, rank 47).

## 2026-06-09 13:07 — Folder scaffold

Created `lucid100-topas-proton-cellular-response/{code,results,figures,artifacts}`
under `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/`.

## 2026-06-09 13:07 — Paper fetch

- Tried BioOne direct PDF → Incapsula bot wall (HTML response).
- Found QUB institutional Open Access mirror at
  `pureadmin.qub.ac.uk/ws/files/231105855/i0033_7587_194_1_9.pdf`.
- HTTP 200, 3.55 MB, version 1.5 PDF. ✅
- `pdftotext -layout` produced 86 KB / 839-line text extraction. ✅

## 2026-06-09 13:08 — Paper digest

Read full Methods, Results, Summary, References, and Appendix Tables A1 & A2.
Key extracted parameters captured in `FIRST_PASS_REPORT.md` §1–§3.

Headline numbers from the paper (Abstract + Appendix):

- Energy range: 0.5–500 MeV protons → LET 60–0.2 keV/μm.
- Total DSB yield: 6.5 DSB/Gy/Gbp at 0.2 keV/μm → 21.2 at 60 keV/μm.
- >95% of DSBs repaired within 24 h.
- Misrepair fraction: 15.8 % at 60 keV/μm with a 3 Mbp detection threshold
  (63.7 % without threshold).
- Predicted dicentrics ≈ 2× experimental Edwards 1985; excess acentrics ≈ 10×.

## 2026-06-09 13:08 — Artifact harvest

- MEDRAS-MC GitHub repo cloned (`artifacts/Medras-MC`, depth 1). Python.
  Author has `damagegenerator/` (writes SDD files for X-ray / proton / carbon)
  and `repairanalysis/` (consumes SDD, runs MEDRAS repair model).
- TOPAS-nBio metadata captured (`artifacts/topas_nbio_meta.json`). The
  extension is public; TOPAS itself is free-for-academic but not on this host.
- Prior LUCID work `lucid-medras-mc` already replicated McMahon-Prise 2021 with
  this same MEDRAS-MC repo (PARTIAL → REPLICATED). Reuse confirmed feasible.

## 2026-06-09 13:09 — Sanity check

Wrote `code/sanity_dsb_yield.py`. Uses MEDRAS-MC's `damageModel.basicXandIon()`
with a tiny `runs=2` setting → checks the X-ray (LET=0) DSB/Gy yield matches
the expected ~35 DSB/Gy/cell mentioned in McMahon 2017/2021, which corresponds
to ~5.7 DSB/Gy/Gbp on Zhu's 6.08 Gbp nucleus and brackets the paper's
6.5 DSB/Gy/Gbp at lowest LET (0.2 keV/μm).

Log saved to `results/sanity_dsb_yield.txt`.

## 2026-06-09 13:10 — Table A2 transcription

Transcribed the full Appendix Table A2 (Damage yield per Gy per Gbp,
12 proton energies × 11 yield columns) to `results/table_A2.csv`. This is the
canonical numerical target for any future full TOPAS-nBio rerun.

## 2026-06-09 13:10 — HPC job plan

Wrote `HPC_JOB_PLAN.md` scoping a uicgpu / Aurora full rerun of the TOPAS-nBio
damage-induction step.

## 2026-06-09 13:10 — Deliverables complete

- `README.md`, `PROGRESS.md`, `FIRST_PASS_REPORT.md`, `ARTIFACT_MANIFEST.md`,
  `HPC_JOB_PLAN.md` written.
- Progress JSON updated under `memory/subagent-progress/`.
- QA retag recommendation: `omics/signature replication` → `simulation/model
  replication`. Documented in README §Worktype correction and FIRST_PASS_REPORT.

Subagent task complete.
