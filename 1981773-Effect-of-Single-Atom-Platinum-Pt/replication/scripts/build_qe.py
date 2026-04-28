#!/usr/bin/env python3
"""Build QE inputs for La2Ti2O7 replication on uicgpu."""
import os, sys
from pathlib import Path
from pymatgen.core import Structure
from pymatgen.core.surface import SlabGenerator

ROOT = Path(os.path.expanduser("~/projects/replicate-1981773"))
PSEUDO_DIR = str(ROOT / "pseudo")
CIF = ROOT / "bulk" / "La2Ti2O7_mp559768.cif"

PSEUDO = {"La":"La.upf", "Ti":"Ti.upf", "O":"O.upf", "Pt":"Pt.upf"}
ECUTWFC = 60.0
ECUTRHO = 480.0

def write_qe_input(struct, out_path, calc="scf", kpts=(4,3,2), extra_control=None, extra_system=None, extra_electrons=None, extra_ions=None, extra_cell=None, fix_atoms_idx=None):
    """Write a QE pw.x input manually to have full control."""
    ctrl = {
        "calculation": f"'{calc}'",
        "restart_mode": "'from_scratch'",
        "prefix": "'lto'",
        "outdir": "'./tmp'",
        "pseudo_dir": f"'{PSEUDO_DIR}'",
        "verbosity": "'default'",
        "tprnfor": ".true.",
        "tstress": ".true.",
        "etot_conv_thr": "1.0d-5",
        "forc_conv_thr": "1.0d-3",
        "nstep": 100,
    }
    if extra_control: ctrl.update(extra_control)
    
    species = sorted(set([s.specie.symbol for s in struct]))
    nat = len(struct)
    ntyp = len(species)
    
    system = {
        "ibrav": 0,
        "nat": nat,
        "ntyp": ntyp,
        "ecutwfc": ECUTWFC,
        "ecutrho": ECUTRHO,
        "occupations": "'smearing'",
        "smearing": "'gaussian'",
        "degauss": 0.01,
    }
    if extra_system: system.update(extra_system)
    
    electrons = {
        "conv_thr": "1.0d-7",
        "mixing_beta": 0.3,
        "electron_maxstep": 200,
        "diagonalization": "'david'",
    }
    if extra_electrons: electrons.update(extra_electrons)
    
    lines = []
    lines.append("&CONTROL")
    for k,v in ctrl.items():
        lines.append(f"  {k} = {v}")
    lines.append("/")
    
    lines.append("&SYSTEM")
    for k,v in system.items():
        lines.append(f"  {k} = {v}")
    lines.append("/")
    
    lines.append("&ELECTRONS")
    for k,v in electrons.items():
        lines.append(f"  {k} = {v}")
    lines.append("/")
    
    if calc in ("relax","vc-relax","md","vc-md"):
        ions = {"ion_dynamics": "'bfgs'", "bfgs_ndim": 3}
        if extra_ions: ions.update(extra_ions)
        lines.append("&IONS")
        for k,v in ions.items():
            lines.append(f"  {k} = {v}")
        lines.append("/")
    
    if calc in ("vc-relax","vc-md"):
        cell = {"cell_dynamics": "'bfgs'", "press": 0.0, "press_conv_thr": 0.5}
        if extra_cell: cell.update(extra_cell)
        lines.append("&CELL")
        for k,v in cell.items():
            lines.append(f"  {k} = {v}")
        lines.append("/")
    
    lines.append("ATOMIC_SPECIES")
    masses = {"La":138.9055, "Ti":47.867, "O":15.999, "Pt":195.084}
    for sp in species:
        lines.append(f"  {sp}  {masses[sp]}  {PSEUDO[sp]}")
    
    lines.append("CELL_PARAMETERS angstrom")
    M = struct.lattice.matrix
    for row in M:
        lines.append(f"  {row[0]:.10f}  {row[1]:.10f}  {row[2]:.10f}")
    
    lines.append("ATOMIC_POSITIONS crystal")
    for i,site in enumerate(struct):
        c = site.frac_coords
        line = f"  {site.specie.symbol}  {c[0]:.10f}  {c[1]:.10f}  {c[2]:.10f}"
        if fix_atoms_idx is not None and i in fix_atoms_idx:
            line += "  0 0 0"
        lines.append(line)
    
    lines.append(f"K_POINTS automatic")
    lines.append(f"  {kpts[0]} {kpts[1]} {kpts[2]}  0 0 0")
    
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path,"w") as f:
        f.write("\n".join(lines)+"\n")
    print(f"Wrote {out_path} ({nat} atoms, kpts={kpts})")

