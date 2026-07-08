# Failure Analysis — Honest Critique of the Replication

**Paper:** Roetteler, Naehrig, Svore, Lauter (2017), arXiv:1706.06752
**Verdict:** REPLICATED
**Set:** QC-100

This file is an intentionally honest inventory of what this replication does
*not* do, what could break the "REPLICATED" verdict on a stricter reading, and
where the pipeline has real weaknesses. It is not a summary of successes —
those live in `REPORT.md` / `REPORT.tex`. It exists so the record does not
overstate the strength of the reproduction.

---

## 1. What we did not do (scope limits)

### 1.1 We did not independently regenerate the resource-count formulas from a re-implemented circuit

The paper's headline numbers — the qubit count $9n + 2\lceil \log_2 n\rceil + 10$
and the Toffoli count $(448 \log_2 n + 4090) n^3$ — are analytical. We
**reconstruct** them by combining the paper's own Table~1 primitive counts
(modular inversion, Montgomery multiplication and squaring) per the composition
rule the authors state in Section~5.2 (Algorithm~1: $4\cdot\mathrm{inv} +
2\cdot\mathrm{squ} + 4\cdot\mathrm{mul}$, iterated $2n$ times).

We do **not** implement the reversible modular inversion, Montgomery
multiplication, or point-addition circuits from scratch, decompose them to
Toffoli$+$AND, and count Toffolis on the resulting reversible netlist. A
genuinely primitive-regenerative replication would build the controlled EC
point-addition circuit in Q\#, Qualtran, or Cirq, decompose to Toffoli, and
count independently — then compare not only the leading coefficient (224) but
also the subleading structure against Table~1.

**Impact on verdict.** The reconstruction we do perform is nontrivial —
it independently derives the exact leading coefficient 224 from the ratio of
the three primitive costs (`inv`:`squ`:`mul` = 32:16:16), which is a genuine
structural check that Table~1 is arithmetically consistent with the paper's
composition rule and Table~2's totals. But the primitives themselves are
accepted on the authors' authority. If Table~1 contained an off-by-a-log-factor
typo, we would not catch it.

### 1.2 The subleading regression coefficient $+2045 n^2$ is accepted on authority

The paper's per-point-addition Toffoli count is regressed as
$224 n^2 \log_2 n + 2045 n^2$. A naive sum of Table~1 subleading terms
($4\cdot(-13.2) + 2\cdot(-13.2) + 4\cdot(-13.2)\cdot n^2 = -158 n^2$) has the
wrong sign and magnitude. The paper (correctly) uses regression against
LIQUi$|\rangle$ simulation of the actual composed circuit rather than the
primitive sum.

We cannot re-run those LIQUi$|\rangle$ simulations — Microsoft never released
the F\# source in a reproducible form. Our closed-form-vs-Table-2 agreement
($\le 2.18\%$) is therefore **self-consistent with the paper's own regression
fit**, not an independent measurement of the $+2045 n^2$ constant.

