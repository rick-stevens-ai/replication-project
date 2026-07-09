"""
Single internal-arithmetic check in Langen et al. 2020 (IRI-DICE).

Paper text:
  "The fraction of protein-coding genes in mammalian genomes is relatively
   low with an estimate of less than 2% of genomic material ... Applying
   this gene-centric paradigm, a DSB in a relevant IRI-DICE target would
   only occur in approximately one out of 50 randomly distributed
   ionization events."

This script reproduces the only quantitative inference the paper makes.
"""

protein_coding_fraction = 0.02   # "<2%", cited from IHGSC 2001
events_per_target_hit = 1.0 / protein_coding_fraction
print(f"Protein-coding fraction (upper bound from paper): {protein_coding_fraction:.4f}")
print(f"Expected ionization events per target hit:        {events_per_target_hit:.2f}")
print()
print("Paper's claim: approximately 1 in 50.")
print(f"Computed:      1 in {events_per_target_hit:.0f}.")
assert abs(events_per_target_hit - 50.0) < 1e-9, "Arithmetic mismatch"
print("PASS: matches paper's own 'one out of 50' statement exactly.")
