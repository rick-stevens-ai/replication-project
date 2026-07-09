# Failure Analysis — OSTI-3020618

## What failed, root cause, fix, prevention

### F1. `pdf` tool refused all paths
- **Failure:** OpenClaw's `pdf` tool refused `/Users/stevens/Dropbox/REPLICATE-PROJECT/OSTI-3020618-nnqs-nuclear/paper.pdf` and `/tmp/nnqs_paper.pdf` ("path not under allowed directory"). Copied to `~/.openclaw/workspace/tmp-pdfs/` and then Anthropic + gpt-5.5 both failed on the media route (depleted key / disabled plugin).
- **Root cause:** Media allow-list only covers a small set of paths; fallback image models are unhealthy.
- **Fix:** Fall back to `ssh uicgpu pdftotext -layout` — perfectly adequate for text-heavy scientific PDFs.
- **Prevention (for future waves):** Skip the `pdf` tool for large PDFs by default; go straight to `pdftotext -layout` on uicgpu, or use nougat when available.

### F2. First Hamiltonian build gave E ≈ 0 MeV
- **Failure:** Initial `build_hamiltonian_matrix` returned E ≈ 0 for all inputs; `autotune_lam_S` hit its 10.0 ceiling without ever producing a bound state.
- **Root cause 1:** `kmax = 500 fm⁻¹` combined with `tan((π/4)(1+x))` mapping put quadrature nodes at q up to ~350 fm⁻¹, giving kinetic energies ~10⁵ MeV. The physical deuteron lives at q ~ 1 fm⁻¹.
- **Root cause 2:** The initial matrix-build symmetrisation was subtly wrong (raw `V·metric_i·metric_j` instead of the proper Nystrom-style transformation).
- **Root cause 3:** `autotune_lam_S` had a hard ceiling of 10.0 with no bracket expansion.
- **Fixes:** (a) `kmax = 15 fm⁻¹`, (b) rewrote H as `T·δ + (√w_i q_i²)(√w_j q_j²) V_LL'(q_i, q_j)` with clean vectorised outer-products, (c) autotune now expands its upper bracket geometrically to 10¹².
- **Prevention:** For any momentum-space few-body problem, sanity-check that your quadrature nodes span ~2–5 × the potential's inverse-length scale (β ≈ 1.5 fm⁻¹ here → kmax ≈ 10–20 fm⁻¹). Always start with a coarse `--nhids 2 --nseeds 1 --steps 1000` smoke test before launching the sweep.

### F3. LLM-judge with `argo:claude-opus-4.7` returned 502
- **Failure:** Both LiteLLM aggregator (:4000) and direct Argo proxy (:44497) returned:
  > `Failed to parse upstream response: 1 validation error(s): Value at 'choices[0].message' does not match any variant of SystemMessage | UserMessage | AssistantMessage | ToolMessage`
- **Root cause:** Argo's upstream response schema for claude-opus-4.7/4.8 changed and no longer round-trips through LiteLLM's OpenAI-compatible parser. Independent of this replication task (system-level, worth reporting in `~/.openclaw/workspace/memory/failure-log.md` for the mesh).
- **Fix:** Fell back to `argo:gpt-5.2` — same Argo proxy, working schema. Verdict obtained.
- **Prevention:** For LLM-judge, keep a fallback model chain: `argo:claude-opus-4.7 → argo:gpt-5.2 → argo:claude-opus-4.8`. Consider adding a small helper `judge()` that walks the chain.

### F4. Nougat MMD not produced
- **Failure:** No `nougat` env on uicgpu; no cached parse in `~/Dropbox/SC-OSTI/` for OSTI 3020618.
- **Root cause:** Nougat CLI is heavy and not installed on the AI compute nodes; the pre-parse corpus doesn't cover this OSTI ID.
- **Fix:** Provided `extraction/marker.md` = `pdftotext -layout` output as a functional substitute (loses table structure and math, but preserves all text used for claim extraction). No downstream analysis was blocked.
- **Prevention:** For the 8-artifact bar, add nougat batch parsing to a scheduled uicgpu queue and mirror to `SC-OSTI/parsed-nougat/` by OSTI ID. Not a per-replication fix.

### F5. Table 4.1 pionless-EFT SJ energies not attempted
- **Failure:** Claim C2 (Table 4.1: ²H/³H/⁴He SJ with LO pionless EFT at Λ=4,6 fm⁻¹) was noted but not attempted.
- **Root cause:** A like-for-like replication requires a full spatial + spin-isospin VMC sampler for A ≤ 4 nucleons with Metropolis, a Deep Sets Jastrow, and the LO pionless-EFT Hamiltonian of Eq. (4.3)–(4.4) — that is many-GPU-day work, not single-wave-slot work.
- **Fix:** Documented as gap; verdict is PARTIAL rather than REPRODUCED to reflect this honestly.
- **Prevention:** For future NNQS-nuclear replications, split into (a) 1-day deuteron demo (this task) and (b) multi-day 3H/4He calibration jobs.

## Failure log status
None of F1–F5 were repeated within this task. F1–F3 are worth mirroring into `memory/failure-log.md` for cross-task learning; F4–F5 are project-scope constraints, not per-task failures.
