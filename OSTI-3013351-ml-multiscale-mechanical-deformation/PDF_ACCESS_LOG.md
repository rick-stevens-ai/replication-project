# PDF Access Log — OSTI 3013351

**Paper:** Machine learning-enabled multiscale modeling of mechanical deformation of aluminum and Al-SiC nanocomposites
**Authors:** Md Shahrier Hasan, Hadia Bayat, Wibe de Jong, Wenwu Xu
**Venue:** Materials & Design, Vol. 260, 115063 (2025-11-04)
**DOI:** 10.1016/j.matdes.2025.115063
**OSTI ID:** 3013351
**License:** CC-BY-NC-ND (Gold OA per Unpaywall / DOAJ)

## PDF Fetch Attempts (all failed from this network / this session)

| # | URL | Result |
|---|-----|--------|
| 1 | https://www.osti.gov/servlets/purl/3013351 | curl exit 28 (timeout) |
| 2 | https://www.osti.gov/pages/servlets/purl/3013351 | HTTP 000 (connection failed, 45s timeout) |
| 3 | https://www.osti.gov/biblio/3013351 | HTTP 000 |
| 4 | https://escholarship.org/uc/item/3k8971w6.pdf | HTTP 403 (CloudFront) |
| 5 | https://escholarship.org/content/qt3k8971w6/qt3k8971w6.pdf | HTTP 403 |
| 6 | https://escholarship.org/uc/item/3k8971w6 (landing) | HTTP 403 |
| 7 | https://doi.org/10.1016/j.matdes.2025.115063 (Elsevier) | web_fetch 403 |
| 8 | https://doaj.org/article/aa21adef45004036a49348da6c976d2e | HTTP 403 (browser check) |

Unpaywall reports `url_for_pdf: null` for both publisher and repository copies — no direct PDF URL is exposed even though the article is Gold OA CC-BY-NC-ND.

## Proceeding from abstract + metadata

Per task instructions: "If no PDF after honest attempts, proceed from abstract/metadata and note it."

Full abstract captured from DOAJ API (`paper_metadata.json`). The reproducible core described in the abstract is unambiguous:

> "A machine learning-enabled multiscale framework is developed for modeling the mechanical response of both pure metal and nanoparticle-reinforced metal matrix nanocomposites (MMNCs). Using aluminum–silicon carbide (Al-SiC) as an example MMNC, atomistic simulations reveal three distinct deformation mechanisms (i.e., defect-free, dislocation-based, and interface separation) governed by the interfaces between the Al matrix and SiC nanoparticles. […] These mechanisms are captured through a combined classification-regression neural network surrogate model that bridges atomic-scale insights with continuum-scale finite element analysis. Machine learning-enabled multiscale modeling of pure Al accurately predicted strain localization and confirmed by in-situ scanning electron microscopic tensile testing on perforated Al specimens."

Reproducible core we CAN spot-check with free tooling:
1. **Combined classification-regression NN surrogate** — one NN outputting both a discrete deformation-mechanism label (defect-free / dislocation / interface separation) AND continuous stress-response.
2. **Multiscale bridging** — micro-scale descriptors (strain history, phase/interface identity) → macro-scale stress response.
3. **Interface-controlled failure mode** — reinforced MMNC shows *more gradual* damage progression vs. single-crystal metal (abrupt failure).

Numerical values (elastic moduli, yield stresses, exact loss numbers, dataset sizes, LAMMPS MD parameters, FE mesh sizes) are NOT in the abstract, so quantitative reproduction is not possible without the paper body. Verdict must be SPOT-CHECK level, not full REPLICATED.
