# Failure Analysis — What Didn't Work, Friction, Residual Gaps

## Actual failures encountered

### F1. Marker install failed on Python 3.14
```
pip install --quiet marker-pdf
→ Encountered error while generating package metadata.
  └─> numpy (upstream numpy metadata build error)
```
Root cause: Marker's transitive dependency on `numpy` (via `torch` /
`transformers`) tries to build from source under Python 3.14, which is
newer than most of Marker's pinned-metadata releases support (Marker
tracks CPython 3.10–3.12 in its wheels). Repro environment is macOS
Homebrew Python 3.14.6 — bleeding-edge; would work under a `pyenv`
3.11 or 3.12 pin.

**Mitigation applied:** produced `extraction/marker.md` from Poppler
`pdftotext` output with an explicit HTML-comment header noting the
fallback. Downstream tooling that greps `extraction/*.md` for token
sequences will still work; anything doing math-mode LaTeX
reconstruction will not. Not on the critical path for this replication.

### F2. Nougat install skipped (heavy)
Nougat requires downloading a ~1.4 GB transformer checkpoint plus a
non-trivial torch stack. Given the QC-100 wave time budget (target
~90 min end-to-end) and the observation that Marker was already
non-installable on this Python version, we did not attempt Nougat.

**Mitigation applied:** produced `extraction/nougat.mmd` from Poppler
`pdftotext -layout` (preserves 2-column and inline-math spacing best of
the CLI tools available) with an explicit comment header noting the
fallback.

### F3. Tesseract OCR fallback crashed on PDF rasterisation
```
ocr__ocr_pdf(..., engine=tesseract, pages=1-12, dpi=200)
→ every page returned UnicodeDecodeError: 'utf-8' codec can't decode
  byte 0x89 in position 270: invalid start byte
```
Not diagnosed further — the same PDF `pdftotext`-s cleanly, so the OCR
route wasn't needed. Byte 0x89 is the PNG magic, suggesting the OCR
pipeline was trying to run Tesseract on the intermediate raster PNG
bytes rather than on the text. Environment-specific tooling bug;
noted for the wave-lead but not blocking this replication.

### F4. Argo `argo:claude-opus-4.8` returned schema error on structured system+user prompt
```
argo:claude-opus-4.8 → {"error":"Failed to parse upstream response:
    1 validation error(s): Value at 'choices[0].message' does not match
    any variant of SystemMessage | UserMessage | AssistantMessage | ToolMessage"}
```
Likely an Argo proxy version issue where the Anthropic-style upstream
response includes a field the proxy's pydantic model doesn't yet
accept. Retried with `argo:gpt-5.2` — worked immediately.

## Bugs I hit in my own code and fixed

### B1. Wrong hidden-subgroup lattice condition for dihedral HSP
First-attempt `dihedral_hsp.py` assumed the linearised subgroup
`K = <(1,d)>` was always of order 2 in `Z_2 × Z_n`. It is not: order
`(1,d) = lcm(2, n/gcd(d,n))`, which is `> 2` unless `2d ≡ 0 (mod n)`.
This produced wrong "on-lattice mass < 1" outputs at odd `n` and made
me realise the reduction is *not* generic for cyclic `N` — which then
led me to correctly re-target Theorem 13's actual hypothesis
(elementary abelian 2-group `N`) in `ims_theorem13.py`. Kept the
buggy-in-name dihedral file as an intentional negative control.

### B2. JSON serialisation of numpy `int8` in output
`json.dumps` refused numpy dtypes. Added a `_clean()` recursion that
converts `np.integer / np.floating / np.ndarray` to native types. Not
research-relevant, but noted.

## Residual gaps (what a v2 replication should add)

### G1. Theorem 8 / Theorem 11 not reproduced
Only Theorem 13 (§6) was reproduced. Theorems 8 (normal HSP in
solvable/permutation groups) and 11 (small commutator subgroup) would
each require:
- (Theorem 8) implementing enough of Beals-Babai to compute a
  composition series of a solvable black-box group — a substantial
  side-project.
- (Theorem 11) enumerating the commutator subgroup and doing an outer
  Abelian-HSP loop of length `|G'|`.

Both are within statevector-simulation reach at small sizes, but each
is a ~day of engineering, not compatible with a 90-min QC-100 wave.

### G2. Non-cyclic G/N branch of Theorem 13 untested
The paper's Theorem 13 covers both `G/N` cyclic (poly-time) and `G/N`
small (poly-time in `input + |G/N|`). We tested only the cyclic side
(`G/N = Z_2`, so `|V| = 1`). Non-cyclic `G/N` would exercise the
`|V|`-loop of Abelian-HSP subproblems that the paper describes — worth
adding in a follow-on. See Open Question Q1.

### G3. No sample-complexity vs. |H| scan
All 15 instances used `|H| = 2`. The empirical
`samples-to-full-recovery ≈ (k+1)` we measured is not a stress test of
the recovery-cost bound in `|H|`. See Open Question Q2.

### G4. Reduction implemented via density-matrix trace, not full |G>|f(g)> statevector
For pedagogical clarity and speed, `coset_state_density` builds
`ρ = MM†` on the group register directly, effectively assuming the
oracle-value register is measured / traced out. A "fully coherent"
version would prepare `1/√|G| Σ|g>|f(g)>` in a `⌈log|G|⌉ + ⌈log|Σ|⌉`
qubit state and let Qiskit-Aer's statevector simulator do the partial
trace. Not needed for correctness but a nicer showcase of the tool.

### G5. No noise / decoherence model
Everything ran on a noiseless statevector. The paper is purely
BQP-theoretical, so noise is out of scope; but a natural follow-on for
QC-100 is to check how fragile the 100 %-on-`K^⊥` result is under a
depolarising-error `H`-gate stack.

## What worked really well
- Recognising during the dihedral-negative-control run that the
  `2d ≡ 0 (mod n)` condition *is* the paper's "elementary abelian 2"
  hypothesis in disguise, and immediately pivoting to `F_2^k`. Saved
  probably 60 min of wrong-direction debugging.
- Keeping the buggy dihedral run as an intentional **negative control**
  in `dihedral_hsp_results.json` — it's now the strongest empirical
  argument in this replication for *why* the paper needs its specific
  hypothesis.
- Statevector-in-numpy (no Qiskit `Statevector` needed) at n≤7 qubits:
  15-instance sweep runs in **0.05 s** wall time. Extremely easy to
  extend.
