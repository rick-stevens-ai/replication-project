# Attempt log — BVBRC-120

Chronological log (Sun 2026-07-05, ~16:18-16:45 CDT)

- **16:19** Target dir created (`~/Dropbox/REPLICATE-PROJECT/BVBRC-120-Bacillus-phage-genomes-Zhang2023/{report/evidence,extraction,work}`). Confirmed non-existent (no overwrite).
- **16:20** PubMed esummary for PMID 37337195 → confirmed title, DOI, PMC. First (WRONG) attempt: fabricated URL `10.1186/s12866-023-02921-x.pdf`; downloaded 8.2 MB PDF but pdftotext showed it was the Zhang J. wound-infection paper. ⚠ mistake logged.
- **16:22** Refetched with correct DOI `10.1186/s12866-023-02907-9`; 10.26 MB PDF verified as the Zhang Y. Bacillus phage paper. Copied to `paper.pdf`.
- **16:22** `pdftotext` of paper → 777 lines. Located methods section (line 470+): 178 host strains + 236 lytic phages, cutoff 30-Dec-2022; tools = PHASTER, GeneMark, WebMGA, VIRIDIC, RAST, Mauve, Easyfig, MAFFT, MView.
- **16:23** Fetched all 9 supplementary XLSX from Springer via uicgpu curl. All present (10-24 KB each).
- **16:23** Parsed S1/S4/S9 via openpyxl → 178 host strains, 20 focal accessions, 236 lytic accessions extracted to CSV.
- **16:24** Env probe on uicgpu: bvbrc56 has efetch/blastn/mafft; bvbrc76 has prokka/fasttree/mafft/blastn. Missing: mmseqs2, iqtree, seqkit → `mamba install -c bioconda mmseqs2 iqtree seqkit` into bvbrc76 (~30 s).
- **16:25** Wrote + launched `download.sh` on uicgpu (`nohup` background). 5 batches of ≤50 accessions via `efetch`.
- **16:26** Download complete: 231/236 unique genomes returned (22 MB FASTA). 5 dropped by NCBI dedup.
- **16:26** Wrote + launched `analyze.sh`: seqkit stats, prodigal, MMseqs2, MASH sketch, phylogeny.
- **16:27** Genome length + GC computed on 231 genomes. Prodigal returned 35,069 predicted proteins.
- **16:28** MMseqs2 clustered 35,069 proteins → 6,875 clusters (30% id, 50% cov). MASH sketched 231 individual FASTA files → 53,361 pairwise-distance rows.
- **16:28** analyze.sh subshell hit two failures: (a) proxy did not propagate → efetch of 13 missing focal accessions failed with DNS resolution error; (b) `import pandas` missing in bvbrc76.
- **16:29** Fixed proxy with hardcoded exports, fetched the 13 missing accessions → 20/20 focal genomes. `pip install pandas numpy` in bvbrc76.
- **16:30** Rewrote as `phase2.sh` — separate prodigal for 20, re-sketch MASH per individual FASTA, MAFFT alignment, IQ-TREE. MAFFT started chugging on divergent 20-genome panel.
- **16:33** MAFFT still running after ~4 min. Decision: kill MAFFT (divergent phage panel is unalignable end-to-end), substitute rapidnj BIONJ on MASH matrix (paper itself uses VIRIDIC ≈ same class of method).
- **16:34** Wrote `phase3.sh`: full pandas analytics + rapidnj tree + MMseqs2 on 20-phage proteome.
- **16:35** `phase3.sh` complete. Summary numbers:
  - 231 genomes: length 7.4-497.5 kb (median 58.5), GC 27.7-50.1% (mean 38.0)
  - MASH pairwise: mean d = 0.940, 92.7% pairs unrelated
  - 35,069 proteins → 6,875 clusters, 3,351 singletons, largest cluster = 99
  - 20 focal genomes: length 18.8-164.3 kb, GC 30.7-43.8%, no core proteins shared by all 20
  - BIONJ tree in Newick recovered clear Wbetavirus + SPP1-like sub-clades
- **16:36** rsync-ed all evidence + logs back to local Dropbox target dir.
- **16:37** Launched Marker (data/stevens/envs/marker) + Nougat (gpustor/anaconda3/envs/nougat) in parallel on uicgpu for `extraction/marker.md` + `extraction/nougat.mmd`.
- **16:38-16:44** Wrote `brief.md`, `REPORT.md`, `open_questions.json` (5 heavy questions with next-steps), `workflow.md`, `artifacts_summary.md`, `failure_analysis.md`, this attempt log, `artifact_harvest.md`.
- **16:45** Compiled LaTeX report to `REPORT.tex`.
- **16:47** Marker + Nougat parses complete; rsync-ed to `extraction/`.
- **16:48** 8-artifact completion bar verified. WAVE_RESULT emitted.
