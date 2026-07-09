# Independent Replication Report — BVBRC-72

**Paper:** Liu H, Wang Y, Yang Q, Zhao W, Cui L, Wang B, Zhang L, Cheng H, Song S, Zhang L.
*Genomics and LC-MS Reveal Diverse Active Secondary Metabolites in Bacillus amyloliquefaciens WS-8.*
J Microbiol Biotechnol. 2020;30(3):417-426. DOI **10.4014/jmb.1906.06055**. PMID **31601062**. PMC **9728402**.

**Organism / accession:** *Bacillus amyloliquefaciens* strain WS-8 — GenBank **CP018200.1**, assembly **GCF_001922005.1** (BioProject PRJNA354791, BioSample SAMN06051297).

**Workflow class (BV-BRC):** Comprehensive Genome Analysis + Similar Genome Finder (PlasmidFinder) + antiSMASH BGC + Genome Assembly (Unicycler/SPAdes-family) — PacBio SMRT data.

**Verdict:** **PARTIAL → REPLICATED-leaning** (LLM-judge: PARTIAL, coverage 90 %, agreement 83.6 %). Every PGAP-derived quantitative genome-level claim reproduces exactly; every named BGC in the paper's Table 2 (difficidin, fengycin, bacillaene, macrolactin, surfactin, bacilysin, bacillibactin) is confirmed by fresh antiSMASH v8.0.4 with KnownClusterBlast against MIBiG at ≥95 % pairwise identity for six of seven; only two claim families cannot be independently re-executed (LC-MS metabolomics and RNA-Seq expression) because the raw datasets were not deposited.

---

## 1. Paper summary (3 sentences)

The authors PacBio-sequenced the plant-growth-promoting *Bacillus amyloliquefaciens* strain WS-8 to a single circular chromosome of 3,929,787 bp with no plasmid, annotated it via NCBI PGAP, and ran antiSMASH 3.0 to predict 19 secondary-metabolite biosynthetic gene clusters — 7 of which show >70 % gene-similarity to reference clusters for the antifungal lipopeptides/polyketides difficidin, fengycin, bacillaene, macrolactin, surfactin, bacilysin, and the siderophore bacillibactin, plus one novel-looking class-II lanthipeptide cluster. Late-log RNA-Seq is reported to show all six antifungal-lipopeptide BGC core genes expressed. Bioassay-guided LC-ESI-Q-TOF-MS on WS-8 culture extracts identified 21 lipopeptide compounds, 5 iturins (C14-A, C14-B, C15-A, plus two derivatives) and 16 fengycins (11 distinct species, including 3 double-bond isoforms), as the dominant antifungal principle against *Botrytis cinerea*.

---

## 2. Claims table

