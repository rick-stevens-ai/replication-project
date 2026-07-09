# Brief — BVBRC-54

Cervantes-Rivera, Tronnet & Puhar (BMC Genomics 2020) produced the first *complete, gapless*
genome for the flagship *Shigella flexneri* pathogenesis lab strain 5a M90T — a circular
chromosome (4,596,714 bp) plus the pWR100 virulence megaplasmid (232,195 bp) — via PacBio SMRT
long reads assembled with Canu and polished with Illumina RNA-seq, then annotated 6,723 primary /
7,328 secondary transcriptional start sites by dRNA-seq. We independently re-downloaded the
deposited Umeå assembly (GCF_004799585.1; replicons CP037923/CP037924) from NCBI, recomputed genome
statistics, and re-ran a BV-BRC-equivalent open-source workflow (Prokka annotation, abricate against
VFDB/Victors/CARD/PlasmidFinder, AMRFinderPlus, MLST) on uicgpu. The two replicons and both lengths
reproduce to the base pair, rRNA/tRNA counts match, and the specialty-gene scan independently
reconstructs the paper's core biology: the entire T3SS apparatus (mxi/spa), invasins (ipa), effector
suite (osp/ipaH), and virF/virB regulators sit on the pWR100 plasmid, while the chromosome carries the
SHI-2 aerobactin island — exactly as the paper describes. The one part not re-executed is the
dRNA-seq TSS catalogue (raw reads not fetched); its data availability is verified but the count was
not independently regenerated.
