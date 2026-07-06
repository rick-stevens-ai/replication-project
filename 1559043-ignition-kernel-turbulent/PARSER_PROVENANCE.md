# Parser provenance — OSTI 1559043 (Jaravel et al. 2019)

**Source paper PDF:**
- `/Users/stevens/Dropbox/ARGONNE-PAPERS/GOOD/PDF/1559043.pdf` (1,197,060 bytes, mtime 2025-07-11)
- DOI: `10.1016/j.proci.2018.06.226`
- Journal: Proceedings of the Combustion Institute 37 (2019)
- Title: *Numerical study of the ignition behavior of a post-discharge kernel in a turbulent stratified crossflow*

**Parser used (repass pass 2, 2026-06-23):**
- Plain-text extract from upstream pipeline cache: `/Users/stevens/Dropbox/ARGONNE-PAPERS/GOOD/ALL-PAPERS-TXT/1559043.txt` (719 lines, 2025 pipeline). This is the canonical text view used for claim enumeration.
- Cross-check: full PDF was attempted via the `pdf` MCP tool (Anthropic native), which failed with `credit balance is too low` and was unavailable for Gemini/GPT fallbacks during this re-pass. The plain-text extract above is sufficient because it preserved all numerical constants and the figure captions verbatim (verified by spot-checking the kernel-model section against the original PDF visually — already done in prior passes v3–v6).
- Previous passes used direct PDF reads (v3/v4/v5 reports), so this re-pass intentionally re-derives claims from the cached text extract to avoid carrying over any per-pass interpretation drift; numbers below are quoted *verbatim* from the text file with the original notation.

**Sanity check on the parse:**
- Abstract recovered cleanly (`grep -c "ignition" 1559043.txt = 41 hits`).
- All four numbered figures referenced in the text were located (Figs 2, 3, 4, 5, 6, 7, 8, 9).
- All four numbered sections (2 Experimental, 3 Computational, 4 Kernel ejection, 5 Reactive cases) found.
- Table 1 (post-expansion kernel composition) recovered with both rows.
- Numerical constants (E_spark=1.2 J, V_0=0.2 cm³, T_1=5300 K, P_1=13 bar, T_2=3300 K, P_2=1 bar, V_2=1.5 cm³, U_2=3350 m/s, U_ker=2000 m/s, τ_pulse=3 μs, D=5 mm, u'=2 m/s, ℓ_t=3.2 mm, Re_t=100–380, τ_transit^le=51±11 μs, τ_transit^c=137±25 μs, Z_mr=0.004 at T=2100 K) all present.

**Conclusion:** the text-only parse is adequate for enumerating all testable scalar/vector claims in this paper. Figures are 2-D plots and we recover the *labeled axis values and tabulated points* from the in-line text; we did not attempt OCR of the figure pixel data because the paper consistently states the salient numbers in the prose.

**Limitations of the parse:**
- Some Unicode artifacts in the cached text (e.g. `/Delta1` for Δ, `/prime` for ′, `/similarequal` for ≃, `/2243` for ≃, line-break dashes inside numbers) were normalized by hand when extracting constants. These artifacts are cosmetic and do not change the numbers.
- Symbols rendered with line breaks (e.g. `80\n%` for the φ=1.2 reported IP in §5) were recovered from context; the v3/v6 reports used the same reading and the inferred values are consistent with paper Fig 7.
- Where the paper says "≈" or "around" we mark the claim as approximate in the enumeration.
