# Artifact Harvest

| Artifact | Source URL | Size | SHA-1 | Notes |
|---|---|---|---|---|
| paper.pdf | https://thermalscience.vinca.rs/pdfs/papers-2018/TSCI170804285Y.pdf | 867,501 B | 3fda2ba1872f1a267898f01613dea7b28c2bebb9 | OA PDF from Thermal Science / Vinca Institute (Serbian OA journal). Fetched via uicgpu (env proxy). |
| paper.txt | pdftotext -layout paper.pdf | 642 lines | — | Full-text extraction of the paper (used for method + Table 1 transcription). |
| Crossref metadata | https://api.crossref.org/works/10.2298/TSCI170804285Y | — | — | Confirmed vol 22 Suppl.1 pp. 185-194, published 2018 (submitted Aug 2017). |

## Notes on retrieval
- doiserbia.nb.rs (the DOI's official landing) was returning HTTP 503 from both local (CherryRd) and uicgpu at the time of the run.
- thermalscience.vinca.rs (the publisher's own site) returned HTTP 200 for the correctly-guessed 2018 path (paper is dated 2017 in the DOI slug but printed in vol 22, 2018).
- No supplementary code was published with the paper; the method was reimplemented from scratch from the paper's equations (12), (13), (14) and Stehfest formula.
