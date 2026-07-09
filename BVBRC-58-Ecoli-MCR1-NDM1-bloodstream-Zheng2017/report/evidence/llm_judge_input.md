You are an impartial scientific-replication judge. Score an independent replication of a genomics paper. Be rigorous; do not inflate.

# PAPER
Zheng B, Yu X, Xu H, et al. "Complete genome sequencing and genomic characterization of two Escherichia coli strains co-producing MCR-1 and NDM-1 from bloodstream infection." Sci Rep 7:17885 (2017). DOI 10.1038/s41598-017-18273-2. Open Access.

## Paper's testable claims
- C1 (data): Complete genomes of EC1002 & EC2474 deposited under GenBank CP021202-CP021210 (chromosome + plasmids).
- C2 (genome stats): EC1002 = 5,177,501 bp chromosome (GC 50.1%) + 4 plasmids; EC2474 = 5,013,813 bp chromosome (GC 50.6%) + 3 plasmids. Per-replicon sizes & GC given in Table 1.
- C3 (MLST): EC1002 = ST405; EC2474 = ST131.
- C4 (AMR content): mcr-1 present; blaNDM-1 present; both on plasmids, on DIFFERENT plasmids from each other; specific resistance-gene complement per plasmid (Table 1). E.g. pEC1002-NDM carries blaNDM-1 + blaCTX-M-14 + rmtC + sul1 + mph + aac(6')-Ib; pEC1002-MCR carries only mcr-1; pEC2474-MCR carries mcr-1 + blaCTX-M-14 + floR + sul2 + aac(3)-IVa + fosA.
- C5 (plasmid replicon typing): pEC1002-MCR IncI2, pEC2474-MCR IncHI2, pEC1002-NDM IncA/C2, pEC2474-NDM IncF, pEC1002-1 IncFII, pEC1002-4 IncFIB, pEC2474-3 IncI1.
- C6 (mcr-1/NDM-1 on separate plasmids -> potential pandrug-resistance dissemination): mcr-1 and blaNDM-1 never co-located; each on its own plasmid.

# INDEPENDENT REPLICATION RESULTS (all on the ACTUAL public GenBank sequences, re-downloaded via NCBI efetch)

## Genome stats (Biopython, my compute vs paper Table 1)
CP021202 EC1002 chr: paper 5,177,501 bp / obs 5,177,498 bp (delta -3); GC paper 50.1 / obs 50.61
CP021203 pEC1002-1: paper 183,509 / obs 183,508 (-1); GC 50.0/49.96
CP021205 pEC1002-MCR: paper 63,392 / obs 63,392 (0); GC 43.0/43.01
CP021206 pEC1002-NDM: paper 111,688 / obs 111,688 (0); GC 52.3/52.33
CP021204 pEC1002-4: paper 92,439 / obs 92,438 (-1); GC 50.0/50.30
CP021207 EC2474 chr: paper 5,013,813 / obs 5,013,813 (0); GC 50.6/50.61
CP021209 pEC2474-MCR: paper 223,982 / obs 223,982 (0); GC 45.8/45.83
CP021210 pEC2474-NDM: paper 75,553 / obs 75,553 (0); GC 50.8/50.78
CP021208 pEC2474-3: paper 86,717 / obs 86,725 (+8); GC 49.5/49.55
All 9 replicons present; sizes match to 0-8 bp; per-replicon GC within 0.5%.

## MLST (tool: mlst 2.35.0, scheme ecoli_achtman_4)
EC1002 -> ST405 (adk35 fumC37 gyrB29 icd25 mdh4 purA5 recA73)  [paper: ST405]  MATCH
EC2474 -> ST131 (adk53 fumC40 gyrB47 icd13 mdh36 purA28 recA29) [paper: ST131]  MATCH

## AMRFinderPlus 3.12.8 (DB 2024-07-22) acquired-resistance genes, mapped to contig/plasmid
EC1002:
  chr CP021202: blaCTX-M-15, tet(B), blaEC, quinolone gyrA/parC/parE mutations  [paper chr: blaCTX-M-15, oqxB, tetB]
  pEC1002-1 CP021203: blaCTX-M-15, aac(3)-IIe, aadA5, dfrA17, erm(B), mph(A)  [paper: blaCTX-M-15, sul, mph, aac(3)-Ib, erm, aadA4, dfrA, arr]
  pEC1002-4 CP021204: blaTEM-1  [paper: blaTEM]
  pEC1002-MCR CP021205: mcr-1.1 (ONLY gene)  [paper: mcr-1 only]  MATCH
  pEC1002-NDM CP021206: blaNDM-1, blaCTX-M-14, blaTEM-1, ble, mph(A), aac(6')-Ib3, aac(3)-IId, rmtC, sul1, qacEdelta1  [paper: blaNDM-1, blaCTX-M-14, blaTEM, sul1, mph, aac(6')-Ib, rmtC, arr]
EC2474:
  chr CP021207: blaCTX-M-55, blaEC  [paper chr: blaCTX-M-55]  MATCH
  pEC2474-3 CP021208: blaCTX-M-55  [paper: blaCTX-M-55]  MATCH
  pEC2474-MCR CP021209: mcr-1.1, blaCTX-M-14, floR, aph(4)-Ia, aac(3)-IVa, sul2, fosA3, ter-genes  [paper: mcr-1, blaCTX-M-14, floR, aph4, sul2, aac(3)-IVa, fosA14]
  pEC2474-NDM CP021210: blaNDM-1, aph(3')-VI, ble  [paper: blaNDM-1, aph]
mcr-1 and blaNDM-1 are on SEPARATE plasmids in each strain (mcr-1 on CP021205/CP021209; blaNDM-1 on CP021206/CP021210). C6 confirmed.

## PlasmidFinder replicon typing (blastn vs PlasmidFinder enterobacteriales DB, 95%id/60%cov)
pEC1002-1 CP021203 -> IncFII (100%)  [paper IncFII] MATCH
pEC1002-4 CP021204 -> IncFIB + IncFIA (99.7/98.8%)  [paper IncFIB] MATCH
pEC1002-MCR CP021205 -> IncI2 (100%)  [paper IncI2] MATCH
pEC1002-NDM CP021206 -> IncC (100%)  [paper IncA/C2; IncC is the renamed IncA/C2] MATCH
pEC2474-3 CP021208 -> IncI1-I(Alpha) (100%)  [paper IncI1] MATCH
pEC2474-MCR CP021209 -> IncHI2 + IncHI2A (100%)  [paper IncHI2] MATCH
pEC2474-NDM CP021210 -> IncFII (100%)  [paper IncF] MATCH

# TASK
Assess each claim C1-C6: reproduced / partially reproduced / not reproduced, on real data. Note minor discrepancies (e.g. AMRFinder-2024 vs ResFinder-2.1 giving fosA3 vs fosA14, aac(3)-IIe vs aac(3)-Ib, extra chromosomal quinolone SNPs, arr not called by AMRFinder). Then give:
1. Per-claim verdict table.
2. Overall coverage % (fraction of testable claims reproduced).
3. Overall agreement % (how well reproduced values match paper).
4. A single canonical verdict from: REPLICATED, PARTIAL, SPOT-CHECK, NO-GO, CONTRADICTED, BLOCKED, FAILED.
5. 2-3 sentence justification.
