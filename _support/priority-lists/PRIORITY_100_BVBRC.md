# PRIORITY_100_BVBRC — Top-100 BV-BRC Papers for Replication

*Built 2026-06-20 14:28 CDT by Ollie. **COMPLETE** (was stub until 14:28 CDT today).*

## Source mix
- **Rows 1-19**: existing BVBRC-* dirs in `~/Dropbox/REPLICATE-PROJECT/`. Verdicts from `MASTER_SCORES_2026-06-20.csv` where available.
- **Rows 20-100**: 81 curated candidates from 2026-06-20 BVBRC-100 curation subagent harvest (10 topic axes × ~8 papers each), Semantic Scholar API, ranked by composite candidate_score (0.4·log10(cites+1) + 0.3·recency + 0.2·OA + 0.1·code-signal).

## Curation summary
- 30 Semantic Scholar API calls; 50.1s wall time
- 120 raw candidates harvested → 81 after axis-balance trim and dedupe (2 existing-BVBRC + 11 near-duplicates dropped)
- Axes: AMR (9), genome assembly (8), pangenomics (8), metabolic modeling (8), phylogenomics (8), virulence (8), biofilm (8), probiotics (8), plasmid/MGE (8), BGC/antiSMASH (8)

## Standing policies
- Free endpoints only (Argo / Sophia / CELS chicago-1/2/4)
- AUDIT_PROTOCOL.md scope ≥80% AND claims ≥80% for REPLICATED verdict
- Multi-judge scoring (3 judges) for every NEW report
- BV-BRC platform login: existing credentials in keychain
- Bacterial-genomics replications generally don't need GPU; CherryRd / uicgpu CPU sufficient

---

## Rows 1-19 (existing dirs)

| Rank | Status | Slug | Verdict | Cov | Agr | Path |
|---:|:---|:---|:---|---:|---:|:---|
| 1 | DONE | BVBRC-01-CRKP-Zhang2022 | REPLICATED | 8 | 7 | `BVBRC-01-CRKP-Zhang2022/` |
| 2 | DONE | BVBRC-02-Ralstonia-Fluit2021 | PARTIAL | 6 | 8 | `BVBRC-02-Ralstonia-Fluit2021/` |
| 3 | DONE | BVBRC-03-Saureus-mastitis-Sivakumar2023 | REPLICATED | 8 | 7 | `BVBRC-03-Saureus-mastitis-Sivakumar2023/` |
| 4 | DONE | BVBRC-04-Variovorax-trehalose-Shrestha2022 | PARTIAL | 6 | 8 | `BVBRC-04-Variovorax-trehalose-Shrestha2022/` |
| 5 | DONE | BVBRC-05-Trueperella-pyogenes-Thakur2022 | REPLICATED | 7 | 8 | `BVBRC-05-Trueperella-pyogenes-Thakur2022/` |
| 6 | DONE | BVBRC-06-Smaltophilia-iron-Kalidasan2018 | SPOT-CHECK | 3 | 8 | `BVBRC-06-Smaltophilia-iron-Kalidasan2018/` |
| 7 | DONE | BVBRC-07-Sherry-AMR-workflow-2023 | REPLICATED | 7 | 9 | `BVBRC-07-Sherry-AMR-workflow-2023/` |
| 8 | DONE | BVBRC-08-Lplantarum-DJF10-Kandasamy2022 | PARTIAL | 6 | 8 | `BVBRC-08-Lplantarum-DJF10-Kandasamy2022/` |
| 9 | DONE | BVBRC-09-blaNDM5-K-pneumoniae-Yuan2019 | REPLICATED | 8 | 8 | `BVBRC-09-blaNDM5-K-pneumoniae-Yuan2019/` |
| 10 | DONE | BVBRC-10-Llactis-LL16-Mileriene2023 | PARTIAL | 7 | 7 | `BVBRC-10-Llactis-LL16-Mileriene2023/` |
| 11 | DONE | BVBRC-11-VREfm-LatAm-Rios2020 | PARTIAL | 6 | 8 | `BVBRC-11-VREfm-LatAm-Rios2020/` |
| 12 | REPORT-PRESENT | BVBRC-12-ML-AMR-pangenomes-Hyun2020 | — | — | — | `BVBRC-12-ML-AMR-pangenomes-Hyun2020/` |
| 13 | REPORT-PRESENT | BVBRC-13-Efaecalis-envadapt-He2018 | — | — | — | `BVBRC-13-Efaecalis-envadapt-He2018/` |
| 14 | DONE | BVBRC-14-HybridAssembly-Ecoli-Kpneu-Khezri2021 | PARTIAL | 5 | 7 | `BVBRC-14-HybridAssembly-Ecoli-Kpneu-Khezri2021/` |
| 15 | DONE | BVBRC-15-Streptomyces-chassis-genome-reduction-2019 | REPLICATED | 8 | 9 | `BVBRC-15-Streptomyces-chassis-genome-reduction-2019/` |
| 16 | DONE | BVBRC-16-Efaecium-probiotic-genome-factors-2018 | SPOT-CHECK | 2 | 6 | `BVBRC-16-Efaecium-probiotic-genome-factors-2018/` |
| 17 | REPORT-PRESENT | BVBRC-17-Ecoli-B2-IBD-metabolic-2018 | — | — | — | `BVBRC-17-Ecoli-B2-IBD-metabolic-2018/` |
| 18 | DONE-NEW-AUDIT | BVBRC-18-Marine-Streptomyces-BGC-2019 | SPOT-CHECK | 2 | 8 | `BVBRC-18-Marine-Streptomyces-BGC-2019/` |
| 19 | DONE-NEW-AUDIT | BVBRC-19-Propionibacterium-pangenome-metabolic | SPOT-CHECK | 2 | 10 | `BVBRC-19-Propionibacterium-pangenome-metabolic/` |

