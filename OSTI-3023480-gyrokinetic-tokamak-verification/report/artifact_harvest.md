# Artifact harvest — OSTI 3023480

| # | URL | Type | Size | Local path | Notes |
|---|-----|------|-----:|-----------|-------|
| 1 | https://www.osti.gov/servlets/purl/3023480 | PDF | 2.19 MB | `work/paper.pdf`, `paper.pdf` | 10-pp open-access preprint, IOP/IAEA Nucl. Fusion 66 036050 |
| 2 | doi:10.1088/1741-4326/ae463f | DOI landing | – | – | published article (paywalled at IOP; OSTI PDF is CC-BY-4.0 preprint) |
| 3 | ORCID Handi Huang 0000-0002-7645-9454 | metadata | – | – | first author, UC Irvine |
| 4 | ORCID Nikolai Gorelenkov 0000-0002-7345-8149 | metadata | – | – | senior author, PPPL |
| 5 | ORCID Zhihong Lin 0000-0003-2007-8983 | metadata | – | – | GTC PI, UC Irvine |
| 6 | ref [12] Duarte et al. 2023 Nucl. Fusion 63 036018 | prior work | – | – | source for NOVA continuum + spectrogram (Figs. 1, 3, 5 in paper are reproduced from this) |
| 7 | ref [11] Bland et al. 2022 Nucl. Fusion 63 016024 | prior work | – | – | first identification of the ST40 chirping mode / H-L-H |
| 8 | ref [14] Gorelenkov 2007 Phys. Lett. A 370, 70 | analytic formula | – | – | source of the BAAE gap frequency formula used in paper §4 |
| 9 | ref [34] Wei et al. 2021 arXiv:2109.08873 | preprint | – | – | XMAP Grad–Shafranov solver + GTC EM formulation |
| 10 | ORNL INCITE (DE-AC05-00OR22725) | compute | – | – | GTC production runs (not accessed) |
| 11 | NERSC (DE-AC02-05CH11231) | compute | – | – | GTC production runs (not accessed) |
| 12 | ST40 discharge #09894, t=0.092 s, TRANSP run 09894A03 | experimental data | – | – | not public; kinetic-profile values in paper §3 used verbatim |
| 13 | GTC source (Zhihong Lin group) | code | – | – | not public (github.com/PrincetonUniversity/gtc requires access request); NOT downloaded |
| 14 | NOVA source | code | – | – | PPPL-internal MHD eigenmode code; NOT downloaded |
| 15 | ALCON source | code | – | – | Deng et al. 2012; GTC-workflow component; NOT downloaded |
| 16 | pdftotext | extractor | 22.05.0 | `/usr/local/bin/pdftotext` | used for PDF → text (`extraction/marker.md`) |
| 17 | Python 3 + math + json | analytic solver | 3.13 | system | zero heavyweight deps; scripts in `work/` |
| 18 | Argo LiteLLM aggregator | LLM judge endpoint | – | http://<tailnet-aggregator>:4000/v1 | Bearer stevens, free per Rick's standing rule |
| 19 | Argo GPT-5.4 | LLM judge #1 | – | – | verdict SPOT-CHECK 5/8 · 5/5 (see `evidence/llm_judge_gpt54.txt`) |
| 20 | Argo GPT-5.2 | LLM judge #2 | – | – | verdict SPOT-CHECK 4/7 · 4/4 (see `evidence/llm_judge_gpt52.txt`) |

Provenance chain: every quantitative comparison in REPORT.md is traceable to (a) a number lifted from the pdftotext of `paper.pdf`, or (b) a number printed by `work/reproduce_baae_v3.py`. LLM judges were fed a description of the physics and asked to grade, not fed the numerical results directly (see `evidence/judge_prompt.txt`).
