#!/usr/bin/env python3
"""
Replication of OSTI 1484740: Electronic and optical properties of 2D GaN
Setup and run DFT calculations using Quantum ESPRESSO

Uses PBE norm-conserving pseudopotentials (ONCVPSP SG15).
Paper uses LDA, but LDA Ga NC pseudo unavailable. PBE provides
comparable results for structural and electronic properties.
"""

import os
import subprocess
import sys

BASEDIR = os.path.expanduser("~/replication")
PSEUDO = os.path.join(BASEDIR, "pseudopotentials")
INPUTS = os.path.join(BASEDIR, "inputs")
OUTPUTS = os.path.join(BASEDIR, "outputs")

# Pseudopotential names
PP_GA = "Ga_ONCV_PBE_sr.upf"
PP_N = "N_ONCV_PBE_sr.upf"
PP_H = "H_ONCV_PBE_sr.upf"

# Paper: a_bulk = 3.19 Å (expt), LDA underestimates by 0.77% -> 3.165 Å
# For PBE, bulk GaN a ≈ 3.22 Å. We use 3.20 Å as starting point.
A_MONO = 3.20  # in-plane lattice constant (Angstrom)
C_VAC = 20.0   # vacuum thickness (Angstrom)
C_VAC_BI = 25.0

def write_monolayer_relax():
    """Monolayer GaN (H-passivated, buckled) vc-relax"""
    content = f"""&CONTROL
    calculation = 'vc-relax',
    prefix = 'gan_mono',
    pseudo_dir = '{PSEUDO}/',
    outdir = '{OUTPUTS}/mono_relax/',
    tprnfor = .true.,
    tstress = .true.,
    forc_conv_thr = 1.0d-4,
    etot_conv_thr = 1.0d-6,
/
&SYSTEM
    ibrav = 0,
    nat = 4,
    ntyp = 3,
    ecutwfc = 80.0,
    ecutrho = 320.0,
    occupations = 'fixed',
    input_dft = 'PBE',
    assume_isolated = '2D',
/
&ELECTRONS
    conv_thr = 1.0d-10,
    mixing_beta = 0.3,
    electron_maxstep = 200,
/
&IONS
    ion_dynamics = 'bfgs',
/
&CELL
    cell_dynamics = 'bfgs',
    cell_dofree = '2Dxy',
    press_conv_thr = 0.1,
/
ATOMIC_SPECIES
    Ga  69.723  {PP_GA}
    N   14.007  {PP_N}
    H    1.008  {PP_H}
CELL_PARAMETERS (angstrom)
    {A_MONO:.6f}    0.000000    0.000000
   {-A_MONO/2:.6f}    {A_MONO*0.8660254:.6f}    0.000000
    0.000000    0.000000   {C_VAC:.6f}
ATOMIC_POSITIONS (crystal)
    Ga  0.333333  0.666667  0.500000
    N   0.666667  0.333333  0.516500
    H   0.333333  0.666667  0.422500
    H   0.666667  0.333333  0.594000
K_POINTS (automatic)
    8  8  1  0  0  0
"""
    return content

def write_monolayer_scf(a_lat, positions):
    """Monolayer SCF with relaxed geometry"""
    content = f"""&CONTROL
    calculation = 'scf',
    prefix = 'gan_mono',
    pseudo_dir = '{PSEUDO}/',
    outdir = '{OUTPUTS}/mono_scf/',
    tprnfor = .true.,
    tstress = .true.,
/
&SYSTEM
    ibrav = 0,
    nat = 4,
    ntyp = 3,
    ecutwfc = 80.0,
    ecutrho = 320.0,
    occupations = 'fixed',
    input_dft = 'PBE',
    assume_isolated = '2D',
/
&ELECTRONS
    conv_thr = 1.0d-10,
    mixing_beta = 0.3,
    electron_maxstep = 200,
/
ATOMIC_SPECIES
    Ga  69.723  {PP_GA}
    N   14.007  {PP_N}
    H    1.008  {PP_H}
CELL_PARAMETERS (angstrom)
    {a_lat:.6f}    0.000000    0.000000
   {-a_lat/2:.6f}    {a_lat*0.8660254:.6f}    0.000000
    0.000000    0.000000   {C_VAC:.6f}
{positions}
K_POINTS (automatic)
    8  8  1  0  0  0
"""
    return content

