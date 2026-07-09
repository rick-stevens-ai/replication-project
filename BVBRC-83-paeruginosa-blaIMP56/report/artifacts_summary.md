# Artifacts Summary — BVBRC-83

**Project directory:** `~/Dropbox/REPLICATE-PROJECT/BVBRC-83-paeruginosa-blaIMP56/`
**Target:** GenBank CP102481.1 (pPE52IMP, 27,635 bp)
**Verdict:** REPLICATED

---

## Report artifacts (`report/`)

| File                   | Purpose                                                          | Source                           |
|------------------------|------------------------------------------------------------------|----------------------------------|
| `REPORT.md`            | Primary narrative report with claims, method, results, verdict.  | Original replication run.        |
| `REPORT.tex`           | LaTeX render of REPORT.md + a dedicated Genuine Critique section that lists 9 caveats not in the Markdown. | Backfill from REPORT.md.         |
| `open_questions.json`  | Five OPEN follow-up questions grounded in *P. aeruginosa* / IMP-56 biology, each with `basis` + `next_steps`. | Backfill from REPORT.md.         |
| `workflow.md`          | Stage-by-stage description of the pipeline (Stage 0 through 7).  | Backfill from REPORT.md.         |
| `artifacts_summary.md` | This file — index of every artifact and where to find it.        | Backfill from REPORT.md.         |
| `failure_analysis.md`  | Post-mortem of failure modes, near-misses, and known limits.     | Backfill from REPORT.md.         |

---

## Work artifacts (`work/`) — referenced but NOT re-read for backfill

Per backfill task rules, `work/` was not opened during this turn. The following are enumerated from REPORT.md's own references only.

| Artifact                                        | Kind                | Referenced in REPORT.md as                               |
|-------------------------------------------------|---------------------|----------------------------------------------------------|
| `work/genbank/CP102481.1.gb`                    | GenBank flat file   | Target plasmid; fetched via NCBI EUtils.                 |
| `work/genbank/AM778842.1.gb`                    | GenBank flat file   | Sibling: pMATVIM-7.                                      |
| `work/genbank/CP033834.1.gb`                    | GenBank flat file   | Sibling: unnamed FDAARGOS_570.                           |
| `work/genbank/KX169264.1.gb`                    | GenBank flat file   | Sibling: pD5170990.                                      |
| `work/genbank/KP975076.1.gb`                    | GenBank flat file   | Sibling: pMRVIM0713.                                     |
| `work/genbank/MN336501.1.gb`                    | GenBank flat file   | Sibling: p4130-KPC.                                      |
| `work/analyze_ppe52imp.py`                      | Python script       | Structural analysis (size, %GC, CDS enum, keyword hits). |
| `work/queries.faa`                              | FASTA (2 proteins)  | RepA (301 aa) + MOBP11 relaxase (609 aa).                |
| `work/siblings_all_proteins.faa`                | FASTA (~222 aa)     | Concatenated proteomes of the 5 siblings.                |
| `work/siblings_all_proteins.p{hr,in,sq}`        | BLAST protein DB    | `makeblastdb` output.                                    |
| `work/repa_mobp11_vs_siblings.tsv`              | BLAST outfmt-6 TSV  | Pairwise identity table; Table 4 of REPORT.md.           |
| `work/cross_tab.tsv` (implicit)                 | TSV                 | Sibling structural summary; Table 5 of REPORT.md.        |
| `work/judge_prompt.json` (implicit)             | JSON                | LLM-judge prompt sent to Argo.                           |
| `work/judge_gpt4o.json`  (implicit)             | JSON                | argo:gpt-4o verdict payload.                             |
| `work/judge_gpt5.2.json` (implicit)             | JSON                | argo:gpt-5.2 verdict payload.                            |

> Files marked "(implicit)" are inferred from REPORT.md's method + results sections; exact filenames on disk may differ. Backfill run did not audit `work/` for exact names.

---

## Extraction (`extraction/`)

| File           | Status                                                            |
|----------------|-------------------------------------------------------------------|
| `marker.md`    | Not present at backfill time (`ENOENT` on read). No Marker-extracted markdown for this paper on disk. Paper is open-access CC-BY (PMC9501424) — re-extraction is possible on demand but was not required for this replication. |

---

## External inputs (not stored locally)

| Input                                       | Access                                      | Cost   |
|---------------------------------------------|---------------------------------------------|--------|
| NCBI EUtils (`efetch.fcgi`)                 | Public HTTPS                                | $0.00  |
| Argo proxy `argo:gpt-4o` (LLM judge)        | `http://127.0.0.1:44497/v1`, Bearer stevens | $0.00  |
| Argo proxy `argo:gpt-5.2` (LLM judge)       | same                                        | $0.00  |
| NCBI BLAST+ 2.17.0 (Homebrew)               | Local binary                                | $0.00  |
| Biopython 1.85                              | pip                                         | $0.00  |
| Python 3.14                                 | System                                      | $0.00  |

Total external cost: **$0.00** (fully free-tier per project convention).

---

## Provenance summary

- Original replication run: 2026-07-03.
- Backfill of sidecar artifacts (this turn): 2026-07-05.
- No re-fetching, no re-analysis, no `work/` reads performed during backfill; sidecars derived from `report/REPORT.md` text only.
- Verdict `REPLICATED` unchanged.

---

## Quick file-map (grep-friendly)

```
report/
├── REPORT.md               # narrative (primary)
├── REPORT.tex              # LaTeX + genuine critique
├── open_questions.json     # 5 OQs with basis + next_steps
├── workflow.md             # 7-stage pipeline
├── artifacts_summary.md    # this file
└── failure_analysis.md     # limits, near-misses, failure modes
work/
├── genbank/*.gb            # 6 GenBank files (1 target + 5 siblings)
├── analyze_ppe52imp.py     # Biopython structural analysis
├── queries.faa             # RepA + MOBP11 relaxase (FASTA)
├── siblings_all_proteins.* # BLAST subject DB
└── repa_mobp11_vs_siblings.tsv  # BLAST results
extraction/
└── (empty — no marker.md)
```
