# Brief — BVBRC-29

**Paper:** Bazinet AL (2017). "Pan-genome and phylogeny of *Bacillus cereus* sensu lato." *BMC Evolutionary Biology* 17:176. DOI 10.1186/s12862-017-1020-1. PMID:28768476.
(Task metadata listed "Liu et al." — the downloaded PDF/txt is the single-author Bazinet 2017 paper; that is the paper replicated here.)

**What:** Bazinet characterized the *B. cereus* sensu lato (s.l.) pan-genome and built the (then) largest phylogeny of the group. Headline claims: the pan-genome is ≈60,000 genes with ≈600 core genes (present in ≥99% of taxa); ~114 complete genomes (BCSL_114) annotated with Prokka and clustered with Roary; three major clades (Clade 1/2/3) that hierBAPS subdivides into nine clusters; all analyses recapitulate the classic Clade + Group (I–VII) classification and confirm species like *B. anthracis* nested within *B. cereus s.s.*

**Why replicate:** The whole pipeline (Mash species delimitation → Prokka annotation → Roary pan/core genome → distance/ML phylogeny) is standard, free, and re-runnable on public NCBI genomes. We independently pull ~25–35 representative *B. cereus* s.l. genomes, recompute genome stats, Mash/FastANI distances, a Roary core/pan-genome, and a FastTree phylogeny, then test the paper's core-fraction, ANI-cluster, and clade-topology claims with a free-Argo LLM judge.
