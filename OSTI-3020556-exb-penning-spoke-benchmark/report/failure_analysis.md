# Failure Analysis — OSTI 3020556

**Verdict:** REPLICATED
**Scope of replication:** analytic core of the CSHI spoke-frequency prediction only.

This document is deliberately honest about **what did not succeed, what was not attempted, and where the replication would fail under stricter tests.**

---

## A. Explicitly NOT attempted (out of scope)

### A1. Full 2D PIC benchmark (Claim C6)
- **What was skipped:** reproducing time-averaged ion density, plasma potential, and electron-temperature profiles from an independently written 2D radial–azimuthal PIC code on the Table-1 problem; measuring the spoke dynamics directly and extracting f_s from a Fourier or time-of-flight analysis; comparing against the paper's multi-code ensemble (PPPL, EP-PIC2D, LePIC2D, …).
- **Why:** the paper's own reference simulation is 12.5M time steps on a 256² grid — a multi-hour, multi-code effort. This is incompatible with the <25-minute efficient replication budget.
- **Consequence:** the "REPLICATED" verdict here covers the paper's *analytic rationalization* of the measured spoke frequency, not the underlying PIC measurement itself. A reader treating this report as "the PIC benchmark has been independently reproduced" would be misled.

### A2. Inter-code comparison
- **What was skipped:** cross-checking the paper's implicit claim that the participating PIC codes agree with each other (the raison d'être of the community benchmark).
- **Why:** no independent PIC code was run; we only reimplemented Eq.4.
- **Consequence:** we cannot say anything about inter-code scatter, which is arguably the most valuable output of a community benchmark.

### A3. Uncertainty propagation
- **What was skipped:** propagating the "≈" in E_r ≈ 100 V/m (typical ±10%) and the fit uncertainty in L_n = 7.1 mm through Eq.4 to produce a proper ±kHz error bar on the 53.00 kHz prediction.
- **Consequence:** the 4-decimal precision on our numbers is spuriously tight; realistic uncertainty on f_s,th is probably ±(2–5) kHz, not ±0.01 kHz.

## B. Weaknesses in what WAS attempted

### B1. R_0 back-solve is borderline circular
- Setting R_0 = 25 mm (natural = domain half-width) gives 52.69 kHz, which matches the paper's ~53 kHz to −0.6%. This is the earned number.
- Back-solving R_0 = 24.85 mm from 53 kHz and then claiming <0.01% agreement is a *self-consistency check on Eq.4*, not an independent test. It should not be read as a stronger validation than the −0.6%.

### B2. Nonlinear-saturation rationalization is unquantified
- The 23% over-prediction (theory 53 kHz vs measured 43.2 kHz, ratio 1.227) is generic to linear-vs-nonlinear behavior but is *not derived* here. Our report matches the ratio to 4 decimals only because we plugged the paper's own numbers back into the paper's own ratio — this is arithmetic consistency, not physics.

### B3. Single-mode assumption
- Eq.4 assumes a single azimuthal mode k = 2/R_0 at r = R_0/2. Real spokes have multi-mode content and radial structure. We did not verify m=1 is dominant in the paper's PIC data (would require reading the paper's mode-decomposition plots, which we did not extract quantitatively).

### B4. E×B kinematic cross-check is qualitative
- v_ExB = E_r / B = 10 km/s → 64 kHz at R_0 = 25 mm. Measured 43.2 kHz corresponds to spoke/E×B ≈ 0.67. This confirms Ref [93]'s statement that spoke velocity < v_ExB but is not a discriminating test of Eq.4 vs alternative theories.

### B5. LLM judge is not an independent physical verifier
- Argo gpt-5.2 at 95% agreement is a language-model consistency check on the same numbers we produced. It has no independent knowledge of whether Eq.4 was transcribed correctly or whether SI units were handled properly. A human review of the formula transcription and unit dimensions would strengthen the result.

## C. Failure modes that would flip the verdict

### C1. Wrong formula transcription
- If Eq.4 as reimplemented actually differs from the equation in arXiv:1805.04438 (e.g., wrong factor of π, wrong k, wrong sign under the sqrt), then the numerical agreement is coincidental and the verdict should degrade to INCONCLUSIVE.
- Mitigation: the report shows the extracted equation inline in Method §; an independent human read of arXiv:1805.04438 pp. containing Eqs. 3–4 would confirm or refute this.

### C2. Wrong parameter reading from Table 1
- If E_r ≠ 100 V/m or L_n ≠ 7.1 mm or m_i is not 4-amu-equivalent, the 53 kHz prediction shifts. Our He-4 mass consistency check (7291.712 mₑ = 4.000 amu) rules out m_i error but not E_r or L_n misreads.
- Mitigation: reread Table 1 and Sec 3 of the paper to reconfirm.

### C3. R_0 is meant to be something other than the domain half-width
- If the paper implicitly uses r_spoke (spoke centroid radius) or a plasma-column radius substantially different from 25 mm, then the "natural R_0 = 25 mm → −0.6% match" story falls apart.
- Mitigation: cross-check R_0 against the density-profile peak from the paper's Fig. showing radial profiles.

## D. What a stronger replication would add

1. A short 2D PIC rerun (WarpX ES-PIC or minimal in-house code) at reduced resolution to independently generate a spoke and directly measure f_s, closing C6 even at low fidelity.
2. A parameter sweep in (E_r, L_n, m_i) to verify the scaling laws experimentally rather than algebraically.
3. A full linear dispersion-relation solve of the 2D E×B problem to confirm CSHI is the dominant branch (addresses open question 3).
4. Uncertainty propagation with realistic ± on E_r and L_n.
5. Human peer read of the Eq.4 transcription from arXiv:1805.04438.

## E. Ledger of failures during this replication run

- No hard failures during the analytic reimplementation, PDF fetch, arXiv resolution, or LLM-judge call.
- The report explicitly declines to score C6 rather than fabricating a PIC number.
- No fabricated numbers detected; all values in REPORT.md are either directly from the paper, computed by `work/replicate_spoke.py`, or from `work/judge.py`.

---

**Bottom line:** the "REPLICATED" verdict is honestly earned for the analytic core (C1, C2 via ratio, C3, C4, C5) and honestly withheld on the full PIC benchmark (C6). Consumers of this report should treat it as *"the paper's own analytic rationalization of ~53 kHz is reproducible from stated parameters and standard constants,"* not as *"the community PIC benchmark has been independently rerun."*
