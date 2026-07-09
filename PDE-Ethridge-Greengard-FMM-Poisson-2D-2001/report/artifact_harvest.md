# Artifact Harvest

Every external resource pulled during this replication.

## Paper

| Field | Value |
|-------|-------|
| Source URL | https://math.nyu.edu/faculty/greengar/poiss2d.pdf |
| Local path | `paper.pdf` |
| Size | 2,995,884 bytes (~2.86 MB) |
| Format | PDF 1.2 |
| SHA-256 | `6634e8d832c85a546a5ef4fe2c08edc5db235195d181b07edde8979e411c091e` |
| Access | Green OA (author's personal page, NYU) |
| Fetched | 2026-07-06 08:17 CDT via `curl -L` |
| S2 corpus ID | 18861715 |
| S2 paper ID | `bb6e23bdc9c556043c40e87095845e9c164e53bc` |
| MAG | 1977737756 |
| DBLP | journals/siamsc/EthridgeG01 |
| DOI | 10.1137/S1064827500369967 |

## APIs consulted

| API | Endpoint | Auth | Purpose |
|-----|----------|------|---------|
| Semantic Scholar Graph | `https://api.semanticscholar.org/graph/v1/paper/DOI:10.1137/S1064827500369967` | Keychain `semantic-scholar-api-key` acct `rick-stevens-ai` | Get metadata + OA PDF URL |
| OpenAlex | `https://api.openalex.org/works/https://doi.org/10.1137/S1064827500369967` | none | Cross-check OA status (OpenAlex reports closed; S2 has GREEN via unpaywall.org) |
| Argo LLM (FREE) | `http://localhost:4000/v1/chat/completions` | Bearer `stevens` | LLM-judge verdict via `argo:gpt-5.4` |

## No datasets/genome/experimental data pulled

This is a computational-mathematics paper. All test data is generated
synthetically inside the replication code (random point sources for C1/C2,
analytic three-Gaussian source for C3/C4). No external datasets required.

## Codes NOT used (though considered)

| Package | Why not | Would enable |
|---------|---------|--------------|
| fmm2dpy | Not installed on CherryRd or uicgpu | Cross-validate our own FMM |
| pyfmmlib | Same | Same |
| kifmm | Same | Same |
| deal.II / FEniCS | Wrong tool (FEM, not FMM) | Boundary-condition variants |
| marker | Not installed locally | Better paper.pdf extraction |
| nougat | Not installed (needs GPU) | Better math extraction |
