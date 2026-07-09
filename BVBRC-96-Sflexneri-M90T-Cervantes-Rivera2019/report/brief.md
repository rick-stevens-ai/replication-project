# Brief — BVBRC-96

Cervantes-Rivera, Tronnet & Puhar (BMC Genomics 2020, PMID 32252626) delivered the first *complete
gapless* genome of the flagship *Shigella flexneri* pathogenesis reference strain 5a M90T — two
circular replicons, a 4,596,714-bp chromosome and the 232,195-bp pWR100 virulence megaplasmid —
assembled with PacBio SMRT reads (Canu 1.7, ~157×) polished by Illumina RNA-seq, then augmented with
6,723 primary / 7,328 secondary transcriptional start sites from dRNA-seq. We independently
re-verified the deposited Umeå assembly (GCF_004799585.1; replicons CP037923/CP037924) via the free
NCBI Datasets REST v2 API, ran a BVBRC-96-workflow-equivalent open-source stack on uicgpu (PlasmidFinder
via abricate for plasmid replicon typing, VFDB/CARD via abricate for Specialty Genes, PGAP GFF for
Comprehensive Genome Analysis feature counts, mash + fastANI for the Similar Genome Finder), and
reproduced every testable structural, phylogenomic and functional claim: both replicons bp-for-bp,
IncFII replicon on pWR100 (PlasmidFinder), the entire T3SS apparatus + effectors on the plasmid
(mxi/spa needle, ipa/ipg invasins, osp effectors, virF/virB master regulators — 64 VFDB hits on the
plasmid), the SHI-2 aerobactin island (iucABCD/iutA) on the chromosome, 5003 CDS / 102 tRNA / 22 rRNA
/ 757 pseudogenes, and 99.933% ANI to the previously-used *S. flexneri* 5b 8401 reference (justifying
the need for a native 5a assembly). The dRNA-seq TSS counts were not re-derived from raw reads and
the de-novo assembly was not re-run from raw PacBio, so this is PARTIAL, not full REPLICATED. A prior
independent sibling report (BVBRC-54) exists for the same paper; this replication is fresh,
non-overwriting, uses independently pulled data, and independently converges on the same conclusion.
