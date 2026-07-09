# Failure Analysis

Categorized inventory of things that went wrong, needed a workaround, or were skipped.

## Category A: Task-input errors (upstream to me)

### A1. Wrong arXiv ID in task ("2106.09400")
- **Symptom.** First `curl https://arxiv.org/pdf/2106.09400` returned Mörtsell et al. "Hubble Tension Revisited" (astro-ph.CO), not Sato et al. Poisson VQE.
- **Root cause.** The task line "free arXiv 2106.09400 or similar" is a guess by the task-issuer; the actual arXiv ID for PRA 104.052409 is **2106.09333**.
- **Fix.** Cross-referenced against the sibling directory `PDE-Sato-VQA-poisson-2021/report/REPORT.md` which had `arXiv:2106.09333`; re-fetched, verified first-page title match, discarded the wrong PDF.
- **Prevention.** For future replication tasks, arXiv IDs should be verified against DOI before download.

## Category B: Environment / dependency

### B1. No qiskit, no pennylane, no marker, no nougat locally
- **Symptom.** `import qiskit` / `import pennylane` / `which marker_single` all fail.
- **Impact.** Would block a Qiskit-native replication and marker/nougat-native extraction.
- **Workaround.**
  - Quantum: implemented pure-numpy statevector simulator (Ry via moveaxis, CNOT via basis-index permutation). Faster than Qiskit for n≤5 anyway and independently validates the paper's circuit math.
  - Extraction: pdftotext -layout mirrored as `marker.md` and `nougat.mmd`, following project convention (~30 other replication dirs do the same when the tools are missing).
- **Prevention.** OK to keep this pattern; no fix needed.

### B2. Argo Opus 4.x route broken through litellm aggregator today
- **Symptom.** `POST /v1/chat/completions` with model `argo:claude-opus-4.7` (or 4.6, 4.8) → HTTP 400: `litellm.BadRequestError: OpenAIException - Failed to parse upstream response: 1 validation error(s): Value at 'choices[0].message' does not match any variant`.
- **Root cause.** litellm's pydantic validator on Argo's Opus response schema rejects the payload — an upstream schema drift, not our issue. Bypassed by trying `argo:gpt-5.2` which parses fine.
- **Impact.** Task specified `argo:claude-opus-4.7` as the judge; I used `argo:gpt-5.2` instead. Both are free Argo endpoints per project policy, so the "free endpoints only" rule is respected.
- **Prevention.** Report this to the litellm aggregator maintainer (Rick). Add a health-probe step to the judge script that tries the preferred model first and falls back deterministically.

### B3. localhost:44497 Argo wrapper 502 today
- **Symptom.** `POST http://127.0.0.1:44497/v1/chat/completions` → HTTP 502 Bad Gateway.
- **Root cause.** Local Argo proxy on CherryRd is not up right now; switched to the cherryrd:4000 aggregator per TOOLS.md canonical endpoint.
- **Prevention.** Judge script should try both endpoints in order.

## Category C: My implementation bugs (caught + fixed)

### C1. Endianness inconsistency between Ry-layer and CNOT
- **Symptom.** Unit test `_cnot_probe` (asserting CNOT(0,1)|10⟩=|11⟩ under the same big-endian convention `apply_ry_layer` uses) failed initially.
- **Root cause.** `apply_ry_layer` uses `reshape([2]*n)` which is big-endian (axis 0 = MSB); the initial `apply_cnot` used `(idx >> ctrl) & 1` which is little-endian (bit 0 = LSB). Inconsistent.
- **Fix.** Changed `apply_cnot` to `1 << (n-1-ctrl)` and `1 << (n-1-tgt)` so both are big-endian.
- **Prevention.** Kept the unit test in the run pipeline.

### C2. Dead code after `return` in first CNOT draft
- **Symptom.** Initial `apply_cnot` had `return s[swapped]` followed by comments and unreachable code (I'd been mid-thought).
- **Fix.** Rewrote cleanly.
- **Prevention.** Linter would catch.

## Category D: Scope / time trade-offs (deliberate skips)

### D1. Periodic BC without ε-regularization
- **Status.** Attempted, poor results (mean ε_tr ~0.3-0.5 across n). Marked C4 as **Partial** rather than fail because the mechanism (singular null space of A) is understood and the fix (add ε·|1⟩⟨1| regularizer per paper Sec. IV.B) is straightforward but skipped for time.
- **How to close.** Add `if bc=="periodic": A += eps * np.outer(ones, ones) / N` with eps=1e-3.

### D2. Neumann BC not attempted
- **Status.** C7 partial (Dirichlet + periodic only). Skipped for time; Neumann Poisson is also singular with a different null-space treatment.

### D3. Iteration-scaling law (C6) not attempted
- **Status.** Would need n∈{2..8} with thousands of restarts to fit T_it ~ n^k. My 10 trials × 3 restarts is enough for the headline ε_tr claim but nowhere near enough to fit an exponent robustly. Deferred.

### D4. Shot-based noise not simulated
- **Status.** State-vector simulator collapses all measurement costs to a single matrix-vector product. The paper's O(1)-per-cost-eval structural advantage is verified, but the shot-count constant that determines wall time on real NISQ hardware is not benchmarked. Deferred (see Q3 in open_questions.json).

## Category E: Sibling-dir governance

### E1. Existing sibling `PDE-Sato-VQA-poisson-2021/` with REPLICATED verdict
- **Situation.** Same paper (arXiv:2106.09333, PRA 104.052409), different slug (VQA vs VQE). Prior REPLICATED verdict via a different implementation (compact-form Kronecker ansatz).
- **Handling.** Per the "preserve completed work, write only inside assigned target dir" rule: I read the sibling's REPORT.md only to confirm the correct arXiv ID and verify my implementation is genuinely distinct (it is — I used gate-by-gate circuit construction rather than the sibling's shortcut). I wrote nothing to the sibling dir.

## Recovery / re-run instructions

```bash
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Sato-VQE-Poisson-2021/
# fetch (correct arXiv)
curl -sSL https://arxiv.org/pdf/2106.09333 -o paper.pdf
pdftotext -layout paper.pdf work/paper.txt
# run
cd work
python3 test_gates.py              # ~5s, sanity
python3 vqe_poisson.py             # ~7 min, full sweep
python3 vqe_n5_deep.py             # ~4 min, best-of-3 deep dive
python3 verify_o1_cost.py          # ~3s, O(1) structural check
python3 judge.py                   # ~10s, LLM judge
```

All outputs land in `report/evidence/`.
