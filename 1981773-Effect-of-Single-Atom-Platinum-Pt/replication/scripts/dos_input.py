#!/usr/bin/env python3
"""Generate nscf + dos.x inputs for a relaxed slab."""
import os, sys
from pathlib import Path
from pymatgen.core import Structure

ROOT = Path(os.path.expanduser("~/projects/replicate-1981773"))
PSEUDO_DIR = str(ROOT / "pseudo")
PSEUDO = {"La":"La.upf", "Ti":"Ti.upf", "O":"O.upf", "Pt":"Pt.upf"}
ECUTWFC = 60.0
ECUTRHO = 480.0

def write_nscf(struct, out_dir, prefix, kpts):
    p = Path(out_dir)
    out_path = p / f"{prefix}_nscf.in"
    species = sorted(set([s.specie.symbol for s in struct]))
    nat, ntyp = len(struct), len(species)
    masses = {"La":138.9055, "Ti":47.867, "O":15.999, "Pt":195.084}
    lines = [
        "&CONTROL",
        "  calculation = 'nscf'",
        "  restart_mode = 'from_scratch'",
        f"  prefix = '{prefix}'",
        "  outdir = './tmp'",
        f"  pseudo_dir = '{PSEUDO_DIR}'",
        "  verbosity = 'low'",
        "/",
        "&SYSTEM",
        "  ibrav = 0",
        f"  nat = {nat}", f"  ntyp = {ntyp}",
        f"  ecutwfc = {ECUTWFC}", f"  ecutrho = {ECUTRHO}",
        "  occupations = 'tetrahedra_opt'",
        f"  nbnd = {int(nat*6)}",  # generous
        "  nosym = .true.",
        "  noinv = .true.",
        "/",
        "&ELECTRONS",
        "  conv_thr = 1.0d-8",
        "  diagonalization = 'david'",
        "/",
        "ATOMIC_SPECIES",
    ]
    for sp in species:
        lines.append(f"  {sp}  {masses[sp]}  {PSEUDO[sp]}")
    lines.append("CELL_PARAMETERS angstrom")
    for r in struct.lattice.matrix:
        lines.append(f"  {r[0]:.10f}  {r[1]:.10f}  {r[2]:.10f}")
    lines.append("ATOMIC_POSITIONS crystal")
    for site in struct:
        c = site.frac_coords
        lines.append(f"  {site.specie.symbol}  {c[0]:.10f}  {c[1]:.10f}  {c[2]:.10f}")
    lines.append("K_POINTS automatic")
    lines.append(f"  {kpts[0]} {kpts[1]} {kpts[2]}  0 0 0")
    out_path.write_text("\n".join(lines)+"\n")
    # dos.x input
    dos_path = p / f"{prefix}_dos.in"
    dos_lines = [
        "&DOS",
        f"  prefix = '{prefix}'",
        "  outdir = './tmp'",
        f"  fildos = '{prefix}.dos'",
        "  Emin = -25.0, Emax = 15.0, DeltaE = 0.05",
        "  degauss = 0.01",
        "  ngauss = 0",
        "/"
    ]
    dos_path.write_text("\n".join(dos_lines)+"\n")
    # projwfc input
    pj_path = p / f"{prefix}_projwfc.in"
    pj_lines = [
        "&PROJWFC",
        f"  prefix = '{prefix}'",
        "  outdir = './tmp'",
        f"  filpdos = '{prefix}'",
        "  Emin = -25.0, Emax = 15.0, DeltaE = 0.05",
        "  degauss = 0.01",
        "/"
    ]
    pj_path.write_text("\n".join(pj_lines)+"\n")
    print(f"  wrote {out_path.name}, {dos_path.name}, {pj_path.name}")

def main():
    # Use the structures from initial build — assume slab relaxed positions will be in final outputs.
    # For now, generate using original build geometry; user can rerun after relax.
    for tag, kpts in [("slab_001",(4,3,1)), ("slab_001_Pt",(4,3,1)),
                      ("slab_010",(4,3,1)), ("slab_010_Pt",(4,3,1))]:
        cif = ROOT / tag / f"{tag.replace('_Pt','_Pt') if '_Pt' in tag else tag}.cif"
        if not cif.exists():
            # try alt names
            candidates = list((ROOT/tag).glob("*.cif"))
            if candidates: cif = candidates[0]
            else: print(f"no cif in {tag}"); continue
        s = Structure.from_file(str(cif))
        # Fix species for doped slab (replace happens already in initial build)
        prefix = "lto"
        print(tag)
        write_nscf(s, ROOT/tag, prefix, kpts)

if __name__ == "__main__":
    main()
