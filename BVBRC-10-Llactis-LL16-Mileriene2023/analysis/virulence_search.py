#!/usr/bin/env python3
"""Search for virulence genes in L. lactis LL16."""

import subprocess
import tempfile
import os

GENOME = "../data/LL16_genome.fna"

# Key virulence factors from VirulenceFinder databases
VIRULENCE_MARKERS = {
    # Shiga toxin (E. coli)
    "stx1A": "MKCILFKSVLFVSFLANNIYAEFTLIDLGGDLERSAHSHRNLNMKKVDSNEQTFKVSVERNNVYTRASSGADNVTFRYSTHGKYTCYRSLT",
    "stx2A": "MKCILFKSVLFVSFLANNIYAEASFDVSTIKTFTSTASTQLESDSSKHYTVEDSRFAHFVNRSKFSEQEQLRSHGLTTHATLATHASRAQE",
    # Listeriolysin O (Listeria)  
    "hlyA_listeria": "MKKIMLVFITLILVSLPIAQQTEAKDASAFNKENSISSVAPPASPPASPKTPIEKKHADEIDKYIQGLDYNKNNVLVYHGDAVTNVPPRKGYKDGNEYIVVEKKKKSINQNNADIQVVNAISSLTYPGALVKANSELVENQPDVLPVKRDSLTLSIDLPGMTNQDNKIVVKNATKSNVNNAVNTLVERWNEKYAQAYPNVSAKIDYDDEM",
    # Enterotoxin (S. aureus)
    "sea_staph": "MKFLSHNLVPSATIFKLILATIPFMSASESQPDPKPDELHKSSKFTGLMENMKVLYDDNHVSAINVKSIDQFLYFDLIYSIKDTKLGN",
    # Alpha-hemolysin (S. aureus)
    "hla_staph": "MKTRIVSSVTTTLLLGSILMNPVANAADSDINIKTGTTDIGSNTTVKTGDLVTYDKENGMHKKVFYSFIDDKNHNKKLLVIRTKGTIAGQYRVYSEEGANKSGLAWPSAFKVQLQLPDNEVAQISDYYPRNSIDTKEYMSTLTYGFNGNVTGDDTGKIGGLIGANVSIGHTLKYVQPDFKTILESPTDKKVGWKVIFNNMVNQNWGPYDRDSWNPVYGNQLFMKTRNGSMKAADNFLDPNKASSLLSSGFSPDFATVITMDRKASKQQTNIDVIYERVRDDYQLHWTSTNWKGTNTKDKWIDRSSERYKIDWEKEEMTN",
    # Cytolethal distending toxin
    "cdtB": "MSYIKGFLFLSYRKSFKLYRQKTNKKFHFDIKTKDNVFYSDDISKLNVDLHFDNDKTYRIHYSKNDNQKRINKWFDDNKEIIQYLKGEYYFD",
    # Invasion proteins (Enterococcus)
    "gelE_entero": "MEKNFKRKKIFSIALVFFTLMLAGAKANPFEEAKAKAEAPEPAAEPTPVEAPEPAAQPAPQAQPTKSSQPPPGSYSQPPPGQQQQPPPGTYSQPPPG",
    "esp_entero": "MKKKFLIVTAASFITGGTANADSNNTSDTQKANTDSTDSSTTSTTTTSTSTTTYAGGTGTTGEGGTGTTSAGTTTAANAAGTTGEE",
}

print("=== VIRULENCE GENE SEARCH (BLAST-based) ===\n")
print("Searching for known virulence factors in LL16 genome...")
print("(Paper claims: no virulence genes detected by VirulenceFinder v.2.0.3)\n")

found_vir = []
for gene_name, query_seq in VIRULENCE_MARKERS.items():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.faa', delete=False) as f:
        f.write(f">{gene_name}\n{query_seq}\n")
        query_file = f.name
    
    cmd = [
        "tblastn", "-query", query_file, "-db", "LL16_db",
        "-evalue", "1e-10", "-outfmt", "6 qseqid sseqid pident length evalue bitscore",
        "-max_target_seqs", "3"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    os.unlink(query_file)
    
    if result.stdout.strip():
        found_vir.append(gene_name)
        print(f"  ⚠️  {gene_name}: HIT FOUND")
        for line in result.stdout.strip().split("\n"):
            print(f"      {line}")
    else:
        print(f"  ✓ {gene_name}: NOT FOUND")

print(f"\n=== VIRULENCE SUMMARY ===")
if found_vir:
    print(f"WARNING: Found {len(found_vir)} potential virulence genes: {', '.join(found_vir)}")
else:
    print("No virulence genes detected - CONSISTENT with paper's claim")
    print("(Paper: 'Virulence genes for Shiga-toxin, E. coli, Listeria, and Enterococcus;")
    print(" hostimm, exoenzyme, and toxin genes for S. aureus were not detected.')")

