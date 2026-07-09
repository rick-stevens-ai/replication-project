# Failure analysis — OSTI 2887218 replication

## Executive summary

**No verdict-changing failures.**  Four correctness bugs were caught and fixed *before* running the final experiment, thanks to a hard convergence check (Alg 1 at ℓ = max weight *must* equal the exact Kraus simulation to machine precision).  This section documents each bug because they are all pitfalls likely to recur in any Pauli-path-truncation replication.

## Bug B1 — Remote process orphaning

**Symptom.**  I killed my SSH-launched python job via `process kill`, but a subsequent `ps -ef` on uicgpu showed the python still running.

**Root cause.**  `process kill` on a `ssh <host> '<cmd>'` session only kills the local SSH driver; the remote shell + python child do NOT receive SIGHUP because Tailscale-mediated SSH keeps a pty open.

**Fix.**  After every `process kill` on an SSH-launched remote job: `ssh <host> 'ps -ef | grep <script>' && ssh <host> 'kill -9 <remote-pid>'`.

**Prevention.**  For long remote jobs, launch with a wrapper that writes remote PID to a file (`echo $$ > /tmp/pidfile; exec python …`) or use nohup + tracked PID list.

## Bug B2 — Kraus depolarizing rescaling (THE big one)

**Symptom.**  Algorithm 1 at ℓ = max weight (all Pauli paths kept, no truncation) did NOT equal the exact Kraus expectation.  Residual error ≈ 8 % of the true value at γ = 0.05, shrinking to ~0.5 % at γ = 0.8.  The pattern (larger discrepancy at smaller γ) was itself a clue — it pointed to a channel-strength convention mismatch.

**Root cause.**  The paper's local depolarizing channel is `D(ρ) = e^{-γ} ρ + (1 − e^{-γ}) tr(ρ) I / 2`.  This form gives eigenvalue `e^{-γ}` on non-identity Pauli operators (the essential property that makes the paper's `e^{-γ·w}` damping true).  My first pass used the standard Kraus form `(1 − p) ρ + (p/3)(X ρ X + Y ρ Y + Z ρ Z)` with `p = 1 − e^{-γ}`.  This gives eigenvalue `1 − 4p/3 = 1 − 4(1−e^{-γ})/3 ≠ e^{-γ}` on non-identity Paulis, off by a systematic factor.

**Fix.**  `q = (3/4) · (1 − e^{-γ})` is the correct Kraus parameter to match the paper.

**How I found it.**  Wrote an independent Schrödinger-in-Pauli-basis simulator (`dev_schrod_pauli.py`).  It disagreed with `exact_expectation` (Kraus dense).  Since Pauli-basis Schrödinger evolution is *manifestly* equivalent to Kraus for the correct channel, the disagreement pointed straight at the Kraus rescaling.

**Prevention.**  ANY Pauli-path replication should include a `Alg1(ℓ = ℓ_max) == exact` unit test before running any figure.  Failure to converge at ℓ_max = *any bug*.

**Wider impact.**  This convention drift is likely responsible for a fraction of the numerical disagreements between Pauli-path papers in the literature.  Filed as Open Question Q3.

## Bug B3 — Transition-amplitude direction (transposed table)

**Symptom.**  Corrected Kraus rescaling still gave the wrong answer at ℓ = ℓ_max (before B4 was found).

**Root cause.**  Paper defines `a_{PQ} = (1/2^n) tr(Q U† P U)` — this is the Pauli decomposition of `U† P U` (Heisenberg-evolved P as an operator).  My first table computed `(1/4) tr(P_b U P_a U†)` — the Pauli decomposition of `U P_a U†` (Schrödinger-evolved P as an operator).  These are *transposes* of each other — same magnitudes, but different row/column orientation.

**Fix.**  Compute `Udag @ P_in @ U` instead of `U @ P_in @ Udag`.

## Bug B4 — Layer time-ordering direction

**Symptom.**  Related to B3.  Even with correct transition amplitudes, the DP was evolving layers in the wrong time-order for a Heisenberg-picture algorithm.

**Root cause.**  Paper explicitly says "t = 1..d indexes the circuit layers in reverse order" — the paper's `layer 1` is nearest the observable in Heisenberg picture, which is the LAST layer in Schrödinger picture.  My `layers[0]` was the FIRST Schrödinger layer.

**Fix.**  In Algorithm 1's DP, iterate `for layer in reversed(layers)`.

**How I convinced myself of the fix.**  For a *fully symmetric* n = 2, d = 1 test at γ = 0, both directions give identical results (only one layer!), which is why my min_verify test initially passed even with wrong ordering.  Only the n ≥ 3, d ≥ 2 tests exposed the ordering bug.

## Anti-patterns caught (and documented for next time)

1. **Trusting a single ℓ-value test.**  My initial "converged at ℓ = max" test used ℓ = n·(d+1) — the tight upper bound.  But my Alg 1 also saturated at ℓ = n·⌈(d+1)/2⌉ = 10 for n = 4, d = 3, because destructive interference kills higher-weight contributions.  Always test convergence via a *sweep* over ℓ.
2. **`process kill` illusion.**  See B1.
3. **Depolarizing-channel convention ambiguity.**  See B2.  Always cite which of `p = 1 − e^{-γ}` vs `p = (3/4)(1 − e^{-γ})` is being used, since both are common.
4. **Ignoring the theorist's index convention.**  See B4.  Read the paper's index convention paragraph twice; time-reverse indexing is standard in Heisenberg-picture algorithms and easy to miss.

## What would have made this replication easier

- **A code repository.**  The paper has none.  Even a 20-line reference implementation would have saved 45 minutes of debugging convention issues.
- **An explicit ℓ = max sanity check in the paper.**  This would have flagged our Kraus mistake in one line.
- **Numerical figures.**  With no figures in the paper, a reproducer has to invent their own workload, choose meaningful (γ, ℓ, n) regimes, and prove they cover the paper's claim — all extra work.
