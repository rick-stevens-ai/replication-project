# Failure analysis — arXiv:1806.11463

## What this replication actually shows

We reproduced the paper's central technical claims at the simulation
tier: the HHL quantum matrix-inversion algorithm, applied to the
paper's exact $2\times 2$ matrix, delivers $A^{-1}|b\rangle$
noiselessly (fidelity 1.000000 vs classical `np.linalg.solve`),
degrades smoothly with parametric gate noise (matching Fig. 1(a)
qualitatively), and --- plugged into a toy 2-point GP --- yields
the same Bayesian predictive mean (0.475) and variance (0.6725)
as classical inversion, to machine precision.

That is a legitimate, positive replication of C1, C2, C3, C5.

## What this replication does NOT show — read this carefully

The verdict REPLICATED is **narrow** and needs to be quoted with
these caveats:

### 1. No Bayesian NN was trained
Neither by us nor by the paper. The paper's contribution is a
Bayesian-inference primitive (HHL for the GP linear solve),
motivated by the infinite-width-NN-is-a-GP correspondence. It is
NOT a Bayesian deep net trained end-to-end on any dataset. So
this replication does not (and cannot) verify any predictive-accuracy
metric of a Bayesian deep net vs a frequentist baseline; the paper
does not report any such metric either.

### 2. The paper's "specific dataset" is a single 2x2 matrix
There is no held-out test set. The paper's empirical section is a
hardware-primitive demonstration of one linear solve, not a
regression benchmark. Our replication mirrors that: the end-to-end
GP posterior is on a 2-point toy problem. This is fair to the
paper --- we replicated what was in the paper --- but it means the
replication says nothing about scale, calibration on held-out data,
or transfer.

### 3. No non-Bayesian baseline
The paper does not compare against non-Bayesian NNs (its argument
is about complexity, not predictive accuracy). We did not add such
a comparison either; it would be off-topic for a replication.
But downstream readers should be aware that the paper is NOT
claiming that Bayesian-via-HHL beats a plain NN on prediction ---
it is claiming that IF you want Bayesian inference on a GP posterior,
HHL gives an asymptotic complexity advantage. That "if" is doing a
lot of work.

### 4. Uncertainty calibration not empirically tested
We reproduce the numerical value of the posterior variance (0.6725).
We do NOT check whether this variance is well-calibrated (do 95%
credible intervals actually cover 95% of held-out points?). The
paper does not check this either. On a toy 2-point problem there is
no test set to check against. See Q3 in `open_questions.json` for
the concrete probe.

### 5. Hardware claim C4 unreproducible
IBMQX5 (paper's F=0.78 headline) has been decommissioned. We
bracket the reported number via noisy simulation at 5-10%
per-gate depolarizing error, which is realistic for 2018-era
superconducting hardware. This is bracketing, not reproduction.
A modern IBM Quantum rerun (Heron, Eagle) would strictly
strengthen the replication --- see Q2 in `open_questions.json`.

### 6. Shallow-circuit shortcut
Our HHL variant is 4 qubits, exploiting the Hadamard-diagonal
structure of the paper's specific $A$. This matches what the
paper's own hardware run did (ref. [49] problem-specific circuit),
so it is fair for reproducing C2/C3. But it is NOT the generic
HHL circuit, and it does not stress-test the QPE step for larger
or less-structured matrices. C5's resource count (6 qubits for
general 2x2, 19 for 4x4) is verified structurally, not by running
the general-purpose circuit.

### 7. Aaronson's "HHL fine print" is not exercised
The known theoretical caveats on HHL --- state-preparation cost,
condition-number dependence, tomography cost at readout ---
determine whether the asymptotic speedup translates to a real
speedup on real data. None of these are tested at this scale
(they cannot be on a $2\times 2$). The paper is honest about
this in its own limitations discussion but the replication should
be too. See Q4 in `open_questions.json`.

## Bottom line

**REPLICATED, but narrowly and honestly.** The paper's specific
empirical demonstration reproduces exactly under simulation, and the
hardware headline is bracketed by realistic noise models. The paper's
broader vision --- Bayesian deep learning at useful scale on quantum
hardware --- is neither confirmed nor refuted by this replication;
that vision was already understood in 2019 to be gated on the
Aaronson caveats and on hardware maturity, and it remains gated on
them today.

**What would flip this verdict:**
- If someone showed that our noiseless HHL 4-qubit implementation
  is a shortcut that does NOT generalize, we would soften to PARTIAL
  (currently: it demonstrably matches the paper's own primitive
  demonstration, which used a similar shortcut per ref. [49]).
- If a modern IBM Quantum rerun of the paper's exact protocol
  produced a fidelity substantially worse than our
  gate_noise=0.05 bracket (say F < 0.5), C4 would need to be
  re-graded rather than "bracketed and out of scope".
- If the noisy-sweep curve differed qualitatively from Fig. 1(a) ---
  non-monotone, or plateau at a different fidelity floor --- C3
  would drop. Currently it matches.
