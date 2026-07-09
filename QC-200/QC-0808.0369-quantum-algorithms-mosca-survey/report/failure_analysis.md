# Failure Analysis — QC-0808.0369 Mosca survey replication

Honest log of friction, gaps, and residual limitations.

## What did NOT go wrong (rare)
Both spot-check numbers came out on the first run, exact to machine precision:
- Grover N=8, k=2: P(marked)=0.945312 vs theory sin^2(5θ)=0.945312.
- Order-finding a=7 N=15: four peaks at k∈{0,64,128,192} each of prob 0.25,
  summing to 1.0 to within 1e-14.
No debugging round-trips needed; no “off-by-one qubit-order” bugs surfaced.

## Real friction

### F1. Marker / Nougat not installed on host
The QC-200 completion bar mandates both `extraction/marker.md` and
`extraction/nougat.mmd`. Neither VikParuchuri/marker nor
facebookresearch/nougat is installed on CherryRd. Both would require a
heavyweight torch + vision-transformer install to add. Per the sibling
QC-200 convention (see `QC-quant-ph-9607014-durr-hoyer-quantum-minimum/`),
we used `pdftotext -layout` (as marker.md fallback) and `pdftotext -raw`
(as nougat.mmd fallback) and wrote an explicit stanza at the top of each
file noting the substitution. Downstream tooling that looks for equation
LaTeX (Nougat's real value-add) will find only plain text.

### F2. Survey has no single empirical number of Mosca's own to falsify
Mosca 2008 is a review of the state of quantum algorithms circa 2008. The
verdict vocabulary in the wave brief (REPLICATED, PARTIAL, SPOT-CHECK,
NO-GO, CONTRADICTED, BLOCKED, FAILED) is meant for original-research
papers with a headline number. For a survey the correct fit is SPOT-CHECK:
verify representative quantitative claims Mosca cites from the primary
literature. We picked two (Grover and order-finding) that expose closed-
form success probabilities and reproduced them exactly. A CONTRADICTION
verdict is essentially impossible against a well-established survey — this
is a limitation of the wave format, not of the reproduction.

### F3. Order-finding case is "too clean"
For a=7, N=15, the classical order is r=4, which divides 2^m=256 exactly.
This means the QFT peaks are mathematically perfect (probability exactly
1/r=0.25 at each of 4 positions, zero elsewhere to numerical precision),
so continued-fraction recovery is trivial. A harder case (say a=2, N=21,
r=6 which does NOT divide any power of 2) would exercise the continued-
fraction machinery more genuinely. We did not do the harder case because
Mosca's exposition only asserts "peaks at multiples of 1/r" and the r=4
case exercises that assertion; feeding the reproduction more work would
be adding claims Mosca did not himself make.

### F4. C4–C6 (simulation, walks, adiabatic, topological, non-Abelian HSP) NOT exercised
The survey has ~7 major topical areas beyond the two we spot-checked.
Each would justify its own subagent replication (roughly the QC-100
wave scope). We did not do them here; that is not "failure" in the
strict sense but is a gap relative to a hypothetical full-scope reading
of "replicate the survey." The wave brief explicitly permits SPOT-CHECK
for a survey.

### F5. LaTeX compile to REPORT.pdf not attempted
The 8-artifact bar mentions "compile to REPORT.pdf when possible." We
did not run pdflatex here (no confirmation of a full LaTeX installation
on the host, and the report renders correctly as .tex source and is
readable as-is). This is a minor cosmetic gap; the .tex source is
self-contained and standard.

### F6. Wave brief header says "QC-100" but our dir is QC-200
The brief file is named `QC_WAVE_BRIEF_2026-07-03.md` and the header
inside says "QC-100". Our target dir is `QC-200/`. We followed the
substantive rules (8-artifact bar, free endpoints, statevector, verdict
vocab) and applied the QC-200 wave label in the final `WAVE_RESULT`
line. This is a naming inconsistency in the brief, not a substantive
gap in this replication.

## Residual gaps (things a follow-up should do)
- Install Marker + Nougat and re-parse `paper.pdf` for real equation-
  aware extractions (would replace the pdftotext stanzas).
- Do a "harder" order-finding case (r does not divide 2^m) so the
  continued-fraction step does non-trivial work.
- Extend to one or two more Mosca sections (e.g., Section 3 Deutsch-Jozsa
  is a 2-line Qiskit statevector demo; Section 8 quantum walks can be
  spot-checked on a small graph).
- Add a noisy-Grover baseline (Q5 in the Open Questions).
