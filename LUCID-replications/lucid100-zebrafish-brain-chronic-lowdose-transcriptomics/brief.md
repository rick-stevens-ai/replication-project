# Brief — Cantabella et al. 2022 (Zebrafish brain transcriptomics under chronic low-dose-rate γ)

**Paper:** Cantabella E, Camilleri V, Cavalie I, Dubourg N, Gagnaire B, Charlier TD, Adam-Guillermin C, Cousin X, Armant O. *Revealing the Increased Stress Response Behavior through Transcriptomic Analysis of Adult Zebrafish Brain after Chronic Low to Moderate Dose Rates of Ionizing Radiation.* Cancers 14(15):3793 (2022). DOI: 10.3390/cancers14153793.

**Topic:** Adult zebrafish exposed for 36 days to chronic γ-irradiation at 0.05, 0.5, or 5 mGy/h. RNA-seq on the telencephalon, followed by RNA in-situ hybridisation in the parvocellular preoptic nucleus (oxytocin, cone–rod homeobox upregulation confirmed). Behavioural assays: hypolocomotion, increased freezing, social stress. Headline numerical result: dose-rate-dependent increase in differentially expressed genes (DEGs) — **27 DEGs at 0.05 mGy/h, 200 DEGs at 0.5 mGy/h, 530 DEGs at 5 mGy/h**.

**LUCID relevance:** Open-access transcriptomic study with deposited raw data (GEO accession **GSE206573**, mentioned 4× in the full text). A genuine replication would re-run STAR/Salmon → DESeq2/edgeR on GSE206573 and recover the 27/200/530 DEG counts within tolerance. That is feasible but **out of scope for a free-local-CPU, single-shot writeup pass** (RNA-seq alignment of 36 zebrafish samples is GB-scale download + GPU/CPU-hours of work).

**Decision:** **SPOT-CHECK only.** Confirm that (a) the DEG counts stated in the abstract are stated identically in the body of the full text, (b) the GEO accession is present and parses, and (c) the dose-rate / exposure-duration / tissue claims are internally consistent. This validates the paper's internal numerical bookkeeping without re-running the RNA-seq pipeline.
