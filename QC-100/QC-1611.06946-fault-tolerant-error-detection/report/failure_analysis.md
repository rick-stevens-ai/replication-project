# Failure Analysis — QC-1611.06946 replication (HONEST CRITIQUE)

This document is deliberately adversarial. It lists what the replication
does **not** fully close, and where a determined skeptic could still push
back on the REPLICATED verdict.

## What the replication genuinely establishes

- **Structural FT property (C2)** — the flag-qubit encoding + Sx stabilizer
  circuit has 0/324 undetected La errors under exhaustive single-Pauli-fault
  enumeration. This is a proof, not a statistic. The paper's core FT claim
  is closed hard.
- **Log-log scaling signature (C7, C8)** — La ~ p^2 (fit 2.17 Sz / 1.92 Sx)
  and Lb ~ p^1 (fit 1.10 Sx) in the sub-threshold regime. The paper's
  Fig 4a slope claim reproduces cleanly.
- **Order-of-magnitude numerical match (C3–C5, C9)** — yield 76–81% vs
  paper 65–78%; err_La 0.18–0.27% vs paper 0.3%; La beats bare qubit by
  2×–50× over 2 decades of p.

## What the replication does NOT close

### 1. Fault-tolerance threshold / pseudo-threshold not independently regenerated

The `[[4,2,2]]` code is a distance-2 detection code (not correction), so
there is no fault-tolerance threshold in the standard sense. The paper
itself does not claim a numerical threshold. However, we also did not
extract a precise pseudo-threshold value (the p at which La = bare
physical qubit) and compare against any paper-quoted value. Our Table
under "Comparison to bare physical qubit" reports the crossover happens
between p=0.03 and p=0.05, but we did not fit an interpolated value or
bracket it with a Wilson interval. A skeptic could rightly ask: *what is
the precise pseudo-threshold, with error bars?* We did not answer that.

### 2. No head-to-head vs. alternative FT-EC schemes

We benchmarked the flag encoding against:
- a naive cat encoding (baseline, expected to break — confirmed);
- two noise models (depol2, single-fault).

We did **not** benchmark against:
- Chao–Reichardt 2018 flag-qubit distance-3 protocols;
- Chamberland–Beverland 2018 fault-tolerant syndrome extraction;
- the `[[7,1,3]]` Steane FT-EC construction;
- distance-3 rotated surface-code patches.

The paper's implicit "this is a good choice for near-term hardware" claim
is therefore only weakly cross-checked. Open question #1 captures the
concrete follow-up.

### 3. Overhead not quantitatively priced

We confirmed the paper's circuit uses 4 data + 1 flag + 1 syndrome ancilla
per stabilizer measurement, but did not assemble a formal resource-cost
comparison (qubit count, 2-qubit gate count, measurement count, wall time
under a given noise model) against alternative schemes. This limits our
ability to independently confirm the paper's implicit resource-efficiency
argument.

### 4. err_Lb systematically low by ~2× (C6 partial match)

Our simulated `err_Lb` at p=0.03 is 0.19% (Sz) / 0.83% (Sx), whereas the
paper reports 1.7% / 2.4%. That's a factor of ~2–9× under-prediction on
Lb. We explain this as "missing non-depolarizing ion-trap noise sources
(leakage, motional heating, correlated crosstalk)", but we did not
actually implement any of those noise channels to close the gap. A
skeptic could argue that the FT gap Lb/La in the paper (~8×) is much
larger than in our sim (~3×), which means we are under-testing exactly
the quantity that most strongly demonstrates FT. Open question #2 is
the concrete follow-up.

### 5. Yield gap on Sx is 11 percentage points

Our Sx yield 76.3% vs paper 65.2%. Explanation is the same as (4) —
missing SPAM / leakage — but was not experimentally closed. Again,
model refinement not attempted.

### 6. Encoding-circuit gate ordering assumed, not enumerated

Our exhaustive-enumeration test uses one canonical CNOT ordering
(`q0→flag, q0→q1, q0→q2, q0→q3, q0→flag`). We did not enumerate the 24
permutations of the data-CNOT block to prove that all of them preserve
FT (or identify which do not). A compiler-driven reordering could
therefore break FT silently. Open question #4 is the concrete follow-up.

### 7. Single-round only — no multi-round cycle test

We tested one stabilizer measurement per shot. Real FT-EC use requires
repeated syndrome extraction with mid-circuit measurement and reset.
Whether the 0/324 single-fault result extends to a 3-round cycle
(fault-point count grows to ~10^4) is untested. Open question #5 is the
concrete follow-up.

### 8. No hardware-realistic sensitivity study

We swept p but did not vary the relative SPAM/CNOT/idle ratios, did not
add T1/T2 dephasing, and did not model measurement crosstalk. The
paper's data implicitly encodes all of these; our replication does not.

### 9. Not literally the paper's Fig 2 gate sequence

The paper's Fig 2a–d shows hand-optimized encoding circuits. Our
flag-qubit construction is FT-equivalent for the same code but not gate
identical. A literal-circuit replication was not attempted; we assume
FT-equivalence (defensible for single-fault claims but not for gate-time
or two-qubit-gate-count comparisons).

### 10. Verdict robustness under adversarial noise models

We ran two noise models (depol2, single) that are both Pauli. Any
non-Pauli / non-Markovian channel that specifically targets the flag
qubit (e.g. leakage on the flag qubit that goes undetected because the
flag measurement projects onto {|0>, |1>}) could in principle break the
FT proof. Our replication assumes flag-measurement is projective and
faithful; the paper's ion-trap experiment implicitly makes the same
assumption but with real leakage.

## Bottom line

The **REPLICATED** verdict is warranted for the paper's stated claims:
FT proof, La ~ p^2 scaling, Lb ~ p linear, La below bare qubit. The
verdict does **not** cover: pseudo-threshold precision, cross-scheme
comparison, resource-cost pricing, non-depolarizing noise robustness,
multi-round cycle behavior, or gate-order sensitivity. Those are the
five open questions to run next.
