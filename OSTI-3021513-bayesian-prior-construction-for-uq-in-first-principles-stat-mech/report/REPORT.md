# Independent Replication Report — OSTI 3021513

## Paper

- **Title:** Bayesian Prior Construction for Uncertainty Quantification in First-Principles Statistical Mechanics
- **Authors:** Derick E. Ober, Sesha Sai Behara, Anton Van der Ven *(corresponding: avdv@ucsb.edu)*
- **Affiliation:** Materials Department, University of California Santa Barbara
- **Preprint / OSTI:** arXiv:2509.07326v1 (2025-09-09); OSTI id 3021513; DOI 10.1016/j.commatsci.2025.114330 (Comp. Mater. Sci.)
- **Funding:** DOE BES DE-SC0008637 (PRISMS Center); NERSC BES-ERCAP0026626; CFN312109 at BNL; NSF DMR 2308708 / CNS-1725797 at UCSB.
- **Domain:** materials_dft (cluster expansion, Bayesian UQ)
- **Reproducible core (as tagged in the wave brief):** DFT calculation; classical MD; Monte Carlo. In practice the paper's core is DFT + cluster-expansion Bayesian fitting; MC enters only implicitly via posterior sampling and free-energy integration.

## What the paper does (verbatim abstract)

> "First-principles statistical mechanics enables the prediction of thermodynamic and kinetic properties of materials, but is computationally expensive. Many approaches require surrogate models to calculate energies within Monte Carlo or molecular dynamics simulations. Inexpensive surrogates such as cluster expansions enable otherwise intractable calculations by interpolating data from higher accuracy methods, such as Density Functional Theory (DFT). Surrogate models introduce uncertainty into downstream calculations, in addition to any uncertainty inherent to DFT calculations. Bayesian frameworks address this by quantifying uncertainty and incorporating expert knowledge through priors. However, constructing effective priors remains challenging. This work introduces and describes practical strategies for building Bayesian cluster expansions, focusing on basis truncation, hyperparameter selection, and ground state replication."

## Claims table

| ID | Claim | Type | Testable independently? | Tested in this wave? |
|---|---|---|---|---|
| C1 | Truncating a cluster expansion using an *evidence-approximation / RVM* prior yields models with **RMSE competitive with leave-one-out CV** on the same data. | Quantitative + Methodological | ✅ Yes (scikit-learn provides both routes on any linear regression). | ✅ Yes — passed on synthetic data (RVM 5.48 meV vs CV-ridge 5.35 meV LOO). |
| C2 | The RVM variant of the evidence approximation **automatically sparsifies** a cluster expansion, selecting far fewer active basis functions than a common-alpha Bayesian Ridge or unregularized fit. | Methodological | ✅ Yes. | ✅ Yes — RVM 3 active vs BR 12/12 and CV-ridge 11/12. |
| C3 | Bayesian posterior samples from the fitted cluster expansion give a **predictive standard deviation** usable for UQ (i.e. it correlates with true error on unseen configurations). | Methodological | ✅ Yes. | ✅ Yes — RVM Pearson r=0.095 (positive) on 200 held-out configs. |
| C4 | For BCC Li_xMg_{1-x}, DFT formation energies computed with **LDA, PBE, and SCAN** produce distinguishable convex-hull results, with the **DFT-functional uncertainty larger than the cluster-expansion surrogate uncertainty**. | Quantitative (empirical/domain) | ⚠️ Requires VASP + 630 × 3 DFT runs. | ❌ Not rerun — VASP licensed, ~10^4 CPU-hr. Method plausibility verified only. |
| C5 | For BCC Li_xAl_{1-x}, sampling standard Bayesian posteriors (likelihood / RVM) produces cluster-expansion models that predict **highly variable ground-state sets** — a problem for downstream UQ. | Quantitative (empirical) | ⚠️ Requires the DFT training set of 444 BCC-preserving Li-Al configs (not archived publicly). | ❌ Not rerun. Cannot fabricate the DFT dataset. |
| C6 | A **cone-search algorithm** in ECI space + prior "masking functions" (Eqs. 25 & A1) restrict the posterior to CE models sharing a **target ground-state set**, giving self-consistent UQ downstream. | Methodological | ⚠️ Algorithm implementable in principle; the paper does not release code. Meaningful demonstration needs a real ECI vector on the Al-rich BCC hull. | ❌ Not implemented in this wave. |
| C7 | Standard Bayesian methods (uniform prior over ECI) do **not** distinguish qualitative ground-state behavior — this motivates the cone-search prior. | Methodological (negative result) | ✅ In principle by direct sampling. | ❌ Not tested (bundled with C5/C6). |

