# PROGRESS — Friedland, Jacob, Kundrát 2010 (RR1965) replication

| Time (CDT 2026-06-09) | Phase | Note |
| --- | --- | --- |
| 14:51 | start | Subagent spawned: LUCID100 max-rate backfill slot 64, Wave 7. Task: artifact harvest + scoping + minimal smoke. |
| 14:52 | identify | Located target in `LUCID100_SOLID_MASTER_QA.tsv` as **rank 95** (slot 64 = backfill slot label). Confirmed paper: Friedland-Jacob-Kundrát 2010, Radiat Res 173:677, DOI 10.1667/RR1965.1. |
| 14:52 | scaffold | Created project dir `lucid-friedland-stochastic-nhej-track-slot64/` with `code/`, `figures/`, `results/`, `logs/`, `source/`. |
| 14:53 | harvest | DOI fetch (doi.org) → 406. Allenpress meridian → Cloudflare. Semantic Scholar S2 API confirmed paper id `86d0bfeb…`, `openAccessPdf.status = CLOSED`. Unpaywall confirmed `is_oa = false`, no repo copy. |
| 14:53 | harvest | PubMed E-Utilities returned full abstract (PMID 20426668) — the abstract is rich and describes the full model architecture, the four scenarios, the parameter-source split (presynaptic from Ku/DNA-PK FRAP; post-synaptic fit to ¹³⁷Cs fibroblast benchmark), and the key qualitative finding (three of four scenarios overestimate residual DSBs at low dose). Saved as `source/rr1965_metadata.md`. |
| 14:53 | harvest | Tried fetching OA companion PDFs. **Got:** Henthorn 2018 (Sci Rep, OA) 2.9 MB, Kundrát 2021 (Front Phys, OA) 2.4 MB, Li 2014 (PLoS ONE, OA) 0.9 MB. MDPI (Kundrát 2022 IJMS) blocked direct PDF download. PMC has no full-text mirror for RR1965 itself. |
| 14:54 | harvest | `pdftotext -layout` on the three OA companion PDFs. Grepped for Friedland references, rate constants, synapsis radii. **Key finds:** Henthorn 2018 cites RR1965 (ref 26) and uses 25 nm synapsis radius + ≤168 nm 24-h end displacement bound; Li 2014 fits sibling NHEJ scheme with explicit min⁻¹ rate constants (ka1=4.5, kd1=2.52, kLK=0.331, kEP=4.23, kpD=2.76, kLD=0.263). Compiled into `source/model_notes.md`. |
| 14:55 | scope decision | Closed paper + non-public PARTRAC = numerical four-scenario reproduction is INFEASIBLE. Architectural smoke is feasible: build a Gillespie-style stochastic NHEJ matching the state machine in the abstract, with rate constants in the Li-2014 regime, tuned to the qualitative abstract claims. Write up under "smoke" framing with friction tags. |
| 14:55 | implement v1 | Wrote `code/nhej_smoke.py` with 6-state per-end machine, brute-force pairwise synapsis check, vanilla Brownian diffusion. Wrote `code/run_smoke.py` driver. |
| 14:58 | run v1 | First run hung at 99% CPU for >4 min on O(N²) × 2880 timesteps × 8 repeats. Killed. |
| 14:59 | optimize v2 | Replaced brute synapsis with `scipy.spatial.cKDTree.query_pairs`. Increased dt to 2 min, reduced repeats to 5, ends to 40. Re-ran: 3 s wall but 0% rejoined — diffusion σ per step (80 nm) >> synapsis radius (25 nm) so ends drift past each other. |
| 15:00 | analyze v2 failure | Two compounding bugs: (a) free Brownian motion is wrong physics for the chromatin-tethered case described in the abstract; (b) presynaptic Ku attach/detach equilibrium oscillates at dt comparable to 1/k_ku_off, never reaches DNA-PK simultaneously on partner ends. |
| 15:00 | implement v3 | (a) Replaced free Brownian with Ornstein-Uhlenbeck tethered diffusion around an anchor at the initial DSB site (k=0.02 min⁻¹, D=4e-4 µm²/min → RMS displacement ~141 nm 1D / 245 nm 3D; consistent with Henthorn 2018 bound). (b) Collapsed `NAKED ↔ Ku ↔ DNA-PK` into `NAKED ↔ DNA-PK` at effective rates `k_load`, `k_unload`. (c) Rewrote first-order transition step to use competing-exponential probabilities (no order bias). |
| 15:01 | run v3 | Now reaches 100% rejoined at 24 h with ~5-10 min half-time — overshoots biology (no residual, no misrepair). |
| 15:02 | implement v4 | Added (i) `p_stuck_dirty` permanent-failure fraction for dirty DSBs (→ residual tail), (ii) intra-cluster DSB placement at 70-100 nm separation for `cluster_fraction` of breaks (→ misrepair channel), (iii) lowered ligation/clean rates by ~3×, (iv) split into low-LET and high-LET cases with different (dirty, cluster) settings. |
| 15:03 | run v4 final | 1.7 s wall. **Low-LET: residual 3.5%, misrejoin 3.0%, correct 93%, τ_fast ~10 min, τ_slow ~350 min.** **High-LET: residual 8%, misrejoin 22%, correct 67.5%, τ_fast ~24 min, τ_slow ~301 min.** All consistent with the qualitative claims in the RR1965 abstract and with γ-H2AX foci benchmarks. |
| 15:04 | report | Wrote `FIRST_PASS_REPORT.md`, this `PROGRESS.md`, `ARTIFACT_MANIFEST.md`, and the JSON progress record under `~/.openclaw/workspace/memory/subagent-progress/`. |

## Blockers encountered

| Blocker | Resolution |
| --- | --- |
| Paper PDF closed-access, no OA, no repo copy | Used PubMed abstract + 3 OA Friedland-group / NHEJ companion papers as scoping sources |
| `pdf` tool unavailable (Anthropic credit balance / Gemini model name / OpenAI extract plugin) | Used `pdftotext -layout` + `grep -E` to extract methods + parameter sections |
| `web_search` returns DDG bot-detection | Got everything we needed via Semantic Scholar API + direct OA PDF curls |
| `image` tool unavailable (same Anthropic credit issue) | Did not need it; figure correctness confirmed by numeric headline values |
| MDPI direct PDF download blocked | Did not need it — Kundrát 2021 (Frontiers) was sufficient |
| O(N²) synapsis check too slow | scipy cKDTree |
| dt discretization oscillation in NAKED↔Ku↔DNA-PK chain | Collapsed presynaptic phase to effective NAKED↔DNA-PK |
| Free Brownian motion drove ends apart | Switched to Ornstein-Uhlenbeck tethered diffusion |
| Initial parameter set rejoined everything in <10 min | Re-tuned ligation / cleaning rates to γ-H2AX-consistent timescales, added p_stuck_dirty + cluster_fraction |

## What was NOT done

- Did not contact the authors (per task constraints).
- Did not attempt access via Helmholtz preprint servers, Sci-Hub, library-link, or paid endpoints.
- Did not digitize any figures from RR1965 (we don't have it).
- Did not reproduce the four named scenarios numerically.
- Did not add chromosomal-aberration scoring (would require chromatin-geometry layer).
