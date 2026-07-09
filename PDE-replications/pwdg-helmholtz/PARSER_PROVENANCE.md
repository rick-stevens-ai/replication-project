# Parser Provenance — pwdg-helmholtz re-pass

- **Source PDF:** `paper.pdf` (350,710 bytes), downloaded 2026-06-23 from open-access preprint:
  `https://centaur.reading.ac.uk/28020/1/Hiptmair%20Moiola%20Perugia%202011%20-%20PVersion%20-%20Plane%20wave%20discontinuous%20Galerkin%20methods%20for%20the%202D%20Helmholtz%20equation%20analysis%20of%20the%20p-version%20-%20SINUM2011.pdf`
- **Reference of record:** Hiptmair, Moiola, Perugia, SIAM J. Numer. Anal. 49(1), 264–284, 2011, DOI 10.1137/090761057.
- **Parser:** `pdftotext -layout` (poppler-utils, `/usr/local/bin/pdftotext`).
- **Parsed output:** `paper.txt`, 1520 lines.
- **Verification:** title block, authors, abstract, and the "Numerical experiments" §5 with mesh families T1/T2/T3 are all cleanly extracted; equations parse as plain text (Greek letters preserved where the PDF used Unicode; some Times-italic math glyphs render as combining marks but are readable).
- **Provenance for numerical comparison:** §5 (Numerical experiments) and §3 (Stability / well-posedness). Reproduced claims are cited by section/equation where possible.
