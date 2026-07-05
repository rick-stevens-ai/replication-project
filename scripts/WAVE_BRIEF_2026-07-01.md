# Replication Wave Brief — 2026-07-01 (night push)

You are executing ONE independent-replication of ONE assigned paper for the X-100 replication project.

## Hard rules
- **Free endpoints only** for any LLM inference (Argo proxy localhost:44497 key=stevens, ALCF Sophia, CELS chicago-1..4). NEVER Anthropic/OpenAI/OpenRouter direct.
- **Real replication only.** Download actual public data (NCBI Datasets REST, BiGG, arXiv source, OSTI PDF, Zenodo, GitHub code) and run actual analysis (FBA/COBRApy, BLAST, numerical PDE solve, quantum sim, etc.). No fabricated numbers.
- **LLM-judge scoring, never regex** for the final verdict/coverage/agreement.
- **Preserve completed work.** Do not overwrite existing sibling replication dirs. Write ONLY inside your assigned target dir.
- Respect API rate limits (S2 API key from keychain `semantic-scholar-api-key` acct `rick-stevens-ai`; NCBI Datasets is free/no-auth but be gentle).

## Compute
- Light analysis: run locally in your workspace (make a venv).
- Heavy compute (large genomes, big FBA sweeps, GPU): `ssh uicgpu` (8×A100, 255 cores, 2TB RAM). Source `~/env.sh` there for proxy internet. Use it for anything nontrivial.

## Output structure (mirror BVBRC-17 exemplar)
Target dir: `~/Dropbox/REPLICATE-PROJECT/<SET-ID-slug>/`
- `report/REPORT.md` — full report: paper summary, claims table (C1..Cn with type + testable? + tested?), Method (numbered, exact data sources + tool versions + commands), Results vs paper (tables), Verdict + justification.
- `report/brief.md` — 1-paragraph what/why.
- `report/attempt_log.md` — chronological log of what you did, what worked/failed.
- `report/artifact_harvest.md` — every public artifact pulled (URL, accession, size, checksum if easy).
- `report/evidence/` — actual outputs (json, csv, logs, small figures).
- `report/open_questions.json` — **MANDATORY**: exactly 5 NEW open research questions that arose from doing THIS replication (JSON list of 5 `{"q":..., "basis":...}`), plus an `## Open Questions` (Q1..Q5) section in REPORT.md. Ground each in what you actually observed/ran — paper-vs-result gaps, unspecified details, follow-on experiments the reproduction suggests, sensitivity/scaling questions, methodological ambiguities. Not generic "future work" copied from the paper. Feeds the cross-project open-questions corpus (Rick standing rule 2026-07-05).
- `work/` — code + downloaded data + intermediate files.

## MANDATORY 8-artifact completion bar (Rick 2026-07-05 — see REPLICATION_DIR_STANDARD_2026-07-05.md)
Before printing WAVE_RESULT, the target dir MUST contain all 8: (1) `paper.pdf`; (2) `extraction/marker.md`; (3) `extraction/nougat.mmd` (pull from central corpus if parsed, else run); (4) `report/REPORT.tex` very detailed section-by-section LaTeX (what worked/didn't per claim); (5) `report/open_questions.json` = 5 heavy-duty non-superficial questions each `{q,basis,next_steps}` + `## Open Questions` in report; (6) `report/workflow.md` (workflow + tools/codes + effort estimate); (7) `report/artifacts_summary.md`; (8) `report/failure_analysis.md`.

## Verdict vocabulary (canonical)
REPLICATED (core claims independently reproduced on real data) · PARTIAL (some claims reproduced, some out of reach) · SPOT-CHECK (data availability + method plausibility verified, no full rerun) · NO-GO (data/code unavailable or paywalled) · CONTRADICTED (rerun disagrees with paper) · BLOCKED (external blocker) · FAILED (attempted, could not reproduce for technical reasons).
"Solid" = REPLICATED or PARTIAL. Aim for solid where the evidence honestly supports it — do not inflate.

## When done
Print a final line: `WAVE_RESULT set=<set> paper=<id> verdict=<VERDICT> dir=<path> one_line=<summary>`
