#!/usr/bin/env python3
"""Search for specific functional genes in L. lactis LL16 genome using BLAST."""

import subprocess
import os
import json
import tempfile

GENOME = "../data/LL16_genome.fna"
PROTEINS = "LL16_proteins.faa"

# Key protein sequences to search for (representative sequences from UniProt/NCBI)
# These are conserved domains/motifs for the genes the paper highlights

KEY_GENES = {
    # GABA pathway
    "gadB_glutamate_decarboxylase": "MFNKNEIDAHMYDLARLCQQLGLDEYVNVTSSPYTSATMPQMTDKLTLTPEQKNEFYTALQGIKYAESSAEASARLFNKPDLLFATESYNSIDKEAATNGEQPIVFNDRPALQFLPAYDDHFYNP",
    # Bile salt hydrolase (BSH)
    "bsh_bile_salt_hydrolase": "MNFSEIKNLKVPDDFILDDGTLDRNIGSWVSEITKKYPDLKTPIANVRFPNLTDEE",
    # Lactococcin B
    "lcnB_lactococcin_B": "MKQFNYLSHKDLAVVVGGSMFASSYAAKEGAAAGIVAGAHFGKNKFHSPAAFAAK",
    # Enterolysin A  
    "enlA_enterolysin_A": "MKRLVKSLNLSSSFFLLALTCGILLDGNTVSAADTISTYSYSD",
    # Tryptophan decarboxylase / aromatic amino acid decarboxylase (serotonin)
    "tdc_tryptophan_decarboxylase": "MENVKGLLKDPKFNEFGIQFHPEVKDPSEYRALIYDAGFGDSFDTF",
    # Fibronectin binding protein
    "fbp_fibronectin_binding": "MKKLALVSTALMATAVAGADNTVVKKEEKLAKNLAAIKDLDKAAQAALE",
    # EF-Tu (elongation factor, used as adhesin indicator)
    "efTu_elongation_factor": "MAKGEFIRTKPHVNVGTIGHVDHGKTTLTAAITKILSKKYGDKEKQERGITINTAHVEYETE",
    # Cold shock protein
    "cspA_cold_shock": "MLEGKVKWFNEGKFGFITPDDGSKDVFVHFNAIQGEGFKTLEEG",
}

# Create BLAST database from genome
print("Building BLAST database...")
subprocess.run(["makeblastdb", "-in", GENOME, "-dbtype", "nucl", "-out", "LL16_db"], 
               capture_output=True, text=True)

# Also make protein db
subprocess.run(["makeblastdb", "-in", PROTEINS, "-dbtype", "prot", "-out", "LL16_prot_db"],
               capture_output=True, text=True)

results = {}
print("\n=== FUNCTIONAL GENE SEARCH (tblastn) ===\n")

for gene_name, query_seq in KEY_GENES.items():
    # Write query to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.faa', delete=False) as f:
        f.write(f">{gene_name}\n{query_seq}\n")
        query_file = f.name
    
    # Run tblastn against genome
    cmd = [
        "tblastn", "-query", query_file, "-db", "LL16_db",
        "-evalue", "1e-5", "-outfmt", "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore",
        "-max_target_seqs", "5"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    os.unlink(query_file)
    
    hits = []
    if result.stdout.strip():
        for line in result.stdout.strip().split("\n"):
            fields = line.split("\t")
            hits.append({
                "subject": fields[1],
                "pident": float(fields[2]),
                "length": int(fields[3]),
                "evalue": float(fields[10]),
                "bitscore": float(fields[11]),
                "sstart": int(fields[8]),
                "send": int(fields[9]),
            })
    
    status = "FOUND" if hits else "NOT FOUND"
    results[gene_name] = {
        "status": status,
        "num_hits": len(hits),
        "best_hit": hits[0] if hits else None,
        "all_hits": hits[:3]  # top 3
    }
    
    if hits:
        best = hits[0]
        print(f"  {gene_name}: {status} (best: {best['pident']:.1f}% identity, E={best['evalue']:.1e}, score={best['bitscore']:.0f})")
    else:
        print(f"  {gene_name}: {status}")

# Save results
with open("functional_genes.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to functional_genes.json")

# Summary
found = sum(1 for v in results.values() if v['status'] == 'FOUND')
print(f"\n=== SUMMARY ===")
print(f"Found: {found}/{len(results)} key genes")
