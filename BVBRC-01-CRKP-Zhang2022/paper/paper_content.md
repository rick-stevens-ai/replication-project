# Zhang et al. 2022 - Genomic Evolution of ST11 CRKP
## DOI: 10.3390/genes13091624
## Source: MDPI Genes, Open Access

### Authors
Na Zhang, Yue Tang, Xiaojing Yang, Meiling Jin, Jiali Chen, Shiyu Qin, Fangni Liu, Xiong Liu, Jinpeng Guo, Changjun Wang, Yong Chen

### Key Quantitative Claims (extracted for replication)

#### Section 3.1: Clinical and Molecular Characterizations
- Total CRKP genome assemblies: 2356
  - 2011-2015: 1620 CRKPs
  - 2016-2020: 736 CRKPs
- ST11 CRKP: 386 total
  - 2011-2015: 165 (10.19% of 1620)
  - 2016-2020: 221 (30.03% of 736)
- Sample sources (of 386):
  - Blood: 31.09% (120/386)
  - Respiratory: 23.06% (89/386)
  - Feces: 20.21% (78/386)
  - Urine: 18.39% (71/386)
  - Wound pus: 2.85% (11/386)
  - Alveolar lavage: 2.07% (8/386)
  - Sterile body fluids: 1.30% (5/386)
  - Catheter: 1.04% (4/386)
- Carbapenemase genes 2011-2015:
  - blaKPC-2: 84.24% (139/165)
  - blaNDM-1: 6.06% (10/165)
  - blaOXA-48: 3.03% (5/165)
- Carbapenemase genes 2016-2020:
  - blaKPC-2: 81.45% (180/221)
  - blaNDM-1: 8.60% (19/221)
  - blaOXA-48: 4.52% (10/221)
- Serotypes: 51 total
  - 2011-2015: 20 serotypes
  - 2016-2020: 36 serotypes
- KL47 2011-2015: 44.85% (74/165)
- KL64 2011-2015: 10.91% (18/165)
- KL64 2016-2020: 47.06% (104/221)
- KL47 2016-2020: 16.74% (37/221)
- Total KL47: 111
- Total KL64: 122
- Country distribution:
  - China: 64.51% (249/386) [note: text also says 64.25%, 248/386 - minor inconsistency in paper]
  - Brazil: 9.84% (38/386)
  - United States: 8.55% (33/386)
- Top years: 2015 (18.13%, 70/386), 2016 (23.58%, 91/386)

#### Section 3.2: Resistance and Virulence
- KL47 carbapenemase genes:
  - blaKPC-2: 96.40% (107/111)
  - blaNDM-1: 1.80% (2/111)
  - blaNDM-5: 0.90% (1/111)
  - blaVIM-1: 0.90% (1/111)
  - blaOXA-245: 0.90% (1/111)
- KL64 carbapenemase genes:
  - blaKPC-2: 97.54% (119/122)
  - blaOXA-181: 1.64% (2/122)
  - blaOXA-48: 0.82% (1/122)
  - blaKPC-30: 0.82% (1/122)
- KL47 with iucABCD/iutA: 34/111
- KL47 with rmpA: 15/111
- KL47 with rmpA2: 33/111
- KL64 with iucCD/iutA: 50.00% (61/122)
- KL64 with iucAB: 50.82% (62/122)
- Resistance genes median both: 15 (IQR 14-18)
- KL64 virulence genes: median 78 (IQR 72-79.25)
- KL47 virulence genes: median 63 (IQR 63-69)
- KL47 plasmids: median 4 (IQR 3-4)
- KL64 plasmids: median 3 (IQR 3-4)

#### Section 3.3: Virulence Gene Distribution
- 134 virulence genes examined in VFDB
- 35 significantly different between KL47 and KL64 (p < 0.05)
- entF in KL47: 100% (111/111)
- entF in KL64: 92.62% (113/122)
- glf in KL64: 95.90% (117/122)
- gnd in KL64: 100% (122/122)

#### Section 3.4: Evolutionary
- 386 strains → 9 clades
- 233 KL47+KL64 strains → 5 clades
- KL64 has 2 extra recombination regions vs KL47

#### Section 3.5: KL47→KL64 Mechanism
- KL47 wzc CD1-VR2-CD2: two sequences of 1491bp + 342bp = 1835bp, GC 53.84%
- KL64 wzc CD1-VR2-CD2: 2138bp, GC 58.14%
- Difference: ~303bp increase in KL64

### Methods Summary
- Data source: PATRIC database (now BV-BRC)
- Inclusion criteria: K. pneumoniae, 2011-2020, human host, 8 sample sources, carrying carbapenemase genes
- Tools: Kleborate (ST/carbapenemase), Abricate+CARD/VFDB/PlasmidFinder, Prokka, Roary, snippy, ClonalFrameML, IQ-TREE, RAxML-ng
- Statistics: Mann-Whitney U, chi-square, Fisher's exact, p < 0.05
