# Artifact Harvest — OSTI 2339566

Public artifacts pulled during replication.

| Artifact | URL / accession | Size | Checksum (md5) | Notes |
|---|---|---|---|---|
| Paper PDF | https://www.osti.gov/servlets/purl/2339566 | 2,719,076 B | 9ef7cb728881156054891188f8465044 | v1.5, 41 pages; fetched via uicgpu proxy (direct fetch from CherryRd hung). Saved to `work/2339566.pdf`. |
| arXiv preprint | https://arxiv.org/abs/2212.01912 (v2) | — | — | Cross-reference for identical content; DOI 10.1021/acs.jctc.2c01119 in JCTC. |

Software tools installed in local venv (`work/.venv/`):

| Package | Version | Purpose |
|---|---|---|
| numpy | (default with scipy) | linear algebra |
| scipy | latest | BFGS VQE optimizer |
| pypdf | latest | PDF text extraction fallback |
| openfermion | 1.7.1 | Fermion-to-qubit transforms, InteractionOperator |
| pyscf | 2.13.1 | Molecular integrals + FCI reference |
| openfermionpyscf | latest | Bridge between the two |
| qiskit | 2.5.0 | (imported for import-check only, not used for circuit runs) |
| qiskit-aer | latest | (installed, not used; classical VQE via scipy is faster) |

No external hardware, no proprietary data. Zero cost. All computations local on CherryRd.
