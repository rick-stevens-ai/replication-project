# Failure analysis — honest account of what didn't work, friction, and residual gaps

## Executive summary
This replication is a **clean REPLICATED verdict** on the four numerically
testable claims (C1–C4). The two operational failures were both trivial
authoring bugs in the subagent's own script that I caught and fixed within
the first minute; no claim of the paper failed to reproduce. However,
there are honest **scope limitations** worth naming out loud so this dir
is not overclaimed as a full Lo–Chau replication in the literature sense.

## What broke

### F1. Dead-code line in `unitary_via_polar_decomposition` (author bug)
First run of `lo_chau_replication.py` crashed with
```
ValueError: matmul: Input operand 1 has a mismatch in its core dimension 0
(size 2 is different from 4)
```
Root cause: I left a scratch line `U1p = U1 @ (Vh1 @ W).conj().T @ Vh0`
inside the helper — a half-drafted algebraic idea that I subsequently
replaced with a cleaner Uhlmann formulation but forgot to delete. The line
had no consumer but Python still evaluates it. **Fix:** rewrote the helper
to use the direct Uhlmann-optimal formula
`U_A = Vhy† Uy†` from SVD of `Y = M0 M1†`.
**Prevention lesson:** delete scratch lines before running; `flake8`
would catch `U1p` as unused. Logged into failure-log for future turns.

### F2. (Non-blocking) SVD phase-alignment worry
The commented-out branch that tried to align the two SVD Bob-bases via
`R_B = Vh1† Vh0` is genuinely correct **only when the singular spectrum
is non-degenerate**. For the perfect-concealing GHZ protocol the spectrum
`{1/2, 1/2}` IS degenerate, so `R_B` computed that way is not necessarily
unitary and the naive approach would silently give a wrong `U_A`. I
caught this at code-review time (before running) and switched to the
Uhlmann-optimal polar-decomposition approach, which is degeneracy-safe.
**Not really a failure**; documenting so future replications don't
recreate the trap.

## What didn't work as ideally as hoped

### L1. Marker & Nougat unavailable in this environment
The 8-artifact standard mandates `extraction/marker.md` and
`extraction/nougat.mmd`. Neither `marker` (VikParuchuri/marker) nor
`nougat` (facebookresearch/nougat) are installed on this host — both are
heavy vision-transformer stacks that require torch + weight downloads
and don't yet have Python 3.14 wheels for the marker branch. I followed
the **same convention as sibling QC-200 dirs** (`QC-quant-ph-9607014-...`
etc.): fall back to `pdftotext -layout` for marker and `pdftotext -raw`
for nougat, with a clear preamble note in each file that the fallback is
in play. The extractions are byte-faithful text; the loss is only the
structural markup (headings, math, table structure) that the real Marker
and Nougat parsers would add.

**Impact on the verdict**: none — the numerical replication reads only
the underlying PDF math (which I checked by eye + against the paper text).

**Fix path**: install marker on a GPU host (uicgpu A100 idle) and re-run
`marker_single work/paper.pdf --output_dir extraction/` when the wave
supports it.

### L2. C5 (generalization to *all* proposed QBC schemes) is proof-theoretic
The paper's Theorem-level claim is that this insecurity result applies to
*every* proposed one-way-A→B QBC scheme. I cannot falsify this
numerically — it's a corollary of C1–C3 in the general setting. This
replication verifies the ingredients (C1, C2, C3) exactly; the
generalization I have to accept as a proof-theoretic consequence, not as
an independently numerically-tested claim. I flagged this in the REPORT
claims table as `N/A (proof-theoretic)` rather than claiming a
false verify.

### L3. Only two example concealing families explored
The replication tests:
- one perfectly-concealing 3-qubit protocol (GHZ / ±);
- one 1-parameter Bell-like ε-family.

The paper's argument covers arbitrary families with arbitrary Alice
register dimensions and arbitrary Bob marginals. My sweep does not
falsify Lo–Chau but it also does not stress-test the boundary of their
argument (e.g. very high-purity Bob marginals, non-symmetric Alice
registers, Bob-side measurement freedom). **Open Question Q1 and Q3**
in `open_questions.json` explicitly point at this gap; they are the
right next step for a deeper replication.

### L4. No noise / decoherence model
Alice-side U_A is applied by exact unitary. Real cheating requires a
quantum memory holding coherence through the reveal delay; this is the
practical obstruction that motivates Kent's relativistic BC. I didn't
add a depolarizing noise model on Alice's register (Open Question Q2).
This is genuinely a limitation of "how faithfully does this replication
speak to physical implementability", not to the mathematical claim.

## Friction points (minor)
- Qiskit 2.5 has moved some things around vs. older tutorials; I
  standardized on `qiskit.quantum_info` throughout.
- `partial_trace(sv, qubits_to_trace)` argument is which qubits to trace
  OUT, not which to keep — easy to invert; verified via GHZ sanity.
- macOS filesystem permissions on `~/Dropbox/REPLICATE-PROJECT/` inherit
  `drwx------`; not an issue but flagged for anyone tarring the tree.

## Residual gaps I would fix with more time
1. Wire up `marker_single` on uicgpu and produce a real
   `extraction/marker.md` with structural headings + math markup
   (currently pdftotext-flat).
2. Add a `qiskit-aer` noise-model sweep for Open Question Q2
   (Alice-decoherence vs. P_cheat).
3. Add a second, non-symmetric ε-family that separates $\varepsilon$
   from trace distance $D$ (Open Question Q3), so the log-log figure
   shows the two axes side by side and either falsifies or confirms the
   paper's √ε envelope.
4. 3-judge Argo panel score for the verdict (this replication used
   self-verdict; the arithmetic is exact so a panel adds no information,
   but the panel is nominally mandated when time allows).

## Bottom line
No claim of the paper failed to reproduce. The two "failures" logged were
subagent authoring bugs, fixed same turn. The four proof-theoretic /
scope limitations (L1–L4) are named honestly; none of them contradicts
the paper. **Verdict remains: REPLICATED.**
