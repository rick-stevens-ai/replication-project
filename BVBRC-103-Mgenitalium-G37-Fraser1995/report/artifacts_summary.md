# Artifacts Summary — BVBRC-103 (Fraser et al. 1995)

## 8-artifact standard status

| # | Artifact | Status | Notes |
|---|---|---|---|
| 1 | `paper.pdf` | **MISSING (paywalled)** | Fraser 1995 *Science* is paywalled; Unpaywall `is_oa=false` for DOI 10.1126/science.270.5235.397. `paper.pdf.PENDING.md` marker present. Genome sequence (the actual object of replication) is fully open. |
| 2 | `extraction/marker.md` | Stub (PENDING) | No PDF to parse; marker.md documents the paywall + zero OA locations. |
| 3 | `extraction/nougat.mmd` | Stub (pending) | Same reason; awaits central Eagle GPU parse only if an OA copy surfaces. |
| 4 | `report/REPORT.tex` (+ .md) | **PRESENT** | Detailed section-by-section report; REPORT.md is the primary narrative, REPORT.tex the LaTeX standard artifact with dedicated critique section. |
| 5 | `report/open_questions.json` | **PRESENT** | 5 heavy-duty open questions with basis + next_steps. |
| 6 | `report/workflow.md` | **PRESENT** | Workflow + tools + work estimate. |
| 7 | `report/artifacts_summary.md` | **PRESENT** | This file. |
| 8 | `report/failure_analysis.md` | **PRESENT** | Honest failure analysis. |

## Evidence / traces

```
BVBRC-103-Mgenitalium-G37-Fraser1995/
├── paper.pdf.PENDING.md              (paywall marker)
├── extraction/
│   ├── marker.md                     (PENDING stub — paywall documented)
│   └── nougat.mmd                    (pending stub)
├── report/
│   ├── REPORT.md                     (primary narrative, verdict REPLICATED)
│   ├── REPORT.tex                    (8-artifact LaTeX report + critique)
│   ├── open_questions.json           (5 questions)
│   ├── workflow.md
│   ├── artifacts_summary.md          (this file)
│   ├── failure_analysis.md
│   ├── brief.md, attempt_log.md, artifact_harvest.md
│   └── evidence/
│       ├── genome_stats.json         (reproduced numeric stats)
│       └── llm_judge.json            (Argo per-claim judgments)
└── work/
    ├── Mgenitalium_G37_NC_000908.2.gb   (780 KB, sha256 50da1e36…)
    ├── Mgenitalium_G37_NC_000908.2.fna  (588 KB, sha256 cc21ace7…)
    ├── analyze_genome.py
    ├── llm_judge.py
    └── analysis_output.txt
```

## Reproduced key numbers (traceable to evidence/genome_stats.json)

- Genome length 580,076 bp (paper 580,070; Δ +6 bp)
- G+C 31.69% (paper ~32%)
- 504 intact CDS + 20 pseudogenes (paper ~470 ORFs)
- 1 rRNA operon; 36 tRNAs; 20/20 amino acids
- Coding density 93.04%; mean CDS 356 aa; N=0

## Verdict: REPLICATED
Core quantitative + structural + historical claims independently reproduced on the open RefSeq descendant of the Fraser sequence using independent software (Biopython) and free compute. C3 gene count CLOSE (expected annotation drift).
