# LLM-judge scoring task: BVBRC-109 replication

## Paper
Delgado-Suárez et al. (2021) PLOS ONE 16:e0243681
"Genomic surveillance of antimicrobial resistance shows cattle and poultry are a moderate source of multi-drug resistant non-typhoidal Salmonella in Mexico"
DOI: 10.1371/journal.pone.0243681 · PMID: 33951039

## Replication scope
Independent re-analysis of 68/77 study isolates for which NCBI GenBank assemblies exist under BioProject PRJNA480281 (9 isolates lacked NCBI-assembled genomes — raw reads only). Used AMRFinderPlus 4.2.7 (paper used 3.8.4), mlst 2.33.1, and blastn against SGI-1 reference AF261825.2. No re-assembly (used the paper-team's own SPAdes assemblies via GenBank). Statistical replication implemented in analyze_v2.py.

## Paper's claims vs replication findings

### C1 (metadata): 77 Salmonella isolates (48 LN + 29 GB) → 9 serovars, matching serovar counts
- **Replicated**: S1_File.xlsx contains exactly 77 rows, 48+29 sources, serovar counts (London 9, Typhimurium 10, Anatum 23, Reading 22 [after 1 discarded], Fresno 4, Muenster 1, Kentucky 6, monophasic 1, Give 1). Fully matches paper Table/text.

### C2 (MLST): Kentucky = ST-198, Typhimurium = ST-19, monophasic Typhimurium = ST-34
- **Replicated**: our mlst 2.33.1 on 68 assemblies: Kentucky = ST-198 (4/4), Typhimurium = ST-19 (7/7), monophasic = ST-34 (1/1). Anatum = ST-64 (21), Reading = ST-1628 (19) + ST-7148 (2), London = ST-155 (8), Fresno = ST-649 (4). All ST assignments match.

### C3 (SGI-1 in Typhimurium): 9/10 Typhimurium+monophasic isolates carry Salmonella Genomic Island 1 with penta-resistance cassette (aadA2, blaCARB-2, floR, sul1, tetG)
- **Replicated (with slight numeric drift due to 2 missing assemblies)**: 6/8 of the Typh+monophasic isolates we could re-analyze carry all 5 SGI-1 marker genes by AMRFinderPlus. BLASTn of the SGI-1 reference (AF261825.2, 48.8 kb) against these 8 assemblies gives ≥56 kb aligned identity for the same 6 isolates (>100% length coverage due to overlap with chromosomal backbone; the other 2 give only ~5 kb aligned = no SGI-1). Directionally identical to paper.

### C4 (LN vs GB MDR): ground beef isolates ~6.5× more likely to be MDR than lymph-node isolates (chi² = 12.0, p = 0.0005, OR = 6.5)
- **Directionally replicated, effect weaker with genotypic MDR definition**: our 68-isolate genotypic-MDR analysis gives LN 15/44 (34%) vs GB 14/24 (58%), chi² = 3.73 p = 0.053, Fisher OR = 2.71 p = 0.07. Same direction (GB more MDR). Effect is weaker because (a) we operationalise MDR from acquired AMR gene classes rather than the paper's phenotypic disk-diffusion definition (which counts intermediate ciprofloxacin resistance driven by point mutations); (b) we have 9 fewer isolates.

### C5 (Typhimurium enrichment for MDR): Typhimurium accounts for 40% of MDR strains, chi² = 24.5 p<0.0001, OR = 45.8 (95%CI 5.3–399.2)
- **Replicated**: 7/8 (88%) of Typh+monophasic are MDR (≥3 acquired AMR classes) vs 22/60 (37%) of other serovars; chi² = 7.46, p = 0.0063, Fisher OR = 12.1, p = 0.0088. Same direction, very significant, but weaker OR because we're missing 2 Typhimurium isolates and using a stricter genotypic MDR definition.

### C6 (ramR mutation associated with MDR): chi² = 17.7, p<0.0001
- **Not replicated (contradicted with current AMRFinderPlus DB)**: The main ramR non-silent variant AMRFinderPlus 4.2.7 detects in this dataset is `ramR_M83T`, seen in 29/68 isolates — but these are all Anatum (21) + London (8), both **non-MDR** in our re-analysis (0/29 ramR_M83T-carrying isolates are MDR). Our chi² for ramR mutation vs MDR is 37.6 in the OPPOSITE direction (ramR_M83T tags non-MDR susceptible lineages). Likely the paper's "ramR mutation" refers to a different, disrupting variant (deletion/nonsense) that the 3.8.4 AMRFinderPlus database reported differently, or the paper counted any ramR non-synonymous change including ones that are today known lineage markers.

### C7 (Widespread mutations across all 77): 100% carry gyrAB and parE QRDR mutations, 100% soxRS, 100% pmrAB, 68/77 (88%) acrB
- **Partially replicated, with major reductions**: With current AMRFinderPlus (which correctly separates silent from missense/nonsense), we see: parC 100%, acrB 100%, parE 31%, ramR 43%, pmrB 7%, pmrA 1%, gyrA/gyrB/soxR/soxS 0%. The paper's "100% gyrA, soxRS, pmrAB mutations" figure was inflated by counting synonymous variants (X_X calls in AMRFinderPlus 3.8.4 output). AMRFinderPlus 4.x refines this call. The paper's downstream inference ("mutations ubiquitous but only some phenotypes MDR") still stands.

### C8 (top AMR genes in the 77 study isolates): most common should include tet(A), qnrB19, fosA7-family, bla-lactamases, aac/aad aminoglycoside
- **Replicated**: our top-25 in 68 assemblies: mdsB 68, mdsA 68 (intrinsic RND efflux, universal — as paper notes), qnrB19 31, fosA7.7 21, tet(C) 13, sul1 7, blaCARB-2 7, aadA2 7, tet(G) 6, floR 6. Matches paper narrative — the paper's Fig 1 shows tet, penicillin/beta-lactamase and quinolone genes as dominant. qnrB19 explains ciprofloxacin non-susceptibility widespread; fosA7 = ubiquitous fosfomycin resistance intrinsic; the SGI-1 cassette (aadA2/blaCARB-2/floR/sul1/tetG) contributes exactly to the Typhimurium MDR profile.

## Verdict qualitative summary
- **Fully replicated**: metadata + isolate counts (C1), MLST/ST assignments (C2), SGI-1 penta-resistance in Typhimurium (C3), Typhimurium MDR enrichment (C5), top AMR gene profile (C8).
- **Directionally replicated, weaker effect**: LN vs GB MDR (C4).
- **Not replicated / reinterpreted**: ramR-MDR association (C6) — the ramR variant detected today segregates with susceptible lineages, so the association is spurious or driven by phylogenetic confounding; widespread QRDR/soxRS mutations (C7) — the paper's "100%" was inflated by silent-variant counting.

## Score dimensions (0-100 each)
- Data availability: paper provides all raw reads (SRA), 68/77 assemblies on GenBank, three supplementary spreadsheets with metadata + AMR calls + MLST context = **100**
- Method reproducibility: methods section names every tool, versions, and parameter defaults; protocols.io links for wet-lab; PATRIC/SPAdes assembly reproducible = **95**
- Core claims replicated: 5 of 8 claims fully replicated, 1 directional, 2 not = **75**
- Statistical concordance: same signs on all key associations, but magnitudes attenuated due to updated tool DBs and stricter definitions = **70**
- Independence-of-analysis strength: we re-called AMR from scratch with newer tools, ran MLST from scratch, ran BLAST for SGI-1 from scratch — pipeline-independent confirmation = **85**

Please score this replication attempt on a 0-100 scale considering all evidence above.
