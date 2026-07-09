# Artifacts Summary — BVBRC-108 (Akter 2023 replication)

**Repo root:** `~/Dropbox/REPLICATE-PROJECT/BVBRC-108-Akter-virulence-antibiotic-resistance-genes-2023/`

## Top-level report artifacts (`report/`)

| File | Purpose |
|---|---|
| `REPORT.md` | Canonical replication report (13 KB): paper-in-a-paragraph, claim table C1–C4, method (§3a assemblies, §3b AMR, §3c VF, §3d LLM-judge), verdict, reproducibility notes. |
| `REPORT.tex` | LaTeX version of REPORT.md with an additional dedicated **Genuine Critique** section (what replicated, what did not, novel Table 1 header-swap finding, methodological weaknesses, re-do recommendations). |
| `open_questions.json` | 5 truly open questions (VF/AMR co-occurrence, MGE linkage / horizontal transfer, database-version sensitivity, minimum assembly-quality threshold, in-silico → phenotype gap) with basis + next steps. |
| `workflow.md` | Step-by-step pipeline: setup → NCBI pull → AMRFinderPlus → VFDB tblastn → LLM-judge → synthesis. |
| `artifacts_summary.md` | This file. |
| `failure_analysis.md` | Honest failure/gap catalog + root causes. |

## Evidence (`report/evidence/`)

Referenced by `REPORT.md`:

- `vf_presence.json` — consolidated per-strain, per-gene VFDB set-A tblastn presence/absence with pident and qcov.
- `<strain>_tblastn_best.tsv` (× 3) — raw tblastn best-hit rows per strain (BFFF11, BFF1B1, BFPS6).
- `amr_summary.tsv` — aggregated AMRFinderPlus calls across all 3 strains.
- `judge_output.json` — raw structured LLM-judge output (Argo `claude-sonnet-4.6`, verdict PARTIAL, coverage 72%, agreement 85%).

## Working files (`work/`)

- `assemblies/BFFF11.fna` — NCBI CP045918.1 (2,761,629 bp, closed chromosome).
- `assemblies/BFF1B1.fna` — NCBI CP046022.1 (3,067,042 bp, closed chromosome).
- `assemblies/BFPS6.fna`  — NCBI GCF_021375735.1 (2,866,855 bp, 45 contigs, N50 270,331).
- BLAST DBs (per strain) — rebuildable in ~10 s each from `assemblies/*.fna`.

## Extraction (`extraction/`)

- `marker.md` — (not present in this run; paper text was worked from the DOI/PMC source directly).

## Key claims → evidence pointers

| Claim | Evidence artifact | Result |
|---|---|---|
| C1 assembly stats | `REPORT.md §3a` table + NCBI records CP045918.1 / CP046022.1 / GCF_021375735.1 | REPRODUCED bp-exact; **Table 1 header swap** noted. |
| C2a 12 always-present VFs | `vf_presence.json`, `*_tblastn_best.tsv` | REPRODUCED (≥98% pident, ≥95% qcov in all 3). |
| C2b cps cluster in BFFF11 | `vf_presence.json` (9 of 11 unique to BFFF11) | REPRODUCED pattern; VFDB-housekeeping conflation noted for cpsA/cpsB. |
| C2c prgB only in BFFF11 | `BFFF11_tblastn_best.tsv` | REPRODUCED (96%/100%). |
| C2d asa1 only in BFFF11 | `BFFF11_tblastn_best.tsv` | REPRODUCED (82.2%/100%). |
| C2e ctrA in BFFF11+BFF1B1 | `*_tblastn_best.tsv` | REPRODUCED. |
| C2f cylI in BFPS6; cylR2 in BFF1B1 | `*_tblastn_best.tsv` | REPRODUCED. |
| C3a lsa(A) shared, others weak | `amr_summary.tsv` | PARTIAL — lsa(A) confirmed all 3; mph(D)/dfr(E) not called by AMRFinderPlus. |
| C3b tet cluster only in BFPS6 | `amr_summary.tsv` | PARTIAL — tet(L)+tet(M) confirmed; tet(S)/tet(45) tool-scope. |
| C4 size ~2.8–3.1 Mb | `REPORT.md §3a` | REPRODUCED. |

## Verdict artifact

`report/evidence/judge_output.json`:
```json
{
  "verdict": "PARTIAL",
  "coverage_pct": 72,
  "agreement_pct": 85,
  "one_liner": "Core virulence and AMR gene claims largely reproduced; tet(S)/tet(45) and minor VF genes unconfirmed.",
  "model": "argo:claude-sonnet-4.6",
  "notes": "Opus-4.7 route returned 502 on prompt size; fell back to Sonnet-4.6."
}
```

## Reproducibility one-liner

```
On uicgpu with envs/amr (AMRFinderPlus 3.12.8 DB 2024-07-22.1, BLAST+ 2.16.0, VFDB set-A, NCBI datasets 18.32.0), the full pipeline from NCBI pull → AMR + VF calls → LLM-judge → REPORT.md runs end-to-end in ~4 min.
```
