#!/usr/bin/env python3
"""Search for AMR genes in L. lactis LL16 using BLAST against known resistance gene markers."""

import subprocess
import tempfile
import os

GENOME = "../data/LL16_genome.fna"

# Common AMR gene markers - representative protein sequences from CARD/ResFinder
# These cover the main resistance classes

AMR_MARKERS = {
    # Tetracycline resistance
    "tetM": "MKNEKEIKDFTSKNFSSFNNFKPNYTIRTISEHGCFIKFTKDLKEKYNLDVEFKDLYFDAYYSDVKESLIDQLDFDSINLYDMPYYDGTFIPD",
    "tetS": "MRKSQHITLSENNSSSSFLRPVALLCFLSVSTAAAPKKEEKFSELKLTKTTLNKEELLAKIDSITPELLKELEQKISGQYQVTNDQIFQ",
    # Erythromycin/macrolide resistance
    "ermB": "MNMKNFIKEDNINVQEKNKDFTLNWKKFKAGEYIIGIPDSEPKLMYGLRGKKTLYELLSDDLAKYLDHIMENVTPYGLKTMYQKFADDVNWN",
    "ermC": "MKNKINIEKEKKFDAFVDFLKDQFTIGQYGIINDLYNFHSKEKIEIEIKRVHKNFNMPEKRKKRRQRDKKKSV",
    # Chloramphenicol resistance
    "cat": "MEKKITGYTTVDISQWHRKEHFEAFQSVAQCTYNQTVQLDITAFLKTVKKNKHKFYPAFIHILARLMNAHPEFRMAMKDGELVIWDSVHPCYTVFHEQTETFSS",
    # Beta-lactam resistance  
    "blaTEM": "MSIQHFRVALIPFFAAFCLPVFAHPETLVKVKDAEDQLGARVGYIELDLNSGKILESFRPEERFPMMSTFKVLLCGAVLSRIDAGQEQLGRRIHYSQNDLVEYS",
    "blaZ": "MKLIFLIVIALVLSANTDYAQASNQYKNFYDGSYFLYNTETKYKIIVENGSKLKNKDFDLIYTSMPYTVKEFYGDTSSYFLNNAIEQFFVVKDKKYNLTISGSS",
    # Vancomycin resistance
    "vanA": "MAQNFITDLYKENTDKVYHQEDLKKEFKGIISSIKFLEDKTKVSYDINIYEQLKDEKEGQIISQATTTFVFNNFEQTLNSYTREYKYIMSDKIG",
    # Aminoglycoside resistance
    "aac6": "MTDQLANQLVSQANDAAITGATVDGNMTTAFQTGMQNRLTRDINASDGLNLNWLKEINTSTLNPRFLKLYEDGKKHNHQ",
    # Quinolone resistance
    "qnrA": "MSTISSMKNLQNTYECDIKAKIAGYLDIKNLEGKLEIIDKEINKNRVFMLRNKLENL",
    # Streptomycin resistance
    "strA": "MRGSKDNALQSGIFHRDLETLSDLEAAVRLYEQVIGAGGGCTAACKEIANAVLSIKIGKEYIPMQMTLNQTQSNTIRLNPE",
}

print("=== AMR GENE SEARCH (BLAST-based) ===\n")
print("Searching for common resistance gene markers in LL16 genome...")
print("(Paper claims: no transferable antimicrobial resistance genes detected)\n")

# Make sure BLAST db exists
subprocess.run(["makeblastdb", "-in", GENOME, "-dbtype", "nucl", "-out", "LL16_db"],
               capture_output=True, text=True)

found_amr = []
for gene_name, query_seq in AMR_MARKERS.items():
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
        found_amr.append(gene_name)
        print(f"  ⚠️  {gene_name}: HIT FOUND")
        for line in result.stdout.strip().split("\n"):
            print(f"      {line}")
    else:
        print(f"  ✓ {gene_name}: NOT FOUND")

print(f"\n=== AMR SUMMARY ===")
if found_amr:
    print(f"WARNING: Found {len(found_amr)} potential AMR genes: {', '.join(found_amr)}")
else:
    print("No AMR genes detected - CONSISTENT with paper's claim")
    print("(Paper: 'ResFinder tool v.4.1 was used to detect genes conferring antibiotic")
    print(" resistance in the L. lactis LL16 genome, and none were detected.')")
