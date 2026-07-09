# Failure analysis — Poremba 2022 replication

Honest catalogue of what did NOT work, what was worked around, and the
residual gaps between this replication and the paper's full claims.

## Blockers we hit and worked around

### 1. Primal Gaussian state is unsimulable at any realistic parameters
Poremba's `Enc` requires preparing the primal Gaussian state
$\lvert\psi_y\rangle = \sum_{s,e}\varrho_{q/\sigma}(e)\omega_q^{-\langle s,y\rangle}\lvert sA{+}e\rangle$
on $(m{+}1)$ qudits of dimension $q$. At the wave-brief's $q{=}257, m{=}128$
this is a superposition over $\mathbb{Z}_q^{m+1} = 257^{129} \approx 4\cdot 10^{310}$
basis states. No CPU or GPU statevector simulator on Earth can hold it.

**Workaround:** we do NOT simulate the full primal Gaussian state. Instead
we (i) note that the paper's Lemma 17 proves the comp-basis measurement of
$\lvert CT\rangle$ has the classical Dual-Regev distribution, so we simulate
that distribution directly at full $(n,q,m)$ resolution (test (a) — REAL);
and (ii) implement the BB84 precursor that Poremba §1 cites as the source
of his complementarity-based deletion idea, at 17 qubits (tests (b)-(e) —
REAL for the BB84 primitive, STAND-IN for the full qudit primal Gaussian).

This is honestly captured in `REPORT.tex` §3.2 and `workflow.md`.

### 2. Empty concrete parameter window for the noise ratio
The paper's constraint $\sqrt{8(m{+}1)}\le 1/\alpha \le q/\sqrt{8(m{+}1)}$
at $q{=}257, m{=}128$ gives $32.12 \le 1/\alpha \le 8.00$ — empty.

**Workaround:** we honored the wave brief's $\sigma_{\mathrm{enc}} = 3.2$
(consistent with the smaller end of the ratio window) and logged the
effective $\alpha_{\mathrm{eff}} \approx 0.0176$. Decryption still works
at rate 1.000 because $\|e\|_\infty \ll q/4$ empirically. But this is a
concrete-parameter tension in the paper that a formal replication should
call out (Open Question 1).

### 3. Marker-pdf and Nougat both uninstallable
- `marker-pdf` 0.2.6: `TypeError: Invalid input type 'PdfDocument'` at
  `pdftext.extraction._load_pdf` on Darwin 25 + `pypdfium2 4.30.0`.
  Not fixable without patching pdftext or downgrading pypdfium2 by 2 majors.
- `nougat` (facebookresearch): pins `transformers==4.28.1` + `torch<2.1`,
  requires building `torchvision` from source, blocked by MacOSX 26 SDK.
  Not installable in reasonable time on m1 CherryRd.

**Workaround:** honest surrogates via `pdftotext -layout` + explanatory
headers + `extraction/README.md`. This mirrors the sibling QC-200
replication `QC-quant-ph-9709029-entanglement-formation-two-qubits-wootters/`,
which hit the same wall.

## Bug caught mid-run
- Initial `lwe_bb84_full.py` had the deletion basis inverted (measured in
  `1-theta` per qubit instead of all-Hadamard). This produced accept rate
  0.01 instead of the correct 1.0 on the first run. Traced back to a
  misreading of the BB84 primitive: honest Del should measure all qubits
  in the SAME basis (Hadamard), not the complementary basis per qubit.
  Fix committed after one iteration; second run yielded 1.000 as expected.

## What is NOT reproduced (out of scope)

| Claim | Why not |
|---|---|
| IND-CPA security under decisional LWE (Thm 5) | Asymptotic, non-empirical. No small-parameter counterexample search attempted. |
| Certified-deletion security under strong Gaussian-collapsing (Thm 6) | Asymptotic + rests on a new assumption (§5.2). No empirical test attempted. |
| (Leveled) FHE extension (§9) | Would require ~1000 additional lines: Mahadev-style FHE compiler + bootstrapping. Deferred to a possible followup (Open Question 5). |
| Fourier-basis Vrfy on the actual primal Gaussian state | Unsimulable at qudit resolution (see Blocker 1). The BB84 stand-in captures the qualitative and 1-bit-granularity quantitative behavior. |

## Residual risks / caveats
- Our test (e) cheater model is one of the two natural adversary strategies
  from BI20; there are more sophisticated coherent adversaries (e.g.,
  measuring in a superposition of bases via an ancilla) that a full
  security-level replication would need to sweep. We do not do this.
- The BB84 stand-in encodes 1 bit per LWE-ciphertext coordinate, whereas
  the paper's qudit register encodes $\log_2 q$ bits per coordinate. The
  cheater exponent $(1/2)^k$ observed here would be $(1/q)^k$ at full
  qudit resolution — the security-margin numbers do NOT transfer 1:1.

## Confidence in the verdict
High for the primitive-level functional claims (test (a)–(e) all pass with
clean numbers matching theory). Low for anything asymptotic. The `REPLICATED`
label is scoped to "the paper's small-parameter Construction 1 functional
properties" and NOT to "the paper's security theorems".
