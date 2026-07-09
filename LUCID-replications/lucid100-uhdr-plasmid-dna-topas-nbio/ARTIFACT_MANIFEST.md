# ARTIFACT MANIFEST — lucid100-uhdr-plasmid-dna-topas-nbio

All artifacts harvested 2026-06-09 from public sources. No paid endpoints used.

## Paper itself

| File | Source | Bytes | Hash (sha256) | License | Notes |
|---|---|---:|---|---|---|
| `artifacts/paper.pdf` | https://iopscience.iop.org/article/10.1088/1361-6560/ae62c6/pdf | 2,013,894 | (computed below) | CC-BY 4.0 | published version, 15 pp. |
| `artifacts/paper.txt` | `pdftotext -layout paper.pdf` | – | – | derived from CC-BY | 1116 lines |

## Bibliographic / openness metadata

| File | Source | Purpose |
|---|---|---|
| `artifacts/crossref.json` | `api.crossref.org/works/10.1088/1361-6560/ae62c6` | canonical metadata, refs count, funding, license |
| `artifacts/semanticscholar.json` | S2 graph API, key in macOS keychain `semantic-scholar-api-key` | abstract, authors, citation count |
| `artifacts/openalex.json` | `api.openalex.org/works/doi:…` | OA status (`is_oa: true`, hybrid, cc-by) |
| `artifacts/unpaywall.json` | `api.unpaywall.org/v2/…` | best_oa_location (publisher, cc-by) |
| `artifacts/unpaywall_dkondo2024.json` | unpaywall | precursor D-Kondo 2024 (oxygen + WR-1065), PMC OA |
| `artifacts/unpaywall_dkondo2021.json` | unpaywall | precursor D-Kondo 2021 (plasmid DNA model) |
| `artifacts/ae62c6_esummary.json` | NCBI eutils | PMID 42013902 |
| `artifacts/ae62c6_epmc.xml` | EuropePMC | empty body — paper not in EPMC fulltext mirror yet |

## Code-availability search outputs

No per-paper repository exists. Recorded in this manifest only:

- TOPAS-nBio main extension repo (open, BSD-style): `https://github.com/topas-nbio/TOPAS-nBio-v2.0` (30 stars). Sibling: `https://github.com/topas-nbio/TOPAS-nBio` (10 stars), `https://github.com/topas-nbio/TOPAS-nBio-regression`, `https://github.com/topas-nbio/qi-topas-nbio`.
- OpenTOPAS host (paper’s v4.0.0 simulator): `https://opentopas.github.io`
- Author GitHub accounts found via GitHub user search: `masilela`, `d-kondo` — both **empty public profiles** (verified via `api.github.com/users/{user}/repos`).
- Paper’s own statement: *"The full set of chemistry parameter files for both models will be released as an example in a future version of TOPAS-nBio."* (Section 2.2.3.) — not yet released as of 2026-06-09.

## Derived analysis artifacts

| File | Purpose |
|---|---|
| `scripts/chemistry_table1.csv` | Table 1 reactions R1..R43*, including kobs in /M/s or /s |
| `scripts/smoke_scavenging_capacity.py` | analytical reproducer (Eq. 4) + intertrack-vs-lifetime check |
| `scripts/smoke_results.csv` | per-DMSO σ, kobs, predicted SSB scaling, paper-reported SSB |
| `figures/smoke_ssb_vs_sigma.png` | log-log SSB(σ) overlay of smoke prediction vs paper numbers |
| `figures/smoke_intertrack_vs_oh_lifetime.png` | Fig. 4-style reproduction |

## Provenance

- All HTTP fetches above 2 MB used `curl -sL --max-time 60 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"`.
- IOPscience PDF endpoint requires a browser-like UA but otherwise serves CC-BY content with HTTP 200 + `content-type: application/pdf`.
- No authentication used. No personal credentials sent to publishers.

## Hash record

Run `shasum -a 256 artifacts/* scripts/*` to regenerate; current values written to `artifacts/SHA256SUMS.txt` by the smoke pipeline.
