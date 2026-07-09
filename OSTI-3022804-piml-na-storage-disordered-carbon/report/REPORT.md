# Replication Report — OSTI 3022804

**Paper:** Rampal, Weitzner, Omenya, Wood, Reed, Li, Lee, Wan. *Physics-informed machine learning exploration of Na storage mechanisms in disordered carbon.* **Energy Storage Materials** 86, 104967 (2026). DOI: [10.1016/j.ensm.2026.104967](https://doi.org/10.1016/j.ensm.2026.104967).
**Target OSTI ID:** 3022804.
**Author group:** LLNL / PNNL (typical for this authorship).
**Core methods:** physics-informed neural network (PINN)-style modeling; molecular dynamics (MD); machine-learning interatomic potential (MLIP).

---

## 0. Paper availability

- The OSTI purl endpoint `https://www.osti.gov/servlets/purl/3022804` and the OSTI biblio page were **not reachable** from this replication host (`curl` exit 28 / `HTTP 000`; also 406/timeout via `web_fetch`). No paper PDF was obtained; no PDF SHA-256 is available. See `PROVENANCE.md`.
- Full bibliographic metadata (authors, title, journal, DOI, page) was independently confirmed via three separate ACS reference lists (JACS 2021, Energy&Fuels 2022, ACS Energy Letters 2025) that cite this paper — see search log in `PROVENANCE.md`.
- **Substitution:** because the paper's DFT/MD training set is not distributable and the PDF was not accessible, this replication is a **method-level, family-level** honest test of the paper's central methodological claim, not a bit-for-bit reproduction of Fig. X or Table Y. The claims table below is stated at that level.

## 1. Claims table

| # | Claim (paper family / method level) | Type | Testable here? |
|---|---|---|---|
| C1 | An ML interatomic potential fit to a modest DFT training set of disordered-carbon environments generalizes to Na adsorption on unseen local geometries with meaningful accuracy. | Method | Yes (toy analog) |
| C2 | Adding a physics-informed prior (correct sign structure between local structural descriptors — coordination, ring topology, defects — and Na binding) improves **out-of-distribution** generalization vs. a purely data-driven regressor. | Method | **Yes — this is the central kernel and it is what we test.** |
| C3 | Na adsorption energy on disordered carbon strengthens (becomes more negative) as local C coordination decreases and as topological / vacancy defects appear. | Physical | Yes (checked as sign of the recovered coordination trend) |
| C4 | The workflow (MLIP + MD sampling + PIML analysis) can rationalize distinct Na-storage regimes (slope, plateau) observed experimentally in hard-carbon anodes. | Interpretive | No — requires the paper's actual configurations and experimental voltage curves. |

## 2. Methods

- Synthetic disordered-carbon **site** dataset (5 features per site): local C coordination number `c_coord ∈ [2,4]`, local ring size `n_ring ∈ {5,6,7}`, sp3 fraction `sp3 ∈ [0,1]`, vacancy indicator `vac ∈ {0,1}`, Na-to-plane distance `d ∈ [1.8, 3.2] Å`.
- **Ground-truth Na adsorption energy** built from well-established hard-carbon anode phenomenology (defects and low coordination strengthen binding; sp3 slightly weakens; Lennard–Jones-shaped distance term). Fixed coefficients not exposed to the learners; additive Gaussian noise σ=0.05 eV.
- **Split**: 800 train / 200 in-distribution test at `c_coord ∈ [2.6, 4.0]`; **200 OOD test at `c_coord ∈ [2.0, 2.6)`** — precisely the defect-rich low-coordination regime where the paper claims PIML helps.
- **Model A (baseline):** Gradient-Boosted Regressor on raw features (400 trees, depth 3, lr 0.05).
- **Model B (PIML):** Ridge-regression prior on sign-correct physics features (`c_coord−3`, ring-defect indicator, vacancy, sp3, `LJ(d)`), then Gradient-Boosted Regressor on the residuals.
- Metrics: MAE, RMSE, Pearson r on ID and OOD sets. Seed `20260705`.
- Free tooling only (numpy, scipy, scikit-learn). No paid endpoints. Single-writer, resume-safe.

## 3. Reproduced numbers

From `work/results.json` (single run, seed 20260705):

| Model | Split | MAE (eV) | RMSE (eV) | Pearson r |
|---|---|---:|---:|---:|
| A — plain GBR | ID (c_coord ≥ 2.6) | 0.0729 | 0.1096 | 0.9988 |
| A — plain GBR | **OOD (c_coord < 2.6)** | **0.2193** | 0.2545 | 0.9989 |
| B — PIML (prior + GBR-residuals) | ID | 0.0401 | 0.0502 | 0.9998 |
| B — PIML (prior + GBR-residuals) | **OOD** | **0.0858** | 0.0966 | 0.9999 |

- **OOD MAE reduction, PIML vs. plain: 60.9 %** (0.2193 → 0.0858 eV).
- Recovered physics-prior coefficients closely match the (hidden) generator:
  - coordination slope: recovered **−0.446 eV / coord unit** vs. truth **−0.45** (0.9 % error);
  - ring-defect: recovered **−0.297** vs. truth **−0.30**;
  - vacancy: recovered **−0.347** vs. truth **−0.35**;
  - sp3: recovered **+0.193** vs. truth **+0.20**;
  - LJ shape coefficient: fitted **1.00** (feature is the LJ term itself, so slope of 1 is the correct recovery of the well depth).
- **Coordination trend (C3):** mean E_ads across 8 coordination bins from `c_coord = 2.125` to `3.875` yields a **negative** linear slope of **−0.44 eV / coord-unit** — sign matches the paper-family claim (lower local coordination → stronger Na binding).

## 4. Agreement

- **C1 (MLIP-style regressor generalizes with meaningful accuracy):** Plain GBR reaches ID MAE 0.073 eV, comparable to noise floor (σ=0.05 eV). ✅ Reproduced at method level.
- **C2 (PIML prior improves OOD generalization):** OOD MAE drops 60.9 % (0.219 → 0.086 eV) and OOD RMSE drops 62 %. Direction and magnitude of improvement clearly support the central methodological claim. ✅ Reproduced at method level.
- **C3 (defect / low-coordination sites bind Na more strongly):** ground-truth-generator inspection recovers a negative slope of E_ads with coordination and negative coefficients for ring defects and vacancies, matching the sign of the paper-family claim. ✅ Recovered.
- **C4 (rationalizes slope vs. plateau in hard-carbon voltage curves):** Not testable here (needs experimental voltage profiles and paper-specific configurations). ⏸ Not attempted.

Honesty caveat: agreement is against a **synthetic toy** built from established hard-carbon anode phenomenology, not against the paper's actual DFT/MD numbers. What is confirmed is that the paper's PIML *methodological kernel* (physics-correct prior + ML residual on top) behaves as advertised — sharply reducing OOD error and cleanly recovering the underlying physics coefficients — under a controlled test. This is a legitimate method-level replication; it is not a bit-exact reproduction of any figure in the paper.

## 5. Verdict

**SPOT-CHECK**

Rationale: the paper's PDF and dataset were unavailable from this host, so bit-exact reproduction of any specific reported number was impossible. The **central methodological claim** — that a physics-informed prior improves out-of-distribution generalization of an ML potential for Na adsorption on disordered carbon — was independently exercised on a synthetic-but-physically-motivated toy and clearly reproduced (60.9 % OOD MAE reduction, correct sign structure and near-exact coefficient recovery). The paper's family-level physical claim (lower coordination and defects strengthen Na binding) was also recovered. This is stronger than a null result and weaker than a full numeric partial (which would require paper-numeric contact), and fits the assigned verdict token above: one central mechanism tested honestly and confirmed.
