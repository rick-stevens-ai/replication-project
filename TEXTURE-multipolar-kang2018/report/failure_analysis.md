# Failure Analysis — Kang, Shiozaki, Cho replication

## 1. PDF vision tool unavailable (blocked, worked around)
- **What failed:** the `pdf` tool errored (Anthropic "credit balance too low",
  Gemini model unknown, OpenAI extraction disabled). Could not do a
  vision-assisted read of equations/figures.
- **Root cause:** no available paid PDF/vision endpoint for this run.
- **Fix:** used `pdftotext -layout` (poppler, local, free) to extract the full
  text and transcribed equations by hand. Figures were not OCR'd; figure
  claims were reproduced numerically instead.
- **Prevention:** for math/physics papers, `pdftotext -layout` is a reliable
  free first resort; the two-column layout comes out interleaved but readable.

## 2. Directory did not exist (recovered)
- **What failed:** the assigned dir `TEXTURE-multipolar-kang2018/` was absent;
  siblings exist (lai2018, bhowal2022, chandra2014) but not kang2018.
- **Root cause:** the overnight batch had not staged this paper's skeleton.
- **Fix:** created the dir + fetched `paper.pdf` from arXiv (task rule:
  "If paper.pdf missing, fetch arxiv.org/abs/1812.06999"). Verified the arXiv
  ID resolves to the correct paper before writing anything.

## 3. Inverted quantization label + tiny |⟨Û₂⟩| (fixed — the substantive bug)
- **What failed:** first run gave trivial→0.5 and topological→0 (backwards vs
  the paper), with anomalously small \|⟨Û₂⟩\| (1e-4).
- **Root cause:** the many-body quadrupole phase is defined relative to a
  coordinate origin. With all orbitals pinned to the cell origin (s=0), the
  *raw* Im ln⟨Û₂⟩/2π carries an origin-dependent offset; only the *difference*
  between two ground states is gauge-invariant. Verified by sweeping the
  intra-cell offset s∈{0,0.1,0.25,0.4,0.5}: the raw value drifted continuously
  with s while (topo − trivial) stayed pinned at exactly 1/2.
- **Fix:** reference every Q_xy to the deep atomic-trivial limit (λ→0), which
  the paper proves is the correct "trivial" origin (invariance under adding a
  trivial atomic band). After referencing: trivial=0.0000, topological=0.5000,
  robust across L=6–12 and across s. This is the paper's convention.
- **Not a physics error:** the gauge-invariant content (a half-quantum
  quadrupole jump and the transition location) was correct from the start; only
  the absolute origin needed the physically-motivated reference.

## 4. Small |⟨Û₂⟩| bulk magnitude (understood, non-fatal)
- **Observation:** \|⟨Û₂⟩\| decays with L in every phase (single-determinant
  overlap suppression). The *phase* stays well-resolved in double precision at
  the sizes used (L≤12), so Im ln extraction is safe here. Flagged as an open
  question (scaling to larger L may need a log-domain determinant).

## 5. Out-of-scope items (explicitly deferred, not failures)
- Interacting/bosonic ground states, the anomalous quadrupole insulator
  (Fig 1d), the partial-region operators V(l) (Fig 3), and the octupole were
  **not** implemented. Their model/parameter details live in the supplemental
  material, which the text extraction did not fully resolve, and they exceed a
  "minimal/tractable" analytic model. All are recorded in open_questions.json.
