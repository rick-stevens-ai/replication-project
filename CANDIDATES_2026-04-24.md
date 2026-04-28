# 15 New Candidate Papers for Replication Set (2026-04-24)

**Prepared by:** Ollie (subagent, candidates-40papers)
**Source:** OSTI API (affiliation/research_orgs Argonne National Laboratory), 2024–2026 Journal Articles, filtered to AI/ML-methodological papers.
**Provenance rule applied:** each candidate has `research_orgs` containing Argonne OR a listed ANL author with contract AC02-06CH11357.
**Constraint:** no proprietary software; replication path specified for each; 2–6 h subagent budget unless flagged as stretch.

## Selection Summary

- Target: add 10–12 of these 15 to the active replication set; the remaining 3–5 serve as documented deferrals.
- The slate is biased toward **under-represented domains** (fusion, epidemiology, soft matter / polymers, neuromorphic, drug/protein, HEP, CFD/PDE, chemistry ML) and away from already-saturated domains (astro, condensed matter, nuclear reactor physics).
- Feasibility scored 1–10 across four axes; overall = rounded mean. Recommendation `ADD` / `DEFER` / `SKIP` is Ollie's read; Rick gets final call.

## Domain balance target

Desired **additions** (of 10–12 total):
- Fusion / plasma: +1  
- Epidemiology / ABM: +1 (already have none)  
- Drug / protein design: +1–2  
- Soft matter / polymers: +1  
- Neuromorphic / spiking: +1  
- Chemistry ML (orbitals/coarse-graining/LLM): +2  
- HEP / accelerator edge AI: +1–2  
- CFD / PDE surrogates: +1  
- Photonics / imaging: +1 (stretch)

---

## Papers

### Paper 1: 2587945 — Spatiotemporal forecasting of the edge localized modes in tokamak plasmas using neural networks
- **Authors:** Samaddar (ANL), Madireddy (ANL), Gong (ORNL), Hansen (Columbia), Joung, Smith (UW–Madison)
- **Year:** 2025 (Aug)
- **Domain:** Fusion plasma / surrogate NN
- **Link:** https://www.osti.gov/biblio/2587945
- **Paper DOI:** 10.1088/2632-2153/adfb41 (Machine Learning: Science and Technology, IOP)
- **Code repo:** MLST papers typically require code release; abstract says neural approximators — look on GitHub under `madireddy` / `samaddar` or IOP supplementary. Even if no public repo, Beam-Emission-Spectroscopy ELM datasets (DIII-D / NSTX synthetic or surrogate) are findable.
- **Core method:** Trains a spatiotemporal neural network (likely ConvLSTM or Fourier-based) on synthetic or experimentally-derived edge-localized-mode plasma signals to forecast ELM bursts a few ms in advance. Replication path: reproduce the architecture in PyTorch on a public ELM/BES synthetic dataset (NSTX or CFS published simulations), train on uicgpu (single A100, ~2 h), compare MSE/ROC of bust-prediction with paper values.
- **Compute estimate:** 3–5 h on 1× A100, or 4–6 h CPU for a scaled-down version.
- **Feasibility scores:**
  - Code available: 5/10 (IOP MLST typically yes; need to check supplementary)
  - Compute tractable: 8/10
  - Domain clear: 9/10 (ELMs are well-defined, BES is standard)
  - Paper specific: 8/10
  - **Overall: 7.5/10**
- **Recommendation:** **ADD** (closes the fusion gap; ANL-lead)
- **Rationale:** First fusion paper with a **journal-grade ML surrogate** in our set. Madireddy is an ANL staff-scientist who publishes open code regularly. Strong domain fit for Rick's DOE narrative.

