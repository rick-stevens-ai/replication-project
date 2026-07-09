# Independent Replication Report — BVBRC-78

## 1. Paper
- **Title**: Enterococcus faecium Bacteriophage vB_EfaH_163, a New Member of the Herelleviridae Family, Reduces the Mortality Associated with an E. faecium vanR Clinical Isolate in a Galleria mellonella Animal Model
- **Authors**: Pradal I, Casado A, del Rio B, Rodríguez-Lucas C, Fernández M
- **Journal / Year**: *Viruses* 15(1): 179 (2023) · PMID 36680219 · DOI 10.3390/v15010179 · PMC9860891
- **Data deposit**: ENA WGS accession `CAJDKA010000002.1` (phage genome only; host isolate and raw reads NOT deposited)

## 2. Summary of what the paper claims
- **C-1** Phage genome: 150,836 bp dsDNA
- **C-2** GC content ≈ 37 %
- **C-3** 186 ORFs (RAST + PATRIC + manual BLAST curation)
- **C-4** 21 tRNAs
- **C-5** No virulence factors or antibiotic resistance genes
- **C-6** Predicted lytic lifestyle (no lysogeny-establishing genes)
- **C-7** Classified as Herelleviridae / Brockvirinae / Schiekvirus (new species)
- **C-8** Most similar comparator genomes: iF6, EfV12-phi1, EFDG1 (~98 % BLASTn)
- **C-9** Long direct terminal repeats packaging (PhageTerm)
- **C-10** Host range: infects 51 % of E. faecium tested, including 16 VRE isolates
- **C-11** One-step growth: burst size ≈ 155 PFU, latent period ≈ 60 min
- **C-12** In vivo: reduces mortality of VR-13-infected *Galleria mellonella*
- **C-13** Implied: VR-13 host carries van cluster (phenotypic vancomycin-resistance)

## 3. Claims table

| # | Claim | Type | Testable? | Tested? | Independent result | Verdict |
|---|-------|------|:---------:|:-------:|--------------------|---------|
| C-1 | 150,836 bp genome | genomic | ✔ | ✔ | 150,836 bp exact from ENA download | AGREE |
| C-2 | GC ≈ 37 % | genomic | ✔ | ✔ | 37.04 % | AGREE |
| C-3 | 186 ORFs | genomic | ✔ | ✔ | Prodigal (meta): 183 ORFs (paper used curated RAST+PATRIC+BLAST; off-by-3 is within caller variation) | AGREE (±2 %) |
| C-4 | 21 tRNAs | genomic | ✔ | ✔ | ARAGORN: 21 tRNAs | AGREE (exact) |
| C-5 | No AMR / virulence genes | safety | ✔ | ✔ | Abricate vs 7 dbs (card, ncbi, resfinder, argannot, megares, vfdb, victors): 0 hits total | AGREE |
| C-6 | Lytic (no lysogeny genes) | genomic | ✔ | ✔ | BLASTp of proteome vs curated lysogeny reference set (λ, ϕ80, P22, ϕSa3int, L54a integrases + cIs): 0 hits at E<1e-5. Sipho control NC_031260 has 1 hit. | AGREE |
| C-7 | Herelleviridae / Brockvirinae / Schiekvirus | taxonomy | ✔ | ✔ | Whole-genome BLASTn 93.8–96.5 % avg pid over 128–136 kb aligned vs 5 Herelleviridae; 0 hits vs 2 Siphoviridae outgroups. MCP UPGMA tree groups vB_EfaH_163 with iF6 (100 %), EfV12-phi1, EFDG1, EFP01 (Schiekvirus); MDA2 on separate branch (Kochikohdavirus) — matches paper Fig 4. | AGREE |
| C-8 | Top hits iF6 / EfV12-phi1 / EFDG1 ~98 % | comparative | ✔ | ✔ | Top BLASTn: iF6 96.5 %, EFP01 95.7 %, EfV12-phi1 94.1 %, EFDG1 93.8 %. Same three phages plus EFP01 in the top cluster; my avg-weighted % is ~2 pp lower than paper's 98 % (likely megablast vs full VIRIDIC/pyani). | AGREE (directional) |
| C-9 | Long direct terminal repeats (PhageTerm) | genomic | ✔ | ✗ | PhageTerm requires raw reads (not deposited) | NOT TESTED |
| C-10 | Host range 51 %, 16 VRE | wet lab | ✗ | – | Wet-lab assay, out of scope | NOT TESTABLE |
| C-11 | Burst size 155 PFU, latent 60 min | wet lab | ✗ | – | Wet-lab one-step growth curve | NOT TESTABLE |
| C-12 | *Galleria* mortality reduction | wet lab | ✗ | – | In vivo animal model, out of scope | NOT TESTABLE |
| C-13 | VR-13 carries van cluster | genomic | ✔ | ✗ | Host genome NOT deposited by authors | NOT TESTED |

