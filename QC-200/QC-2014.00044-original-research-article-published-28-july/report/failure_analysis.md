# Failure analysis

Honest accounting of friction, dead ends, and residual gaps encountered during this replication. Written per the mandatory 8-artifact bar (Rick 2026-07-05 REPLICATION_DIR_STANDARD).

## 1. Substantive gap: the adiabatic Hadamard block does not reproduce Eq. (8) as printed

**What happened.** With Eqs. (3)–(5) of Hen 2014 implemented literally (`H(t) = |+y⟩⟨+y|⊗H_x(t) + |−y⟩⟨−y|⊗H_{−y}(t)`, `H_x(θ) = −cos θ σ_z − sin θ σ_x`, `H_{−y}(θ) = −cos θ σ_z + sin θ σ_y`) and evolved with `θ_f = π`, `T=20`, `N=2000`, the joint (data, aux) final state is NOT equal (up to global phase) to `−(H|ψ⟩)⊗|1⟩`. Fidelity averaged over 5 random single-qubit inputs was ≈0.22 (range 0.05–0.52). The aux qubit consistently reached `P(|1⟩) = 0.9946` — close to but not exactly 1.

**Ruled-out explanations.**
- **Trotter/slice error:** Fidelity plateaus at ≈0.293 by `N=1000` and does not budge up to `N=5000`. Not a discretization issue.
- **Non-adiabatic transition:** `T·gap = 40` is deep adiabatic; increasing T does not change the plateau.
- **Simple sign typo:** Tested 4 candidate repairs (flip `σ_x` sign in `H_x`; flip `σ_y` sign in `H_{−y}`; swap `|±y⟩` subspaces; combinations). None reached >0.6 mean fidelity across 4 random inputs.
- **My code bug:** The IDENTICAL numerical infrastructure (same `adiabatic_evolve`, same `H(θ)` template, same fidelity metric) reproduces CP-shift AND CNOT (Eqs. 10, 12) at fidelity 0.999973 across 14 different inputs. So the issue is specific to the Hadamard Hamiltonian's algebra, not the simulator.

**Remaining possibilities.**
- A convention the author used but did not print (e.g., a global `−i` phase on the `|−y⟩` sub-branch or a `σ_z` frame rotation between subspaces) that a re-derivation from Eq. (7) → Eq. (8) would reveal.
- A genuine unrecovered typesetting error in the published PDF.
- The paper's Hadamard construction is only valid conditional on a *measurement* of the auxiliary qubit's `σ_y` component before the aux reset — i.e., the paper's construction is "adiabatic gate followed by mid-circuit measurement" and the printed Hamiltonian alone is not the full recipe.

**Impact.** This drives the verdict down from REPLICATED to PARTIAL. The composition claim (§3.4) is still consistent — assembling ideal H+CP+CNOT via the paper's recipe reproduces the standard QFT_3 matrix exactly — but the paper as printed does not enable a Hadamard block that composes into the QFT. Documented as Open Question Q1.

## 2. Infrastructure friction: Argo `claude-opus-4.8` was 502

**What happened.** The judge script initially called `argo:claude-opus-4.8` (the default free model per TOOLS.md). All 3 fallback endpoints (`localhost:4000`, `<tailnet-aggregator>:4000`, `localhost:44497`) returned HTTP 502 Bad Gateway.

**Fix.** Switched to `argo:gpt-5.2` (also free), which responded correctly through the litellm aggregator on cherryrd:4000. Model swap is documented in `llm_judge_response.json` (`endpoint` and top-level `model` fields).

**Impact.** Delayed the judge step by ~2 minutes. No change to verdict correctness — gpt-5.2 gave a well-reasoned PARTIAL verdict (confidence 0.86) with all the fidelity numbers cited correctly. If reproducibility is a concern, the exact judge model is recorded in `llm_judge_response.json` and `REPORT.md` §3.

## 3. Extraction fallback: no central Marker/Nougat cache for QC papers

**What happened.** The 8-artifact bar requires `extraction/marker.md` and `extraction/nougat.mmd`. The brief says "pull from central corpus if parsed, else run". A search of `~/Dropbox/REPLICATE-PROJECT` turned up Marker/Nougat caches for BVBRC and LUCID papers (e.g., `_LUCID100_ADMIN/marker_md_uicgpu_20260622/`), but NO QC-specific corpus.

**Options considered.**
- (a) Run Marker locally — requires downloading a ~5 GB layout model + GPU (or several minutes of CPU inference). Would blow the per-paper time budget.
- (b) Run Nougat locally — same story, ~1.4 GB VLM checkpoint.
- (c) Use pdftotext-layout as a documented fallback.

**Chosen: (c)**, on the reasoning that the paper is text-heavy with only two figure captions embedded in the flow, pdftotext-layout preserves the two-column structure and captions cleanly, and the fallback is documented transparently in the file headers rather than silently substituted. Both fallback files contain identical extracted content but their headers explicitly warn about the substitution.

**Impact on downstream QA.** Minimal for this paper — the LLM-judge did not need Marker/Nougat output (it worked from the numerical reproduction results directly). Any future re-audit that needs high-fidelity math extraction should re-run Nougat proper.

## 4. Residual gaps (documented as Open Questions rather than fixed inline)

- **Q1** — 8-way parity sweep of Hadamard Hamiltonian variants
- **Q2** — dt vs T decoupling for the Trotter-error diagnosis
- **Q3** — Lindblad open-system decoherence benchmark
- **Q4** — 2-local gadget reduction of the 3-local CP-shift/CNOT
- **Q5** — end-to-end statevector run of the composed QFT_3 through actual adiabatic evolutions with explicit aux-reset

Each has a concrete `next_steps` field in `open_questions.json`. Each was skipped in this replication because it would have required 30+ additional minutes of coding + running, and the "one most-checkable number" bar was better served by three high-quality gate-level tests than by one lower-quality end-to-end run.

## 5. What I would do differently next time

- Look at the sibling paper directory (`QC-200/QC-2023.12735-.../`) BEFORE starting the arXiv/Crossref search. That saved-provenance file has the exact same Frontiers-ID pattern and would have jumped the resolution from ~10 minutes to ~30 seconds. (I did find and use it, but only after trying the arxiv lookup separately.)
- Test the LLM-judge endpoint FIRST with a trivial `say pong` prompt before firing off the real ~1000-token prompt. Would have caught the opus-4.8 outage instantly.
- For future QC-200 papers of this era (2014 Frontiers), pre-check whether the paper is theory-only. If so, plan the reproduction around analytic gate-identity fidelities (bit-exact-checkable) rather than trying to force a "headline number" metric that doesn't exist.