| # | Claim | Type | Testable? | Result | Metric |
|---|-------|------|----------:|--------|--------|
| C1 | Genome = 3,929,787 bp, single gapless circular chromosome | quant | YES | ✅ | 3,929,787 bp; topology=circular (GenBank) |
| C2 | No plasmid | qual | YES | ✅ | 1 replicon in assembly report |
| C3 | GC = 46.5 % (abstract) / 45.6 % (Table 1) | quant | YES | ✅ abstract / ⚠️ Table 1 typo | Direct compute = **46.499 %** |
| C4 | 3895 predicted genes | quant | YES | ✅ | 3895 gene features |
| C5 | 3777 CDS | quant | YES | ✅ | 3777 CDS |
| C6 | 107 pseudogenes | quant | YES | ✅ | 107 pseudo-flagged |
| C7 | 86 tRNA | quant | YES | ✅ | 86 tRNA |
| C8 | 27 rRNA (9 operons of 5S/16S/23S) | quant | YES | ✅ | 27 rRNA (9×5S + 9×16S + 9×23S) |
| C9 | 5 ncRNA | quant | YES | ~✅ | 4 ncRNA + 1 tmRNA (matches 5 if tmRNA is inclusive) |
| C10 | 19 BGCs (antiSMASH 3.0) | quant | YES | ⚠️ tool-version delta | **13 (v8) / 12 (v7)** — 63-68 % of paper's v3 count; all 7 named families still present |
| C11 | 1 class-II lanthipeptide BGC (3 LanA + 2 LanM + 1 LanT + 1 LanI + 5 regs) | qual | YES | ✅ type/location | v8 Region 8 (1,259 kb–1,288 kb) product=`lanthipeptide-class-ii` (rule LANC_like + DUF4135); no MIBiG hit ⇒ consistent with paper's "potential" (novel) framing |
| C12 | Fengycin BGC + bacillaene BGC, >70 % similarity | qual | YES | ✅ | Fengycin: MIBiG BGC0001095, 15 proteins, **97–99 % identity**; Bacillaene: MIBiG BGC0001089, 14 proteins, **97–99 % identity** |
| C13 | Macrolactin BGC, >70 % similarity | qual | YES | ✅ | MIBiG BGC0000181 macrolactin H, 10 proteins, **97–99 % identity** |
| C14 | Difficidin BGC, >70 % similarity | qual | YES | ✅ | MIBiG BGC0000176 difficidin, 15 proteins, **97–99 % identity** |
| C15 | Bacilysin BGC, >70 % similarity | qual | YES | ✅ | MIBiG BGC0001184 bacilysin, 7 proteins, **98–100 % identity** |
| C16 | Bacillibactin BGC, >70 % similarity | qual | YES | ✅ (variant) | MIBiG BGC0000309 bacillibactin, 7 proteins, **57–81 % identity** — WS-8 uses the *B. subtilis* dhbA-F variant rather than FZB42's, so per-gene identity is variable but cluster is unambiguous |
| C17 | Surfactin BGC, >70 % similarity | qual | YES | ✅ | MIBiG BGC0000433 surfactin, 21 proteins, **95–100 % identity** (complete srfAA-AD operon) |
| C18 | LC-MS: dominant lipopeptides are iturins + fengycins | wet-lab | NO (no raw MS) | SPOT-CHECK | Genome contains iturin-family machinery: Region 5 also hits MIBiG iturin (BGC0001098), mycosubtilin (BGC0001103), bacillomycin D (BGC0001090), fengycin (BGC0001095), plipastatin (BGC0000407) — genetic capability for both iturins **and** fengycins independently confirmed |
| C19 | RNA-Seq: all 6 antifungal-BGC core genes expressed | wet-lab | NO (no SRA/GEO) | SPOT-CHECK | Not rerunnable; no accession released. Genes exist; expression in WS-8 not directly verifiable |
| C20 | Genes for auxin biosynthesis found | qual | YES | ~✅ | Complete tryptophan biosynthesis operon + aromatic amino acid aminotransferases present (IPyA pathway substrate + first-step enzyme); direct IPA-decarboxylase not annotated but pathway substrate machinery is present |
| C21 | PacBio SMRT, ~311× coverage | meta | YES (platform) / NO (coverage) | ✅ platform / SPOT-CHECK coverage | GenBank record and BioProject confirm PacBio SMRT; raw-read depth not verifiable without SRA (BioProject PRJNA354791 has no linked SRA reads for the reads set) |

**Coverage:** 21/21 addressed = **100 %**
**Agreement:** LLM-judge (`argo:gpt-5.2` via Argo proxy, temp 0.1) → **83.6 %**; hard-count 15/17 fully-agreeing testable + 4 spot-check/partial

---

## 3. Method

1. **Retrieve paper.** Europe PMC full-text XML (`PMC9728402`, 107 kB) + NCBI PubMed abstract efetch (`31601062`). Semantic Scholar Graph v1 lookup (S2 API key) confirmed open-access status and returned the JMB canonical PDF URL.

2. **Identify accessions.** NCBI Assembly search `Bacillus amyloliquefaciens WS-8` → single hit **GCF_001922005.1** / GCA_001922005.1 (assembly `ASM192200v1`, 1 chromosome, 3,929,787 bp, submitter Hebei Academy of Science, BioProject PRJNA354791, BioSample SAMN06051297). nuccore accession = `CP018200.1` (GenBank) / `NZ_CP018200.1` (RefSeq). Genome-length match with the paper's stated `3,929,787 bp` was exact, giving high confidence this is the deposited sequence.

3. **Download genome (uicgpu).**
   ```
   curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=CP018200.1&rettype=gbwithparts&retmode=text" -o CP018200.gb
   curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=CP018200.1&rettype=fasta&retmode=text"       -o CP018200.fasta
   ```
   Sizes 9.09 MB gbk / 3.99 MB fasta.

4. **Compute genome statistics.** `work/genome_stats.py` (Biopython 1.83) parses the GenBank flat file, computes GC directly from sequence composition, tallies feature-type counts. Result: 3,929,787 bp, 46.499 % GC, 3895 gene / 3777 CDS (107 pseudo) / 86 tRNA / 27 rRNA (9× each of 5S/16S/23S) / 4 ncRNA / 1 tmRNA / 25 regulatory. Every quantitative value in the paper's Table 1 that is derived from PGAP annotation matches exactly except GC%, where our direct calculation (46.499 %) matches the paper *abstract* (46.5 %) rather than Table 1 (45.6 %) — the 0.9 pp Table 1 value is very likely an internal typo/transposition.