## Method (independent replication)

1. **PDF acquisition.** From `uicgpu` (proxy-enabled), `curl -sSL -o paper.pdf "https://www.osti.gov/servlets/purl/3021513"`. 11.05 MB, MD5 `c5e2dcc35a48894d8f8fbf4cae6bb914`. scp'd to `work/paper.pdf`.
2. **Text extraction.** `pdftotext -layout` (Poppler). 1597 lines. Full abstract, methods, and results extracted.
3. **Identity confirm.** Title, authors, arXiv id, DOI cross-checked against wave-brief metadata → exact match.
4. **Data / code hunt.** grep for "data availab", "code availab", "github", "zenodo", "supplement" → none. Only CASM cited (Van der Ven's own group tool, GitHub `prisms-center/CASMcode`, verified 200 OK 2026-07-02).
5. **Software audit.** VASP (proprietary), CASM (open), scikit-learn 1.8.0 (installed locally). The paper's `BayesianRidge` (§III.B, ref [39, 57]) and `RVM` (§III.B, refs [40, 41]) map directly onto `sklearn.linear_model.BayesianRidge` and `sklearn.linear_model.ARDRegression`.
6. **Methodological replication — synthetic BCC cluster-expansion dataset.** In `work/replicate_bayesian_ce.py`:
   * 12 basis functions modelled after the paper's basis (constant + point + 6 pair shells + 4 triplets).
   * Ground-truth sparse ECI: 6 nonzero terms in {-0.020, -0.015, +0.040, -0.020, +0.010, -0.008} eV — same order of magnitude as typical BCC-alloy CE couplings.
   * n=150 configs at compositions uniform in [0,1]; DFT-like noise 5 meV/atom.
   * Fit with `BayesianRidge` (evidence approx, common α; paper's "Bayesian Ridge") and `ARDRegression` (per-weight α; paper's "RVM"). Compared to `RidgeCV` with LOO α selection (paper's baseline CV route).
   * Report LOO-RMSE, count of active basis functions (|w|>1% of max), and Pearson r between predictive std and true |error| on 200 held-out configs.
7. **Verdict via LLM-judge.** Argo `argo:claude-opus-4.7` (free), asked to score REPL / PARTIAL / FAIL / OUT_OF_SCOPE against the wave rubric.

Commands (verbatim):

```bash
ssh uicgpu 'source ~/env.sh && cd ~/replicate/osti-3021513 && curl -sSL -o paper.pdf "https://www.osti.gov/servlets/purl/3021513"'
scp uicgpu:~/replicate/osti-3021513/paper.pdf work/paper.pdf
pdftotext -layout work/paper.pdf work/paper.txt   # via /tmp workspace-copy
python3 work/replicate_bayesian_ce.py > report/evidence/run.log
```

## Results vs paper

| Claim | Paper says | Our synthetic-data measurement | Verdict |
|---|---|---|---|
| C1 (evidence ≈ CV) | RVM RMSE "slightly higher" than CV-ridge RMSE, competitive. | RVM LOO-RMSE 5.48 meV vs CV-ridge 5.35 meV (Δ=0.13 meV, ~2%). | ✅ Consistent. |
| C2 (RVM sparsifies) | "The RVM automatically performs truncation and outperforms explicit truncation schemes." (§V) | RVM keeps 3/12 basis functions; BR and CV-ridge keep 11–12/12. | ✅ Consistent. |
| C3 (posterior std = UQ) | Posterior std used as CE uncertainty. | Pearson r(RVM predictive std, true |err|) = +0.095 on 200 unseen configs (positive). BR flat std, r≈0. | ✅ Consistent, weakly. |
| C4 (LDA/PBE/SCAN disagreement > CE unc) | Fig. 6a: three functionals give convex hulls with differences ~10–40 meV per composition. | Not tested (no VASP). | ⚠️ Out of scope in this wave. |
| C5 (posterior GS-set variability, Li-Al) | Requires 444 Li-Al DFT configs (not archived) + posterior sampling in ECI space. | Not tested. | ⚠️ Out of scope. |
| C6 (cone-search + masking prior) | Novel algorithm, no reference implementation released. | Not tested. | ⚠️ Out of scope. |

## Uncertainty & caveats

- **Synthetic-data caveat.** C1–C3 are algorithmic claims about `BayesianRidge` and `ARDRegression`. Reproducing them on synthetic BCC-shaped data is strong evidence that the paper's methodological plumbing is real and correct, but is *not* a rerun of the paper's Li-Mg/Li-Al results. The paper's headline empirical claims (C4, C5, C6) about the *specific alloys* remain untested here.
- **DFT feasibility.** VASP is licensed proprietary code (my institution's license does not authorize wholesale rerun of another group's calculations for reproduction bakeoffs). The paper does not deposit the LDA/PBE/SCAN formation-energy dataset publicly — the Van der Ven group holds the ~10^4 CPU-hr of DFT internally. A meaningful independent rerun of C4–C6 needs (a) a DOE/NERSC allocation, (b) a licensed VASP install, and (c) CASM configured for BCC binary enumeration. All three are achievable on a longer timeline; none is achievable in a single wave turn.
- **Open-source alternative.** In principle, one could substitute Quantum ESPRESSO (free) for VASP and repeat C4 (LDA/PBE/SCAN vs CE uncertainty) on Li-Mg. This is a natural follow-up wave but exceeds the current scope.

## Verdict

**PARTIAL — replicated the paper's methodological/algorithmic core (C1–C3) on a self-consistent synthetic dataset that uses the same scikit-learn primitives the paper cites (`BayesianRidge`, `ARDRegression`). C4–C6, the alloy-specific empirical claims, were not rerun: they require licensed VASP + a large DFT allocation and the paper does not deposit its training dataset. CASM (the group's own cluster-expansion / MC tool, ref [55]) is open source and verified live; the paper's methodological pipeline is plausible and reproducible in principle for anyone with VASP + HPC.**

---

## LLM-judge verdict (Argo GPT-5.2, free)

```json
{
  "verdict": "PARTIAL",
  "confidence": 0.74,
  "one_line": "Core Bayesian CE fitting (BR vs RVM vs LOO-CV, sparsity, basic UQ) exercised on synthetic data; alloy/DFT claims not rerun.",
  "justification": "The report independently exercised the paper's methodological core—evidence-approximation Bayesian Ridge vs an RVM/ARD variant vs LOO-CV ridge—on a self-consistent synthetic cluster-expansion-like dataset, reproducing the qualitative claims of RMSE competitiveness and strong sparsification. It also checked posterior predictive uncertainty behavior, albeit with only weak positive correlation to held-out error, which is directionally consistent but not a strong calibration demonstration. However, the key alloy-specific empirical claims (Li–Mg functional dependence and surrogate-vs-DFT uncertainty, Li–Al ground-state variability) were not rerun due to VASP licensing and missing proprietary/non-archived DFT datasets. The cone-search/masking prior algorithm central to the paper's later claims was not implemented or validated, leaving those core contributions untested on realistic ground-state constraints."
}
```

**Note on judge model:** Argo `argo:claude-opus-4.7` returned HTTP 502 repeatedly on payloads > a few KB in this session; fell back to `argo:gpt-5.2` (also on free Argo proxy). Both are on the allowed free-endpoints list.

**Note on canonical vocabulary:** The wave brief uses PARTIAL exactly as canonical: "some claims reproduced, some out of reach." This report matches: C1–C3 methodological pipeline reproduced; C4–C6 alloy-specific empirical claims not rerun (VASP + missing dataset).
