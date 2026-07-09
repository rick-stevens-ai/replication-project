# Claims Table — BVBRC-73

| ID | Claim | Type | Testable? | Tested? | Observed | Verdict |
|----|-------|------|-----------|---------|----------|---------|
| C1 | Genome size 4,494,515 bp | quantitative | yes | yes | 4,494,464 bp (Δ 51 bp = 0.001%) | REPLICATED |
| C2 | GC content 58.87% | quantitative | yes | yes | 58.87% (Δ +0.001) | REPLICATED |
| C3 | 93 contigs | quantitative | yes | yes | 93 contigs (exact match) | REPLICATED |
| C4 | 4,229 CDS (RAST annotation) | quantitative | partial | yes | Prodigal: 4,063 CDS (Δ -166, -3.9%); Prodigal open-ends 4,108 | PARTIAL (annotation-method dependent) |
| C5 | 102 tRNA genes | quantitative | yes | yes | Aragorn: 96 tRNA (Δ -6, -5.9%) | PARTIAL (tool-dependent; paper used tRNAscan-SE via RAST) |
| C6 | 13 rRNA genes | quantitative | yes | yes | Barrnap: 13 rRNA (11×5S + 1×16S + 1×23S, exact match) | REPLICATED |
| C7 | MLST ST 492 (pubMLST Aeromonas scheme, 6-locus) | quantitative | yes | yes | Fresh PubMLST scan (2026-07-03): 5 exact allele matches (gyrB=633, groL=91, gltA=340, metG=124, recA=1460) + ppsA best-match 627 at 99.44% (near-miss allele). NO ST match in 2,755 profiles. ST 492 profile in PubMLST (gyrB=112, groL=347, gltA=44, metG=217, ppsA=384, recA=381) matches NONE of the observed alleles. | **CONTRADICTED** |
| C8 | Contains T2SS, T3SS, T6SS secretion systems | qualitative | yes | yes | VFDB scan: Exe T2SS (9 genes), T3SS (37 genes), T6SS (16 genes) — all present | REPLICATED |
| C9 | Contains adhesion/flagella/pili genes | qualitative | yes | yes | VFDB scan: Polar flagella (40), Lateral flagella (17), Tap type IV pili (7), MSHA type IV pili (6), Type I pili (3) | REPLICATED |
| C10 | Multidrug-resistant (β-lactam, tetracycline, ampicillin resistance genes present) | qualitative | yes | yes | CARD/NCBI/ResFinder/ARGannot/MEGARes concordant: cphA4 (carbapenem class-B MBL), OXA-12/blaOXA-12/ampS (class-D β-lactamase penicillin), rsmA (regulator, MDR efflux). β-lactam resistome REPLICATED. Paper's specific tetracycline gene not detected in current CARD/ResFinder scan — likely low-identity or database revision. | PARTIAL (β-lactam resistome REPLICATED; specific tetracycline claim not detected in current DBs) |
| C11 | Close phylogenetic relationship to A. veronii TH0426 (China) and B565 (both catfish) | qualitative | yes | yes | Skani ANI: Alim_AV_1000 vs TH0426 = 96.34%; vs B565 = 96.47%; vs A. hydrophila = 87.81% (outside species); vs A. salmonicida = 85.87%. Species-level clustering with TH0426/B565 confirmed. | REPLICATED |
| C12 | 2 intact + 1 incomplete phage regions (PHASTER) | quantitative | yes | not-tested | PHASTER web API rejected upload attempts (broken pipe on 4.5 MB submission); no local PHASTER install. Methodology is standard and the finding is consistent with typical Aeromonas genomes. | SPOT-CHECK (data + method plausible; not independently rerun) |
| C13 | Wet-lab MDR phenotype (Table 3) | phenotypic | wet-lab | no | Requires cultures & Vitek/disc diffusion — not reproducible from genome alone. Genotypic AMR is consistent with observed resistance to β-lactams. | Not reproducible (genotype consistent) |

