# Artifact Harvest — PDE-municipal-sewage-cfd-2020

Every external artifact pulled and its provenance.

## Public artifacts pulled

| # | URL | Kind | Size | Notes |
|---|-----|------|-----:|-------|
| 1 | `https://doi.org/10.24297/jam.v18i.8345` | DOI | HTML redirect | Resolves to publisher landing |
| 2 | `https://rajpub.com/index.php/jam/article/view/8345` | Publisher landing HTML | ~50 KB | Contains `citation_pdf_url` meta tag |
| 3 | `https://rajpub.com/index.php/jam/article/download/8345/7894` | **PDF (OA)** | 406 604 B | The paper. Saved as `paper.pdf`. md5 not computed; PDF v1.7, 10 pages. |
| 4 | `https://api.crossref.org/works/10.24297/jam.v18i.8345` | JSON metadata | ~2 KB | Used to verify true title (Tororo, Uganda) — brief metadata was wrong |

## Public code / datasets pulled

None. This paper does not release code (paper reports it was implemented in OpenFOAM but no case files were shared). No supplementary datasets were referenced.

## Software artifacts used (already installed)

| # | Software | Version | Host | Source |
|---|----------|---------|------|--------|
| 1 | OpenFOAM | v1906 | uicgpu | Ubuntu `openfoam/focal` package |
| 2 | pdftotext | poppler 24.x | CherryRd | Homebrew |
| 3 | numpy | ≥1.24 | CherryRd | pip |
| 4 | matplotlib | ≥3.6 | CherryRd | pip |
| 5 | Python | 3.11 | CherryRd | system |

## Central-corpus lookups attempted

- **Marker corpus (Eagle/SCOUT/LUCID/OSTI):** NOT queried for this newly-added PDE paper. Fallback: `pdftotext -layout` (adequate for this text-native PDF).
- **Nougat corpus:** NOT queried. Same fallback.

If a real Marker/Nougat parse is later pulled from Eagle, replace `extraction/marker.md` and `extraction/nougat.mmd` accordingly.

## Municipal / utility records (NOT pulled)

The paper's §4.1 recommendation cites "NWSC and municipal office" records for the 535 → 1200 connection numbers. These are not indexed in any public database. Would require direct correspondence with National Water and Sewerage Corporation (Uganda) or Busitema University Faculty of Engineering. Marked out-of-scope in this replication; see Open Question Q5.
