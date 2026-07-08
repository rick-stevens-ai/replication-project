#!/usr/bin/env python3
"""Step 1: Create PD_systems.faa with clear headers mapping system -> protein."""
import os

BASEDIR = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/36123438-Anti-phage-defense-Ecoli")

# Read system-protein map
system_map = {}
with open(os.path.join(BASEDIR, "data/system_protein_map.tsv")) as f:
    next(f)  # skip header
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) == 2:
            system_map.setdefault(parts[0], []).append(parts[1])

# Read all protein sequences
sequences = {}
current_id = None
current_seq = []
with open(os.path.join(BASEDIR, "data/defense_proteins.fasta")) as f:
    for line in f:
        if line.startswith(">"):
            if current_id:
                sequences[current_id] = "".join(current_seq)
            current_id = line.split()[0][1:]  # Get accession
            current_seq = []
        else:
            current_seq.append(line.strip())
    if current_id:
        sequences[current_id] = "".join(current_seq)

# Write PD_systems.faa with system-annotated headers
outpath = os.path.join(BASEDIR, "data/PD_systems.faa")
with open(outpath, "w") as out:
    for system in sorted(system_map.keys(), key=lambda s: (s.split("-")[1], int(s.split("-")[2]) if s.split("-")[2].isdigit() else 0)):
        proteins = system_map[system]
        for i, acc in enumerate(proteins, 1):
            seq = sequences.get(acc, "")
            if seq:
                gene_label = f"gene{i}" if len(proteins) > 1 else "single"
                out.write(f">{acc} | {system} | {gene_label} | len={len(seq)}aa\n")
                # Write in 80-char lines
                for j in range(0, len(seq), 80):
                    out.write(seq[j:j+80] + "\n")

print(f"Wrote {outpath}")
print(f"Systems: {len(system_map)}")
print(f"Total proteins: {sum(len(v) for v in system_map.values())}")
for sys_name in sorted(system_map.keys(), key=lambda s: (s.split("-")[1], int(s.split("-")[2]) if s.split("-")[2].isdigit() else 0)):
    prots = system_map[sys_name]
    print(f"  {sys_name}: {len(prots)} protein(s) — {', '.join(prots)}")