def write_monolayer_bands(a_lat, positions):
    """Monolayer band structure along Γ-M-K-Γ"""
    content = f"""&CONTROL
    calculation = 'bands',
    prefix = 'gan_mono',
    pseudo_dir = '{PSEUDO}/',
    outdir = '{OUTPUTS}/mono_scf/',
/
&SYSTEM
    ibrav = 0,
    nat = 4,
    ntyp = 3,
    ecutwfc = 80.0,
    ecutrho = 320.0,
    occupations = 'fixed',
    input_dft = 'PBE',
    assume_isolated = '2D',
    nbnd = 30,
/
&ELECTRONS
    conv_thr = 1.0d-10,
    mixing_beta = 0.3,
/
ATOMIC_SPECIES
    Ga  69.723  {PP_GA}
    N   14.007  {PP_N}
    H    1.008  {PP_H}
CELL_PARAMETERS (angstrom)
    {a_lat:.6f}    0.000000    0.000000
   {-a_lat/2:.6f}    {a_lat*0.8660254:.6f}    0.000000
    0.000000    0.000000   {C_VAC:.6f}
{positions}
K_POINTS {{crystal_b}}
4
    0.0000  0.0000  0.0000  40  ! Gamma
    0.5000  0.0000  0.0000  40  ! M
    0.3333  0.3333  0.0000  40  ! K
    0.0000  0.0000  0.0000   1  ! Gamma
"""
    return content

def write_bands_pp(prefix):
    content = f"""&BANDS
    prefix = '{prefix}',
    outdir = '{OUTPUTS}/{prefix.replace("gan_","")}_scf/',
    filband = '{OUTPUTS}/{prefix}_bands.dat',
/
"""
    return content

def write_bilayer_relax():
    """Bilayer GaN (H-passivated, buckled) vc-relax"""
    content = f"""&CONTROL
    calculation = 'vc-relax',
    prefix = 'gan_bi',
    pseudo_dir = '{PSEUDO}/',
    outdir = '{OUTPUTS}/bi_relax/',
    tprnfor = .true.,
    tstress = .true.,
    forc_conv_thr = 1.0d-4,
    etot_conv_thr = 1.0d-6,
/
&SYSTEM
    ibrav = 0,
    nat = 6,
    ntyp = 3,
    ecutwfc = 80.0,
    ecutrho = 320.0,
    occupations = 'fixed',
    input_dft = 'PBE',
    assume_isolated = '2D',
/
&ELECTRONS
    conv_thr = 1.0d-10,
    mixing_beta = 0.3,
    electron_maxstep = 200,
/
&IONS
    ion_dynamics = 'bfgs',
/
&CELL
    cell_dynamics = 'bfgs',
    cell_dofree = '2Dxy',
    press_conv_thr = 0.1,
/
ATOMIC_SPECIES
    Ga  69.723  {PP_GA}
    N   14.007  {PP_N}
    H    1.008  {PP_H}
CELL_PARAMETERS (angstrom)
    {A_MONO:.6f}    0.000000    0.000000
   {-A_MONO/2:.6f}    {A_MONO*0.8660254:.6f}    0.000000
    0.000000    0.000000   {C_VAC_BI:.6f}
ATOMIC_POSITIONS (crystal)
    H   0.333333  0.666667  0.356000
    Ga  0.333333  0.666667  0.420000
    N   0.666667  0.333333  0.433200
    N   0.333333  0.666667  0.521200
    Ga  0.666667  0.333333  0.534800
    H   0.666667  0.333333  0.596800
K_POINTS (automatic)
    8  8  1  0  0  0
"""
    return content

def write_pdos(prefix, outdir):
    content = f"""&PROJWFC
    prefix = '{prefix}',
    outdir = '{OUTPUTS}/{outdir}/',
    filpdos = '{OUTPUTS}/{prefix}_pdos',
    Emin = -15.0,
    Emax = 15.0,
    DeltaE = 0.05,
/
"""
    return content

if __name__ == "__main__":
    os.makedirs(INPUTS, exist_ok=True)
    for d in ['mono_relax', 'mono_scf', 'bi_relax', 'bi_scf']:
        os.makedirs(os.path.join(OUTPUTS, d), exist_ok=True)

    # Write relaxation inputs
    with open(os.path.join(INPUTS, "mono_relax.in"), 'w') as f:
        f.write(write_monolayer_relax())
    with open(os.path.join(INPUTS, "bi_relax.in"), 'w') as f:
        f.write(write_bilayer_relax())
    with open(os.path.join(INPUTS, "mono_bands_pp.in"), 'w') as f:
        f.write(write_bands_pp("gan_mono"))
    with open(os.path.join(INPUTS, "bi_bands_pp.in"), 'w') as f:
        f.write(write_bands_pp("gan_bi"))
    with open(os.path.join(INPUTS, "mono_pdos.in"), 'w') as f:
        f.write(write_pdos("gan_mono", "mono_scf"))

    print("Input files written successfully!")
    print(f"Inputs: {INPUTS}")
    print(f"Outputs: {OUTPUTS}")
