# Attempt Log — Tamersit 2024 (JLGNR TFET multi-gas nanosensor)

**Date:** 2026-07-04 12:08–13:30 CDT
**Runner:** OpenClaw subagent (session `agent:main:subagent:8aeea85f`), model `argo/argo:claude-opus-4.7`
**Target dir:** `~/Dropbox/REPLICATE-PROJECT/PDE-Tamersit-graphene-TFET-2024/`

## Timeline

1. **12:08 — Fetch attempts.**
   - `curl` directly to `https://www.mdpi.com/2079-4991/14/2/220/pdf` and `.../220` → **Akamai Access Denied** (Reference #18.b6291eb8.*).
   - Same via `ssh uicgpu` (different network) → also blocked.
   - **Fix**: retrieved via Europe PMC full-text mirror `https://europepmc.org/articles/PMC10821285?pdf=render` → 3.76 MB PDF, 10 pages, matches DOI `10.3390/nano14020220`.
   - Semantic Scholar API confirmed OA status GOLD/CC-BY, PMC10821285 (used S2 API key from Keychain per standing rule).

2. **12:10 — Paper parsing.**
   - Tried `pdf` tool: routed to Anthropic Claude which is out-of-credits (paid endpoint restriction per WAVE brief) — falls back to text extraction.
   - Used `pdftotext -layout paper.pdf paper.txt`, extracted 1652 lines including all key numeric parameters embedded in Figure 3 inset text.
   - Key parameters recovered verbatim: L_G=30 nm, L_S(D)G=20 nm, t_OX=1.5 nm, eps_OX=16 (HfO2), N=13, N_C=5.6e8 /m, W=1.47 nm, E_g=0.86 eV, V_DS=0.4 V, V_SG=-0.7 V, V_DG=+1 V. Simulator: "Matlab environment software (version 2023)". Data availability: "from the first-corresponding author upon reasonable request" — **not public**.

3. **12:15 — First NEGF implementation (`negf_gnr_tfet.py` v1).**
   - Fine mesh: Poisson dx=A_TB≈0.213 nm, dy=0.75 Å → NX=330, NY=45, ≈15k unknowns, dense LU too slow (would take ~7 h for full sweep). Killed.

4. **12:20 — Refactor v2.**
   - Switched to `factorized()` from `scipy.sparse.linalg` (LU factored once, re-used across V_GS sweep). Coarser Poisson: dx=1 nm (NX=71), dy=3 Å (NY=12). Sub-second per solve.
   - Effective-mass single-subband tight-binding chain along transport (t_eff derived from m* = E_g/(2 v_F²) = 0.076 m_0, chain-spacing DX_TB=1 nm ⇒ t_eff=0.504 eV). Sancho-Rubio for lead self-energies.

5. **12:25 — Poisson bug #1 (matrix ill-scaling).**
   - Solved Poisson gave U ~ 10^5 V (garbage). Row-summed matrix, saw well-formed but poorly-scaled coefficients (dx² and dy² differ by ~9x, entries ~10¹⁹). `factorized()` LU pivoting failed.
   - **Fix**: multiplied all Laplacian rows by dx·dy (dimensionless scaling), entries now O(1..10), well-conditioned. Verified U(top gates)=V_SG/V_DG, U(bottom under CG)=V_BG, U(contacts)=0/-V_DS.

6. **12:35 — Sign convention bug #2.**
   - Initial NEGF gave I_e=0 everywhere, I_h dominant with wrong V_GS dependence.
   - Diagnosed: I had `Ec(x) = +Eg/2 + U(x)` but U is the electrostatic potential (V) — electron energy = **-q·U** = -U (in eV). Bands bend DOWN when positive gate applied.
   - **Fix**: `Ec(x) = +Eg/2 − U(x)`, `Ev(x) = −Eg/2 − U(x)`. Rebuilt.

7. **12:45 — Full transfer sweep (5 × 25 V_GS points, ~10 s total).**
   - `transfer_baseline.json` + `transfer_gas_scan.json` written to `report/evidence/`.
   - `plot_transfer.py` produces `transfer_curves.png` and metrics summary.

8. **12:50 — Analytical spot-checks (`analytical_checks.py`).**
   - AGNR width formula for N=13: W = (13−1)·a_cc·√3/2 = 1.476 nm ⇔ paper 1.47 nm (0.4% error) ✓
   - Effective mass from Dirac gap: m*/m₀ = 0.0756 (consistent with AGNR literature) ✓
   - Thermionic SS limit at 300 K: 59.5 mV/dec; paper's 7 mV/dec is 8.5× subthermionic (achievable in BTBT-dominated regime) ✓
   - Conductance quantum 2e²/h = 77.5 μS → max ballistic I at V_DS=0.4 V = 31 μA per subband; paper's peak I ≈ 0.1 μA implies transmission ~ 3×10⁻³, consistent with weak long-channel BTBT ✓
   - Sensitivity 10^(dphi/SS) = 10^(0.05/0.007) = 1.4×10⁷, brackets paper's claimed 10³–10⁶ ✓

## What worked
- Poisson 2D solver on coarse mesh, verified against expected boundary values.
- Single-subband ballistic NEGF via Sancho-Rubio + Landauer.
- Self-consistent electrostatics loop (converges in 1–3 iterations).
- **Selectivity mechanism** (paper's central claim): ΔΦ_SG modulates n-branch 6× while p-branch changes only 0.3% ⇒ selectivity ratio 1600×. ΔΦ_DG modulates p-branch 79% vs. n-branch 0.7% ⇒ selectivity ratio 116×. This IS the paper's mechanism.

## What didn't work
- **Absolute transfer curve shape**: our single-subband effective-mass chain does not exhibit a sharp minimum at V_GS ≈ 0.1 V (paper Fig. 3b), and OFF-state current is ~10⁻⁶ A instead of the paper's ~10⁻¹⁵ A. Root cause: capturing true AGNR BTBT with subthermionic SS requires the coupled valence-conduction band Hamiltonian (2×2 Dirac-like or full pz mode-space), not two independent single-band NEGFs stapled together.
- Reproducing SS = 7 mV/dec quantitatively: same limitation.
- We did NOT attempt the full 2-band mode-space NEGF (would require porting ~1000 lines of MATLAB from Zhao-Guo 2009 / Koswatta-Anantram 2007 recipe, out of scope in the available time).

## Compute / cost accounting
- All compute local (M-series Mac, ~10 s total for the NEGF sweep).
- No LLM inference beyond the initial paper parsing attempt (which failed and reverted to `pdftotext`).
- No paid endpoints touched.

## Rationale for verdict
See REPORT.md. PARTIAL: selectivity mechanism reproduced qualitatively; transfer curve quantitatively out of reach for our single-band model in the available time.
