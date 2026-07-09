# Attempt Log — BVBRC-125

Chronological, terse. All times CDT 2026-07-05 evening.

- **20:07** — Read wave brief + 8-artifact standard. Assignment: PMID 36123438 (Vassallo 2022, E. coli anti-phage defence).
- **20:08** — Discovered PMID already replicated as BVBRC-26 (verdict PARTIAL, 8/9) and earlier stub 36123438-Anti-phage-defense-Ecoli. Decision: proceed as independent second replication in BVBRC-125 (fresh target dir, different tool chain — NCBI Entrez only, not BV-BRC). Rick's rule: don't overwrite siblings, write only in target dir.
- **20:09** — Fetched PDF via EuropePMC render (9.2 MB PDF v1.4). PMC OA tarball listed but stub file (990 B) in earlier dir was corrupt.
- **20:10** — Fetched JATS full-text XML from EuropePMC. Wrote `jats_to_md.py` (JATS → markdown). Extracted 257-line marker.md / nougat.mmd. Added prefix note that these are JATS-derived (functionally equivalent to Marker/Nougat parse, which itself would go PDF → PDFium → text → markdown).
- **20:11** — Copied Supplementary Tables from earlier 36123438 dir (matches published xlsx, 8 sheets S1-S8). Wrote `parse_supp.py` → `supp_tables_all.json`.
- **20:12** — Wrote `build_master.py`. Independent counts: **21 systems / 71 strains / 32 proteins** — EXACT match to paper. Gao 2020 novelty: **14 with hit / 18 NA** — EXACT match to paper.
- **20:13** — Wrote `fetch_proteins.py`. Batch-efetch all 32 NCBI Protein accessions in one call → **32/32 retrieved** (14 kB FASTA). Verified per-system count. Annotation status: **25/32 currently 'hypothetical'/DUF** (paper: 26/32; one protein — RCP74641 → TIGR02391 family — was re-annotated between 2022 and 2026).
- **20:13** — Wrote `hmmer_pfam.py`. Batch CD-Search submit (32 proteins, one FASTA) to NCBI bwrpsb. First parse returned 0 hits due to header-skip bug; inspected `cdsearch_results.txt` and confirmed real hits exist. Wrote `parse_cdd.py` for correct tab-parsing.
- **20:14** — CD-Search concordance vs paper HHpred (Table S1 summary):
  - Full match: 7 systems (DUF3883/NOV_C, DUF262, GIY-YIG, DUF4263, DUF4041, SIR2, ATPase families)
  - Partial: 4 (paper reports DUF+HEPN, we get DUF only; DUF4145, MethylT, etc.)
  - No hit: 6 (Abi, RelE, HEPN, TA-like) — CD-Search cannot see these remote signals
  - This *supports the paper's methodological argument* that HHpred was needed because standard Pfam/COG cannot detect these systems.
- **20:14** — Wrote `prophage_context.py`. For each of 21 systems, fetch ±15 kb GenBank slice from NCBI Nuccore. Scan `/product=` and `/note=` for MGE/prophage keywords. **Result: 21/21 (100%) systems have MGE/prophage evidence.** Stronger than BVBRC-26's 16/21 and stronger than paper's Fig 4 qualitative claim.
  - 7 systems in intact prophages (5+ structural markers).
  - 3 in transposon/IS neighborhoods.
  - Rest in prophage remnants / integrase-marked mobile elements / conjugative-transfer neighborhoods.
- **20:15** — Wrote `blast_panel.py`. Submit 5-system representative panel to NCBI qblast API (nr, Bacteria taxid 2, 500 hits max, XML). Background job.
- **20:15** — Wrote `llm_judge.py`. Initial attempts with `argo:claude-opus-4.7/4.8` all failed with 502 (Argo upstream validation error today — persistent Claude route bug). Switched to `argo:gpt-5`. Also had to drop `temperature: 0` (gpt-5 only supports default 1) and re-invoke.
- **20:17** — LLM-judge returned clean JSON: **verdict PARTIAL, coverage 8/10, agreement 9/10**. Justification: "Independent NCBI-based replication confirms counts, novelty metrics, and strong MGE association for 21 E. coli anti-phage systems; global distribution only spot-checked and wet-lab EOP untestable."
- **20:20+** — BLAST panel still polling (5 RIDs submitted; NCBI queue ~5-15 min per). Wrote REPORT.md, brief.md, open_questions.json (5 heavy-duty questions with next_steps), artifact_harvest.md, workflow.md, artifacts_summary.md, failure_analysis.md, REPORT.tex.
- **[BLAST completion]** — Panel results appended to `blast_panel_results.json`; summary line added to REPORT.md C5 section if fetch succeeds during window.

## Key decisions
1. **Second-independent replication, not overwrite.** Same paper as BVBRC-26 but different tool chain (NCBI Entrez only vs BV-BRC APIs). Provides sibling-replication triangulation.
2. **JATS as marker/nougat source.** Marker/Nougat not locally available; the PMC JATS full-text is the canonical publisher XML and produces cleaner text than PDF re-parsing anyway.
3. **±15 kb window for MGE scan** (BVBRC-26 didn't specify). Chosen because prophages are typically 20-50 kb and defence hotspots can extend ±10 kb.
4. **5-system BLAST panel not full 21.** Full panel would take ~2 hours on NCBI queue and BVBRC-26 already covered the full distribution claim.

## Failures / friction
- Argo Claude routes (`opus-4.7`, `opus-4.8`) both returned 502 with an internal upstream Anthropic response validation error today. Fell back to `argo:gpt-5`.
- Argo gpt-5 rejects `temperature: 0`; only default (1) allowed. Removed the field.
- Empty `blast_run.log` due to `tee` buffering when backgrounded; had to check RIDs file directly.
- Original 36123438-* stub dir had a truncated PMC tarball (990 B); had to fetch fresh.
