# Artifact harvest

## Paper PDF
- **Source:** https://www.osti.gov/servlets/purl/2349026
- **Fetched via:** `ssh uicgpu curl -sL -o /tmp/osti_2349026.pdf 'https://www.osti.gov/servlets/purl/2349026'`
- **HTTP:** 200
- **Size:** 5,025,832 bytes
- **MD5:** `df95983131d50dbedc1c5bca5900ad7a`
- **Local copy:** `work/paper.pdf`
- **PDF version:** 1.5, 9 pages of main text

## Code repo (surrogate line search)
- **Source (paper's stated code URL):** https://github.com/QMCPACK/stalk/releases/tag/v0.1
- **Tarball:** https://codeload.github.com/QMCPACK/stalk/tar.gz/refs/tags/v0.1
- **HTTP:** 200
- **Size:** 181,488 bytes
- **MD5:** `b7e6e413603b24dfd34082c5b97d9b10`
- **Local copy:** `work/code/stalk-v0.1.tar.gz` (extracted to `work/code/stalk-0.1/`)
- **Contents:** README, lib/{hessian.py, linesearch.py, linesearchiteration.py, parallellinesearch.py, parameters.py, pessampler.py, targetlinesearch.py, targetparallellinesearch.py, util.py}, tests/, docs/examples/{benzene.py, coronene.py, morse_3p.py, nxs.py}, surrogate_classes.py, surrogate_macros.py
- **License:** included, LGPL/permissive
- **Note:** STALK is the generic surrogate-Hessian parallel line-search library for *atomic structure relaxation* (as originally developed by Tiihonen, Kent, Krogel, J. Chem. Phys. 156, 054104 (2022)). The paper's VQC-specific adaptation code (interfacing the SWS sparse-wave-function simulator, IBM Qiskit / ibm_brisbane driver, molecular Hamiltonian pipelines from PySCF, etc.) is **NOT included** in this v0.1 release. STALK provides the core algorithm; the paper's application layer is not public.

## Sparse Wave Function Simulator (SWS)
- **Cited as ref (86, 87)** in the paper.
- **Not released** in the STALK v0.1 tarball, and no separate public URL for the SWS is given in the paper's Data/Materials/Software Availability section.
- This is the primary blocker to a full-fidelity replication of the H₂O/N₂/H₄ chemistry results in Table 1 / Figs. 2–3.

## Preprint / supplementary
- **arXiv:** https://arxiv.org/abs/2404.02951 (ref 138 in the paper — same content, listed as the pointer for "Data for figures ...").
- **SI Appendix:** hosted at https://www.pnas.org/lookup/suppl/doi:10.1073/pnas.2408530122/-/DCSupplemental — not pulled in this replication attempt (main-paper figures were sufficient).

## Local software stack for replication
- Python 3.12.13, numpy 2.5.0, scipy 1.18.0, qiskit 2.5.0, qiskit-aer 0.17.2 (venv at `work/venv/`).
- All local statevector simulation; no external services used, no LLM inference used, no API calls.
