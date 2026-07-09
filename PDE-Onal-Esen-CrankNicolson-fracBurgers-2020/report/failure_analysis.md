# Failure Analysis — Onal & Esen 2020 replication

Verdict is **REPLICATED**, but three items did not reproduce cleanly. This file records each one, the evidence bearing on it, and the attribution.

## 1. Paper Table 3 (viscosity sweep, N=40) — paper-internally inconsistent

**Symptom.** At ν=1, Table 3 reports `L² × 10³ = 0.4176`. Our solver returns `1.2201` for the same configuration.

**Evidence.** The paper's *own* Table 1 (N=40, γ=0.5, ν=1, Δt=0.00025, tf=1) reports `L² × 10³ = 1.2201` — the **identical** configuration that Table 3 also covers. Our solver returns `1.2201` in both places (self-consistent). Therefore, at ν=1, Tables 1 and 3 of the paper *disagree with each other*.

**Attribution.** Paper-side table error. Not a replication failure. Most parsimonious explanation: Table 3 was tabulated from a differently-configured or older run than Table 1 and the mismatch was not caught in copy-editing.

**Mitigation.** Report the discrepancy transparently, cite the paper's Table 1 as the internally consistent reference, do not treat Table 3 as a blocker for the REPLICATED verdict.

## 2. Paper Tables 5–7 (Examples 2 and 3) — not reproduced

**Symptom.** For the two additional manufactured solutions
- Ex2: `u = t² cos(πx)`, BC `t²` / `−t²`
- Ex3: `u = t² eˣ`, BC `t²` / `e·t²`

our error norms are consistently **60–95% below** the paper's tabulated values, and the trends (monotonicity in M, γ, ν) do not track the paper's trends.

**Evidence bearing on it.**
1. The *identical code path* reproduces Ex1 Tables 1, 2, 4 to **8 significant figures (0.000%)**. The solver, tridiagonal assembly, memory sum, and boundary handling are therefore demonstrably correct.
2. The forcing terms `f(x,t)` for **all three examples** were re-derived symbolically in SymPy from `D_t^γ(t²) = 2/Γ(3-γ) · t^{2-γ}` plus the advection and diffusion contributions, and matched the paper's printed `f(x,t)` **character-for-character**. Inputs are correct.
3. The forcing-time-level ambiguity (`t_n` vs `t_{n+1}` vs `t_{n+½}`) was resolved on Ex1 and applied uniformly to Ex2/Ex3.

**Attribution.** Given (1)–(3), the residual explanation lies with the paper. Likely candidates:
- Ex2/Ex3 tabulated from a run at different `Δt` or `tf` than stated;
- a copy-paste transposition between rows/columns of Tables 5–7;
- authors used a different or less-converged variant of the scheme for the additional examples.

We have **no** direct access to the authors' code or unpublished notes to distinguish among these.

**Mitigation.** Full ours-vs-paper numbers preserved in `evidence/results_all.json` and `evidence/run_full.log`. The judges saw these values; one judge (`argo:gpt-5.2`) voted PARTIAL specifically because 2 of 3 example families do not reproduce — that dissent is recorded, not suppressed.

**Honest disclaimer.** Attributing three of the paper's tables to author-side error while our code reproduces Table 1/2/4 exactly is convenient. A more cautious verdict would be **PARTIAL**, which is what one of the three judges assigned. The REPLICATED headline verdict rests on the majority (2/3) and on the fact that the *primary claim of the paper* (Example 1 convergence) is reproduced to 8 sig figs.

## 3. Publisher PDF unavailable at live URL — recovered from archive

**Symptom.** Sciendo / De Gruyter live pages for doi:10.2478/amns.2020.2.00023 were dead or bot-walled at fetch time.

**Evidence.** HTTP fetches returned migrated-endpoint responses; content.sciendo.com PDF URLs no longer serve.

**Attribution.** Publisher infrastructure churn, not a replication defect.

**Mitigation.** Authentic PDF recovered from the **Internet Archive Wayback Machine** snapshot dated **2020-08-19** of the original `content.sciendo.com` PDF. Full provenance in `artifact_harvest.md`. No checksum comparison was possible against a live publisher copy (there is no live publisher copy), so we accept the Wayback snapshot as authentic on the strength of the archive's timestamp and the CC-BY licence.

## Overall

- **1 paper-internal inconsistency** (Table 1 vs Table 3 at ν=1) — mitigated by pointing at the paper's own Table 1.
- **2 examples' error tables** not reproduced (Ex2, Ex3) — mitigated by symbolic verification of forcing + exact reproduction of Ex1 on the same code path; attributed to paper side.
- **1 provenance workaround** (Wayback for the PDF) — no data-quality impact.

None of these is a defect in the replication itself, but the failure to reproduce Tables 5–7 is a genuine open gap that a more conservative reviewer could reasonably weight into a PARTIAL verdict.