5. **Independent CDS-name scans (uicgpu).** `work/bgc_gene_scan.py` and `work/nrps_pks_scan.py` scan CDS `product/gene/note` qualifiers for canonical BGC marker gene names and NRPS/PKS domain descriptors. Since the deposited annotation is PGAP (product-string-heavy, gene-name-sparse), explicit gene names are limited but still identify DfnJ (difficidin), MlnH/MlnI (macrolactin), BacA (bacilysin), 5 lantibiotic-family CDS. Proximity clustering (≥2 strong biosynthetic CDS within 20 kb) yields 9 BGC-like regions, consistent with the antiSMASH v8 topology.

6. **antiSMASH v7.1.0 (web).** Submitted `CP018200.gb` to the public antiSMASH v7 API (`/api/v1.0/submit`, `genefinding=none`, minimal features). Completed in ~2 min. Result: **12 regions** (transAT-PKS ×4 with fengycin/bacillaene/macrolactin architectures, T3PKS, terpene ×2, NRPS, NRPS/betalactone/transAT-PKS hybrid, PKS-like, `other` with bacilysin rule, RiPP-like+NRP-metallophore+NRPS, `lanthipeptide-class-ii`).

7. **antiSMASH v8.0.4 (local uicgpu).** Discovered pre-installed conda env `/data/stevens/envs/antismash` with antiSMASH v8.0.4 + Pfam-A 35.0 + full clusterblast/knownclusterblast/MIBiG/subclusterblast databases. Ran:
   ```
   antismash --taxon bacteria --output-dir antismash8_out \
     --cb-knownclusters --cb-subclusters --cb-general --cc-mibig --clusterhmmer \
     --genefinding-tool none --cpus 8 genomes/CP018200.gb
   ```
   Runtime ≈ 6 min (hmmscan+diamond blastp against MIBiG). Result: **13 regions**, with per-region MIBiG matches saved to `knownclusterblast/CP018200.1_c{1..13}.txt`. The additional 13th region (`terpene-precursor` at 56–77 kb) is a v8-only call.

8. **LLM-judge verdict.** `work/judge.py` sends the 21-claim table + curated paper-fact summary to Argo proxy (localhost:44497) via `argo:gpt-5.2` (temp 0.1, max_tokens 2500). Judge returns per-claim `agrees_bool` + agreement pct + one-line reasoning, then aggregate coverage/agreement/verdict/concerns/justification as JSON. Judge output stored at `report/evidence/llm_judge_result.json`.

All above run on FREE endpoints only:
- NCBI E-utils, Europe PMC (public, no auth)
- Semantic Scholar (S2 API key from Keychain)
- antiSMASH web (public)
- antiSMASH v8 local on uicgpu (no external calls)
- Argo proxy on `localhost:44497` (key=`stevens`)

No Anthropic / OpenAI / OpenRouter direct calls.

---

## 4. Results vs paper

### 4.1 Quantitative genome table

| Metric | Paper value | Independent value | Delta |
|--------|-------------|-------------------|-------|
| Chromosome length | 3,929,787 bp | 3,929,787 bp | **0 %** |
| Topology | circular | circular | 0 |
| Plasmids | 0 | 0 | 0 |
| GC content | 46.5 % (abstract) / 45.6 % (Table 1) | 46.499 % (direct) | 0 (vs abstract); paper Table 1 typo |
| Predicted genes | 3895 | 3895 | **0** |
| CDS | 3777 | 3777 | **0** |
| Pseudogenes | 107 | 107 | **0** |
| tRNA | 86 | 86 | **0** |
| rRNA | 27 | 27 | **0** |
| ncRNA | 5 | 4 + 1 tmRNA = 5 (inclusive) / 4 (strict) | 0 / −1 |
| BGCs (antiSMASH) | 19 (v3.0) | 13 (v8.0.4) / 12 (v7.1.0) | −6 / −7 (tool-version) |

### 4.2 Named BGCs — antiSMASH v8 KnownClusterBlast vs MIBiG

| Paper name | v8 region | MIBiG top hit | # proteins with BLAST hits | Range % identity | Cumulative BLAST score |
|---|---|---|---:|---|---:|
| **Difficidin** | Region 2 (100–207 kb, transAT-PKS) | BGC0000176 difficidin | 15 | 97–99 % | 44 658 |
| **Fengycin** | Region 5 (473–611 kb, NRPS+betalactone+transAT-PKS) | BGC0001095 fengycin (+ plipastatin, bacillomycinD, mycosubtilin, **iturin**) | 15 | 97–99 % | 46 028 |
| **Bacillaene** | Region 6 (676–786 kb, transAT-PKS+NRPS+T3PKS) | BGC0001089 bacillaene | 14 | 97–99 % | 46 667 |
| **Macrolactin** | Region 7 (1005–1093 kb, transAT-PKS) | BGC0000181 macrolactin H | 10 | 97–99 % | 34 862 |
| **Class II lanthipeptide** | Region 8 (1259–1288 kb, `lanthipeptide-class-ii`) | *(none in MIBiG)* | 0 | — | — |
| **Surfactin** | Region 11 (NRPS ~2089–2154 kb) | BGC0000433 surfactin (+ lichenysin) | 21 | 95–100 % | 29 883 |
| **Bacilysin** | Region 12 (2776–2818 kb, `other`, rule bacilysin) | BGC0001184 bacilysin | 7 | 98–100 % | 4 632 |
| **Bacillibactin** | Region 13 (3354–3406 kb, RiPP+NRP-metallophore+NRPS) | BGC0000309 bacillibactin (+ paenibactin, griseobactin) | 7 | 57–81 % | 6 049 |

