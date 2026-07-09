# Brief

**Paper:** Rahman et al., *J. Adv. Vet. Anim. Res.* 10(3): 570-578 (Sep 2023). PMID 37969805 / PMC10636080 / DOI 10.5455/javar.2023.j711.

**What:** WGS + annotation + MLST + AMR/virulence profiling + phylogenetic placement of *Aeromonas veronii* strain **Alim_AV_1000**, isolated from the liver of a diseased stinging catfish (*Heteropneustes fossilis*) in Mymensingh, Bangladesh (Oct 2021). The paper reports the first WGS-characterized *A. veronii* strain from Shing fish in Bangladesh and additionally tests antibiogram + wet-lab fish pathogenicity.

**Why replicate:** The paper makes explicit numerical claims (genome size, N50, CDS count, MLST ST 492, AMR/virulence counts, 2-intact-prophage claim, closest phylogenetic relative TH0426) all backed by a deposited genome (GCA_026738955.1). These are directly testable from public data — a canonical bioinformatics-replication target.

**Method (short):** Downloaded the deposited assembly + PGAP annotation via NCBI Datasets v2; recomputed assembly stats (contigs, N50, GC%, coding density); ran abricate against CARD/ResFinder/NCBI-AMRFinder/VFDB/PlasmidFinder; queried pubMLST for the MLST profile; computed ANI (skani + fastANI) to TH0426, B565, FDAARGOS_632; used PGAP feature counts as proxy for prophage clustering.

**Verdict:** PARTIAL. Assembly-level statistics reproduce exactly (contigs 93, N50 150,337, L50 12, GC 58.87%, size Δ=51 bp); annotation counts reproduce within tool-variance (tRNA 102 exact, CDS 4,099 vs paper's RAST 4,229); PlasmidFinder confirms 0 plasmids; prophage gene clustering is qualitatively consistent with paper's PHASTER "2 intact + 1 incomplete". **BUT** the MLST claim ST 492 is **contradicted** — my scan finds a completely different allele profile (0 of ST 492's 6 alleles match), and the BioProject accession stated in the paper (PRJNA810265) is wrong (points to a different organism, *Pasteurella multocida* DC2020, by the same institution). Correct BioProject is PRJNA827572.
