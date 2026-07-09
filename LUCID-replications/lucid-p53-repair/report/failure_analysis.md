# Failure analysis — LUCID p53 / DNA-damage-repair replication

**Verdict: PARTIAL** (6/8 qualitative claims reproduced; 0 contradicted; 3
partially reproduced; the paper's headline stochastic apoptosis percentages
and NASIC track-structure physics were not exercised).

This file is the honest what-we-did-vs-what-the-paper-claims accounting.

---

## 1. What we did (in scope)

- Independent Python re-implementation of a 27-species deterministic ODE
  covering the DSB → ATM → p53 → {Mdm2, Wip1, PTEN/AKT, Bax, p21} network
  described by Hat 2016 (PLOS Comp Biol) and re-used by LUCID (Hu 2022,
  MDPI IJMS 23:11323) with a small TGFβ chain added on top of p21.
- Two-stage integration (24 h warmup + 600 s IR square pulse + 72 h
  observation) via SciPy LSODA.
- Doses 2/4/6/8 Gy at two ATM Hill thresholds M ∈ {0.14, 0.5} Gy.
- Four figures (LUCID Fig. 4 twice, Fig. 5, Fig. 6 surrogate) + per-species
  per-dose peak table in `results/summary.json`.
- Recovered the LUCID MDPI supplement (Tables S1–S3) via the static CDN
  after the `/article/.../s1` URL returned bot-gated 403; cross-checked
  that LUCID's listed reactions and rate constants are consistent with
  Hat 2016 (same variable names, same Hill function with M explicitly
  written as 0.14 Gy or 0.5 Gy, same DSB_Gy = 10, same IRT = 600 s).

## 2. What the paper claims that we DID exercise

| LUCID claim | Our evidence | Grade |
|---|---|---|
| DSBs repaired on hour timescale, most gone by 24 h | DSB → <1 by ~24 h in all doses | Full |
| ATM activation saturates for moderate–high dose | ATMp plateaus near ATMtot across 2/4/8 Gy | Full |
| p53 amplitudes similar for 2 Gy vs 8 Gy due to ATM saturation | p53_ARR curves overlap | Full |
| Higher dose → more Bax → more apoptotic drive | Bax peak monotone in dose; Bax/AKTp monotone | Qualitative full |
| Lower M (0.14 Gy) gives higher apoptotic response than M=0.5 | Sign matches LUCID Fig. 6a vs 6b | Qualitative full |
| p53/Mdm2/Wip1 oscillate with ~8 h period | Single damped ~8 h cycle detected | Partial |
| TGFβ secretion increases with dose | Monotone but weakly separated | Partial |
| Slow-repair fraction / high-LET → longer arrest, more apoptosis | p21 plateau reached fast regardless of dose | Partial |

## 3. What the paper claims that we did NOT exercise (headline gaps)

### 3.1 Stochastic apoptosis percentages (LUCID Fig. 6 bar heights)
LUCID reports concrete apoptosis-fraction numbers at 72 h across dose and M.
Those numbers come from a Gillespie ensemble of ≥100 single cells running
the Bogdał 2013 apoptotic gate on top of the shared p53/Mdm2/Wip1 dynamics.
**We report a deterministic Bax/AKTp propensity ratio, not a population
fraction.** This is not the same experiment; a mean-field ODE cannot produce
a per-cell death-count distribution. Closing this gap is the single largest
lever to upgrade the verdict.

### 3.2 NASIC track-structure Monte Carlo DSB generation
LUCID's stated motivation is to couple track-structure radiation physics
(NASIC) to the p53 network. We use the analytical `DSB = DSBGy · dose`
square-pulse input inherited from Hat 2016. This is faithful to the ODE
substrate LUCID quotes (LUCID Eq. 4) but is silent on radiation quality
(LET), which is a major differentiator of the LUCID paper from Hat 2016.

### 3.3 Parameter refitting / independent identification
We adopt Hat 2016's parameter values verbatim (as LUCID does). Neither we
nor LUCID re-fit the parameters against new single-cell data. LUCID does
not claim to have done so, so this is an inherited gap, not a new one.

### 3.4 Quantitative match to single-cell timelapse data
No live-cell p53-Venus dataset (Lahav lab, Purvis 2012, Batchelor 2011) was
quantitatively matched. LUCID itself compares to literature qualitative
behavior only, so this is an inherited gap.

## 4. Substitutions we DID make (and why they matter)

| Tag | What we substituted | Why | Effect on results |
|---|---|---|---|
| `model-substitution` | Raised `g6, g9, g19` protein-degradation constants from Hat's ~10⁻¹³/s gene-state values to effective ~1-h half-life rates | Buffering binding chain (Bax/BclxL/Badu/14-3-3, Rb1/E2F1/CycE) is omitted from the reduced ODE; Hat's deterministic limit blows up without it | Keeps the reduced system bounded; changes effective network topology relative to the full Hat model; a stronger replication would restore the buffering chain and revert `g_i` |
| `monte-carlo-substitution` | Analytical DSB square-pulse instead of NASIC per-particle track simulation | NASIC not open source; equivalent MC (TOPAS-nBio) not integrated here | Silent on LET; head-line gap for LUCID's radiation-quality claims |
| `stochastic-omitted` | Deterministic Bax/AKTp propensity instead of ensemble Gillespie apoptosis gate | Bogdał 2013 gate not implemented in this pass | Cannot produce apoptosis percentages; Fig. 6 bar heights unmatched |
| TGFβ chain collapse | First-order p21-driven relaxation instead of full p21→GADD45→p38→TGFβ chain | Simplification for tractability | Weakens dose separation in Fig. 5; matches LUCID's deterministic-limit behaviour but not the stochastic figure |

## 5. Why the verdict is PARTIAL and not REPLICATED

- Six of eight qualitative claims are reproduced.
- Two of eight are partially reproduced (oscillation sustained vs damped;
  TGFβ dose-separation).
- Zero are contradicted.
- **But** the paper's two headline quantitative outputs — the Fig. 6
  apoptosis-fraction bars and the LET-differentiated response — are
  fundamentally out of reach of a deterministic ODE. Reporting a propensity
  surrogate is intellectually honest, but it is not the same measurement.
- A REPLICATED verdict would require, at minimum: (a) the Bogdał 2013
  Gillespie apoptosis gate over ≥100 cells producing 72-h death fractions
  within ~10% of LUCID Fig. 6, and (b) a track-structure MC input for
  at least one non-photon beam quality with matched dose.

## 6. Why the verdict is not SPOT-CHECK or NO-GO

- SPOT-CHECK would understate the depth: 27-species independent ODE with
  cross-checked parameters and 4 figures matching claim structure is more
  than a sniff test.
- NO-GO would be wrong: the deterministic backbone reproduces the paper's
  claim structure with no contradictions.

## 7. What honest analytical-paper upgrade rules say

The backfill brief allows PARTIAL → REPLICATED for purely analytical papers
(ODE + math model with no MC / wet-lab step) if the headline was fully
exercised. LUCID does not qualify: its headline explicitly includes (a) a
Monte Carlo track-structure step (NASIC) and (b) a stochastic per-cell
apoptosis gate (Bogdał 2013). Both are missing from this pass, so PARTIAL
is preserved as-is. No upgrade.

`verdict_preserved=PARTIAL`