## Rows 20-100 (curated candidates, ranked)

| Rank | Axis | Title | Year | Venue | Cites | Score | DOI |
|---:|:---|:---|---:|:---|---:|---:|:---|
| 20 | Genome_assembly_hy | Unicycler: Resolving bacterial genome assemblies from short and long sequenci... | 2016 | bioRxiv | 7488 | 1.8298 | `10.1371/journal.pcbi.1005595` |
| 21 | BGC_antiSMASH | antiSMASH 5.0: updates to the secondary metabolite genome mining pipeline | 2019 | Nucleic Acids Res. | 2464 | 1.7267 | `10.1093/nar/gkz310` |
| 22 | Genome_assembly_hy | Completing bacterial genome assemblies with multiplex MinION sequencing | 2017 | bioRxiv | 917 | 1.4951 | `10.1099/mgen.0.000132` |
| 23 | Pangenomics_compar | Super-pangenome analyses highlight genomic diversity and structural variation... | 2023 | Nature Genetics | 218 | 1.3762 | `10.1038/s41588-023-01340-y` |
| 24 | Plasmid_MGE_ecolog | Microbial evolution through horizontal gene transfer by mobile genetic elements | 2024 | Microbial Biotechnology | 182 | 1.375 | `10.1111/1751-7915.14408` |
| 25 | AMR_genotype_pheno | Comprehensive prediction of secondary metabolite structure and biological act... | 2020 | Nature Communications | 306 | 1.3449 | `10.1038/s41467-020-19986-1` |
| 26 | Metabolic_modeling | RAVEN 2.0: A versatile toolbox for metabolic network reconstruction and a cas... | 2018 | bioRxiv | 322 | 1.3437 | `10.1371/journal.pcbi.1006541` |
| 27 | Plasmid_MGE_ecolog | Nonnutritive sweeteners can promote the dissemination of antibiotic resistanc... | 2021 | The ISME Journal | 244 | 1.3357 | `10.1038/s41396-021-00909-x` |
| 28 | Metabolic_modeling | Spatial reconstruction of single enterocytes uncovers broad zonation along th... | 2018 | bioRxiv | 399 | 1.3308 | `10.1101/261529` |
| 29 | Plasmid_MGE_ecolog | Inter-plasmid transfer of antibiotic resistance genes accelerates antibiotic ... | 2024 | The ISME Journal | 133 | 1.3208 | `10.1093/ismejo/wrad032` |
| 30 | BGC_antiSMASH | A deep learning genome-mining strategy for biosynthetic gene cluster prediction | 2019 | Nucleic Acids Research | 309 | 1.3165 | `10.1093/nar/gkz654` |
| 31 | Pangenomics_compar | PPanGGOLiN: Depicting microbial diversity via a partitioned pangenome graph | 2019 | bioRxiv | 218 | 1.3062 | `10.1371/journal.pcbi.1007732` |
| 32 | Virulence_pathogen | Genetic diversity, mobilisation and spread of the yersiniabactin-encoding mob... | 2018 | Microbial Genomics | 313 | 1.2888 | `10.1099/mgen.0.000196` |
| 33 | Genome_assembly_hy | Comparison of long-read sequencing technologies in the hybrid assembly of com... | 2019 | bioRxiv | 245 | 1.2764 | `10.1099/mgen.0.000294` |
| 34 | AMR_genotype_pheno | Direct antimicrobial resistance prediction from clinical MALDI-TOF mass spect... | 2020 | Nature Medicine | 204 | 1.2747 | `10.1038/s41591-021-01619-9` |
| 35 | Phylogenomics_outb | MTBseq: a comprehensive pipeline for whole genome sequence analysis of Mycoba... | 2018 | PeerJ | 216 | 1.2746 | `10.7717/peerj.5895` |
| 36 | Biofilm_niche_adap | Biochemistry of Bacterial Biofilm: Insights into Antibiotic Resistance Mechan... | 2025 | Life | 71 | 1.2429 | `10.3390/life15010049` |
| 37 | BGC_antiSMASH | Mini review: Genome mining approaches for the identification of secondary met... | 2020 | Computational and Structu | 165 | 1.238 | `10.1016/j.csbj.2020.06.024` |
| 38 | Metabolic_modeling | What Makes a Bacterial Species Pathogenic?:Comparative Genomic Analysis of th... | 2016 | PLoS Neglected Tropical D | 277 | 1.2076 | `10.1371/journal.pntd.0004403` |
| 39 | BGC_antiSMASH | Genome Mining for Unknown-Unknown Natural Products | 2023 | Nature Chemical Biology | 82 | 1.2076 | `10.1038/s41589-022-01246-6` |
| 40 | Plasmid_MGE_ecolog | Selfish, promiscuous and sometimes useful: how mobile genetic elements drive ... | 2021 | Philosophical Transaction | 116 | 1.2073 | `10.1098/rstb.2021.0234` |
| 41 | Plasmid_MGE_ecolog | How do interactions between mobile genetic elements affect horizontal gene tr... | 2023 | Current Opinion in Microb | 75 | 1.1923 | `10.1016/j.mib.2023.102282` |
| 42 | Phylogenomics_outb | Core Genome Multilocus Sequence Typing Scheme for High-Resolution Typing of E... | 2015 | Journal of Clinical Micro | 262 | 1.168 | `10.1128/JCM.01946-15` |
| 43 | Probiotic_benefici | Genome mining identifies cepacin as a plant-protective metabolite of the biop... | 2019 | Nature Microbiology | 129 | 1.1656 | `10.1038/s41564-019-0383-z` |
| 44 | BGC_antiSMASH | Thirty complete Streptomyces genome sequences for mining novel secondary meta... | 2020 | Scientific Data | 106 | 1.1618 | `10.1038/s41597-020-0395-9` |
| 45 | Genome_assembly_hy | Comparison of R9.4.1/Kit10 and R10/Kit12 Oxford Nanopore flowcells and chemis... | 2023 | Microbial Genomics | 60 | 1.1541 | `10.1099/mgen.0.000910` |
| 46 | Genome_assembly_hy | Evaluation of the accuracy of bacterial genome reconstruction with Oxford Nan... | 2024 | bioRxiv | 50 | 1.153 | `10.1099/mgen.0.001246` |
| 47 | Genome_assembly_hy | Benchmarking hybrid assembly approaches for genomic analyses of bacterial pat... | 2020 | BMC Genomics | 74 | 1.15 | `10.1186/s12864-020-07041-8` |
| 48 | Probiotic_benefici | metaProbiotics: a tool for mining probiotic from metagenomic binning data bas... | 2024 | Briefings Bioinform. | 36 | 1.1473 | `10.1093/bib/bbae085` |
| 49 | AMR_genotype_pheno | GenTB: A user-friendly genome-based predictor for tuberculosis resistance pow... | 2021 | Genome Medicine | 61 | 1.147 | `10.1186/s13073-021-00953-4` |
| 50 | Plasmid_MGE_ecolog | Antidepressants promote the spread of antibiotic resistance via horizontally ... | 2022 | Environmental Microbiolog | 67 | 1.143 | `10.1111/1462-2920.16165` |
| 51 | Virulence_pathogen | Enabling genomic island prediction and comparison in multiple genomes to inve... | 2022 | Microbial Genomics | 49 | 1.1396 | `10.1099/mgen.0.000818` |
| 52 | Biofilm_niche_adap | Bacteria use exogenous peptidoglycan as a danger signal to trigger biofilm fo... | 2025 | Nature Microbiology | 36 | 1.1273 | `10.1038/s41564-024-01886-5` |
| 53 | Plasmid_MGE_ecolog | Co-effect of cadmium and iron oxide nanoparticles on plasmid-mediated conjuga... | 2021 | Environment International | 67 | 1.113 | `10.1016/j.envint.2021.106453` |
| 54 | AMR_genotype_pheno | Prediction of Antimicrobial Resistance in Gram-Negative Bacteria From Whole-G... | 2020 | Frontiers in Microbiology | 59 | 1.1113 | `10.3389/fmicb.2020.01013` |
| 55 | Biofilm_niche_adap | Lysogenic bacteriophages encoding arsenic resistance determinants promote bac... | 2023 | The ISME Journal | 45 | 1.1051 | `10.1038/s41396-023-01425-w` |
| 56 | Plasmid_MGE_ecolog | Spatial mapping of mobile genetic elements and their bacterial hosts in compl... | 2024 | Nature Microbiology | 37 | 1.1019 | `10.1038/s41564-024-01735-5` |
| 57 | BGC_antiSMASH | Engineered CRISPR-Cas9 for Streptomyces sp. genome editing to improve special... | 2025 | Nature Communications | 30 | 1.0965 | `10.1038/s41467-025-56278-y` |
| 58 | Metabolic_modeling | A Resource Allocation Trade-Off between Virulence and Proliferation Drives Me... | 2016 | PLoS Pathogens | 135 | 1.0834 | `10.1371/journal.ppat.1005939` |
| 59 | Virulence_pathogen | Whole spectrum of Aeromonas hydrophila virulence determinants and the identif... | 2023 | Scientific Reports | 39 | 1.0808 | `10.1038/s41598-023-34887-1` |
| 60 | Pangenomics_compar | A comparative study of antibiotic resistance patterns in Mycobacterium tuberc... | 2025 | Scientific Reports | 20 | 1.0789 | `10.1038/s41598-025-89087-w` |
| 61 | Biofilm_niche_adap | Antimicrobial resistance patterns, virulence genes, and biofilm formation in ... | 2024 | BMC Infectious Diseases | 32 | 1.0774 | `10.1186/s12879-024-09117-2` |
| 62 | Genome_assembly_hy | The long and short of it: benchmarking viromics using Illumina, Nanopore and ... | 2024 | Microbial Genomics | 31 | 1.0721 | `10.1099/mgen.0.001198` |
| 63 | Genome_assembly_hy | Comparison of Illumina and Oxford Nanopore Technology for genome analysis of ... | 2023 | BMC Genomics | 37 | 1.0719 | `10.1186/s12864-023-09343-z` |
| 64 | Virulence_pathogen | Forest and Trees: Exploring Bacterial Virulence with Genome-Wide Association ... | 2021 | Trends in Microbiology | 50 | 1.063 | `10.1016/j.tim.2020.12.002` |
| 65 | Biofilm_niche_adap | Comparative and functional genomics of the Lactococcus lactis taxon; insights... | 2017 | BMC Genomics | 99 | 1.06 | `10.1186/s12864-017-3650-5` |
| 66 | Phylogenomics_outb | Whole Genome and Core Genome Multilocus Sequence Typing and Single Nucleotide... | 2017 | Applied and Environmental | 98 | 1.0583 | `10.1128/AEM.00633-17` |
| 67 | Virulence_pathogen | Comparative genomics and prediction of conditionally dispensable sequences in... | 2016 | BMC Genomics | 115 | 1.0558 | `10.1186/s12864-016-2486-8` |
| 68 | Pangenomics_compar | Comparative Genomics of Bacillus amyloliquefaciens Strains Reveals a Core Gen... | 2017 | Frontiers in Microbiology | 96 | 1.0547 | `10.3389/fmicb.2017.01438` |
| 69 | Phylogenomics_outb | Comparison of Whole Genome (wg-) and Core Genome (cg-) MLST (BioNumericsTM) V... | 2020 | Frontiers in Microbiology | 56 | 1.0523 | `10.3389/fmicb.2020.01729` |
| 70 | Biofilm_niche_adap | pH Adaptation stabilizes bacterial communities | 2024 | npj Biodiversity | 26 | 1.0425 | `10.1038/s44185-024-00063-5` |
| 71 | BGC_antiSMASH | Deep self-supervised learning for biosynthetic gene cluster detection and pro... | 2022 | bioRxiv | 37 | 1.0419 | `10.1371/journal.pcbi.1011162` |
| 72 | Virulence_pathogen | A GWAS on Helicobacter pylori strains points to genetic variants associated w... | 2018 | BMC Biology | 74 | 1.04 | `10.1186/s12915-018-0550-3` |
| 73 | Metabolic_modeling | Genome-scale metabolic reconstructions and theoretical investigation of metha... | 2015 | Microbial Cell Factories | 123 | 1.0374 | `10.1186/s12934-015-0377-3` |
| 74 | Metabolic_modeling | Emergence of microbial diversity due to cross-feeding interactions in a spati... | 2016 | bioRxiv | 100 | 1.0317 | `10.1186/s12918-017-0430-4` |
| 75 | Phylogenomics_outb | Core Genome Multilocus Sequence Typing and Single Nucleotide Polymorphism Ana... | 2018 | Journal of Clinical Micro | 70 | 1.0305 | `10.1128/JCM.00517-18` |
| 76 | Pangenomics_compar | Cicer super-pangenome provides insights into species evolution and agronomic ... | 2024 | Nature Genetics | 55 | 1.0293 | `10.1038/s41588-024-01760-4` |
| 77 | Probiotic_benefici | Unveiling the Probiotic Potential of Streptococcus thermophilus MCC0200: Insi... | 2024 | Microorganisms | 24 | 1.0292 | `10.3390/microorganisms12020347` |
| 78 | Virulence_pathogen | Targeting anti-virulence factor strategies of bacterial pathogens | 2025 | Biosafety and Health | 20 | 1.0289 | `10.1016/j.bsheal.2025.01.006` |
| 79 | Biofilm_niche_adap | Probiotic Lactobacillus sp. Strains Inhibit Growth, Adhesion, Biofilm Formati... | 2021 | Microorganisms | 40 | 1.0251 | `10.3390/microorganisms9040728` |
| 80 | AMR_genotype_pheno | Direct prediction of carbapenem resistance in Pseudomonas aeruginosa by whole... | 2023 | Journal of Clinical Micro | 28 | 1.025 | `10.1128/jcm.00617-23` |
| 81 | BGC_antiSMASH | Targeted Genome Mining Reveals the Biosynthetic Gene Clusters of Natural Prod... | 2021 | Journal of the American C | 39 | 1.0208 | `10.1021/jacs.1c01516` |
| 82 | Phylogenomics_outb | vSNP: a SNP pipeline for the generation of transparent SNP matrices and phylo... | 2024 | BMC Genomics | 16 | 1.0122 | `10.1186/s12864-024-10437-5` |
| 83 | Probiotic_benefici | Safety assessment of Enterococcus lactis strains complemented with comparativ... | 2023 | BMC Genomics | 25 | 1.006 | `10.1186/s12864-023-09749-9` |
| 84 | AMR_genotype_pheno | Machine learning-based prediction of antibiotic resistance in Mycobacterium t... | 2024 | BMC Infectious Diseases | 20 | 0.9989 | `10.1186/s12879-024-10282-7` |
| 85 | Biofilm_niche_adap | Trait‐Based Life History Strategies Shape Bacterial Niche Breadth | 2025 | Advancement of science | 38 | 0.9964 | `10.1002/advs.202405947` |
| 86 | Probiotic_benefici | Safety assessment of Enterococcus lactis based on comparative genomics and ph... | 2023 | Frontiers in Microbiology | 23 | 0.9921 | `10.3389/fmicb.2023.1196558` |
| 87 | Virulence_pathogen | Improved prediction of bacterial CRISPRi guide efficiency from depletion scre... | 2024 | Genome Biology | 19 | 0.9904 | `10.1186/s13059-023-03153-y` |
| 88 | Phylogenomics_outb | Whole-Genome Sequencing for Tracing the Genetic Diversity of Brucella abortus... | 2021 | Pathogens | 32 | 0.9874 | `10.3390/pathogens10060759` |
| 89 | Probiotic_benefici | Whole genome sequence analysis and in-vitro probiotic characterization of Bac... | 2023 | Genomics | 22 | 0.9847 | `10.1016/j.ygeno.2023.110637` |
| 90 | Probiotic_benefici | Mining the genome of Bacillus velezensis FS26 for probiotic markers and secon... | 2023 | Microbial Pathogenesis | 37 | 0.9819 | `10.1016/j.micpath.2023.106161` |
| 91 | Metabolic_modeling | Metabolic modelling in a dynamic evolutionary framework predicts adaptive div... | 2016 | BMC Evolutionary Biology | 74 | 0.98 | `10.1186/s12862-016-0733-x` |
| 92 | Pangenomics_compar | A chromosome-level reference genome and pangenome for barn swallow population... | 2023 | Cell Reports | 21 | 0.977 | `10.1016/j.celrep.2023.111992` |
| 93 | Probiotic_benefici | Assessment of Safety and Probiotic Traits of Enterococcus durans OSY-EGY, Iso... | 2020 | Frontiers in Microbiology | 35 | 0.9725 | `10.3389/fmicb.2020.608314` |
| 94 | Pangenomics_compar | PanGraph: scalable bacterial pan-genome graph construction | 2022 | bioRxiv | 24 | 0.9692 | `10.1101/2022.02.24.481757` |
| 95 | Metabolic_modeling | Pangenome reconstruction of Lactobacillaceae metabolism predicts species-spec... | 2023 | bioRxiv | 19 | 0.9604 | `10.1128/msystems.00156-24` |
| 96 | Pangenomics_compar | Comparative genomics and pangenome-oriented studies reveal high homogeneity o... | 2020 | BMC Genomics | 23 | 0.9521 | `10.1186/s12864-020-06863-w` |
| 97 | AMR_genotype_pheno | Pioneering Klebsiella Pneumoniae Antibiotic Resistance Prediction With Artifi... | 2024 | Journal of Medical Intern | 15 | 0.9516 | `10.2196/58039` |
| 98 | AMR_genotype_pheno | Global genomic epidemiology of chromosomally mediated non-enzymatic carbapene... | 2023 | Frontiers in Microbiology | 13 | 0.9485 | `10.3389/fmicb.2023.1271733` |
| 99 | Phylogenomics_outb | Aspergillus Outbreak in an Intensive Care Unit: Source Analysis with Whole Ge... | 2024 | Journal of Fungi | 13 | 0.9285 | `10.3390/jof10010051` |
| 100 | AMR_genotype_pheno | Machine learning-based colistin resistance marker screening and phenotype pre... | 2023 | Journal of Infection | 12 | 0.8856 | `10.1016/j.jinf.2023.11.009` |

## Provenance
- Existing inventory: `~/Dropbox/REPLICATE-PROJECT/BVBRC-*/` (19 dirs)
- Score map: `MASTER_SCORES_2026-06-20.csv` (152 rows)
- Curated candidates: `/tmp/bvbrc_top81_curated.tsv` (81 rows from 2026-06-20 BVBRC-100 curation subagent)
- Curation summary: `/tmp/bvbrc_curation_summary.md`
- Raw harvest: `/tmp/bvbrc_candidates_raw.tsv` (120 rows pre-trim)