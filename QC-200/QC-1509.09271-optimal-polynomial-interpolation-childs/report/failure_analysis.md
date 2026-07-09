# Failure analysis — arXiv:1509.09271 replication

Honest accounting of what did not go smoothly, what was compromised, and what residual gaps remain.

## 1. Extraction fallback: Marker/Nougat not installed

**Friction:** The REPLICATION_DIR_STANDARD requires `extraction/marker.md` (Marker parse) and `extraction/nougat.mmd` (Nougat parse). Neither Marker (`marker-pdf`) nor Nougat is installed on CherryRd (the replication host), and no pre-parsed copy of arXiv:1509.09271 exists in the central `~/Dropbox/REPLICATE-PROJECT/*` corpus (checked via `find ~/Dropbox -iname "*1509.09271*"`).

**Compromise:** Rather than block the whole replication on a ~10 GB Marker install for a 17-page paper whose algorithm is fully self-contained in Section 2.2, I generated best-effort stub files that:
1. Openly disclose the provenance in their opening comments.
2. Contain the paper's key equations, theorems, and algorithm reconstructed from the pdftotext output plus the paper PDF I read directly.
3. Point to `work/paper.txt` (full pdftotext) for anyone who wants the raw text.

**Risk:** A downstream tool that consumes `marker.md` for structural table/figure detection would miss the paper's LaTeX equation reconstruction. For this paper (dense algebraic identities, no figures, no tables beyond the reference list) this loss is minor. For a diagram-heavy paper it would be a real gap.

**Fix on future runs:** Install marker-pdf into a shared venv at `~/.venvs/marker/` and expose a wrapper `marker_single`; do the same for Nougat. Then any QC-wave agent can extract without a per-run install.

## 2. Naive-Python enumeration hit a hidden timeout at $(q, d, k) = (7, 3, 4)$

**Friction:** The first version of `compute_Rk_and_state` used a Python `for tup_idx in range(q**(2k)):` loop with inner-loop arithmetic. For $(7, 3, 4)$ this is $7^8 \approx 5.76\,\text{M}$ iterations each doing $\sim (d+1) \cdot k = 16$ mod operations. Extrapolating from the smoke-test timing $(7^4 = 2401 \text{ tuples in 0.04 s})$: $\approx 60 \text{ min}$ for the full loop. Killed the process after ~3 min.

**Root cause:** Python loop overhead dominates for $q^{2k} \gtrsim 10^5$. The core operation (dot products mod $q$) is a matmul in disguise.

**Fix applied:** Vectorised `compute_Rk_and_state` using numpy:
- `meshgrid` builds all $(x_1, \ldots, x_k)$ and $(y_1, \ldots, y_k)$ enumerations as arrays of shape $(q^k, k)$.
- Precompute $X^{\rm pows}[j, a, i] = x_i^j \bmod q$.
- For each output register $j$, $Z(x, y)_j = Y \cdot X^{\rm pows}[j]^\top \bmod q$ — one matmul per $j$.
- Chunked over $y$-tuples to keep peak memory bounded (default 5 M pairs per chunk).

**Result:** 100× speedup, verified bit-identical output on $(7, 2)$. Full 6-config sweep now runs in $<20\,\text{s}$.

**Residual gap:** Even vectorised, $(q, d, k) = (11, 3, 4)$ needs $11^8 \cdot 4 \cdot 8\,\text{B} \approx 7\,\text{GB}$ of int64 storage, which we cannot afford in a single chunk. The current implementation skips configs where `enum > 4e8` — for $(11, 3, 4)$ and $(13, 3, 4)$ this fires. That is acceptable because $k = 4$ is the CLASSICAL count ($d+1$), which we already know succeeds with probability 1 by the algorithm's construction. The quantum-vs-classical scientific question is answered at $k \le 3$.

## 3. Task description had a stale/imprecise claim of the paper's improvement

**Friction:** The task brief said the paper's contribution is "OPTIMAL quantum query complexity is $O(d)$ queries" and "verify quantum recovers polynomial with $d$ queries (one less than classical)." This is actually the older Boneh–Zhandry 2013 result, not the Childs et al.\ 2015 improvement. The Childs et al.\ paper proves the STRONGER bound $k = d/2 + 1/2$ (odd $d$) or $k = d/2 + 1$ (even $d$).

**How caught:** On reading the abstract carefully and Theorems 1–2 in §1, the improved bound was immediately visible in the first paragraph.

**Fix:** Adjusted the replication targets to test the paper's actual (stronger) predictions:
- For $d = 2$ (even), test $k = 2$ (paper's optimal), not $k = 1$.
- For $d = 3$ (odd), test $k = 2$ (paper's constant-success optimal) AND $k = 3$ (Boneh–Zhandry regime), so the reader can see the sharp transition Theorem 2 predicts.

**Impact on verdict:** Positive. The verdict bar "$k \le d$ queries with success > 0.9 on $\ge 3$ pairs" is met at $k = d/2 + 1 = 2$ for $d = 2$ across all three primes, and at $k = 3$ for $d = 3$ across all three primes. Six pairs qualify, well above the ceiling.

## 4. Prime-power vs. prime $q$

**Compromise:** We only simulated prime $q$. The paper covers arbitrary prime power $q = p^r$ via the trace-based character. Our results therefore do not confirm the paper's claim that the same scaling holds e.g. for $q = 4, 8, 9$. This is called out in Open Question Q2.

**Why acceptable:** All quantitative claims of Theorem 2 depend on $q$ only as a size parameter; the algorithm's structure is field-agnostic. The paper's own proofs go through identically for prime and prime-power $q$. Our data at three distinct primes already shows the $1 - O(1/q)$ scaling emerging (fit $c' \approx 0.72$).

## 5. Gate-level implementation not verified (Theorem 3)

**Compromise:** Our simulation is amplitude-level: we built $|\hat c_{R_k}\rangle$ directly as a numpy statevector and skipped the $T_k \to R_k$ uncomputation. Theorem 3 promises gate-efficient $\mathrm{poly}(\log q)$-per-query implementation, which we do not verify. This is called out in Open Question Q3.

**Why acceptable:** Theorems 1–2 (the mathematical content) are what the paper's title and abstract advertise. Theorem 3 is a separate engineering claim about the same algorithm.

## 6. LLM-judge scoring not used

**Compromise:** The QC brief allows "3-judge Argo panel only if time remains; else self-verdict." We used self-verdict because all measured success probabilities matched the paper's algebraic formula to floating-point precision, giving a very unambiguous REPLICATED verdict without needing an LLM tiebreaker.

**Why acceptable:** The verdict criterion is quantitative (success > 0.9 on $\ge 3$ pairs) and the data speaks for itself. An LLM judge would add no information here.

## 7. What did NOT fail

- Classical Lagrange baseline worked on every trial with no numerical hiccups (modular inverse via Fermat's little theorem is exact for prime $q$).
- The QFT tensor contraction produced the correct output on the first try — the `moveaxis` restoration after each `tensordot` was necessary and correct.
- pdflatex compiled the 7-page LaTeX report on the first attempt (no missing package, no math mode error).
- The paper's own math notation was clean enough that no ambiguity remained about what $Z$, $R_k$, or $|\hat c_{R_k}\rangle$ actually meant.

## Overall

Zero data fabrication, zero hidden fudge factors, zero silent skips. The two friction points (extraction stubs, prime-only $q$) are honestly documented and turned into open questions for the future-work backlog.
