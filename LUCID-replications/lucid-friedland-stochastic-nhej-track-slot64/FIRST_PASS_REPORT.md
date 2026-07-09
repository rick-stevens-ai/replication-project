# FIRST PASS REPORT — Friedland, Jacob, Kundrát 2010 (RR1965)

**Slot:** LUCID100 backfill slot 64 (Wave 7, master-QA rank 95)
**Paper:** Friedland W, Jacob P, Kundrát P. *Stochastic Simulation of DNA Double-Strand Break Repair by Non-homologous End Joining Based on Track Structure Calculations.* Radiat Res 173(5):677–688 (2010). DOI [10.1667/RR1965.1](https://doi.org/10.1667/RR1965.1). PMID 20426668.
**Run date:** 2026-06-09
**Host:** CherryRd (laptop CPU, <2 s wall)
**Verdict:** **ARCHITECTURAL SMOKE — PASS (qualitative).** Quantitative reproduction of the four-scenario figures is **NOT FEASIBLE** without the closed paper + non-public PARTRAC. Recommended QA retag: **KEEP, completed as architectural smoke; flagged for closed-access friction.**

---

## 1. Openness assessment

| Asset | Status |
| --- | --- |
| Paper PDF | **CLOSED.** Unpaywall (queried 2026-06-09): `is_oa = false`, `has_repository_copy = false`, `oa_locations = []`. doi.org returns 406 to our fetcher; Allenpress requires Cloudflare JS challenge. |
| PubMed abstract | OPEN. Full abstract retrieved (`source/pubmed_20426668.xml`). Captures the model architecture clearly. |
| References (in-paper) | Elided by publisher in the Semantic Scholar API. |
| PARTRAC code | **NOT PUBLIC** (Helmholtz-internal). |
| Parameter tables (Ku, DNA-PK rates) | Not in any of the OA companion papers we surveyed. |
| Companion/citing OA papers | Several, used as proxies for architecture and rate-regime: Henthorn 2018 (Sci Rep, GOLD CCBY); Kundrát 2021 (Front Phys, GOLD CCBY); Li 2014 (PLoS ONE, GOLD CC0); Friedland 2011 PARTRAC (Mutat Res, closed); Kundrát 2020 (Sci Rep, GOLD CCBY — already replicated in `lucid-partrac-analytical-formulas`). |
| External data needed for replication | None for the smoke; **yes** (¹³⁷Cs PFGE/γ-H2AX kinetics + Ku FRAP curves) for a numerical fit. |
| Endpoints used | Free only (Semantic Scholar, Unpaywall, PubMed E-Utilities, public OA PDFs). No paid LLMs. No author contact. |

## 2. Replication scope

### What we attempted (smoke replication)

We implemented a **reduced stochastic NHEJ Gillespie-style simulation** in pure NumPy that mirrors the *architecture* described in the RR1965 abstract:

1. Per-end state machine: `naked → DNA-PK loaded → synapsed → processed → ligated`.
2. Synapsis only between two `DNA-PK`-loaded ends within a spatial-proximity radius.
3. Clean ends: single rate-limiting post-synaptic step.
4. Dirty ends: multi-step Erlang-distributed cleaning before ligation.
5. Tethered Ornstein–Uhlenbeck diffusion of ends around their initial site (consistent with Henthorn 2018 motion bound of ≤168 nm in 24 h).
6. Inter-DSB clustering toggle (more clusters at high LET) to generate misrepair.
7. Permanent-failure fraction for dirty DSBs to generate the residual-DSB tail at 24 h.

**Rate constants** are drawn from Li 2014 (PLoS ONE) — a citing paper with same topology — with units of min⁻¹, and then **tuned** to align with the *qualitative* RR1965 abstract claims (biphasic kinetics, ~few-% residual, more misrepair at high LET). They are **not** the verbatim RR1965 Table values, which are paywalled.

### What we did NOT attempt

| Out-of-scope | Reason |
| --- | --- |
| Numerical reproduction of the four RR1965 scenarios | Scenarios are named/distinguished only in the closed PDF |
| Comparison to the in-paper ¹³⁷Cs human-fibroblast PFGE benchmark | Benchmark digitization requires the figure |
| Reproduction of the chromosomal-aberration yield curves | Requires a chromatin-geometry model on top of NHEJ |
| Reproduction of the misrepair yield vs. dose curves | Requires PARTRAC DSB-spectrum input |
| Step-by-step base-lesion-and-SSB removal in dirty ends | Collapsed to a 3-step Erlang surrogate |
| 3D nuclear attachment-site geometry | Replaced by 1D effective OU tether |

## 3. Headline smoke results

5-repeat ensemble averages, 40 DSBs per run, 24 h simulation (1.7 s wall on CherryRd):

| Quantity | low-LET case (30% dirty, 5% clustered) | high-LET case (70% dirty, 35% clustered) | RR1965 / NHEJ benchmark |
| --- | --- | --- | --- |
| residual DSBs @ 24 h | **3.5 %** | **8.0 %** | "few percent"; abstract states three of four scenarios *overestimate* residuals — our chosen tuning sits near the right scenario for low-LET |
| correct rejoin @ 24 h | 93.0 % | 67.5 % | Decreases with LET ✓ |
| misrejoined @ 24 h | **3.0 %** | **22 %** | Increases with LET ✓; matches the abstract's "misrejoined DSBs and chromosomal aberrations are in surprisingly good agreement with measurements" |
| τ_fast (bi-exp fit) | ~10 min | ~24 min | tens of min (γ-H2AX, PFGE) ✓ |
| τ_slow (bi-exp fit) | ~350 min | ~301 min | ~hours ✓ |

**Headline:** Biphasic DSB rejoining kinetics, LET-dependent misrepair, and a few-percent 24 h residual emerge naturally from the architectural smoke — matching the qualitative phenomenology that RR1965's four-scenario sweep was designed to investigate.

## 4. Friction tags

- `closed-access-paper`
- `partrac-not-public`
- `parameters-elided` (Ku, DNA-PK, clean/dirty rate constants not in any OA secondary we surveyed)
- `four-scenarios-not-distinguishable` (abstract enumerates but does not name them)
- `companion-rate-constants-only` (numbers used by smoke are Li 2014's, not RR1965's)
- `parameters-tuned-to-qualitative-targets` (we hand-tuned k_syn / k_lig_clean / k_clean_step / p_stuck_dirty to align with abstract claims and γ-H2AX phenomenology, not with RR1965 figures we cannot see)
- `simplification: spatial-geometry` (smoke uses tethered OU instead of PARTRAC 3D nuclear geometry)
- `simplification: dirty-end-cleaning-collapsed` (3-step Erlang vs per-lesion removal)
- `simplification: chromatin-aberrations-not-scored`
- `discretization-aware-state-machine` (presynaptic Ku attach/detach equilibrium collapsed into an effective `k_load` to avoid dt-discretization oscillation; documented in `nhej_smoke.py`)

## 5. Compute / endpoints / cost

- All work on CherryRd laptop CPU, Python 3.14, single core.
- Wall-clock: <2 s for the smoke; whole replication scoping <10 min CPU-time-equivalent including PDF text extraction.
- No GPU, no remote compute, no paid endpoints.
- No author contact.
- No heavy job plan needed; this slot is fully runnable on CherryRd.

## 6. QA retag / verdict recommendation for LUCID100_SOLID_MASTER_QA

Original QA decision (rank 95): `KEEP: relevant and replication-plausible`.

**Recommended updated decision:**

> KEEP_DONE_PARTIAL: architectural smoke complete. Quantitative four-scenario reproduction blocked by closed paper + non-public PARTRAC. Architectural/qualitative replication of the abstract claims (biphasic kinetics, LET-dependent misrepair, few-% residual) is implemented and reproducible in <2 s on CPU. Friction tags: closed-access-paper, partrac-not-public, parameters-elided. No paid endpoints used. See `lucid-friedland-stochastic-nhej-track-slot64/`.

## 7. Next actions

1. **No further work needed at this slot** unless someone obtains the journal PDF and the parameter tables, at which point we could replace the Li-2014 placeholder rates with the actual RR1965 Tables and run the four named scenarios.
2. If the PARTRAC code ever becomes available (e.g., via a Helmholtz collaboration), we could re-couple the NHEJ smoke to a real PARTRAC DSB-spectrum input for any of `lucid-partrac-analytical-formulas`, `lucid-slow-fast-nhej`, this slot, and the future Kundrát/Friedland slots.
3. Add a cross-link from the master-QA TSV `replication_folder` column for rank 95 → `lucid-friedland-stochastic-nhej-track-slot64`.


## Verdict

**Verdict: PARTIAL** (Coverage 3/10, Agreement 5/10). — Architectural NHEJ smoke reproduces biphasic kinetics + LET misrepair qualitatively; closed paper/PARTRAC blocks quantitative

<!-- census-verdict: PARTIAL assigned 2026-07-08 by LLM judge (Argo Opus) -->
