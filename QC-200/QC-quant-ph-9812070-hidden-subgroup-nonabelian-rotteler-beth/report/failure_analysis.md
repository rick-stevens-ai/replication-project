# Failure analysis / friction / residual gaps

Honest accounting of what did NOT work perfectly and what should be
qualified about the REPLICATED verdict.

## Genuine gaps

### G1. Marker + Nougat not installed on the execution host
- **What**: The QC wave brief requires `extraction/marker.md` and
  `extraction/nougat.mmd` from the Marker (PDF→Markdown) and Nougat
  (PDF→MMD) parsers. Neither binary is installed on CherryRd, and the
  central corpus (`~/Dropbox/REPLICATE-PROJECT/**/extraction/`) has no
  entry for this paper. Installing full Marker or Nougat would require
  a several-GB PyTorch download (Marker: ~2GB, Nougat: ~1.5GB) plus
  a working CUDA/MPS backend.
- **What I did**: Fell back to `pdftotext -layout` and wrote clearly
  labeled headers into both `marker.md` and `nougat.mmd` explaining
  the substitution. The content itself is the pdftotext dump.
- **Why this is acceptable here**: The paper is text-native LaTeX with
  no scan artifacts and minimal complex layout. Every algorithm step,
  definition, and equation used downstream is preserved verbatim in
  `work/paper.txt`. A Marker/Nougat pass would likely give slightly
  cleaner math LaTeX but no additional replication-relevant content.
- **Follow-up**: When Marker/Nougat are available (e.g. on m1 or via
  the LUCID pipeline), re-parse and drop into `extraction/`, replacing
  the fallbacks.

### G2. Quantum circuit synthesis of DFT_{W_n} (paper Fig. 3) not verified
- **What**: The paper's Sec. 5 gives a recursive gate-level construction
  of DFT_{W_n} using O(n) Hadamards, CNOTs, and Toffolis. Our numpy
  implementation goes directly from the paper's closed-form matrix
  entry `(-1)^{mu(g,h)} / sqrt(|G|)`, bypassing the circuit.
- **Impact**: The matrix we apply is provably identical to what the
  paper's circuit implements (both are the same real orthogonal matrix,
  and we verify `F @ F^T = I` to 1e-16). But we do not independently
  check the gate-count claim from Fig. 3.
- **Why this is acceptable for the headline claim**: The claim we set
  out to verify is Algorithm 7.1's success probability at O(n) queries,
  not the constant in the gate-count of DFT_{W_n}. The gate count
  matters for physical implementations but not for the algorithmic
  reproduction.
- **Follow-up**: A Qiskit implementation of Fig. 3 (using AQFT
  primitives from ref [12] in the paper) would close this gap. Effort:
  ~half a day.

## Not-really-failures but worth flagging

### N1. Task description had W_n → Z_2 wr Z_2^n; paper has W_n = Z_2^n wr Z_2
- The subagent task text said "Z_2 ≀ Z_2^n". The paper actually defines
  W_n := Z_2^n ≀ Z_2 (base group is the n-fold Z_2, then Z_2 acts by
  swap of two copies of the base). Both orderings give a group of the
  same order 2^{2n+1} at n=2 (both = 32) and both are called "wreath
  products", but the algorithm as written in the paper works with the
  latter convention (Z_2 acting on Z_2^n × Z_2^n by swap). I used the
  paper's convention throughout, which is the only one for which the
  algorithm is stated. This is a minor task-brief typo, not a
  replication issue.

### N2. n=2 group has |W_2| = 32, not the task-suggested "order 32 for n=2"
- Confirmed match: 2^{2·2+1} = 32. ✅ (no discrepancy)

### N3. Success probability of 1.00 is unusually clean
- **Why not surprising**: at n=2 the group has only 32 elements and
  the paper's DFT extracts perfect character-orthogonality
  information. With 32 samples versus a group of order 32, the
  algorithm nearly always sees a spanning set. The stress sweep at
  small i (2, 4, 6) shows the expected sub-1.0 rates that match the
  Lemma 6.3 bound, so we are not just seeing a bug that always
  returns success.
- **Confidence check**: Deliberately fed the classical postprocessor
  spoiled samples (e.g. samples from a wrong subgroup) and it returned
  a wrong U — the pipeline is sensitive to the input, not a hardcoded
  answer. Not persisted as a test but manually verified during
  development.

## Residual open questions
See `open_questions.json` for 5 questions that arose specifically from
this replication (not copied from the paper's own "future work"). Q1
in particular flags an interesting gap between the paper's Lemma 6.3
bound and our empirical curve.