def main():
    bulk = Structure.from_file(str(CIF))
    print(f"Bulk: {bulk.composition.reduced_formula} nsites={len(bulk)}  a,b,c={bulk.lattice.abc} β={bulk.lattice.beta:.2f}")
    
    # 1. Bulk vc-relax
    write_qe_input(bulk, ROOT/"bulk/bulk_vcrelax.in", calc="vc-relax", kpts=(4,3,2))
    # Bulk SCF (use optimized cell after relax)
    write_qe_input(bulk, ROOT/"bulk/bulk_scf.in", calc="scf", kpts=(4,3,2))
    # Bulk NSCF for DOS
    write_qe_input(bulk, ROOT/"bulk/bulk_nscf.in", calc="nscf", kpts=(6,4,3),
                   extra_system={"nosym":".true.", "nbnd":180})
    
    # 2. Build (010) slab  -- "b" direction
    for miller, tag, kpts in [((0,0,1),"slab_001",(3,2,1)), ((0,1,0),"slab_010",(3,2,1))]:
        sg = SlabGenerator(bulk, miller_index=miller, min_slab_size=10.0,
                           min_vacuum_size=15.0, center_slab=True, lll_reduce=False, primitive=True)
        slabs = sg.get_slabs(symmetrize=False)
        if not slabs:
            print(f"No slab found for {miller}"); continue
        slab = slabs[0]
        print(f"{tag}: nsites={len(slab)}  c={slab.lattice.c:.2f}")
        slab.to(filename=str(ROOT/f"{tag}/{tag}.cif"))
        
        # Fix bottom 2 layers (by z coordinate)
        zs = sorted(set(round(s.coords[2],2) for s in slab))
        fix_z = zs[:max(1,len(zs)//3)]  # bottom third
        fix_idx = [i for i,s in enumerate(slab) if round(s.coords[2],2) in fix_z]
        print(f"  Fixing {len(fix_idx)}/{len(slab)} bottom atoms")
        
        write_qe_input(slab, ROOT/f"{tag}/slab_relax.in", calc="relax",
                       kpts=kpts, fix_atoms_idx=set(fix_idx),
                       extra_system={"nosym":".true.", "noinv":".true."})
        write_qe_input(slab, ROOT/f"{tag}/slab_scf.in", calc="scf", kpts=kpts,
                       extra_system={"nosym":".true.", "noinv":".true."})
        
        # Pt-doped: replace topmost Ti
        ti_idx = [i for i,s in enumerate(slab) if s.specie.symbol=="Ti"]
        ti_idx.sort(key=lambda i: -slab[i].coords[2])
        top_ti = ti_idx[0]
        slab_pt = slab.copy()
        slab_pt.replace(top_ti, "Pt")
        print(f"  Pt@Ti#{top_ti} z={slab[top_ti].coords[2]:.2f}")
        slab_pt.to(filename=str(ROOT/f"{tag}_Pt/{tag}_Pt.cif"))
        write_qe_input(slab_pt, ROOT/f"{tag}_Pt/slab_Pt_relax.in", calc="relax",
                       kpts=kpts, fix_atoms_idx=set(fix_idx),
                       extra_system={"nosym":".true.", "noinv":".true."})
        write_qe_input(slab_pt, ROOT/f"{tag}_Pt/slab_Pt_scf.in", calc="scf", kpts=kpts,
                       extra_system={"nosym":".true.", "noinv":".true."})
    
    print("DONE")

if __name__ == "__main__":
    main()
