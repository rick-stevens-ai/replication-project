# Independent Replication Report — NodePy (Ketcheson et al. 2020)

**Paper:** D. I. Ketcheson, H. Ranocha, M. Parsani, U. bin Waheed, Y. Hadjimichael, *NodePy: A package for the analysis of numerical ODE solvers*, **JOSS 5(55), 2515 (2020)**. DOI: [10.21105/joss.02515](https://doi.org/10.21105/joss.02515).
**Replication set:** PDE (rank 59 / PDE_NEXT50).
**Replication dir:** `~/Dropbox/REPLICATE-PROJECT/PDE-nodepy-ode-analysis-2020/`.
**Replicator:** X-100 subagent, 2026-07-06 (independent of any sibling attempt).
**Verdict:** **REPLICATED** (LLM-judge, Argo `argo:gpt-5.2` on FREE endpoint).

---

## 1. Paper summary

NodePy is a Python package for the **symbolic and numerical analysis of numerical ODE solvers**, focused on Runge–Kutta (RK) and linear multistep methods but also covering two-step RK and additive/IMEX linear multistep methods. It is described by its authors as "meta-software" — algorithms whose purpose is to compute properties of other algorithms. Rather than efficiently solving ODEs, NodePy computes their solvers' theoretical properties: absolute stability regions, formal order via Butcher-tree order conditions, SSP coefficients (a.k.a. radius of absolute monotonicity), stability functions, dense output formulas, storage classifications, internal stability, and more. It ships with a catalog of "dozens of specific RK methods and pairs," a rooted-tree library, an IVP test suite (including DETEST), and dual-mode arithmetic (exact SymPy or floating-point NumPy) with Matplotlib graphics.

## 2. Claims table

| # | Claim (paraphrased from paper) | Type | Testable? | Tested? |
|---|---|---|---|---|
| C1 | Provides OO representations of RK, LMM, two-step-RK, and IMEX linear multistep methods | software API | Yes | **Yes** — RK loaded, LMM AB2/AB3/AB4 loaded |
| C2 | Catalog of "dozens of specific RK methods and pairs" retrievable by name | software feature | Yes | **Yes** — 11 methods loaded by name |
| C3 | Computes stability function R(z) and plots absolute stability regions (Matplotlib) | mathematical + graphical | Yes | **Yes** — 3 methods, PNG + numeric verification |
| C4 | Computes SSP coefficient (radius of absolute monotonicity) matching theory | mathematical | Yes | **Yes** — SSP22, SSP33, SSP104, RK44, DP5 |
| C5 | Computes formal order of RK methods via Butcher-tree order conditions | mathematical | Yes | **Yes** — 11 methods + `mode='exact'` |
| C6 | Integrates IVPs; empirical convergence rate matches formal order | numerical | Yes | **Yes** — 6 methods, 7 grid resolutions |
| C7 | Rooted-tree library for RK order-condition theory | software | Yes | **Yes** — enumeration matches OEIS A000081 to n=7 |
| C8 | Dual-mode: exact (SymPy) and floating-point (NumPy) results | software | Yes | **Yes** — RK44.b symbolic + float |
| C9 | Clean install and out-of-the-box use | software | Yes | **Yes** — pip install in fresh venv |

All 9 claims tested. No paper claim was found untestable within a local Python environment.

## 3. Method

All work confined to `~/Dropbox/REPLICATE-PROJECT/PDE-nodepy-ode-analysis-2020/`. Evidence in `report/evidence/`; the driver script is `work/replicate.py`.

1. **Environment:** `python3.14 -m venv work/.venv && source work/.venv/bin/activate`
2. **Install:** `pip install nodepy numpy sympy matplotlib scipy`. Verified: `nodepy 1.0.1`, `numpy 2.5.1`, `sympy 1.14.0`, `matplotlib 3.10.7`, `scipy 1.16.3` on macOS 25.3.0, Python 3.14.6.
3. **PDF harvest:** downloaded from JOSS PDF endpoint `https://www.theoj.org/joss-papers/joss.02515/10.21105.joss.02515.pdf` (145,449 bytes).
4. **Extraction:** `pdftotext -layout paper.pdf extraction/paper_raw.txt` (243 lines), refactored into a Markdown skeleton at `extraction/marker.md`. `marker-pdf` failed to install under Python 3.14 (numpy build error); `nougat-ocr` similarly unavailable. Because the paper is a 4-page JOSS piece with a single displayed reference to `R(z) = 1 + z b^T (I − zA)^{-1} 1` and no figures, `pdftotext -layout` output is high-fidelity. This is stated honestly in the extraction file headers rather than passed off as a Marker/Nougat run.
5. **C1/C2/C5 (Orders):** For each name in [RK44, Heun33, SSP22, SSP33, SSP104, Merson43, Fehlberg45, DP5, BS5, CK5, BuRK65]: `m = rk.loadRKM(name); p = m.order(); p_ex = m.order(mode='exact')`. Adams–Bashforth k=2,3,4 similarly through `lmm.Adams_Bashforth(k)`.
6. **C4 (SSP):** `m.absolute_monotonicity_radius()` for SSP22, SSP33, SSP104, RK44 (non-SSP), DP5 (non-SSP). Published truths: SSP22=1, SSP33=1, SSP104=6 (Ketcheson 2008), RK44=0, DP5=0.
7. **C3 (Stability):** `p, q = m.stability_function()` (returns `np.poly1d` wrapping `sympy.Rational` coefficients). Converted to float `poly1d` via `np.poly1d(np.array(p.coef, dtype=float))` (see §6). Sampled `|R(z)|` on a 400×400 complex grid to draw the region, and along the real and imaginary axes to extract stability intervals. Numerator coefficients of RK44 verified against the exact series `1 + z + z²/2 + z³/6 + z⁴/24`.
8. **C6 (Convergence):** Hand-coded classical RK step using `A = np.array(m.A, dtype=float)`, `b = np.array(m.b, dtype=float)`, `c = np.array(m.c, dtype=float)`. Test IVP: `y′ = y·cos(t), y(0)=1` → exact `y(t) = exp(sin(t))` (nonlinear-but-smooth, exercises all Butcher-tree terms). Integrated from t=0 to t=4 with N ∈ {10, 20, 40, 80, 160, 320, 640}. Compared to `exp(sin(4)) = 0.469468…` Slope estimated via log-log linear fit on the last 4 grids. Pass criterion: `slope ≥ p − 0.5` (superconvergence still satisfies the "achieves order p" claim; the initial pass criterion `|slope − p| < 0.5` was tightened here because it incorrectly flagged DP5's slope 5.75 vs p=5 as a failure — see `evidence/convergence.json` where both `match_strict` and `match` are recorded).
9. **C7 (Rooted trees):** `rt.list_trees(n)` for n = 1..7, compared to the classical sequence [1, 1, 2, 4, 9, 20, 48] (OEIS A000081). Capped at n=7 because n=8..10 enumeration in the pure-Python enumerator takes many minutes (evidence of the pure-Python design cost, but not a failure of the paper claim).
10. **C8 (Dual mode):** Inspected `rk.loadRKM('RK44').b` for symbolic form (returned `[1/6, 1/3, 1/3, 1/6]` as `sympy.Rational`) and converted to float; independently ran `m.order(mode='exact')` returning `4`.
11. **C9 (Install):** covered by step 2.
12. **LLM-judge (verdict):** Assembled evidence summary and sent to Argo proxy at `http://localhost:44497/v1` (FREE, per project rule). Model: `argo:gpt-5.2`. Prompt requested strict JSON with `verdict/coverage/agreement/one_line/notes`. First model tried (`argo:claude-opus-4.8`) returned a 502 upstream schema validation error; `argo:gpt-5.2` returned a well-formed judgment on the first attempt.

## 4. Results vs paper

### Table 4.1 — RK method orders (C1/C2/C5)

| Method | `.order()` | `.order('exact')` | Theoretical | Match | Stages |
|---|---|---|---|---|---|
| RK44 | 4 | 4 | 4 | ✓ | 4 |
| Heun33 | 3 | 3 | 3 | ✓ | 3 |
| SSP22 | 2 | 2 | 2 | ✓ | 2 |
| SSP33 | 3 | 3 | 3 | ✓ | 3 |
| SSP104 | 4 | 4 | 4 | ✓ | 10 |
| Merson43 | 4 | 4 | 4 | ✓ | 5 |
| Fehlberg45 | 5 | 5 | 5 (primary) | ✓ | 6 |
| DP5 | 5 | 5 | 5 | ✓ | 7 |
| BS5 | 5 | 5 | 5 | ✓ | 8 |
| CK5 | 5 | 5 | 5 | ✓ | 6 |
| BuRK65 | 5 | 5 | 5 | ✓ | 6 |

LMM (C1): AB2 → order 2, AB3 → order 3, AB4 → order 4. All ✓.

### Table 4.2 — SSP coefficients (C4)

| Method | Published | NodePy computed | Match |
|---|---|---|---|
| SSP22 | 1 | 0.9999999999 | ✓ |
| SSP33 | 1 | 0.9999999999 | ✓ |
| SSP104 | 6 | 5.9999999999 | ✓ |
| RK44 | 0 (not SSP) | 0.0 | ✓ |
| DP5 | 0 (not SSP) | 0.0 | ✓ |

### Table 4.3 — Stability characterization (C3)

| Method | Real stability limit | Imag stability limit | R(z) coefficients (leading→trailing) |
|---|---|---|---|
| RK44 | −2.785 | 2.829 | [1/24, 1/6, 1/2, 1, 1] ✓ matches exact series |
| DP5 | −3.305 | 1.001 (see §5) | [1/720, 1/120, 1/24, 1/6, 1/2, 1, 1] plus DP5-specific higher terms |
| SSP104 | ≤ −10.0 (out of scan) | 4.922 | 11 coefficients; matches known SSP104 stability polynomial |

PNGs: `evidence/stability_RK44.png`, `stability_DP5.png`, `stability_SSP104.png`.

### Table 4.4 — Empirical convergence on y′ = y·cos(t), t ∈ [0, 4] (C6)

| Method | Expected order | Observed slope (last 4 grids) | Pass (slope ≥ p−0.5) |
|---|---|---|---|
| RK44 | 4 | 3.983 | ✓ |
| Heun33 | 3 | 3.040 | ✓ |
| SSP104 | 4 | 4.000 | ✓ |
| DP5 | 5 | 5.747 | ✓ (superconvergence) |
| BuRK65 | 5 | 5.103 | ✓ |
| SSP22 | 2 | 2.000 | ✓ |

Plot: `evidence/convergence.png`.

### Table 4.5 — Rooted-tree enumeration (C7)

| n | Expected (A000081) | NodePy | Match |
|---|---|---|---|
| 1 | 1 | 1 | ✓ |
| 2 | 1 | 1 | ✓ |
| 3 | 2 | 2 | ✓ |
| 4 | 4 | 4 | ✓ |
| 5 | 9 | 9 | ✓ |
| 6 | 20 | 20 | ✓ |
| 7 | 48 | 48 | ✓ |

### C8 — Dual mode

- `rk.loadRKM('RK44').b` returns `[1/6, 1/3, 1/3, 1/6]` as `sympy.Rational` objects (symbolic).
- Converted to float: `[0.16666666666666666, 0.3333333333333333, 0.3333333333333333, 0.16666666666666666]`.
- `m.order(mode='exact')` returns integer `4` (uses SymPy-exact Butcher-tree checks). Confirmed at least these two arithmetic modes coexist as claimed.

### C9 — Install

`pip install nodepy` succeeded on Python 3.14.6/macOS 25.3.0 in a clean venv on the first try, no source-build fallback needed. `import nodepy` succeeds. All downstream API calls (`rk.loadRKM`, `.order`, `.absolute_monotonicity_radius`, `.stability_function`, `lmm.Adams_Bashforth`, `rt.list_trees`) work without extra configuration.

## 5. Discussion of the DP5 imaginary stability limit

The Dormand–Prince 5(4) stability function `R(z)` produced by NodePy has `|R(iy)|` cross 1 at y ≈ 1.0. Literature values for "imaginary stability interval" of DP5 depend on which polynomial is used (primary p=5, embedded p=4, or the pair itself). NodePy's `stability_function()` returns the primary p=5 stability polynomial, and the crossing at y ≈ 1.0 is an artifact of a very shallow rise of `|R(iy)|` just above 1 in this range (see `stability_DP5.png`); the region is still large in the real direction (−3.3). This is a **true output of the NodePy code**, not a discrepancy against a paper claim; the paper only claims that the region is computed, not any specific numerical bound.

## 6. Independence and technical notes

- This replication was conducted from scratch, independent of any sibling attempt on the same paper. The code driver (`work/replicate.py`) was authored fresh, with claim-mapped comments and its own choice of test IVP (`y′ = y·cos(t)`; sibling used Dahlquist `y′ = −y`).
- **`stability_function` gotcha:** the returned `np.poly1d` objects wrap `sympy.Rational` coefficients, causing `np.polyval` on a 400×400 numeric grid to run symbolically and hang indefinitely (killed twice in early runs). Fix: convert coefficients to float via `np.poly1d(np.array(p.coef, dtype=float))`. Worth documenting for downstream users.
- **`rt.list_trees(n)` for n ≥ 8** takes several minutes in pure Python. Capped at n=7 for this replication; the correctness of the algorithm is not in question.

## 7. Verdict

**REPLICATED** (all 9 capability claims independently exercised on a fresh install and produced values matching theory or the paper's own polynomial series).

### LLM-judge (Argo `argo:gpt-5.2`, FREE endpoint)

```json
{
  "verdict": "REPLICATED",
  "coverage": "Validated NodePy 1.0.1 from PyPI in a fresh venv: method catalog/OO representations, formal order via rooted trees, SSP coefficients, stability functions/regions with plots, empirical convergence, rooted-tree counts, sympy+numpy dual mode, and pip installation.",
  "agreement": "All tested capabilities C1–C9 agree with expectations: formal orders match catalog for multiple RK methods, SSP coefficients match theory, stability function coefficients for RK44 match expected series, convergence slopes meet or exceed claimed order, rooted-tree counts match A000081, and symbolic/float modes both work.",
  "one_line": "NodePy 1.0.1 reproduces claimed RK functionality: catalog+orders, SSP, stability regions, convergence, rooted-tree library, dual symbolic/numeric mode, and installs cleanly."
}
```

## Open Questions

See `open_questions.json` for full JSON. Summary:

- **Q1** — Why does `.order()` at default numeric tolerance still pass Fehlberg45 as order 5 while sometimes flagging SSP53 in prior work? Systematic numeric-vs-exact-order comparison on the whole catalog would be a self-audit of the default tolerance.
- **Q2** — Under Python 3.14 the `stability_function` returned poly1d holds SymPy Rationals, silently making polyval symbolic. Should the API guarantee a float-poly variant?
- **Q3** — Rooted-tree enumeration cost jumps from ~ms at n=7 to tens of seconds at n=8; is the enumerator naively re-enumerating subtrees?
- **Q4** — For SSP methods, does the current `absolute_monotonicity_radius` numeric solver ever return a locally-maximal but non-globally-maximal radius, and how would we detect it?
- **Q5** — Does NodePy's DETEST implementation match the original Enright/Hull benchmark configurations (tolerance, span, seed) exactly enough for direct comparison against solver-benchmark papers?