### Paper 2: 2587579 — Mesh-based super-resolution of fluid flows with multiscale graph neural networks
- **Authors:** Barwey, Pal, Patel, Balin, Lusch, Vishwanath — **all ANL**
- **Year:** 2025 (May)
- **Domain:** CFD / PDE surrogate / graph neural networks
- **Link:** https://www.osti.gov/biblio/2587579
- **Paper DOI:** 10.1016/j.cma.2025.118072 (CMAME)
- **Code repo:** Barwey routinely publishes on GitHub (`shivambarwey`) using PyTorch Geometric; Nek5000/NekRS datasets are open.
- **Core method:** GNN that performs spectral-element-aware super-resolution on 3D unstructured meshes. Modifies message-passing layer to sync coincident graph nodes across element boundaries (compatible with SEM/FEM). Replication path: download a small Nek5000 turbulent-channel low-resolution mesh and its high-resolution counterpart, implement the modified MP layer in PyTorch Geometric, train on a coarsened slice, compare L2 field error vs. paper.
- **Compute estimate:** 3–4 h on 1× A100 for a tractable-size mesh.
- **Feasibility scores:**
  - Code available: 7/10
  - Compute tractable: 8/10
  - Domain clear: 9/10
  - Paper specific: 9/10 (CMAME papers are very methodologically explicit)
  - **Overall: 8.3/10**
- **Recommendation:** **ADD** (high-confidence pick)
- **Rationale:** All-ANL authors, open-source ecosystem (PyG, Nek), a clean methodological delta (sync layer) to verify. Very quotable if it lands.

### Paper 3: 3014231 — Sequence-based generative AI design of versatile tryptophan synthases
- **Authors:** Lambert (Caltech), Tavakoli (Caltech), **Dharuman (ANL)**, Yang (Caltech), … (Nat. Commun.)
- **Year:** 2026 (Jan)
- **Domain:** Protein design / protein language model (drug-discovery adjacent)
- **Link:** https://www.osti.gov/biblio/3014231
- **Paper DOI:** 10.1038/s41467-026-68384-6
- **Code repo:** Uses **GenSLM** — Argonne's open-source protein language model (github.com/ramanathanlab/genslm). Dataset (TrpB sequences) public via UniProt.
- **Core method:** Fine-tune GenSLM on TrpB β-subunit sequences, sample novel sequences, filter by AlphaFold-predicted structure / expression proxies, then in-silico score catalytic viability. Replication path (in-silico only): download GenSLM-25M, fine-tune on a small public TrpB MSA (~10k seqs), sample 1000 novels, score perplexity / pLDDT via ESMFold.
- **Compute estimate:** 4–5 h on 1× A100 for the 25M model; no wet-lab step.
- **Feasibility scores:**
  - Code available: 9/10 (GenSLM open)
  - Compute tractable: 7/10
  - Domain clear: 8/10
  - Paper specific: 7/10 (wet-lab validation we cannot reproduce; ML half we can)
  - **Overall: 7.8/10**
- **Recommendation:** **ADD**
- **Rationale:** Uses ANL's flagship open protein-LM (GenSLM). Replication scope = the generative/filtering pipeline; the wet-lab step is documented-as-uncomputable honestly.

### Paper 4: 3012452 — EC-Bench: A Benchmark for Enzyme Commission Number Prediction
- **Authors:** Henry (ANL) et al.
- **Year:** 2026 (Jan)
- **Domain:** Bioinformatics / protein function classification
- **Link:** https://www.osti.gov/biblio/3012452
- **Paper DOI:** 10.1093/bioadv/vbag004 (Bioinformatics Advances)
- **Code repo:** Benchmark papers almost always ship the dataset + baselines on GitHub; Henry group at ANL (ModelSEED) is prolific there.
- **Core method:** Curates a held-out EC-number prediction benchmark (leakage-controlled) and evaluates a handful of baseline models (ESM + classifier, ProteinBERT, …). Replication path: download the benchmark, run one of the baselines (ESM-2 embeddings + MLP head), reproduce reported F1.
- **Compute estimate:** 2–3 h on 1× A100 (embedding + linear head).
- **Feasibility scores:**
  - Code available: 9/10
  - Compute tractable: 9/10
  - Domain clear: 9/10
  - Paper specific: 9/10 (benchmark paper = maximally specific)
  - **Overall: 9.0/10**
