# Parser Provenance — Re-pass (2026-06-23)

## Sources used for claim enumeration

- **Main PDF text:** extracted via `pdftotext -layout source.pdf source.txt`
  (Poppler `pdftotext`, layout mode preserves columns/lines). Output: `source.txt`,
  829 lines. No marker/nougat MD is available for DOI `10.1371/journal.pone.0057953`
  in `_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/` (checked 2026-06-23;
  the only PLOS pone entries are 0044293, 0108234, 0187274, 0205691, 0250160 —
  not 0057953).
- **Supporting Info S1 (mathematical model):** plain-text extract
  `supplements/FileS1_MathematicalModel.txt` (produced previously via macOS
  `textutil` from the `.doc`). All 9 reactions + all 10 rate constants
  + 4 initial concentrations + 12 NBS1 scaling factors + 1 ATM scaling factor
  are present and readable.
- **Table S1 (FRAP k\*on / koff vs LET):** plain-text extract
  `supplements/TableS1.txt` (textutil). All 8 LET rows present.
- **Figure TIFFs (S1–S4):** PNG conversions in `supplements/FigureS{1,2,3,4}.png`,
  for vision-based digitization only.

## Rationale

- pdftotext is sufficient for the main text and references; the paper is
  text-rich (no equations embedded as images in the body).
- For numerical parameter tables and reaction networks we rely on the supplement
  text extracts, not the PDF, because the supplements contain the canonical
  numerical values.

## Tools used in this re-pass

- `pdftotext -layout` (Poppler) for paper body.
- Direct read of pre-extracted supplement `.txt` files.
- Python 3 + scipy/numpy for new reproductions (no internet, FREE compute on
  CherryRd local).
- Argo Opus 4.7 (FREE per standing rule) as the LLM driving the agent loop.

No new external data fetches were required — the paper, all 6 supplements,
and prior reproduction code were already present locally.
