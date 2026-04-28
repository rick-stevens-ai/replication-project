#!/usr/bin/env python3
"""Extract final geometry from QE relax output and write nscf+scf inputs."""
import sys, re
from pathlib import Path

def parse_final(output):
    """Return (cell_params[3x3], positions [(sym, x,y,z)]) from the LAST BFGS step."""
    lines = output.split("\n")
    # find all occurrences of ATOMIC_POSITIONS (crystal) and CELL_PARAMETERS  
    pos_blocks = []
    cell_blocks = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        if "ATOMIC_POSITIONS" in ln:
            unit = ln.split("(")[-1].replace(")","").strip() if "(" in ln else "crystal"
            pos = []
            j = i+1
            while j < len(lines):
                l = lines[j].strip()
                if not l: break
                parts = l.split()
                if len(parts) < 4: break
                sym = parts[0]
                try:
                    x,y,z = float(parts[1]), float(parts[2]), float(parts[3])
                except:
                    break
                pos.append((sym, x, y, z))
                j += 1
            pos_blocks.append((unit, pos))
            i = j
        elif "CELL_PARAMETERS" in ln:
            cells = []
            j = i+1
            for k in range(3):
                parts = lines[j+k].split()
                cells.append([float(p) for p in parts[:3]])
            cell_blocks.append(cells)
            i = j+3
        else:
            i += 1
    return cell_blocks, pos_blocks

def write_scf_nscf(inp_file, cell, positions, prefix="lto", kpts_scf=(3,2,1), kpts_nscf=(4,3,1)):
    """Write scf and nscf inputs based on extracted geometry."""
    orig = Path(inp_file).read_text()
    # Get ATOMIC_SPECIES block, control params from original
    # Simplest: rewrite full input
    PSEUDO = {"La":"La.upf","Ti":"Ti.upf","O":"O.upf","Pt":"Pt.upf"}
    masses = {"La":138.9055,"Ti":47.867,"O":15.999,"Pt":195.084}
    species = sorted(set([p[0] for p in positions]))
    nat, ntyp = len(positions), len(species)
    
    for tag, calc, kpts, extra in [
        ("scf","scf",kpts_scf,{}),
        ("nscf","nscf",kpts_nscf,{"nbnd":nat*6, "occupations":"'tetrahedra_opt'"}),
    ]:
        out_path = Path(inp_file).parent / f"{prefix}_{tag}_final.in"
        L = [
            "&CONTROL",
            f"  calculation = '{calc}'",
            "  restart_mode = 'from_scratch'",
            f"  prefix = '{prefix}'",
            "  outdir = './tmp'",
            "  pseudo_dir = '/home/stevens/projects/replicate-1981773/pseudo'",
            "  verbosity = 'low'",
            "/",
            "&SYSTEM",
            "  ibrav = 0",
            f"  nat = {nat}", f"  ntyp = {ntyp}",
            "  ecutwfc = 60.0  ecutrho = 480.0",
            "  nosym = .true.  noinv = .true.",
        ]
        if calc == "scf":
            L += ["  occupations = 'smearing'", "  smearing = 'gaussian'", "  degauss = 0.01"]
        else:
            for k,v in extra.items():
                L.append(f"  {k} = {v}")
            L.append("  degauss = 0.01")
        L.append("/")
        L += ["&ELECTRONS", "  conv_thr = 1.0d-7", "  mixing_beta = 0.3", "  diagonalization = 'david'", "/"]
        L.append("ATOMIC_SPECIES")
        for sp in species:
            L.append(f"  {sp}  {masses[sp]}  {PSEUDO[sp]}")
        L.append("CELL_PARAMETERS angstrom")
        for r in cell:
            L.append(f"  {r[0]:.10f}  {r[1]:.10f}  {r[2]:.10f}")
        L.append("ATOMIC_POSITIONS crystal")
        for sym,x,y,z in positions:
            L.append(f"  {sym}  {x:.10f}  {y:.10f}  {z:.10f}")
        L.append("K_POINTS automatic")
        L.append(f"  {kpts[0]} {kpts[1]} {kpts[2]}  0 0 0")
        out_path.write_text("\n".join(L)+"\n")
        print(f"wrote {out_path}")

if __name__ == "__main__":
    out_file = sys.argv[1]  # e.g. slab_001/slab_relax.out
    in_file  = sys.argv[2]  # e.g. slab_001/slab_relax.in  (for reference)
    text = Path(out_file).read_text()
    cells, positions = parse_final(text)
    if cells:
        final_cell = cells[-1]
    else:
        # extract from input
        import re
        m = re.search(r"CELL_PARAMETERS[^\n]*\n((?:[^\n]+\n){3})", Path(in_file).read_text())
        final_cell = [[float(x) for x in line.split()[:3]] for line in m.group(1).strip().split("\n")]
    final_pos = positions[-1][1] if positions else []
    # If unit is alat or bohr, don't handle; assume crystal
    print(f"Extracted {len(final_pos)} atoms, cell from last block")
    write_scf_nscf(in_file, final_cell, final_pos)
