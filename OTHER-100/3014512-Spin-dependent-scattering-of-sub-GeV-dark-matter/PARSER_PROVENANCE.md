# Parser Provenance — OSTI 3014512 re-pass

**Paper:** Gori, Knapen, Lin, Munbodh, Suter, "Spin-Dependent Scattering of Sub-GeV Dark Matter: Models and Constraints", Phys. Rev. D 112, 075019 (2025).

## Source file
- `3014512.pdf` (1,661,241 bytes) in project root, sha256 unchanged from pass-1.

## Parser pipeline used in this re-pass

1. **Primary extraction:** `pdftotext -layout /tmp/repass-paper/paper.pdf paper.txt`
   - Tool: Xpdf `pdftotext` 4.05 (via Homebrew, `/usr/local/bin/pdftotext`)
   - Mode: `-layout` (preserves column geometry; needed because the paper is two-column PRD style)
   - Result: 1857-line plain text dump, all 27 published pages captured.
   - Symbols: Greek/math glyphs come through as ligatures (σ̄, μ, χ, ϕ, π, ε…) — usable for human reading; numerical constants and equation coefficients all preserved verbatim.
   - Stored at `/tmp/repass-paper/paper.txt` (ephemeral; rerun any time).

2. **PDF model attempts (fallback only):**
   - `pdf` tool with `anthropic/claude-opus-4-8` → 400 (credit balance).
   - `pdf` tool with `google/gemini-3-flash-preview` → unknown model.
   - `pdf` tool with `openai/gpt-5.5` → extract plugin disabled.
   - Net: vision/LLM PDF route unavailable for this run; `pdftotext` is the canonical source.

3. **Cross-check vs pass-1:** Section/equation/figure numbering matches the published PRD paginated text; equation numbers (1)–(82) and (C1)–(D32) in our extract are exactly those cited in the original.

## What the parser can/cannot capture

- ✅ All numbered equations with explicit numerical coefficients (e.g. Eq. 22 `gp ≈ 8.11 × 10⁻⁴ × cGG`, Eq. 24 `gn ≈ -3.50 × 10⁻⁵ × cGG`, Eq. 26 cγγ, Eq. 30 SIDM `σ/mχ ≤ 1.1 cm²/g`, Eq. 33/37 SIDM viscosity cross sections, Eq. 40 `F_A'(0) = 0.22(15)`, Eq. 41 `gp,n ≈ 0.22 g'`, `gχ = -g'/2`, Eq. 43 `g' ≤ (1/√2) mA'/TeV`, Eq. 45 ε ~ 5×10⁻⁵ g', Eq. 47/48/49 K→πA' / B→KA' BR formulas, Eq. 61/62 g-factors, Eq. 72 multi-phonon `C_l,d`, Eqs. 76–78 G(q) for each mediator, Eqs. 80–82 / E1–E4 rate integrals, Eqs. E10–E14 nuclear-recoil limits).
- ✅ Table II OGM/Shell-model `f_p`, `f_n`, `λ_a,ϕ`, `λ_A'` values for ⁹isotopes ²⁷Al, ²³Na, ¹⁹F, ²⁹Si, ⁷³Ge, ⁶⁹Ga, ⁷¹Ga, ⁷⁵As, ¹²⁷I.
- ✅ Numerical benchmarks: `m_a,ϕ = 0.3 q₀` (light) and `3 q₀` (heavy), `m_A' = 10 GeV`, `g_p = 1.5 × 10⁻³` at the A' benchmark star in Fig. 4, `v₀ = 220 km/s`, `vₑ = 240 km/s`, `vₑₛc = 500 km/s`, `ρ_χ = 0.4 GeV/cm³`.
- ✅ SN-1987A trapping window: `2 × 10⁻⁶ ≲ g_p ≲ 7 × 10⁻⁶` for `100 keV ≲ m_a ≲ 100 MeV`.
- ✅ KSVZ UV-completion bound: `|g_p| ≲ 2 × 10⁻²`, `|g_n| ≲ 7 × 10⁻⁴`.
- ⚠️ Pixel-perfect read-off of every curve in Figs. 1–10 is not done from the text dump — figures themselves are bitmaps inside the PDF. We read off approximate (m_χ, σ̄) tuples from the published axes where the paper text quotes them, and otherwise compare to the DarkELF SD pipeline numerically.
- ⚠️ Reference [92] (Zenodo data record DOI:10.5281/zenodo.17154960) holds the authors' own raw data for Figs. 2, 6–10. We do **not** download it here (would constitute direct reuse rather than reproduction); we compare our independent DarkELF numerics against the published plots.

## Key textual landmarks identified for the re-pass
- Sec. II: Eqs. (1)–(8) Lagrangians + non-relativistic Hamiltonians for ϕ / a / A' (light & heavy).
- Sec. III A: Eqs. (20)–(29) — meson decay, SN1987A, HB-star, CHARM, E137, KSVZ UV bounds on g_p,n.
- Sec. III B: Eqs. (30)–(37) — SIDM viscosity cross sections for ϕ and a mediators in Born/Hulthén regimes; Fig. 2, Fig. 3.
- Sec. IV: Eqs. (38)–(51) — A' anomalon bound (43), kinetic mixing (44–45), K→πA'/B→KA' branching ratios (47–49), SN1987A rescaling (50), A'→νν width (51), Fig. 4 with star benchmark `m_A' = 10 GeV, g_p = 1.5 × 10⁻³`.
- Sec. V: Eqs. (52)–(82) — DM-nucleus matching, OGM, Cℓd phonon correlator (72), Debye-Waller (73), G(q) for each operator (76–78), rate integrals (80–82). Figure 5 phonon partial DOS.
- Sec. VI: Figs. 6 / 7 / 8 (main reach plots) and conclusions (vii).
- Appendix A: Figs. 9 / 10 optimized mediator-mass scan.
- Appendix E: DarkELF implementation; Eqs. (E1)–(E14) are the exact rate integrals with the energy threshold step function (these are the actual integrals the code evaluates).

## Outputs of this parser
- Plain text: `/tmp/repass-paper/paper.txt`
- Equation/claim ledger: `repass/CLAIMS_LEDGER.md` (next file).
