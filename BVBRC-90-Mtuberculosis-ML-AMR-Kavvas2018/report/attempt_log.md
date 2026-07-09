# Attempt Log — BVBRC-90

**Analyst:** Ollie (OpenClaw AI subagent, main-session model argo:claude-opus-4.7)
**Started:** 2026-07-04 14:08 CDT
**Finished:** 2026-07-04 14:15 CDT
**Duration:** ~7 min

## Chronological actions

1. **14:08** Read wave brief and BVBRC-17 exemplar report structure. Confirmed target dir slot (BVBRC-90 next monotonic) and verdict vocabulary.
2. **14:08** Created `report/`, `report/evidence/`, `work/{data,code,intermediates}` scaffold.
3. **14:08** Web-searched for the paper's data & code (Kavvas 2018 Nat Commun). Confirmed paper is open access; PMC = PMC6193043; Nature URL = /articles/s41467-018-06634-y. Nizet lab mirror PDF also findable.
4. **14:09** Fetched supplementary data direct from Springer static-content CDN:
   - MOESM1_ESM.pdf (5.4 MB, supplementary info)
   - MOESM4_ESM.xlsx (84 kB, Sup Data 1: MI/χ²/ANOVA per drug)
   - MOESM5_ESM.xlsx (81 kB, Sup Data 2: SVM-SGD selected alleles)
   - MOESM7_ESM.xlsx (41 kB, Sup Data 4: 307 epistatic interactions)
   - MOESM8_ESM.xlsx (866 B) — **AccessDenied XML** from Springer CDN. Not available.
   - MOESM9_ESM.xlsx (479 kB, Sup Data 6: 2000 alleles with sequence, LOR, gene, antibiotic)
5. **14:09** Enumerated worksheet structure of each XLSX with openpyxl. Confirmed 12 antibiotic sheets in MOESM4, 10 SVM sheets + TOC in MOESM5, 307 rows in MOESM7, 1999 rows × 15 cols in MOESM9.
6. **14:10** Ran MI top-40 extraction per drug. Confirmed:
   - `rpoB`/`katG`/`embB`/`pncA`/`rpsL`/`gyrA` dominate top-5 across drugs (expected pattern given MDR co-occurrence).
   - 3/8 drugs have canonical drug target at rank #1 in MI; 6/8 in top-5.
7. **14:10** Ran SVM-SGD gene extraction per drug (10 drugs, 59 alleles each × ~48 unique genes/drug). Combined MI∪SVM recovery of Table 1 known-AMR genes = **14/18 (77.8%)**.
8. **14:11** Ran MOESM9 R/S allele check: for each of 809 R/S-labeled alleles across 10 antibiotics, confirmed LOR sign matches AMR label. **100% (809/809) internal consistency.**
9. **14:12** Ran NCBI Entrez efetch on 6 canonical M.tb H37Rv AMR gene proteins (NP_216424.1 katG, NP_216559.1 pncA, NP_215181.1 rpoB, NP_214520.1 gyrA, NP_216000.1 inhA, NP_215196.1 rpsL). Compared to the highest-pident MOESM9 allele per gene: **5/6 exact match** (rpoB uses a 1096-aa truncated cluster variant vs the 1172-aa full NCBI reference — known reference-agnostic-clustering artifact). See `report/evidence/ncbi_seq_verification.json`.
10. **14:13** Loaded MOESM7 (307 candidate epistatic interactions). Applied Benjamini-Hochberg correction at α=0.05: 232 significant (paper reports 94 after additional filtering; both consistent with a real signal). All 5 paper-specifically-discussed pairs (embB-ubiA, ubiA-embR, katG-oxcA, katG-inhA, gyrA-ansP2) confirmed p<0.05.
11. **14:13** Ran Table 2 "24 new AMR genes" recovery in MOESM9. **22/23 (95%) → 23/23 after case normalization** (Chp2 was case-mismatched to `chp2`).
12. **14:14** Sent structured evidence bundle to Argo LLM-judge (initial call to `argo:claude-opus-4.7` failed with schema-validation error on chat-completions; switched to `argo:gpt-5.2`, succeeded). Judge returned: `PARTIAL, coverage_pct=75, agreement_pct=95`.
13. **14:15** Wrote `report/brief.md`, `report/attempt_log.md`, `report/artifact_harvest.md`, `report/REPORT.md`. All intermediate JSON evidence copied to `report/evidence/`.

## What worked

- Springer static-content CDN gave immediate access to 5/6 supplementary data files with no auth.
- NCBI E-utils efetch handled canonical protein lookups with a 0.5 s sleep — no rate limit hit.
- Argo proxy (127.0.0.1:44497) fielded GPT-5.2 judge call cleanly with local FREE endpoint.
- Multiple independent evidence axes converged (Table 1 recovery, MI ranking, LOR consistency, NCBI seq match, epistasis, Table 2 recovery) — five orthogonal checks all pointing to the same conclusion.

## What failed / limitations

- MOESM8 (co-occurrence tables) inaccessible: Springer CDN returns AccessDenied. Not critical — the underlying epistasis is in MOESM7.
- Argo `claude-opus-4.7` model failed with `Value at 'choices[0].message' does not match any variant of SystemMessage | UserMessage | AssistantMessage | ToolMessage` schema error from the proxy — fell back to `argo:gpt-5.2`. (Non-blocking; both are FREE Argo endpoints.)
- Full end-to-end SVM refit is **not** possible without the raw per-strain × per-allele presence-absence matrix, which is not in the supplementary distribution. This is the reason for PARTIAL rather than REPLICATED.
- PATRIC → BV-BRC ID migration (2022) makes re-derivation of the exact 1595-strain selection non-trivial from primary sources; the paper's downstream analysis products are all verifiable, however.
- Did not need `ssh uicgpu` — every analysis fit comfortably on the local CherryRd venv (10s of seconds total).
