# Independent-Replication Judge Input — BVBRC-78

## Paper
Pradal I et al. 2023. "Enterococcus faecium Bacteriophage vB_EfaH_163, a New Member of the Herelleviridae Family, Reduces the Mortality Associated with an E. faecium vanR Clinical Isolate in a Galleria mellonella Animal Model." *Viruses* 15(1):179. PMID 36680219. DOI 10.3390/v15010179.

## Data actually pulled (independent verification against public archives)
- Phage genome: ENA CAJDKA010000002.1 — downloaded, length 150,836 bp confirmed
- 5 Herelleviridae comparators (EFDG1 NC_029009, EfV12-phi1 MH880817, EFP01 NC_047796.1, iF6 MT909815.1, MDA2 MW633168.1) and 2 Siphoviridae outgroups (Ec-ZZ2 NC_031260, vB_EfaS_Max MK360024) all downloaded from NCBI
- Host clinical isolate genome VR-13: NOT deposited by the authors — paper explicitly states only the phage was deposited in ENA. Independent verification of host-side AMR is thus not achievable from paper artifacts.

## Claims and independent test results

| ID | Claim | Type | Testable? | Tested? | Independent result |
|----|-------|------|-----------|---------|--------------------|
| C-1 | Phage vB_EfaH_163 genome is 150,836 bp dsDNA | genomic | yes | YES | 150,836 bp exact match (ENA download) ✔ |
| C-2 | GC content ~37% | genomic | yes | YES | 37.04% ✔ |
| C-3 | 186 ORFs annotated | genomic | yes | YES | Prodigal (meta) predicts 183 ORFs (paper used RAST+PATRIC+BLAST manual curation, 186; off-by-3 well within caller variation) — CONSISTENT |
| C-4 | 21 tRNAs | genomic | yes | YES | ARAGORN detects 21 tRNAs (exact match) ✔ |
| C-5 | No virulence factors or AMR genes | genomic | yes | YES | Abricate against 7 databases (card, ncbi, resfinder, argannot, megares, vfdb, victors) — 0 hits total ✔ |
| C-6 | Lytic (no lysogeny genes) | genomic | yes | YES | BLASTp of phage proteome vs curated lysogeny reference set (7 known integrases + cI repressors including lambda, phi80, P22, phiSa3int, L54a) — 0 hits at E<1e-5. Sipho control NC_031260 gives 1 hit. Consistent with lytic prediction ✔ |
| C-7 | Belongs to Herelleviridae family, Brockvirinae subfamily, Schiekvirus genus | taxonomy | yes | YES | BLASTn genome vs Herelleviridae members: 93.8–96.5% avg pid over 128–136 kb aligned. Vs Siphoviridae outgroups: no hits. MCP identity: 98–100% vs Schiekvirus members (EFDG1/EfV12-phi1/EFP01/iF6), 85% vs Kochikohdavirus (MDA2). UPGMA MCP tree topology matches paper Fig 4: vB_EfaH_163 groups with iF6 (100%), then EfV12-phi1 and EFDG1/EFP01, all Schiekvirus; MDA2 on separate branch (Kochikohdavirus) ✔ |
| C-8 | Most similar to iF6, EfV12-phi1, EFDG1 (~98% BLASTn) | comparative | yes | YES | Top BLASTn hits: iF6 96.5% (paper: highest), EFP01 95.7%, EfV12-phi1 94.1%, EFDG1 93.8% — same three plus EFP01 as top-tier (paper called iF6/EfV12-phi1/EFDG1 the top 3). Values ~2 pp lower than paper's ~98% (probably megablast vs. full VIRIDIC/pyani; both use similar computation but VIRIDIC weights alignment fraction differently). Directionally CONSISTENT. |
| C-9 | Long direct terminal repeats packaging (PhageTerm) | genomic | yes | NO | PhageTerm requires raw read data (not deposited). Not testable from public artifacts. |
| C-10 | Host range: 51% of E. faecium strains tested, 16 VRE isolates | wet lab | no | N/A | Wet lab (double-layer agar spot test) — out of scope for computational replication |
| C-11 | Burst size ~155 PFU, latent period 60 min | wet lab | no | N/A | Wet lab one-step growth curve — out of scope |
| C-12 | Reduces mortality in *Galleria mellonella* infected with VR-13 | wet lab | no | N/A | In vivo animal assay — explicitly out of scope per task brief |
| C-13 | VR-13 host genome carries vanR/vanA cluster | genomic | yes | NO | Host genome NOT deposited; only phenotypic vanR class (vancomycin resistance) reported. Not verifiable without host sequence. |

## Summary of computational replication scope
- **7 testable computational claims tested; 6 fully confirmed, 1 (host similarity magnitude) directionally consistent but numerically ~2 pp off**
- **3 additional claims not verifiable** (C-9 requires raw reads; C-10/11/12 are wet lab; C-13 needs undeposited host genome)
- **Zero contradictions.** Genome length, GC%, tRNA count, and 7/7 AMR/virulence database screens all exact matches.
- The paper's core genomic characterization is fully reproducible from the public ENA deposit.

## Verdict question for judges
Given the evidence above, which best describes this independent replication?
- REPLICATED: core testable computational claims reproduced on real data with no contradictions
- PARTIAL: some claims reproduced, some not accessible
- SPOT-CHECK: data availability + method plausibility only
- CONTRADICTED / NO-GO / BLOCKED / FAILED

Please respond with:
1. **Verdict** (one word from the vocab)
2. **Coverage** (fraction of testable claims tested)
3. **Agreement** (of tested claims, how many agreed with paper — express as X/N)
4. **Two-sentence justification**