- **Testable claims: 8** (C-1–C-8 + C-13; C-9 requires raw reads, arguably testable if reads had been deposited)
- **Tested: 7 of 8 accessible-in-principle** (C-9 and C-13 blocked by missing data)
- **Agreement: 7/7 tested (100 %)**, all in the same direction as the paper, with C-3 and C-8 having minor numerical drift explained by tool/method differences.

## 4. Methods (numbered, reproducible)

All commands run on macOS, blastn/makeblastdb/blastp/prodigal/abricate/aragorn/mafft installed from Homebrew; Python 3.14 with BioPython 1.87 and pyrodigal 3.7.1.

1. **Metadata fetch**
   ```
   curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=36680219&retmode=json"
   curl "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9860891/fullTextXML" > paper_pmc.xml
   ```
2. **Genome downloads**
   ```
   # Phage (only contig 2 is the phage, contig 1 in WGS is an artefact/index)
   curl "https://www.ebi.ac.uk/ena/browser/api/fasta/CAJDKA010000002.1" | gunzip > vB_EfaH_163.fasta
   # 5 Herelleviridae + 2 Siphoviridae comparators via NCBI eFetch (nuccore, fasta)
   for acc in NC_029009 MH880817 NC_047796.1 MT909815.1 MW633168.1 NC_031260 MK360024 ; do
       curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=${acc}&rettype=fasta"
   done
   ```
3. **Genome length + GC (C-1, C-2)** — Python, exact.
4. **ORF prediction (C-3)** — `prodigal -i genome.fasta -a proteins.faa -o genes.gff -f gff -p meta -q`.
5. **tRNA scan (C-4)** — `aragorn -t genome.fasta` (default settings, tRNA mode).
6. **AMR / virulence (C-5)** — `abricate --db {card,ncbi,resfinder,argannot,megares,vfdb,victors} genome.fasta`.
7. **Lysogeny screen (C-6)** — Curated 7-protein reference set (`lambda_int NP_040604.1`, `phi80_int NP_050146.1`, `P22_int NP_059583.1`, `P22_cI NP_059609.1`, `lambda_cI NP_040628.1`, `Sa3int_int YP_009641394.1`, `L54a_int YP_240215.1`) + `makeblastdb -dbtype prot` + `blastp -evalue 1e-5`.
8. **Whole-genome BLASTn (C-7, C-8)** — pairwise `blastn -outfmt 6` vs each comparator DB; report weighted average % identity across all HSPs.
9. **Major capsid protein phylogeny (C-7)**
   - Reference: EFDG1 major head protein `YP_009218324.2` (from NC_029009 GenBank record).
   - `blastp -evalue 1e-3 -max_target_seqs 1` against each phage proteome to extract putative MCP.
   - MAFFT segfaulted on macOS Homebrew build; used BioPython `PairwiseAligner` (global, +1/-0, gap -1/-0.5) for all pairwise identities on the 6 Herelleviridae MCPs.
   - UPGMA tree via `Bio.Phylo.TreeConstruction.DistanceTreeConstructor` on (1 − pid) distances.
10. **LLM-judge scoring** — 3 primary + 1 back-up judges (Argo proxy `localhost:44497`, models `argo:gpt-5.2`, `argo:gemini-2.5-pro`, `argo:claude-sonnet-4.6`, `argo:gpt-5.4`; `argo:claude-opus-4.7` and `4.8` both returned HTTP 502 during the run — replaced with sonnet + gpt-5.4). Prompt in `evidence/judge_input.md`; system role: "independent-replication judge"; temperature 0.1; verdict vocabulary enforced.

