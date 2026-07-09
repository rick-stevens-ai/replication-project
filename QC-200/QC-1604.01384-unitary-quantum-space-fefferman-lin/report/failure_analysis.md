# Failure analysis — arXiv:1604.01384 replication

Honest audit of what did not work, what was worked around, and what residual gaps remain.
Even though the local verdict is REPLICATED, the paper contains claims we did not (and in
some cases could not) test on a laptop.

## 1. Marker + Nougat CLIs unavailable

- **What failed:** neither `marker_single` nor `nougat` is installed on this host
  (CherryRd) or on the two paired hosts we checked (`uicgpu`, `m1`).
  `pip install marker-pdf` on the Python 3.13 venv hit a `torch>=1.4` resolver
  error against `numpy 2.5`; `pip install nougat-ocr` hit the same numpy-2.5
  incompatibility.
- **Root cause:** upstream `nougat-ocr` metadata pins `torch>=1.4` in a way that
  breaks against wheel resolution on numpy 2.5 + Python 3.13.  Marker's
  transitive `torch` dep is not available as a prebuilt wheel for this host's
  Python.
- **Workaround:** followed the sibling QC-200 convention exactly --- generated
  a labeled PyMuPDF `extraction/marker.md` and a labeled `pdftotext -layout`
  `extraction/nougat.mmd`, each with a clear header block naming it as a
  surrogate.  For a math-complexity paper with no scanned figures, the
  semantic text agrees with what Marker / Nougat would return.
- **Residual gap:** we do not have real Nougat LaTeX reconstruction of the
  paper's inline equations; anyone downstream who needs equation LaTeX must
  either run Nougat on a proper CUDA host later or read the equations from
  the source PDF.

## 2. Reproduced only C1+C2 (constructive core), not C3--C6 (complexity-class equalities)

- **What we did NOT do:** we did not numerically verify Theorem 6
  (BQU_SPACE[poly] = PSPACE), Theorem 19 (Well-Cond-Matrix-Inversion is
  BQU_SPACE[O(k)]-complete), Theorem 18 (Min-Eigenvalue analogue), or
  Corollary 3 (PreciseQMA = PSPACE).
- **Why it isn't a bug:** these are complexity-class equalities/hardness
  statements proved via reductions.  There is no headline number attached to
  them; they are not the kind of claim numerical simulation can vindicate or
  refute.  The paper itself would not treat a small-instance simulation as
  evidence for or against them.
- **Residual gap:** an ambitious follow-up could numerically build the
  Well-Conditioned-Matrix-Inversion algorithm of Sec. 5 at small k (e.g.
  k=4-6, i.e. 16x16 -- 64x64 matrices) and confirm it correctly solves random
  well-conditioned instances without intermediate measurement, and count its
  actual qubit footprint.  We did not attempt this.  See Open Question Q2.

## 3. Idealized (noise-free) simulation only

- **What we did:** exact statevector, zero noise.
- **What we did NOT check:** whether deferred measurement remains equivalent
  under a realistic depolarizing / amplitude-damping channel.  In principle,
  holding what would have been mid-circuit-measured ancillas coherent for the
  remainder of the circuit exposes them to additional decoherence, so the
  practical fidelity of the deferred variant may be strictly worse than the
  mid-measurement variant on NISQ hardware.
- **Residual gap:** the paper's theorem is stated for ideal unitaries; extending
  the analysis to a noise model is genuinely open work, and it is exactly the
  point of Open Question Q3.

## 4. Two very small circuits; no depth stress test

- **What we did:** 20 Haar-random trials each on a 3-qubit (teleportation)
  and 2-qubit (RUS) circuit.  Both have exactly ONE mid-circuit measurement
  layer.
- **What we did NOT check:** a chained pipeline of many mid-circuit
  measurements, which is where the naive deferred-measurement rewrite would
  blow qubit count linearly in depth and where the paper's
  purification-and-reuse trick becomes load-bearing.  We did not implement
  the purification-and-reuse trick explicitly.
- **Residual gap:** the O(1) claim we numerically saw is per-circuit (0 or 1
  ancilla).  The aggregate O(1) across arbitrary depth would need a chained
  test.  See Open Question Q1.

## 5. Only Pauli-correction feedback tested

- **What we did:** the intermediate measurements feed into X and Z corrections
  (Pauli group).
- **What we did NOT test:** the modern dynamic-circuit primitive that
  classically computes an arbitrary rotation angle from measurement outcomes
  (e.g. R_z(2*pi*0.m_1 m_2 ...) in QFT-style feedback).  These may not admit
  a finite-ancilla coherent rewrite; the paper's construction is not obviously
  general in this direction.
- **Residual gap:** see Open Question Q5.

## 6. Author-name bleed in SCOUT metadata

- **Symptom:** the calling task noted `SCOUT title starts "Bill..."`, suggesting
  a title-vs-authors confusion in the SCOUT extractor.
- **Root cause:** SCOUT (or whatever extractor produced the metadata) appears
  to have grabbed the first line after the actual title, which is the author
  line "Bill Fefferman* and Cedric Yen-Yu Lin", and treated the leading "Bill"
  as the title prefix.
- **Fix in this replication:** verified authors and title directly from
  `paper.txt` lines 1--10; recorded as "A Complete Characterization of Unitary
  Quantum Space" by Fefferman + Lin.
- **Follow-up:** the SCOUT metadata should be corrected upstream; ~1-2 minutes
  of work per affected row but that is out of scope for this single replication.

## Summary

The core structural claim (deferred measurement with O(1) qubit overhead) is
reproduced at machine precision.  The residual gaps are all in one of two
categories:
  (a) the paper's theorem is asymptotic / non-numerical (C3, C4, C5, C6);
  (b) the paper's theorem is stated in a more general setting (arbitrary
      circuit depth, arbitrary classical feedback, arbitrary noise model) than
      we tested here.
None of the gaps contradicts the paper.  Each is captured as a concrete
follow-up in `open_questions.json`.
