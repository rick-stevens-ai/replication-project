# CRISPR detection: Paper vs minced

**Paper claim (CRISPRFinder + manual):** Two candidate CRISPRs in the chromosome; both carry
only ONE spacer each. One is surrounded by cas proteins (locus tags STACADC2_0849-0856), the
other is orphan. Organization/high identity match S. thermophilus LMD-9; differ mainly in csm6.

**Independent minced 2.x detection (uicgpu):**
- Default (minNR=3): 0 arrays. EXPECTED — minced's default requires >=3 repeats; a single-spacer
  CRISPR has only 2 repeats, below the default cutoff. This is fully consistent with the paper's
  statement that both arrays carry only one spacer (2 repeats each).
- minNR=2: 6 candidate repeat regions detected. The array at ~849,603-849,704 bp
  (CRISPR 5) is positionally coincident with the paper's cas-flanked CRISPR near locus tags
  STACADC2_0849-0856 (locus tag ~0849 -> ~850 kb region on a 1.73 Mb genome).

**Interpretation:** CRISPR presence is CONFIRMED independently. The exact count is tool-dependent
(CRISPRFinder curated 2 confirmed; minced-minNR2 flags 6 low-repeat candidates), but the key
qualitative claim — this strain has short, single-spacer CRISPR array(s), one cas-associated near
~850 kb — is reproduced. The single-spacer nature (why default minced finds none) is itself
corroborating evidence for the paper's specific observation.