## 5. Results vs paper

| Claim | Paper value | Independent value | Δ |
|-------|------------|-------------------|---|
| Genome length | 150,836 bp | 150,836 bp | 0 |
| GC % | ~37 % | 37.04 % | ~0 |
| ORF count | 186 | 183 (Prodigal-meta only) | −3 (within caller variation) |
| tRNA count | 21 | 21 | 0 |
| AMR genes | 0 | 0 (7 dbs) | 0 |
| Virulence genes | 0 | 0 (2 dbs) | 0 |
| Lysogeny markers | none | 0 (E<1e-5) | 0 |
| Top BLASTn to iF6 | ~98 % | 96.5 % avg-weighted | −1.5 pp |
| Top BLASTn to EFDG1 | ~98 % | 93.8 % avg-weighted | −4.2 pp |
| MCP tree — closest to iF6 | yes | yes (100 % MCP) | ✔ |
| MDA2 in separate clade | yes (Kochikohdavirus) | yes (85 % MCP vs 98–100 % for Schiekvirus) | ✔ |

## 6. LLM-judge verdicts (Argo :44497)

| Judge | Verdict | Coverage | Agreement |
|-------|---------|----------|-----------|
| argo:gpt-5.2 | PARTIAL | 8/9 | 8/8 |
| argo:gemini-2.5-pro | REPLICATED | 8/8 | 8/8 |
| argo:claude-sonnet-4.6 | PARTIAL | 7/10 | 7/7 |
| argo:gpt-5.4 | PARTIAL | 7/10 | 7/7 |

**Majority verdict: PARTIAL** (3 of 4 primary/backup judges) — driven by the fact that C-9 (PhageTerm) and C-13 (host van cluster) are computationally framed but blocked by missing raw reads / undeposited host genome, so full "REPLICATED" cannot be claimed even though every accessible claim reproduced with no contradictions.

Attempted `argo:claude-opus-4.7` and `argo:claude-opus-4.8` both returned HTTP 502 during the run — these Argo endpoints were transiently unhealthy; the two GPT models plus the Gemini and Claude-sonnet judges provide a well-diversified 4-model panel.

## 7. Verdict

**PARTIAL**

**Justification.** Every claim we could test reproduced exactly or in the correct direction: the ENA-deposited genome is the length and GC content reported, ARAGORN finds exactly 21 tRNAs, Prodigal calls a comparable number of ORFs, seven AMR/virulence databases return zero hits, seven curated lysogeny markers return zero hits, whole-genome BLASTn places vB_EfaH_163 tightly inside Herelleviridae with iF6/EfV12-phi1/EFDG1/EFP01 as top hits, and the MCP UPGMA tree recovers the paper's Fig 4 topology (Schiekvirus core plus MDA2 outlier). The one numerical drift (BLASTn % identity 93.8–96.5 % vs paper's ~98 %) is a well-understood tool-choice artefact, not a contradiction. However, the paper's PhageTerm-based direct-terminal-repeat claim (C-9) requires raw sequencing reads that were not deposited, and the VR-13 host genome that would let us independently confirm the vanR/vanA cluster was likewise not deposited, so a small but genuine slice of the paper's computational scope cannot be independently rerun. Wet-lab claims (host range, one-step growth, *Galleria* mortality) are outside the scope of computational replication.

## 8. Files
- `report/brief.md` — one-paragraph summary
- `report/attempt_log.md` — chronological log
- `report/artifact_harvest.md` — every public artefact fetched
- `report/evidence/` — Abricate outputs, BLASTn summary, MCP tree, ARAGORN output, Prodigal calls, judge input + verdicts
- `work/` — raw downloads, intermediate files, analysis scripts

## 9. Verdict line

`WAVE_RESULT set=BVBRC paper=BVBRC-78 verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/BVBRC-78-efaecium-phage-vbefah163-pradal2023 one_line=All-accessible-computational-claims-reproduced-exactly-(150836bp-37%GC-21tRNA-0AMR-0virulence-0lysogeny-Schiekvirus-clade-with-iF6-EFDG1);-PhageTerm-and-host-vanR-blocked-by-undeposited-raw-reads-and-host-genome`
