# Artifact harvest

| # | Source | URL / accession | What we got | Size |
|---|--------|-----------------|-------------|------|
| 1 | Taylor & Francis full-text HTML | https://www.tandfonline.com/doi/full/10.1080/25765299.2019.1613746 | article body, all equations, section text | ~49 kB text (`work/paper_text.txt`) |
| 2 | Same, `showPopup` table popups (`data-id=t0001..t0012`) | (same base URL, popup rendered client-side) | Numeric values from Tables 1, 2, 6, 7, 10, 11, 12 (the 6 tables with L₂/L∞ or pointwise numbers we needed) | `work/paper_tables.md` |
| 3 | OpenAlex work record | https://api.openalex.org/works/doi:10.1080/25765299.2019.1613746 | metadata: OA status (gold), primary_location, publisher, license | in-line JSON, discarded |

## Provenance notes
- PDF endpoint (`/doi/pdf/...?needAccess=true`) is Cloudflare-guarded from cURL and from `ssh uicgpu`; JS challenge only clears in a real browser context. HTML full-text at `/doi/full/...` clears the same challenge with a normal Chromium (openclaw profile). Both endpoints serve the same content.
- License CC BY-NC 4.0 → reproducing table values for scientific verification is permitted.
- No external code or datasets pulled — all reference numbers come from the paper itself, all replicated numbers from our from-scratch Python implementation.

## Generated evidence (in `report/evidence/`)
- `results_1d.json` — numerical outputs for Tables 1, 2, 6, 11
- `results_2d.json` — numerical outputs for Table 12
- `run_1d.log` / `run_2d.log` — stdout of the replication runs
