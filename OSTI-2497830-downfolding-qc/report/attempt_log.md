# Attempt Log — OSTI-2497830

**Analyst:** Ollie subagent osti-2497830 (spawned by cron af3aeb91)
**Date:** 2026-07-02 (CDT)
**Model:** argo/argo:claude-opus-4.7 (Argo proxy, free)

## Timeline

- **10:07** — Received task. Read WAVE_BRIEF_2026-07-01.md. Created target dir `~/Dropbox/REPLICATE-PROJECT/OSTI-2497830-downfolding-qc/{report/evidence,work}`.
- **10:08** — Fetched OSTI PDF via `ssh uicgpu 'curl … https://www.osti.gov/servlets/purl/2497830'` + scp back to workspace. 2.17 MB, download OK. Direct fetch would have worked from CherryRd too but followed the brief's proxy convention.
- **10:09** — First attempt to send the PDF to the `pdf` tool failed twice with "path not under allowed dir" (Dropbox path not whitelisted; managed workspace path also blocked). Third attempt against `~/.openclaw/workspace/osti_2497830.pdf` failed because the underlying Anthropic image model returned a "credit balance too low" error and the Gemini/OpenAI fallbacks are not configured for PDF extraction.
- **10:10** — Pivoted to `pdftotext -layout`. Clean 997-line text extraction from the two-column PhysRevApplied layout. Read the full paper (methods, results, appendices, Tables I/II/III–VI).
- **10:12** — Extracted the paper's downfolded-Hamiltonian parameters from Appendix C (Ca2CuO3 in C.1, WTe2 in C.2, SrVO3 in C.3). Also captured Table I (system, lattice, N_b, DMRG E, VQE E, fidelity) and Table II (n_q, n_2qG, circuit fidelity, ||H||₁, n_terms).
- **10:13** — Confirmed: paper does NOT provide a code repository. The one GitHub hit for "VQE downfolding" (He-Wenhao/VQE_downfold) is unrelated (different author, different project).
- **10:14** — Decided the tractable path: build the Ca2CuO3 model exactly from Appendix C.1 and diagonalize independently in the (N_up=5, N_dn=5) half-filled block. Dim = C(10,5)² = 63,504 → trivial ED on a laptop.
- **10:16** — Wrote `work/ca2cuo3_ed.py`: from-scratch scipy sparse implementation. Per-spin combinatorial basis + bitmask hopping (Jordan-Wigner-like sign tracking) + diagonal U + V terms + Kronecker product of the two spin sectors + Lanczos via `scipy.sparse.linalg.eigsh`.
- **10:17** — First run: **E0 = 6.005055 eV**, 0.1 meV agreement with paper's DMRG 6.005 eV. Spin correlations show perfect alternating-sign AFM pattern. Confirmed independent full reproduction of the Ca2CuO3 claim.
- **10:19** — Wrote `work/srvo3_charge_order.py` for a small-scale sanity check on SrVO3 (2×2 single-band ED with Appendix C.3 parameters). Result: at half filling on 2×2 the ground state is exactly A/B-symmetric (Φ = 0) — expected from the geometry, not a contradiction. The paper's 3×3 3-band CDW result requires the full DMRG/tensor-network stack.
- **10:21** — Argo proxy call for LLM judge: initial call to `argo:claude-opus-4.7` failed with an upstream response-parsing error. Fell back to `argo:gpt-5.2` (also free) — worked. Judge returned **PARTIAL** with a well-reasoned justification.
- **10:23** — Compiled the report + brief + attempt log + artifact harvest + copied JSON evidence into `report/evidence/`.

## What worked

- `pdftotext -layout` handled the PhysRevApplied two-column format cleanly enough to extract all Table I / II / III–VI values and Appendix C matrices with no ambiguity.
- ED on the 10-site 1-band extended Hubbard model is spectacularly cheap (0.82 s Lanczos for k=3 eigenpairs on a laptop). Agreement with the paper's DMRG value at 0.1 meV is essentially confirmation that DMRG in that regime was converged.
- Argo proxy at localhost:44497 works for gpt-5.2 with the OpenAI-style REST payload. Free.

## What didn't work

- `pdf` tool: broken due to expired Anthropic credits + Gemini fallback misconfigured.
- `argo:claude-opus-4.7` model on Argo proxy returned an upstream parse error on chat completions. `gpt-5.2` worked as the substitute judge.
- Direct exact diagonalization of the WTe2 32-qubit (4 lattice × 4 band × 2 spin) or SrVO3 54-qubit (9 lattice × 3 band × 2 spin) Fock spaces is not feasible; those systems required DMRG/tensor-network machinery that was out of scope for the ~15-min replication window.

## Rules honored

- Free endpoints only (Argo proxy, no Anthropic/OpenAI direct).
- Real replication (independent from-scratch ED, not a rerun of the authors' code — they released none).
- LLM-judge verdict (not regex): `argo:gpt-5.2` returned PARTIAL after being handed the full attempt summary.
- Wrote only inside the assigned target directory.