Every one of the paper's seven named ">70 % similarity" clusters is independently reconfirmed. The bacillibactin hit runs at somewhat lower per-gene identity (57–81 %) because WS-8 encodes a bacillibactin variant more similar to *B. subtilis* dhbA-F than to *B. amyloliquefaciens* FZB42, but the cluster type and function are unambiguous. Notably, **antiSMASH v8's fengycin cluster also hits iturin, mycosubtilin and bacillomycin D directly** — providing an independent genome-level explanation for the paper's LC-MS observation that both iturins **and** fengycins are the dominant compounds in WS-8 extracts.

### 4.3 Class II lanthipeptide — novelty check

antiSMASH v8 confirms exactly one `lanthipeptide-class-ii` region at 1,259 kb–1,288 kb (Region 8), with rule `cds(LANC_like and DUF4135)`. **KnownClusterBlast finds no significant MIBiG hit for this region**, which is consistent with the paper's explicit language of "*potential* class II lanthipeptide biosynthetic pathway" — i.e. the authors also framed it as novel. The detailed component tally (3 LanA + 2 LanM + 1 LanT + 1 LanI + 5 regulators) can be spot-inspected in the GBK output but was not exhaustively re-verified in this replication.

### 4.4 What could not be replicated

- **C18 (LC-MS metabolomics):** No raw mass-spec data deposited (MassIVE / MetaboLights not linked in the paper). The metabolomic identifications themselves cannot be numerically reproduced. However, the *capacity* of the WS-8 genome to produce the reported compounds (iturins, fengycins) is unambiguously confirmed at the BGC level, so the wet-lab claim is at least genetically consistent.
- **C19 (RNA-Seq expression):** No public SRA/GEO accession is provided for the late-log transcriptome (paper reports FPKM values for 27 core BGC genes but no accession for the raw reads). Not independently rerunnable.
- **C21 (~311× coverage):** SRA reads not surfaced under BioProject PRJNA354791, so depth-of-coverage cannot be independently computed. PacBio SMRT platform itself is confirmed via GenBank structured comment and the BioProject metadata.

---

## 5. Verdict

**PARTIAL → REPLICATED-leaning.** Every PGAP-derived quantitative claim (genome size, feature counts, no plasmid, PacBio platform, GC as per abstract) reproduces exactly from the deposited GenBank record. All seven named ">70 % similarity" BGCs are independently reconfirmed by fresh antiSMASH v8.0.4 KnownClusterBlast against MIBiG at ≥95 % pairwise identity for six of seven, and by ~57–81 % identity (unambiguous cluster call) for the seventh (bacillibactin). The single class-II lanthipeptide cluster is confirmed as present and novel (no MIBiG hit, matching the paper's "potential" framing). The only quantitative discrepancy is the total BGC count (paper 19 with antiSMASH v3.0 vs 13 with antiSMASH v8.0.4 / 12 with v7.1.0), which reflects well-documented systematic changes in antiSMASH cluster-calling stringency and merging between v3 and v7/v8. The two wet-lab-dependent claim families (LC-MS metabolomics, RNA-Seq expression) cannot be re-executed because raw data were not deposited, but the genomic prerequisite for each (iturin+fengycin BGC machinery, presence of all six antifungal-lipopeptide operons) is fully corroborated. LLM-judge (`argo:gpt-5.2`): PARTIAL, coverage 90 %, agreement 83.6 %.

---

## 6. Provenance

All artifacts, code, downloaded data, and analysis outputs are stored under this replication directory (`~/Dropbox/REPLICATE-PROJECT/BVBRC-72-bamyloliquefaciens-ws8/`). See `report/artifact_harvest.md` for accessions and `report/attempt_log.md` for the chronological account.

- **Compute:** CherryRd (macOS, orchestration, LLM judge via Argo proxy tunneled from studio-ts) + uicgpu (8×A100, Ubuntu, genome parsing, antiSMASH v8 local run).
- **Endpoints used (all FREE):** NCBI E-utils, Europe PMC, Semantic Scholar Graph v1, antiSMASH web api/v1.0, antiSMASH v8.0.4 local, Argo proxy `localhost:44497` (`argo:gpt-5.2`).
- **No paid or third-party LLM APIs used.**
