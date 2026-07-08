# PARSER_PROVENANCE.md — PMID 26392213 (Outer mucus niche, Li et al. 2015)

Pass-2 re-pass — paper sourcing & parsing.

## Primary source
- **Publisher PDF (definitive):**
  - URL: https://www.nature.com/articles/ncomms9292.pdf
  - File: `/tmp/ncomms9292.pdf` (8,311,943 bytes, PDF 1.6, 33 pages)
  - Downloaded: 2026-06-23 13:45 CDT (this pass) with `curl -sSL -A "Mozilla/5.0"`
  - Parser: `pdftotext -layout` (Poppler at `/usr/local/bin/pdftotext`)
  - Output: `/tmp/ncomms9292.txt` (1452 lines, full body + Methods + References)
  - Pages 1–13 = main paper; pages 14–33 = supplementary figures/tables embedded.

- **Secondary source (cross-check):**
  - PMC HTML: https://pmc.ncbi.nlm.nih.gov/articles/PMC4595636/
  - Fetched via `web_fetch` (readability extract), used for cross-checking abstract,
    Results section narrative, and figure captions. PMC fetch was truncated at 20K
    chars (extractor limit), so the PDF was used for any quantitative claims past
    the iron-harvesting section.

## Data sources (re-confirmed pass-2)
- **16S amplicon:** Figshare DOI 10.6084/m9.figshare.1499145 (already downloaded
  pass-1, 3 FASTQ files + 3 QIIME mapping files in `data/raw/`, MD5-verified).
  *Not* SRA — the SRA accession PRJEB8805 contains only whole-genome assemblies
  of 12 sDMDMm2 isolates.
- **RNA-seq (B. theta + E. coli mucus vs content):** Paper does NOT cite an
  ArrayExpress/GEO/SRA accession in either the main text or the deposited
  Figshare bundle. Supplementary Data 1, 2, 3, 10, 11 are described as
  Excel tables of differentially-expressed genes, hosted as Supplementary
  Information at Nature.com — the raw FASTQ for the RNA-seq experiment is
  **not publicly deposited**. (Re-checked text 2026-06-23.)
- **Metabolomics (mass spec, Q-TOF flow-injection):** Not deposited;
  Supplementary Data 5 + 12 are HMDB annotation tables only.
- **32P bacterial replication, ICP-MS iron, IF microscopy, two-photon movies:**
  no raw deposit; numeric values quoted in the paper text and in
  Supplementary Table 1 only.

## Claim parsing method
1. `pdftotext -layout` of the publisher PDF.
2. Manual enumeration of every quantitative or qualitatively-testable claim
   from the Abstract, Results subsections, figure captions, and Methods.
3. Cross-checked numeric quotes against the PMC HTML version.
4. Each claim tagged with: source-locator (figure/section), what is asserted,
   what data would be needed to test it, and whether pass-1 covered it.

## Reproducibility log
- All commands run on host CherryRd, conda env `microbiome` (miniforge),
  Python 3.10, scikit-bio 0.7.2, vsearch 2.31.0, mafft, FastTree.
- Re-pass script: `code/repass/repass_analysis.py` (single file, deterministic
  seed where stochastic).
- Re-pass outputs: `results/repass/`.
- Original pass-1 layout kept under `scripts/` and `analysis/`; pass-1 report
  preserved as `report/REPORT.pass1.md`.
