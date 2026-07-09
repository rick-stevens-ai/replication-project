# Attempt log — PDE-Herbert-2021-dielectric-continuum-qm

**Wave:** PDE-100 (rank 5), 2026-07-03.
**Assigned paper:** Herbert (2021) *Dielectric continuum methods for quantum chemistry*,
DOI 10.1002/wcms.1519, cites=141.

**Host:** CherryRd (macOS 25.3, x64). No uicgpu compute needed — problem is small
(4 solutes × 2 solvents × 4 methods × RHF/6-31G* = 96 s wall on 1 laptop core).

## Timeline

**18:09 CDT.** Read wave brief. Read BVBRC-17 exemplar + PDE-Wang-PoissonBoltzmann-2021 report as scaffold template.

**18:10.** Created target dir `~/Dropbox/REPLICATE-PROJECT/PDE-Herbert-dielectric-continuum-qm-2021/{report/evidence,work}`.
Attempted direct Wiley DOI fetch → HTTP 403 (bot check).
Queried Semantic Scholar `openAccessPdf` (with keychain S2 API key per standing rule): got arXiv preprint URL.
Fetched `https://arxiv.org/pdf/2203.06846` → HTTP 200, 3.3 MB PDF.

**18:11.** `pdf` tool failed (Anthropic credit balance and Gemini model routing errors — known environment issue). Fell back to `pdftotext -layout` → 4748 lines of extractable text. Grep hunt for "Table 1", "kcal/mol", "IEF-PCM", "COSMO" surfaced the key benchmark table on p.14 (Sec 2.4) verbatim.

**18:12.** Read Table 1: 4 solutes (H2O, CH3CONH2, NO+, CN-) × 2 solvents (toluene ε=2.4, water ε=78.3) × 5 methods (SVPE, SS(V)PE, SPE, COSMO ζ=0, COSMO ζ=1/2). Herbert states in the paragraph after Table 1 that "the statistical difference between these methods is ≲ 0.1 kcal/mol for neutral solutes and ≈ 0.5 kcal/mol for ions, even at ε_s = 2." This is the **concrete, testable, self-contained** claim — perfect target for a replication.

**18:12.** Chose replication engine: **PySCF** (free, open source, no license). Has C-PCM, IEF-PCM, COSMO, SS(V)PE in `pyscf.solvent.pcm.PCM`. Local install via project venv: `pyscf 2.13.1`.

**18:13.** Smoke test on H2O in water at RHF/6-31G*: all four PCM variants returned dG_elst in [-7.15, -7.25] kcal/mol — spread 0.10 kcal/mol. That's the paper's central claim, live. Wrote full replication script `work/replicate_table1.py` covering all 4×2×4 = 32 PCM SCFs.

**18:14.** Full run completed in 96.5 s. Results:
- Water (ε=78.3): neutral spreads 0.10 (H2O) and 0.16 (CH3CONH2) kcal/mol; ion spreads 1.21 (NO+) and 0.66 (CN-). Neutrals match "~0.1 kcal/mol" paper bound; ions slightly over "~0.5 kcal/mol" but within the same order of magnitude.
- Toluene (ε=2.4): COSMO is a clear outlier for ions — NO+ at -39.6 vs C-PCM/IEF-PCM/SS(V)PE at ≈ -47.5 (a ~8 kcal/mol gap). Directly reproduces the low-dielectric COSMO ion pathology visible in the paper's Table 1 (COSMO ζ=0 column vs SVPE).
- Absolute values differ from paper's SVPE reference by ~1-9 kcal/mol due to PySCF using Bondi vdW radii vs Chipman/Herbert's isodensity ρ₀=0.001 cavity. This was flagged a priori as an unfair comparison of absolute magnitudes — the cross-method-agreement claim is the physics-testable one.

Moved outputs to `report/evidence/table1_replication.{json,csv}` and `report/evidence/run_table1.log`.

**18:15.** LLM-judge round-trip. First tried `argo:claude-opus-4.7` via `urllib` → HTTP 502 upstream. Retried with `argo:gpt-5.2` → verdict `PARTIAL` (coverage 0.6, agreement 0.75). Rerun with `argo:claude-opus-4.7` succeeded on second attempt → verdict `REPLICATED` (coverage 0.75, agreement 0.85). Both judges agree the neutral-water and toluene-COSMO-ion claims reproduce; both flag the ion-water spread as slightly wider than the paper's ~0.5 kcal/mol bound.

**18:16.** Consensus verdict: **PARTIAL** — conservative call given ion-water spread (1.21 kcal/mol for NO+) exceeds the paper's stated ~0.5 kcal/mol bound. All qualitative physics (method convergence in high-ε, COSMO low-ε ion pathology) reproduces cleanly; C1 (formal operator equivalence) is derivational and not numerically testable; C4 (absolute SVPE numbers) requires isodensity cavity not available in PySCF.

**18:17.** Wrote REPORT.md, brief.md, artifact_harvest.md, this attempt_log.md.

## Friction tags

- `pdf-tool:down-anthropic-credit-and-gemini-routing` — worked around with `pdftotext`.
- `cavity:PySCF-Bondi-vdW-vs-paper-isodensity` — expected absolute-value gap, does not affect the physics claim.
- `source:review-paper-no-code` — replication built from equations + standard implementations.
- `judges:PARTIAL-vs-REPLICATED-split` — kept the conservative call.