- **Recommendation:** **ADD** (easiest pick in the set)
- **Rationale:** Benchmarks are the optimal replication target — explicit metrics, open data, clear baselines. Strengthens bioinformatics coverage.

### Paper 5: 3005506 — Cartesian equivariant representations for learning and understanding molecular orbitals
- **Authors:** King (UChicago/Berkeley), Grzenda (UChicago), Zhu (PME), **Hudson (ANL)**, **Foster (ANL)**, Cheng (Berkeley/IST Austria)
- **Year:** 2025 (Nov)
- **Domain:** Chemistry ML / equivariant deep learning
- **Link:** https://www.osti.gov/biblio/3005506
- **Paper DOI:** 10.1073/pnas.2510235122 (PNAS)
- **Code repo:** Foster/Hudson publish via Globus/DLHub + GitHub; probable repo under `foster-lab` or `bingqing-cheng`.
- **Core method:** Equivariant GNN (e3nn-style) that assigns chemically meaningful global labels (bonding / antibonding / localization) to Kohn–Sham molecular orbitals. Replication: generate a small QM9 subset with PySCF (HF or B3LYP), extract MO tensors, train an e3nn classifier on the bonding-character labels, match reported accuracy on held-out molecules.
- **Compute estimate:** 4–5 h (QM9 small subset + e3nn training on 1× A100).
- **Feasibility scores:**
  - Code available: 7/10
  - Compute tractable: 8/10
  - Domain clear: 8/10
  - Paper specific: 8/10
  - **Overall: 7.8/10**
- **Recommendation:** **ADD**
- **Rationale:** Ian Foster is ANL royalty; paper is chemistry-ML with clean open-source dependency (PySCF + e3nn). PNAS visibility.

### Paper 6: 3030077 — Attention-based functional-group coarse-graining: a deep learning framework for molecular prediction and design
- **Authors:** Han (UChicago/ANL-affiliated), Sun, Nealey, **de Pablo (UChicago/ANL)**
- **Year:** 2025 (Nov)
- **Domain:** Soft matter / polymers / molecular coarse-graining
- **Link:** https://www.osti.gov/biblio/3030077
- **Paper DOI:** 10.1038/s41524-025-01836-7 (npj Computational Materials)
- **Code repo:** de Pablo group publishes on GitHub; npj Comp Mat requires code availability.
- **Core method:** Transformer/self-attention operating on coarse-grained functional-group tokens of molecules; trained data-efficiently on polymer-property tasks. Replication: tokenize a public polymer set (e.g., PI1M or polymer genome) at functional-group level, train the attention model, match reported R² on property prediction.
- **Compute estimate:** 3–4 h on 1× A100.
- **Feasibility scores:**
  - Code available: 7/10
  - Compute tractable: 8/10
  - Domain clear: 8/10
  - Paper specific: 7/10
  - **Overall: 7.5/10**
- **Recommendation:** **ADD**
- **Rationale:** Closes the soft-matter / polymer gap with a real AI methods paper (not review).

### Paper 7: 2564521 — Expediting field-effect transistor chemical sensor design with neuromorphic spiking graph neural networks
- **Authors:** Ferreira (UChicago/ANL), Ding (UChicago/ANL), Zhang, Pu (UChicago/ANL), Donnat, Chen (UChicago), Chen (ANL)
- **Year:** 2025 (Mar)
- **Domain:** Neuromorphic / spiking GNN / chemical sensors
- **Link:** https://www.osti.gov/biblio/2564521
- **Paper DOI:** 10.1039/d4me00203b (Mol. Syst. Des. Eng.)
- **Code repo:** UChicago+ANL groups; likely public. Snntorch / NorseTorch-compatible.
- **Core method:** Spiking graph neural network (encodes molecules as graphs, message-passing via spiking neurons) to predict probe–analyte affinities for FET sensor design. Replication: reconstruct the spiking GNN in `snntorch` + PyG, train on a small molecule→affinity dataset (MoleculeNet), reproduce rank correlation numbers.
- **Compute estimate:** 3–4 h on 1× A100 (spiking nets are light).
- **Feasibility scores:**
  - Code available: 6/10
  - Compute tractable: 9/10
  - Domain clear: 7/10
  - Paper specific: 7/10
  - **Overall: 7.3/10**
