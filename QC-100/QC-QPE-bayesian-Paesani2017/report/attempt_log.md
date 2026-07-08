# Attempt Log — QC-QPE-bayesian-Paesani2017

- Read WAVE_BRIEF + STATUS_AUDIT; confirmed no phase-estimation dir exists in QC-100 (dedup OK). QPE is on the explicit "still-untaken" list.
- Selected rank-14 candidate (arXiv:1703.05169, Bayesian QPE / RFPE) — highest-ranked untaken "quantum phase estimation" direction with reproducible classical-simulator core + OA.
- Fetched ar5iv full text for the paper AND the underlying RFPE method paper (Wiebe & Granade 2016, arXiv:1508.00869) via curl (free web_fetch, not paid pdf tool). Extracted algorithm + exact likelihood + noise equations + target numbers (4.8741 rad, N(pi,pi^2), M=ceil(1.25/sigma), 0.72 kcal/mol, T2~32).
- Implemented RFPE + IPEA in NumPy.
  - BUG 1 (fixed): first cut mixed radian (4.8741) with fractional [0,1) phase convention -> RFPE diverged, IPEA garbage. Rewrote to a single consistent convention.
  - BUG 2 (fixed): used rejection sampling + circular stats on a broad prior -> no information gain, sigma stuck. Switched to exact Wiebe-Granade convention: likelihood (1+cos(M(phi-theta)))/2 in radians, importance-weighted posterior mean/var. RFPE then converged 1 rad -> 3.8e-5 rad in 50 steps (validated single-run trace).
  - BUG 3 (fixed): IPEA power/feedback mapping was inverted (M=2^(n-k) with LSB at M=1). Corrected to M=2^(j-1) with LSB read first and feedback theta=omega/M canceling lower bits. IPEA then exact (err=0) for representable phases, 16-bit accurate (~1e-5 rad) otherwise.
  - BUG 4 (fixed): C2 H2 PES had 4 catastrophic-outlier bond lengths -> traced to RFPE prior straddling the 0/2pi wrap boundary for phases near 0.4 rad. Fixed by mapping energies to a phase window centered at pi (like the paper's prior) + alias guard. avg error dropped from 10.3 -> 0.0028 kcal/mol.
- Ran full sweep (C1 1000 runs, C2 16 pts x 20, C3/C4 scans x 40): all consistent.
- Generated 4 evidence plots (Matplotlib).
- LLM judge = free Argo gpt-5.2: coverage 9/10, agreement 8/10, verdict PARTIAL.
- No paid endpoints; light compute run locally (NumPy). Wrote report + work.
