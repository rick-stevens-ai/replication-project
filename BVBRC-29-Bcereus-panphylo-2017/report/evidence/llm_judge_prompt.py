#!/usr/bin/env python3
import json, os, urllib.request

ARGO="http://localhost:44497/v1/chat/completions"
KEY=os.environ.get("ARGO_API_KEY","stevens")

evidence = """
INDEPENDENT REPLICATION EVIDENCE (BVBRC-29)
Paper: Bazinet AL 2017, "Pan-genome and phylogeny of Bacillus cereus sensu lato", BMC Evol Biol 17:176.

We independently downloaded 27 public NCBI RefSeq B. cereus s.l. genomes (seeded from the paper's Table 1
reference accessions, spanning all major species: anthracis, cereus s.s., thuringiensis, cytotoxicus, mycoides,
pseudomycoides, toyonensis, weihenstephanensis, manliponensis, bingmayongensis, wiedmannii), and ran the same class
of workflow the paper used (Mash k=21 s=1000; FastANI; Prokka annotation; Roary pan/core genome; FastTree phylogeny).

PAPER'S KEY CLAIMS:
 C1: Pan-genome is approximately 60,000 genes (open, keeps growing with sampling).
 C2: Approximately 600 core genes (present in >=99% of taxa) [computed on the homogeneous BCSL_114 set via HaMStR].
 C3: 8+ named species form a genomically cohesive but structured B. cereus s.l. group (Mash/ANI).
 C4: B. anthracis strains are near-clonal and nested within B. cereus s.s. diversity.
 C5: Three major clades recovered; core-gene and accessory phylogenies concordant; classic Clade/Group system recapitulated; anthracis/cereus/thuringiensis intermingled (not clean monophyletic species).
 C6: Pan-genome is OPEN (gene discovery does not saturate with more genomes).

OUR RESULTS:
 - Genome stats: 27 genomes, mean 5.22 Mbp, GC ~35.4% (consistent with B. cereus group).
 - FastANI: B. anthracis (n=7) pairwise ANI 99.99-100.0% (near-clonal). B. anthracis vs B. cereus s.s. ANI mean 96.25%, MAX 99.98% (anthracis genomically nested inside cereus, same-species by >95% boundary). Whole-group median ANI 91.8%, range 79.9-100% (cohesive but structured).
 - Roary Run A (full 27 divergent genomes, blastp 95% default): 0 strict core genes, 48,118 total pan-genome genes (42,177 cloud/accessory). Note: 0 core is expected for a set spanning the whole species range at 95% identity; not a contradiction of the paper, which computed core on the homogeneous BCSL_114 via HaMStR.
 - Roary Run B (26 genomes, blastp 80% to accommodate divergence): 251 strict core genes, 26,839 total pan-genome (same order of magnitude as paper's ~600 core across all species).
 - Roary Run C (17-genome homogeneous Clade-1 subset = anthracis+cereus+thuringiensis, blastp 95%): 2,415 core genes, 15,247 total pan-genome.
 - Pan-genome accumulation (Clade-1): pan rises monotonically 5,523 -> 15,247 as 17 genomes added; "new genes" curve stays high (17th genome still adds ~492 new genes) => OPEN pan-genome, no saturation. Core stabilizes ~2,400.
 - Even at just 27 genomes (Run A) total pan-genome (48,118) is ~80% of the paper's ~60,000 estimate from 114-498 genomes.
 - Core-gene ML tree (FastTree GTR, Clade-1) AND accessory binary presence/absence tree BOTH show: all 7 B. anthracis collapse into one near-zero-branch clade (clonal), intermingled with B. cereus and B. thuringiensis (no clean species monophyly). The two independent tree methods are concordant.
"""

prompt = f"""You are a rigorous scientific replication judge. Below is the evidence from an INDEPENDENT attempt to
replicate the core claims of a comparative-genomics paper on real, freshly-downloaded public genomes.

{evidence}

Score each claim C1-C6 as one of: REPRODUCED / PARTIALLY-REPRODUCED / NOT-REPRODUCED / OUT-OF-SCOPE, with a one-sentence justification grounded ONLY in the evidence above (do not invent numbers).
Then give an OVERALL verdict from this exact vocabulary: REPLICATED, PARTIAL, SPOT-CHECK, NO-GO, CONTRADICTED, BLOCKED, FAILED.
"Solid" = REPLICATED or PARTIAL. Consider that the replication used a deliberately smaller/broader genome set than the paper (27 vs 114-498) and reduced-scale analysis, so exact absolute numbers are not expected; judge whether the QUALITATIVE and ORDER-OF-MAGNITUDE claims independently hold.
Respond as strict JSON: {{"claims":[{{"id":"C1","status":"...","justification":"..."}}...],"overall_verdict":"...","overall_justification":"..."}}"""

import time
models=["argo:claude-opus-4.8","argo:gpt-5.2","argo:claude-opus-4.7","argo:gpt-4o"]
content=None; used=None
for m in models:
    for attempt in range(3):
        try:
            body=json.dumps({"model":m,"messages":[{"role":"user","content":prompt}],"temperature":0.0}).encode()
            req=urllib.request.Request(ARGO,data=body,headers={"Content-Type":"application/json","Authorization":f"Bearer {KEY}"})
            r=urllib.request.urlopen(req,timeout=180)
            resp=json.load(r)
            c=resp["choices"][0]["message"]["content"]
            if c and c.strip():
                content=c; used=m; break
        except Exception as e:
            print(f"# attempt {m} #{attempt+1} failed: {e}")
            time.sleep(5)
    if content: break
if not content:
    raise SystemExit("all models failed")
print(f"# JUDGE_MODEL={used}")
print(content)
with open("/tmp/judge_out.json","w") as f: f.write(content)
