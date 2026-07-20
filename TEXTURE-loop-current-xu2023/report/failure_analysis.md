# Failure analysis — arXiv:2306.16192 replication

## Honest negatives / out-of-scope items (marked, not faked)
1. **TSL / CSL / double-Chern-Simons headline claims — NOT replicated.**
   These require SU(3)-symmetric tensor networks (iPEPS/iPESS with QSpace,
   CTMRG contraction) and ED entanglement spectra. Out of scope for an
   overnight single-node run. Captured as open questions 1-2. The loop-current
   kernel's Chern/Kubo routines do NOT apply (this is a spin model, not a band
   metal), so we deliberately did not force them.
2. **Two-magnon spectra (Appendix A 4, Fig. 13) — NOT replicated.** Only the
   ONE-magnon instability line (Eq. 3) was implemented. Open question 3.
3. **iPEPS magnetization jump / SU(3)-broken phase energetics — NOT replicated.**
   Variational tensor-network comparison. Open questions 4-5. We DID reproduce
   the single-magnon flat-band precursor (infinite compressibility signature).

## Bugs hit during the run
### B1. Per-k Python loop hung (>2.5 min, killed)
- **Symptom:** first `run_checks.py` produced no output for >150 s.
- **Root cause:** Claim 3 scanned 61×41=2501 parameter points, each calling
  `all_magnon_eigs` which looped over an 8100-point BZ with a Python-level
  `np.linalg.eigvalsh` per k → ~20M tiny 3×3 diagonalizations in pure Python.
- **Fix:** vectorised `all_magnon_eigs` to build the full `(nk*nk,3,3)` complex
  Bloch stack and call `eigvalsh` once (batched). Runtime dropped to seconds.
- **Prevention:** for BZ sweeps, always batch the Bloch matrices and diagonalise
  the stack; never loop eigvalsh over k in Python. (This mirrors the shared
  kernel's own vectorised `all_eigvals`, which we should have followed first.)

### B2. Block-buffered stdout hid progress
- **Symptom:** `process poll` showed "no new output" while the job ran.
- **Root cause:** Python stdout is block-buffered under a non-TTY pipe.
- **Fix:** run with `python3 -u` (unbuffered). Progress then streamed live.

## Validity notes
- All 5 checks agree with the paper to **machine precision** (max errors
  0, 1.4e-14, 0 mismatches/100%, 0, ~1e-15). This is expected: they are exact
  algebraic identities of the printed matrix and formulas, so a correct
  transcription of Eq. A1 reproduces them exactly. The check therefore validates
  (a) our transcription of Eq. A1 from the PDF, and (b) internal consistency of
  the paper's stated q=0 eigenvalues, instability line, and flat-band claim.
- The finite-grid boundary band (47/2501 points within 0.03 of the Eq.3 line)
  was excluded from the Claim-3 classification to avoid grid-resolution false
  mismatches; away from the line agreement is exactly 100%.
