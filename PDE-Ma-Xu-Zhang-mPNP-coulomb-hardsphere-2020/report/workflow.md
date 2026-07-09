# Workflow — Replication of Ma-Xu-Zhang mPNP (DOI 10.1137/19M1310098)

Session `d8f26e02` on `CherryRd`, 2026-07-04, ~30 min wall clock.

## 0. Pre-flight
- ABORT-check: `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -i pnp` — no top-level hit; proceeded. (The prior Ollie 2026-05-28 replication is buried two levels deep at `PDE-replications/modified-pnp/` and was missed by the direct-children check. Both replications are preserved.)
- Session scratch: `~/Dropbox/REPLICATE-PROJECT/PDE-Ma-Xu-Zhang-mPNP-coulomb-hardsphere-2020/`.
- Toolchain: Python 3.14.6, numpy 2.4.3, scipy 1.18.0, matplotlib default, poppler `pdftotext`.

## 1. Data acquisition
1. Semantic Scholar API `/graph/v1/paper/DOI:10.1137/19M1310098` (S2 key from macOS Keychain) → DOI, corpus ID, `openAccessPdf.url` pointing to arxiv.org/pdf/2002.07489.
2. `curl -L -o work/paper.pdf https://arxiv.org/pdf/2002.07489` → 1,006,890 bytes, HTTP 200.
3. `pdftotext -layout work/paper.pdf work/paper.txt` → 1343-line text for equation transcription and grep.

## 2. Claim triage
Nine candidate claims C1–C9 extracted from the paper. Three (C1, C2, C3) selected as testable inside a single ~30-min compute session without implementing the WKB Coulomb self-energy (Eq. 3.22) or reproducing external MC/MD databases. C4–C9 declared out of scope.

## 3. Implementation
1. `work/src/mfmt_1d.py` — vectorised 1D MFMT weighted-density integrator (cumulative sums + linear endpoint corrections, strict O(h^2)).
2. `work/src/experiment_convergence.py` — MFMT convergence test at $(\epsilon,q,a)=(0.2,0.3,0.15)$, $c_i(x)\equiv 1$, $c_{tot}=2$, $N\in\{200,400,800,1600,3200\}$; analytic Carnahan–Starling target $\mu_{hs}^{CS} = 0.238752$.
3. `work/src/pb_newton.py` — steady mPNP Newton solver:
   - MF: single Newton on $-2\epsilon^2\phi'' - (e^{-\phi} - e^{\phi}) = 0$ with 2nd-order one-sided Robin BCs. 5 iter to $|R| = 3.5\times 10^{-12}$.
   - SC: outer damped Picard ($\omega=0.4$) on $\mu^{hs}(x)$ around inner Newton on $\phi$; bulk-offset subtraction; 35 outer iter to $\mu_{rel\_diff} = 8.7\times 10^{-10}$.
   - Grid: $N=401$, $x \in [-(1-a), 1-a] = [-0.85, 0.85]$, $h = 4.25\times 10^{-3}$.
4. `work/src/plots.py` — two evidence PNGs (`fig41_convergence.png`, `fig45_mf_vs_sc_replication.png`).

## 4. Numerical execution
```bash
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Ma-Xu-Zhang-mPNP-coulomb-hardsphere-2020/work
python3 src/experiment_convergence.py     # -> report/evidence/fig41_convergence.json
python3 src/pb_newton.py                  # -> report/evidence/fig45_newton_mf_sc.json
python3 src/plots.py                      # -> report/evidence/*.png
python3 src/llm_judge.py                  # -> report/evidence/llm_judge.json
```

## 5. Scoring
- LLM judge: Argo `:44497` (free per project rule). Fallback chain `argo:claude-opus-4.7 → argo:claude-sonnet-4.6 → argo:gpt-5.2`. Opus 4.7 returned HTTP 502; **Sonnet 4.6** delivered the verdict (recorded in `evidence/llm_judge_model.txt`).
- Judge input: structured prompt with C1/C2/C3 statements + numerical evidence table.
- Judge output: per-claim SUPPORTED/CONTRADICTED/INSUFFICIENT and overall verdict from canonical vocabulary.

## 6. Verdict & report
- All three tested claims **SUPPORTED**.
- Overall verdict: **REPLICATED**.
- Section 7 of `REPORT.md` adds a cross-check vs the prior Ollie 2026-05-28 replication that had implemented LC/LS as well — both agree on MFMT + MF + SC.

## 7. Post-flight
- Duplicate-work notice added at the top of `REPORT.md`.
- No overwrite of the earlier replication; both preserved for cross-validation.
- Recommend Ollie's earlier LC/LS-inclusive replication as canonical; this one as an independent MFMT + MF + SC cross-check.
