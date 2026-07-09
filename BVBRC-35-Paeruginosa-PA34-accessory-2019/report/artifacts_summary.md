# Artifacts Summary — BVBRC-35 (Subedi et al. 2019, *P. aeruginosa* PA34)

## 8-artifact standard status

| # | Artifact | Status | Notes |
|---|---|---|---|
| 1 | `paper.pdf` (via `work/paper.pdf`) | **PRESENT** | PLOS OA, 3.7 MB — fully accessible (PMC6464166). Not yet copied to top-level `paper.pdf`; symlink recommended. |
| 2 | `extraction/marker.md` | Needs backfill | Not present as of 2026-07-05; paper is OA (europepmc `fulltext.xml` 167 KB + `fulltext.txt` 59 KB already in `work/`) so a Marker parse is straightforward. |
| 3 | `extraction/nougat.mmd` | Needs backfill | Same source; add to Kukla's Eagle batch queue. |
| 4 | `report/REPORT.tex` (+ .md) | **PRESENT** | Detailed 6-section LaTeX with dedicated genuine-critique section. REPORT.md is the primary narrative. |
| 5 | `report/open_questions.json` | **PRESENT** | 5 heavy-duty open questions with basis + next_steps. |
| 6 | `report/workflow.md` | **PRESENT** | Full workflow + tools + compute estimate. |
| 7 | `report/artifacts_summary.md` | **PRESENT** | This file. |
| 8 | `report/failure_analysis.md` | **PRESENT** | Honest failure analysis. |

## Evidence / traces

```
BVBRC-35-Paeruginosa-PA34-accessory-2019/
├── paper.pdf (RECOMMENDED: symlink to work/paper.pdf)
├── work/
│   ├── paper.pdf                       (3.7 MB, PLOS OA original)
│   ├── fulltext.xml, fulltext.txt      (europepmc full text, 167KB + 59KB)
│   ├── europepmc_search.json
│   ├── download_genomes.sh, run_pangenome.sh, run_amr.sh
│   ├── analyze_roary.py, judge.py
│   ├── genome_stats.json, summary_statistics.txt
│   ├── roary_venn.json                 (reproduced Fig-1 Venn)
│   ├── amr.out, pipeline.out, roary.log
│   └── (raw genomes + Prokka + Roary intermediates on uicgpu: /data/stevens/pa34_repl/)
├── report/
│   ├── REPORT.md                       (primary narrative, verdict REPLICATED)
│   ├── REPORT.tex                      (8-artifact LaTeX + critique)
│   ├── open_questions.json             (5 questions)
│   ├── workflow.md
│   ├── artifacts_summary.md            (this file)
│   ├── failure_analysis.md
│   ├── brief.md, attempt_log.md, artifact_harvest.md
│   └── evidence/
│       ├── roary_summary_statistics.txt
│       ├── roary_venn.json
│       ├── genome_stats.json
│       ├── PA34_resfinder.tsv, PA34_card.tsv, PA34_vfdb.tsv
│       ├── amr_summary.txt
│       ├── PA34_mlst.tsv               (ST1284)
│       └── llm_judge_verdict.txt
└── extraction/
    ├── marker.md                       (NEEDS BACKFILL — europepmc fulltext.xml available)
    └── nougat.mmd                      (NEEDS BACKFILL — batch queue)
```

## Reproduced key numbers (traceable to evidence/)

- Pangenome 7,639 (paper 7,643; Δ4 / 0.05%)
- Core 5,079 (paper 5,078; Δ1)
- PA34 accessory 1,212 (paper 1,213; Δ1)
- PA34 unique 543 (paper 543; EXACT)
- No-ortholog PAO1/PA14/VRFPA04: 886/737/945 (paper 886/737/946; only VRFPA04 Δ1)
- PA34∩VRFPA04 exclusive: 124 (EXACT)
- Chromosome 6,810,079 bp GC 66.07%; pMKPA34-1 95,404 bp GC 57.2% (EXACT); pMKPA34-2 26,862 bp GC 61.0% (EXACT)
- MLST ST1284 (EXACT); exoU present; AAC(3)-IId 99.9% id; 16 acquired AMR genes (paper ≥12; delta = newer ResFinder DB)

## Verdict: REPLICATED
12/13 computational claims reproduce; 4 EXACT, rest Δ≤1 gene. Only wet-lab (C14) and manual MAUVE GIs (C13) out of reach.