- **Recommendation:** **ADD**
- **Rationale:** Directly fills the neuromorphic gap; model family has mature OSS (snntorch). Argonne-Chicago collaboration.

### Paper 8: 3020780 — Generative modeling enables molecular structure retrieval from Coulomb explosion imaging
- **Authors:** Li (SLAC), Jahnke (EuXFEL), Boll (EuXFEL), Han (Stanford), Xu (Stanford), Meyer (EuXFEL), …, **Ho (ANL)** — Nat. Commun.
- **Year:** 2026 (Mar)
- **Domain:** Photonics / XFEL / generative models for molecular structure
- **Link:** https://www.osti.gov/biblio/3020780
- **Paper DOI:** 10.1038/s41467-026-70160-5
- **Code repo:** Han/Xu are Jiaqi Han / Minkai Xu — authors of popular geometric generative codebases on GitHub.
- **Core method:** Conditional generative model (likely diffusion / flow-matching over 3D coordinates) that takes CEI momentum distributions as input and outputs molecular 3D geometry. Replication: use a published small-molecule dataset (QM9 or MD17) to synthesize a toy CEI-like signal (radial momentum projection) and train a conditional equivariant diffusion model; evaluate reconstruction RMSD for blind molecules.
- **Compute estimate:** 5–6 h on 1× A100 (ambitious, stretch).
- **Feasibility scores:**
  - Code available: 7/10
  - Compute tractable: 6/10
  - Domain clear: 7/10 (our replication will simplify the experimental CEI forward model)
  - Paper specific: 6/10
  - **Overall: 6.5/10**
- **Recommendation:** **ADD (stretch)**
- **Rationale:** The ambitious "stretch" pick; combines photonics + generative ML. Honest scope: we replicate the ML pipeline on synthetic CEI, not the actual LCLS data.