**Impact on verdict.** If a genuine primitive re-implementation yielded a
different subleading term, our reconstruction would still match Table~2
(because we use the paper's fit), but the paper's underlying regression could
be wrong in a way we would fail to detect.

### 1.3 No comparison against alternative Shor-ECDLP decompositions in the same framework

We cross-check against Qualtran's implementation of Litinski~2023, which is a
**different algorithm** (windowed) implemented by a **different group** in a
**different framework**. The $\sim 170\times$ ratio confirms that (a) both
algorithms are in the same complexity class $\Theta(n^3 \log n)$ and (b) the
follow-on work's own advertised improvement is real. It does **not** validate
Roetteler's specific coefficients against, e.g.:

- H\"aner-Roetteler-Svore~2017 arithmetic variants (Toffoli-optimal multipliers).
- Gidney-Ekera~2019 windowed Montgomery techniques applied to ECDLP.
- Ekera-H\aa stad~2018 phase-estimation-reduction (which cuts the $2n$-iteration
  count by a factor of 2--3 at the cost of classical postprocessing).

A full triangulation across these three alternatives would either validate
Roetteler's $448 \log_2 n + 4090$ coefficient tightly or expose an anomaly.
We did not do this.

### 1.4 Error-correction overhead is entirely absent

Everything we report — and everything the paper reports — is **logical**.
Physical cost under a specific fault-tolerant code (surface code, lattice
surgery, or newer LDPC codes) multiplies logical Toffoli count by a
distillation factor of $10^2$--$10^4$ (depending on code distance, distillation
depth, target logical error) plus a routing factor of $O(1)$--$O(\log n)$.

For a policy-relevant answer to "how many physical qubits to break ECC-521?"
the logical Toffoli count is only a factor 3 to 5 in the final answer; the
remaining orders of magnitude come from FT overhead we did not compute.

**Impact on verdict.** None on the replication itself (the paper also does not
give FT overhead), but the practical bottom line is silent.

### 1.5 Toffoli depth and simulation-time columns of Table~2 were not tested

We reproduce columns 2 and 3 of Table~2 (qubits and Toffoli count). Column~4
(Toffoli depth) is empirically $\sim 0.917 \times$ the count and we did not
derive it independently. Column~5 (LIQUi$|\rangle$ simulation wall-clock time)
is not a claim about the quantum algorithm at all, but a wall-clock number for
a specific classical simulator on specific 2017 hardware — not meaningfully
replicable.

## 2. Where the pipeline has real weaknesses

### 2.1 The Qualtran cross-check runs on `mod=251`, not the actual NIST primes

`qualtran_symbolic.py` sets `mod=251` (a small odd prime) so the QROM
specializer can complete. This is fine for **cost** counting (window structure
and per-step Toffoli count depend on $n$ not on the specific $p$) but is not a
functional simulation of ECDLP over P-256. A stronger cross-check would run
Qualtran at the actual NIST primes; the QROM specializer has practical limits
at $n \ge 128$ and would need re-engineering.

### 2.2 `code/qualtran_crosscheck.py` fails at symbolic $n$

The "concrete-point attempt" fails on `ECAddR` QROM specialization at symbolic
$n$. We kept it for provenance but did not fix it. If Qualtran's `ECAddR` API
changes, our symbolic path may also break.

### 2.3 Table 2 CSV is manually transcribed

`data/roetteler_2017_table2.csv` was typed by hand from the paper's PDF.
Independent OCR (nougat / marker) was not run against the table. A cross-check
via nougat would catch typos. `extraction/nougat.mmd` is a stub, not a full
extraction.

### 2.4 We rely on a specific Qualtran version

Qualtran 0.7.0's `FindECCPrivateKey` API and cost decomposition are still
evolving. If a future version renumbers `.toffoli` vs `.and_bloq` or reweights
AND-cost, our numbers change. The version pin in `tool_versions.txt` mitigates
this but does not eliminate the fragility.

### 2.5 The reproducer does not check for numerical drift over Python / numpy versions

`analytic_reconstruction.py` uses `math.ceil(math.log2(n))`, which is exact
for the seven cryptographic $n$. If a future Python changes `math.log2` (very
unlikely) the qubit column could jitter. We did not add a hash-of-output check
in CI.

## 3. Modes of failure that would change the verdict

| Failure mode | If found, verdict becomes |
|---|---|
| Independent primitive re-implementation gives a different leading coefficient (not 224) | PARTIAL — paper's Section 5.2 derivation would be shown to be internally inconsistent |
| Independent primitive re-implementation gives leading coefficient 224 but a subleading term differing from $+2045 n^2$ by more than a factor 2 | Still REPLICATED (this replication) but the paper's fit would be flagged for review |
| Table 1's per-primitive counts turn out to contain a typo that changes a leading coefficient | REPLICATED (this reconstruction is consistent with the paper as-written) but with a flagged erratum |
| Qualtran's `FindECCPrivateKey` cost is discovered to be miscounting Toffolis | Cross-check C6 becomes NOT ESTABLISHED but core replication (C1, C2, C3, C5) unaffected |
| A different modern tool (Cirq-FT, tket, custom Rust) gives $10^{12}$ Toffoli for $n=256$ (an order of magnitude off Roetteler) | Would trigger a serious re-audit — currently no evidence for this |

## 4. Honest one-paragraph summary

The core replication result — reproducing Roetteler et al.'s qubit and Toffoli
formulas exactly on qubits and to $\sim 1\%$ on Toffoli, plus deriving the
leading coefficient 224 from the ratio of the paper's own primitive costs — is
real work on public materials in $\sim 250$ lines of Python. But the deepest
possible test (re-implementing the reversible circuits, counting Toffolis on
the resulting netlist, and cross-verifying the subleading regression constant
$+2045 n^2$) was not done. The Qualtran cross-check is a sanity check across a
follow-on algorithm, not a direct verification of Roetteler's own numbers. The
REPLICATED verdict is legitimate at the level the paper's own deliverable
operates (analytical resource counts + Table 2) and it should not be read as
"the underlying reversible arithmetic has been re-audited from scratch."
