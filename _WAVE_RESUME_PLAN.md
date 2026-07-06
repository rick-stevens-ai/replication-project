# Replication Wave Resume Plan — 2026-06-25 05:00 CDT

Root cause both lanes stalled after 2026-06-23 14:31: auto-roller / wave fan-out is
NOT a daemon; it only advances while a session is active. Session went idle → no
re-trigger → waves stopped.

## LUCID-100 (Ollie-owned)
- 108 dirs, 105 with REPORT.md before this session.
- 8 dirs have FIRST_PASS_REPORT.md + artifacts but NO final audited REPORT.md (closeout needed).
- WAVE A (running, 5 children, launched 2026-06-25 04:59):
  lucid100-corpuscular-doserate-dna-damage-senescence
  lucid100-deinococcus-comparative-genomics-strains
  lucid100-highlet-pbmc-p53-inflammation
  lucid100-let-hyperradiosensitivity-high-let
  lucid100-low-dose-ct-gene-expression-dna-integrity
- WAVE B (queued, batch 2 — launch after A clears):
  lucid100-multiscale-uhdr-survival-model
  lucid100-rt-dna-repair-tp53-apoptosis-model
  slot61_mscs_yH2AX_pATM_lowdose_2024
- Each closeout: audit FIRST_PASS vs real paper, verdict + Coverage/10 + Agreement/10,
  MANDATORY 6/22 reproducibility-blocker critique (name precise missing artifact if data-blocked).

## LUCID Second-100 (low-friction OA computational pool)
- 116 PDFs harvested; harvest DONE. Bottleneck = replication throughput.
- COMPLETED (10): 001 017 019 040 065 075 077 092 099 100
- Batch B (5, reports written): 097 098 072 076 066  → 15/15 staged dirs have reports
- Batch C QUEUED (23 track-structure MC, GPU-eligible, radmc on uicgpu):
  16 20 23 24 26 31 33 39 41 42 46 49 53 56 59 64 73 79 81 82 83 89 90
  → these need harvest-to-dir staging first (only 16 of 100 dirs exist), then replicate.
  → TOPAS-nBio/Geant4-DNA on uicgpu is the compute path for MC papers.

## UPDATE 2026-06-25 10:16 CDT
- WAVE A done: corpuscular=PARTIAL 6.5/8.5, deinococcus=REPLICATED 8.0/9.5, highlet-pbmc=REPLICATED 8.5/9.5 (wrote report/REPORT.md). let_hrs + ldct finished but WROTE NOTHING -> re-run.
- WAVE A2 (running, 5 children): lucid_let_hrs2, lucid_ldct2, lucid_uhdr, lucid_tp53, lucid_slot61.
- 5/5 cap IS STILL HARD-ENFORCED at runtime. Roll in batches of 5.
- Second-100 batch C: 22/23 PDFs already harvested in _harvest/pdfs_expanded/ (named NNN__doi-slug.pdf). rank 90 MISS (Springer chapter, paywalled). Ready to replicate, no new harvest.

## SECOND-100 BATCH C QUEUE (replicate 5 at a time, after WAVE A2)
16 20 23 24 26 31 33 39 41 42 46 49 53 56 59 64 73 79 81 82 83 89  (22 papers)
Each: mkdir s100-NNN/{source,ocr,code,evidence,figures,report}; copy PDF to source/paper.pdf; pdf-read; replicate central claim or SPOT-CHECK if full MC engine needed (engine live on uicgpu); verdict + Coverage/10 + Agreement/10 + 6/22 blocker critique to report/REPORT.md.
GPU-heavy MC full-runs: offload to hcodex (runs OUTSIDE the 5-child cap) targeting uicgpu TOPAS-nBio/Geant4-DNA.

## CLOSEOUT 2026-06-25 ~11:00 CDT — BOTH TASKS COMPLETE
- LUCID-100: 108/108 dirs reported. 8 closeouts done+disk-verified (ldct written directly after 2 subagent lost-writes).
- Second-100 batch C: 22/22 reports on disk (rank 90 excluded = paywalled Springer chapter). Verdicts: ~3 PARTIAL (020,046,079), rest SPOT-CHECK (track-structure MC papers need full TOPAS-nBio/Geant4-DNA runs on uicgpu for promotion to REPLICATED). Highlights: 033 LQ back-fit matched headline 30.37% to 1%; 046 X-ray core reproduced exactly; 023 caught haploid/diploid table-text mismatch; 026 caught 16x concentration discrepancy.
- Total Second-100 staged dirs with reports: 37 (15 prior + 22 batch C).
- NEXT (future): promote SPOT-CHECK MC papers via real uicgpu TOPAS-nBio/Geant4-DNA runs (hcodex, outside 5-cap); harvest+stage remaining Second-100 ranks beyond batch C; rank 90 needs institutional/Playwright fetch.
- LESSON: subagents sometimes finish analysis but end before writing REPORT.md. Fix that worked: instruct 'write report EARLY (stub), then refine; read it back to confirm'. Zero lost-writes after adding that guard.