### Paper 9: 3030075 — Microsecond-latency feedback at a particle accelerator by online reinforcement learning on hardware
- **Authors:** Scomparin, Caselle, Santamaria Garcia, Xu, Blomley, Dritschler, … (ANL listed as research_org)
- **Year:** 2026 (Apr)
- **Domain:** Accelerator physics / HEP / edge-RL / FPGA
- **Link:** https://www.osti.gov/biblio/3030075
- **Paper DOI:** 10.1088/2632-2153/ae5b20 (Machine Learning: Science and Technology)
- **Code repo:** hls4ml/KCU-based; MLST requires code. Look on GitHub under KIT/Argonne accelerator AI.
- **Core method:** Online RL policy (tiny neural network, likely actor-critic) deployed on FPGA to provide microsecond-latency feedback control of a particle-accelerator subsystem. Replication: reproduce the policy architecture in PyTorch on a **simulated** accelerator environment (simple LQR / cart-pole-with-delay surrogate that matches the paper's reward and latency budget), match reward curves and reaction-time statistics.
- **Compute estimate:** 3 h on CPU (RL is small-network).
- **Feasibility scores:**
  - Code available: 7/10
  - Compute tractable: 9/10 (simulation-only)
  - Domain clear: 7/10
  - Paper specific: 7/10
  - **Overall: 7.5/10**
- **Recommendation:** **ADD**
- **Rationale:** HEP/accelerator + edge AI is a hot ANL theme. Replication avoids the real FPGA hardware by simulating the environment — honest caveats included.

### Paper 10: 2540219 — Bayesian Calibration of Stochastic Agent Based Model via Random Forest
- **Authors:** Robertson (Sandia), Safta (Sandia), **Collier (ANL)**, **Ozik (ANL)**, Ray (Sandia)
- **Year:** 2025 (Mar)
- **Domain:** Epidemiology / agent-based models / UQ / surrogate-based Bayesian calibration
- **Link:** https://www.osti.gov/biblio/2540219
- **Paper DOI:** 10.1002/sim.70029 (Statistics in Medicine)
- **Code repo:** Collier/Ozik publish ABM code (CityCOVID, Repast) on GitHub; Sandia QUESO/Dakota is open.
- **Core method:** Calibrates a stochastic ABM by training a random-forest surrogate on a modest design of model runs, then doing Bayesian inference on the surrogate (replacing the expensive ABM likelihood). Replication: use a small Python-native ABM (e.g., NetworkX-based SIR on Chicago synthetic population, or Repast-Py), generate a Latin-hypercube sweep, fit sklearn RF, run emcee / UltraNest over surrogate, compare posterior coverage vs. paper.
- **Compute estimate:** 3–4 h on CPU.
- **Feasibility scores:**
  - Code available: 8/10
  - Compute tractable: 9/10
  - Domain clear: 9/10
  - Paper specific: 9/10
  - **Overall: 8.8/10**
- **Recommendation:** **ADD** (high confidence)
- **Rationale:** Fills the epidemiology / ABM gap with an ANL-authored methods paper. Very replicable — RF surrogate + MCMC is textbook.

### Paper 11: 3018329 — Propagating synthetic populations with dynamic Bayesian networks: a framework for long-horizon demographic forecasting
- **Authors:** Oshanreh (UW), **Khan (ANL)**, MacKenzie (UW)
- **Year:** 2025 (Dec)
- **Domain:** Demography / social simulation / DBN
- **Link:** https://www.osti.gov/biblio/3018329
- **Paper DOI:** 10.1016/j.tbs.2025.101226 (Travel Behaviour and Society)
- **Code repo:** PSID data is public; DBN toolkits (pgmpy, bnlearn) open.
- **Core method:** Learns two Dynamic Bayesian Networks (individual- and household-level) from PSID longitudinal panels, then forwards-simulates 1000 runs over 24 years of life-event transitions (employment, childbirth, marriage, etc.). Replication: download PSID subset (or use `bnlearn` synthetic dataset), fit DBN with pgmpy, forward-simulate, compare aggregate demographic trajectories.
- **Compute estimate:** 2–3 h on CPU.
- **Feasibility scores:**
  - Code available: 7/10 (PSID access process)
  - Compute tractable: 10/10
  - Domain clear: 8/10
  - Paper specific: 8/10
  - **Overall: 8.3/10**
- **Recommendation:** **ADD**
- **Rationale:** Rare social-science / demographic AI paper in our portfolio; cheap to replicate; ANL co-author.

### Paper 12: 2586547 — Assessment of fine-tuned large language models for real-world chemistry and material science applications
- **Authors:** Van Herck, Gil, Jablonka, Abrudan, … (EPFL-lead, Argonne as research_org — likely via Ramanathan lab / Jablonka ANL affiliation)
- **Year:** 2024 (Nov)
- **Domain:** LLMs for chemistry / materials
- **Link:** https://www.osti.gov/biblio/2586547
- **Paper DOI:** 10.1039/d4sc04401k (Chemical Science)
- **Code repo:** Jablonka's group publishes `chemlift` / `gptchem` on GitHub.
- **Core method:** Fine-tunes open-weights LLMs (e.g., Llama-2, Mistral) on chemistry/materials property-prediction tasks expressed in natural language; benchmarks accuracy vs. classical ML and vs. GPT-3.5. Replication: take 1–2 of the paper's tasks (e.g., solubility, band-gap prediction), reuse `gptchem`-style prompting to fine-tune a 7B model with LoRA on uicgpu, reproduce R²/MAE numbers.
- **Compute estimate:** 5–6 h on 1× A100 (LoRA fine-tune of 7B).
- **Feasibility scores:**
  - Code available: 9/10 (gptchem open)
  - Compute tractable: 7/10
  - Domain clear: 8/10
  - Paper specific: 8/10
  - **Overall: 8.0/10**
- **Recommendation:** **ADD**
- **Rationale:** Representative LLM-for-science paper with ANL in research_orgs. Timely; reusable infrastructure for future LLM replications.

### Paper 13: 3001927 — Machine learning enabled discovery of superhard and ultrahard carbon polymorphs
- **Authors:** Balasubramanian (UIC/ANL), Manna (UIC/ANL), Banik (UIC/ANL), Srinivasan (UIC/ANL), … (ANL Center for Nanoscale Materials)
- **Year:** 2025 (Nov, online 2024)
- **Domain:** Materials / inverse design / evolutionary + ML
- **Link:** https://www.osti.gov/biblio/3001927
- **Paper DOI:** 10.1016/j.commatsci.2024.113506
- **Code repo:** Sankaranarayanan/Banik group publishes on GitHub (SCAN-ML); USPEX / evolutionary-search codes open.
- **Core method:** Couples an evolutionary structure search with an ML surrogate (likely GAP or SOAP+GPR) for hardness/formation-energy to find novel superhard carbon polymorphs; validates with DFT. Replication: use a small pre-trained C interatomic potential (MACE-OFF carbon or Allegro-C), run a constrained evolutionary search (ASE + PyXtal) for 100 random C16 seeds, rank by predicted hardness proxy (elastic constants).
- **Compute estimate:** 4–5 h on 1× A100 or mixed.
- **Feasibility scores:**
  - Code available: 7/10
  - Compute tractable: 7/10
  - Domain clear: 8/10
  - Paper specific: 7/10
  - **Overall: 7.3/10**
- **Recommendation:** **DEFER** (materials already well-represented; keep on shelf)
- **Rationale:** Solid paper, but our materials/ML slice is the most saturated domain. Add only if we drop one of the current materials entries.

### Paper 14: 3008127 — Modeling COVID-19 Impacts on Prison Population
- **Authors:** Martinez-Moyano (ANL), Macal (ANL)
- **Year:** 2025 (May)
- **Domain:** Epidemiology / system dynamics / ABM
- **Link:** https://www.osti.gov/biblio/3008127
- **Paper DOI:** 10.2172/3008127 (Technical Report)
- **Core method:** System-dynamics / ABM hybrid for COVID-19 spread in Illinois prison system. Replication: build a compartmental SEIR + prison-flow model in PyDSTool or `epiabm`, tune to the report's parameters, compare trajectory predictions.
- **Compute estimate:** 2–3 h on CPU.
- **Feasibility scores:**
  - Code available: 3/10 (tech report, no GitHub expected)
  - Compute tractable: 9/10
  - Domain clear: 6/10
  - Paper specific: 5/10 (high-level concept model; spec may be thin)
  - **Overall: 5.8/10**
- **Recommendation:** **SKIP** (tech report + thin spec)
- **Rationale:** Not a journal paper and methodology may be underspecified. Include in the assessed-15 for completeness, but don't add to active set — Paper 10 (Robertson/Collier/Ozik) already carries the ABM flag with a much stronger spec.

### Paper 15: 3013579 — Transforming jet flavour tagging at ATLAS (GN2)
- **Authors:** ATLAS Collaboration (~2938 authors; ANL is a Tier-1 ATLAS institution; listed research_orgs are UC Berkeley / Colorado, but ANL contracts SC0018988/SC0021046 appear in the contract string)
- **Year:** 2026 (Jan)
- **Domain:** HEP experimental ML / transformer flavour tagging
- **Link:** https://www.osti.gov/biblio/3013579
- **Paper DOI:** 10.1038/s41467-025-65059-6 (Nat. Commun.)
- **Code repo:** ATLAS released **GN2 code publicly** (salt / umami frameworks, github.com/umami-hep). Public datasets (R22 PFlow jets) via CERN OpenData + GN2 training ntuples.
- **Core method:** Transformer (attention over tracks+constituents) producing b / c / light quark classification probabilities per jet. Replication: pull the public GN2 training dataset (small subset), train a scaled-down GN2-lite (4 layers, ~1M params) in `salt`, reproduce ROC-AUC for b-tagging on a held-out subset.
- **Compute estimate:** 5–6 h on 1× A100 (with a subset).
- **Feasibility scores:**
  - Code available: 9/10 (umami-hep + ATLAS OpenData)
  - Compute tractable: 7/10
  - Domain clear: 8/10
  - Paper specific: 9/10
  - **Overall: 8.3/10**
- **Recommendation:** **ADD (stretch, with caveat)**
- **Rationale:** ATLAS affiliation is ANL-partial at best (ANL isn't in the paper's `research_orgs` field), but the **code + data are truly open**, and the method is the canonical modern HEP transformer result. Score honestly as "ANL-adjacent" in the portfolio. If Rick wants pure-ANL-provenance purism, swap this for another.

---

## Domain Coverage After Additions

Assuming we **ADD** Papers 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15 (13 adds), and defer/skip 13 and 14:

| Domain | Current (30) | Proposed Add | After |
|--------|-------------:|-------------:|------:|
| Materials / ML | 4 | 0 (13 deferred) | 4 |
| DFT / Physical chem | 2 | 0 | 2 |
| Chemistry ML (orbitals, coarse-grain, LLM) | 0 | 3 (5, 6, 12) | 3 |
| Nuclear (reactor, VMC, CHF) | 3 | 0 | 3 |
| Astrophysics | 3 | 0 | 3 |
| Quantum | 2 | 0 | 2 |
| Combustion | 1 | 0 | 1 |
| Dark matter / particle | 1 | 0 | 1 |
| HEP experimental | 0 | 1 (15 ATLAS) | 1 |
| Accelerator / edge-RL | 0 | 1 (9) | 1 |
| Condensed matter | 3 | 0 | 3 |
| Power / electrical | 2 | 0 | 2 |
| ML methods (BO, NODE, MT) | 3 | 0 | 3 |
| Graph algorithms | 2 | 0 | 2 |
| Bioinformatics | 2 | 1 (4 EC-Bench) | 3 |
| Drug / protein design | 0 | 1 (3 GenSLM) | 1 |
| Neuromorphic / spiking | 0 | 1 (7) | 1 |
| Math | 1 | 0 | 1 |
| MD / MSM | 1 | 0 | 1 |
| Control | 1 | 0 | 1 |
| FDTD / PDE | 1 | 0 | 1 |
| CFD / fluid ML | 0 | 1 (2) | 1 |
| Fusion / plasma | 0 | 1 (1) | 1 |
| Photonics / XFEL imaging | 0 | 1 (8) | 1 |
| Soft matter / polymers | 0 | 1 (6) | 1 |
| Epidemiology / ABM / social | 0 | 2 (10, 11) | 2 |
| **TOTAL** | **30** | **+13** | **43** |

(If Rick wants exactly 40, drop Paper 8 *and* Paper 15 — they are the two stretch picks. That yields 30 + 11 = 41; drop the ATLAS one for 40 if strict.)

---

## Recommended final "Add these ~10" slate (if Rick picks conservatively)

Ordered by confidence (highest first):
1. **Paper 4 (3012452)** EC-Bench — 9.0
2. **Paper 10 (2540219)** Bayesian ABM calibration — 8.8
3. **Paper 2 (2587579)** Mesh super-resolution GNN — 8.3
4. **Paper 11 (3018329)** DBN demographic forecasting — 8.3
5. **Paper 15 (3013579)** ATLAS GN2 jet tagging — 8.3 *(swap-out candidate if ANL purism)*
6. **Paper 12 (2586547)** Fine-tuned LLMs chemistry — 8.0
7. **Paper 5 (3005506)** Equivariant molecular orbitals — 7.8
8. **Paper 3 (3014231)** GenSLM tryptophan synthases — 7.8
9. **Paper 1 (2587945)** ELM fusion NN — 7.5
10. **Paper 9 (3030075)** RL FPGA accelerator — 7.5
11. **Paper 6 (3030077)** Polymer coarse-graining — 7.5
12. **Paper 7 (2564521)** Spiking GNN FET — 7.3

**Defer:** Paper 13 (carbon polymorphs, materials already saturated), Paper 8 (stretch — photonics generative), Paper 14 (tech report, thin spec)

---

_End of candidate list. Generated by subagent candidates-40papers on 2026-04-24._
