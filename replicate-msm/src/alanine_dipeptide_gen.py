"""
Phase 3: Alanine Dipeptide MD Trajectory Generation

Generates the trajectory ensemble for MSM analysis.
Designed to run on Polaris (A100/CUDA) or Aurora (Intel PVC/OpenCL).

Paper setup (Appendix A, Nüske et al. 2017):
- AMBER ff99SB-ILDN force field
- TIP3P water, cubic box (2.3222 nm)^3, 651 water molecules
- Langevin thermostat, 300 K
- PME electrostatics (cutoff 0.9 nm, grid 0.1 nm)
- Integration timestep: 2 fs
- H-bond constraints (SHAKE/LINCS)

Trajectory ensemble:
- 11,388 ultra-short simulations × 20 ps each (save every 50 fs)
- 8 starting structures with probabilities [0.05, 0.05, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1]
- Starting structures sample different regions of φ/ψ space

Checkpoint-restart:
- Saves progress every CHECKPOINT_INTERVAL simulations
- On SIGTERM (preemption), saves immediately and exits cleanly
- On restart, skips completed simulations automatically
"""

import numpy as np
import os
import sys
import signal
import json
import pickle
from pathlib import Path
from datetime import datetime

try:
    import openmm as mm
    from openmm import app, unit
    HAS_OPENMM = True
except ImportError:
    HAS_OPENMM = False
    print("WARNING: OpenMM not available. Install with: conda install -c conda-forge openmm")

# --- Checkpoint config ---
CHECKPOINT_INTERVAL = 200  # save every 200 simulations (~2-3 min of work)
SHUTDOWN_REQUESTED = False


def handle_sigterm(signum, frame):
    """Handle preemption signal — set flag for graceful shutdown."""
    global SHUTDOWN_REQUESTED
    SHUTDOWN_REQUESTED = True
    print(f"\n  *** SIGTERM received at {datetime.now().isoformat()} — will checkpoint and exit after current sim ***", flush=True)


def get_platform():
    """Select best available OpenMM platform."""
    default_plat = os.environ.get('OPENMM_DEFAULT_PLATFORM', '')
    for name in ([default_plat] if default_plat else []) + ['CUDA', 'OpenCL', 'CPU']:
        try:
            platform = mm.Platform.getPlatformByName(name)
            print(f"  Using {name} platform", flush=True)
            return platform
        except:
            continue
    platform = mm.Platform.getPlatformByName('CPU')
    print("  Fallback to CPU platform", flush=True)
    return platform


def build_alanine_dipeptide_system():
    """
    Build alanine dipeptide in explicit TIP3P water.
    Returns topology, system, and positions.
    """
    from openmm.app import ForceField, Modeller, PME, PDBFile

    # Try openmmtools first (cleanest)
    try:
        from openmmtools.testsystems import AlanineDipeptideExplicit
        testsystem = AlanineDipeptideExplicit(constraints=app.HBonds,
                                               nonbondedMethod=PME,
                                               nonbondedCutoff=0.9*unit.nanometers)
        return testsystem.topology, testsystem.system, testsystem.positions
    except ImportError:
        pass

    # Fallback: PDBFixer
    pdb_path = '/tmp/ala_dipeptide_correct.pdb'
    try:
        from pdbfixer import PDBFixer
        import urllib.request
        url = "https://raw.githubusercontent.com/openmm/openmm/master/wrappers/python/tests/systems/alanine-dipeptide-implicit.pdb"
        urllib.request.urlretrieve(url, pdb_path)

        fixer = PDBFixer(filename=pdb_path)
        fixer.findMissingResidues()
        fixer.findMissingAtoms()
        fixer.addMissingAtoms()
        fixer.addMissingHydrogens(7.0)

        forcefield = ForceField('amber99sbildn.xml', 'tip3p.xml')
        modeller = Modeller(fixer.topology, fixer.positions)
        modeller.addSolvent(forcefield, model='tip3p',
                           boxSize=mm.Vec3(2.3222, 2.3222, 2.3222)*unit.nanometers)
        system = forcefield.createSystem(modeller.topology, nonbondedMethod=PME,
                                        nonbondedCutoff=0.9*unit.nanometers,
                                        constraints=app.HBonds)
        return modeller.topology, system, modeller.positions
    except ImportError:
        pass

    # Final fallback: hand-built PDB
    pdb_text = """\
CRYST1   30.000   30.000   30.000  90.00  90.00  90.00 P 1           1
ATOM      1  CH3 ACE     1       2.000   1.000   0.000  1.00  0.00           C
ATOM      2 HH31 ACE     1       2.000   2.090   0.000  1.00  0.00           H
ATOM      3 HH32 ACE     1       1.486   0.637  -0.890  1.00  0.00           H
ATOM      4 HH33 ACE     1       1.486   0.637   0.890  1.00  0.00           H
ATOM      5  C   ACE     1       3.430   0.520   0.000  1.00  0.00           C
ATOM      6  O   ACE     1       4.400   1.240   0.000  1.00  0.00           O
ATOM      7  N   ALA     2       3.622  -0.795   0.000  1.00  0.00           N
ATOM      8  H   ALA     2       2.798  -1.373   0.000  1.00  0.00           H
ATOM      9  CA  ALA     2       4.934  -1.415   0.000  1.00  0.00           C
ATOM     10  HA  ALA     2       5.464  -1.056   0.888  1.00  0.00           H
ATOM     11  CB  ALA     2       5.731  -1.056  -1.244  1.00  0.00           C
ATOM     12  HB1 ALA     2       5.179  -1.412  -2.115  1.00  0.00           H
ATOM     13  HB2 ALA     2       6.696  -1.554  -1.204  1.00  0.00           H
ATOM     14  HB3 ALA     2       5.859   0.027  -1.308  1.00  0.00           H
ATOM     15  C   ALA     2       4.780  -2.926   0.000  1.00  0.00           C
ATOM     16  O   ALA     2       3.699  -3.454  -0.002  1.00  0.00           O
ATOM     17  N   NME     3       5.890  -3.612   0.001  1.00  0.00           N
ATOM     18  H   NME     3       6.782  -3.113   0.002  1.00  0.00           H
ATOM     19  CH3 NME     3       5.876  -5.056   0.001  1.00  0.00           C
ATOM     20 HH31 NME     3       6.900  -5.418   0.001  1.00  0.00           H
ATOM     21 HH32 NME     3       5.360  -5.434  -0.880  1.00  0.00           H
ATOM     22 HH33 NME     3       5.360  -5.434   0.882  1.00  0.00           H
TER
END
"""
    with open(pdb_path, 'w') as f:
        f.write(pdb_text)

    pdb = PDBFile(pdb_path)
    forcefield = ForceField('amber99sbildn.xml', 'tip3p.xml')
    modeller = Modeller(pdb.topology, pdb.positions)
    modeller.addSolvent(forcefield, model='tip3p',
                       boxSize=mm.Vec3(2.3222, 2.3222, 2.3222)*unit.nanometers)
    system = forcefield.createSystem(modeller.topology, nonbondedMethod=PME,
                                    nonbondedCutoff=0.9*unit.nanometers,
                                    constraints=app.HBonds)
    return modeller.topology, system, modeller.positions


def generate_starting_structures(topology, system, positions, n_structures=8):
    """
    Generate 8 diverse starting structures by running short MD
    and selecting frames from different φ/ψ regions.
    """
    import mdtraj as md

    integrator = mm.LangevinMiddleIntegrator(300 * unit.kelvin, 1.0 / unit.picoseconds, 2.0 * unit.femtoseconds)
    platform = get_platform()

    simulation = app.Simulation(topology, system, integrator, platform)
    simulation.context.setPositions(positions)
    simulation.minimizeEnergy()

    print("  Running 2 ns equilibration to generate diverse starting structures...", flush=True)
    simulation.context.setVelocitiesToTemperature(300 * unit.kelvin)

    all_positions = []
    all_phi_psi = []

    top_md = md.Topology.from_openmm(topology)

    for i in range(200):
        simulation.step(5000)  # 10 ps
        state = simulation.context.getState(getPositions=True)
        pos = state.getPositions(asNumpy=True).value_in_unit(unit.nanometers)
        all_positions.append(pos.copy())

        frame = md.Trajectory(pos.reshape(1, -1, 3), top_md)
        phi_idx = md.compute_phi(frame)[0]
        psi_idx = md.compute_psi(frame)[0]
        phi_val = md.compute_dihedrals(frame, phi_idx)[0, 0] if len(phi_idx) > 0 else 0
        psi_val = md.compute_dihedrals(frame, psi_idx)[0, 0] if len(psi_idx) > 0 else 0
        all_phi_psi.append([phi_val, psi_val])

    all_phi_psi = np.array(all_phi_psi)

    from sklearn.cluster import KMeans
    kmeans = KMeans(n_clusters=n_structures, random_state=42, n_init=10)
    labels = kmeans.fit_predict(all_phi_psi)

    starting_structures = []
    starting_phi_psi_out = []
    for k in range(n_structures):
        cluster_mask = (labels == k)
        distances = np.linalg.norm(all_phi_psi[cluster_mask] - kmeans.cluster_centers_[k], axis=1)
        best_idx = np.where(cluster_mask)[0][np.argmin(distances)]
        starting_structures.append(all_positions[best_idx])
        starting_phi_psi_out.append(all_phi_psi[best_idx])

    return starting_structures, np.array(starting_phi_psi_out)


# ============================================================
# Checkpoint-restart trajectory generation
# ============================================================

def load_checkpoint(ckpt_path):
    """Load checkpoint if it exists. Returns (completed_count, dihedrals_list) or (0, [])."""
    if not ckpt_path.exists():
        return 0, []
    try:
        data = np.load(ckpt_path, allow_pickle=True)
        completed = int(data['completed'])
        dihedrals = list(data['dihedrals'])  # list of arrays
        print(f"  *** Resuming from checkpoint: {completed} simulations already done ***", flush=True)
        return completed, dihedrals
    except Exception as e:
        print(f"  WARNING: Corrupt checkpoint, starting fresh: {e}", flush=True)
        return 0, []


def save_checkpoint(ckpt_path, completed, dihedrals_list, n_per_struct, start_probs):
    """Save current progress to checkpoint file."""
    # Stack whatever we have — may be ragged if interrupted mid-structure
    if len(dihedrals_list) > 0:
        dihedrals_arr = np.array(dihedrals_list)
    else:
        dihedrals_arr = np.array([])
    np.savez(
        ckpt_path,
        completed=completed,
        dihedrals=dihedrals_arr,
        n_per_struct=n_per_struct,
        start_probs=start_probs,
    )
    print(f"  [checkpoint] Saved {completed} simulations to {ckpt_path}", flush=True)


def run_short_simulations(topology, system, starting_structures, n_total=11388,
                          traj_length_ps=20, save_interval_fs=50, output_dir=None):
    """
    Run ensemble of short non-equilibrium simulations with checkpoint-restart.

    Saves checkpoint every CHECKPOINT_INTERVAL sims and on SIGTERM.
    On restart, loads checkpoint and skips completed work.
    """
    global SHUTDOWN_REQUESTED

    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "data" / "alanine_short"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ckpt_path = output_dir / "checkpoint.npz"
    final_path = output_dir / "dihedrals_short.npz"

    start_probs = np.array([0.05, 0.05, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1])
    n_per_struct = np.round(start_probs * n_total).astype(int)
    n_per_struct[-1] = n_total - n_per_struct[:-1].sum()

    steps_per_save = int(save_interval_fs / 2)
    n_saves = int(traj_length_ps * 1000 / save_interval_fs)

    print(f"  Total simulations: {n_total}", flush=True)
    print(f"  Steps per save: {steps_per_save}, saves per traj: {n_saves}", flush=True)
    print(f"  Simulations per starting structure: {n_per_struct}", flush=True)
    print(f"  Checkpoint interval: every {CHECKPOINT_INTERVAL} sims", flush=True)

    # Load checkpoint
    completed, all_dihedrals = load_checkpoint(ckpt_path)

    if completed >= n_total:
        print(f"  All {n_total} simulations already complete!", flush=True)
        return np.array(all_dihedrals)

    platform = get_platform()

    import mdtraj as md
    top_md = md.Topology.from_openmm(topology)

    dummy_pos = np.zeros((1, top_md.n_atoms, 3))
    dummy_traj = md.Trajectory(dummy_pos, top_md)
    phi_indices = md.compute_phi(dummy_traj)[0]
    psi_indices = md.compute_psi(dummy_traj)[0]

    # Figure out where to resume: which struct_idx and sim_idx
    sim_count = 0  # global counter across all structures
    last_ckpt_count = completed

    for struct_idx in range(len(starting_structures)):
        n_sims = n_per_struct[struct_idx]
        if n_sims == 0:
            continue

        # Check if this entire structure block was already done
        if sim_count + n_sims <= completed:
            sim_count += n_sims
            continue

        print(f"  Starting structure {struct_idx+1}/8: {n_sims} simulations...", flush=True)

        for sim_idx in range(n_sims):
            # Skip already-completed sims within this block
            if sim_count < completed:
                sim_count += 1
                continue

            # Check for shutdown request
            if SHUTDOWN_REQUESTED:
                print(f"  Shutting down gracefully at sim {sim_count}/{n_total}", flush=True)
                save_checkpoint(ckpt_path, sim_count, all_dihedrals, n_per_struct, start_probs)
                print(f"  Exiting. Resubmit to resume from sim {sim_count}.", flush=True)
                sys.exit(0)

            integrator = mm.LangevinMiddleIntegrator(
                300 * unit.kelvin,
                1.0 / unit.picoseconds,
                2.0 * unit.femtoseconds
            )

            simulation = app.Simulation(topology, system, integrator, platform)
            simulation.context.setPositions(starting_structures[struct_idx] * unit.nanometers)
            simulation.context.setVelocitiesToTemperature(300 * unit.kelvin)

            traj_dihedrals = np.zeros((n_saves + 1, 2))

            # Initial frame
            state = simulation.context.getState(getPositions=True)
            pos = state.getPositions(asNumpy=True).value_in_unit(unit.nanometers)
            frame = md.Trajectory(pos.reshape(1, -1, 3), top_md)
            traj_dihedrals[0, 0] = md.compute_dihedrals(frame, phi_indices)[0, 0]
            traj_dihedrals[0, 1] = md.compute_dihedrals(frame, psi_indices)[0, 0]

            for save_idx in range(n_saves):
                simulation.step(steps_per_save)
                state = simulation.context.getState(getPositions=True)
                pos = state.getPositions(asNumpy=True).value_in_unit(unit.nanometers)
                frame = md.Trajectory(pos.reshape(1, -1, 3), top_md)
                traj_dihedrals[save_idx + 1, 0] = md.compute_dihedrals(frame, phi_indices)[0, 0]
                traj_dihedrals[save_idx + 1, 1] = md.compute_dihedrals(frame, psi_indices)[0, 0]

            all_dihedrals.append(traj_dihedrals)
            sim_count += 1

            if sim_count % 500 == 0:
                print(f"    {sim_count}/{n_total} complete", flush=True)

            # Periodic checkpoint
            if (sim_count - last_ckpt_count) >= CHECKPOINT_INTERVAL:
                save_checkpoint(ckpt_path, sim_count, all_dihedrals, n_per_struct, start_probs)
                last_ckpt_count = sim_count

    # Final save
    all_dihedrals = np.array(all_dihedrals)
    np.savez(final_path, dihedrals=all_dihedrals, start_probs=start_probs, n_per_struct=n_per_struct)
    print(f"  Saved final results: {final_path} — shape {all_dihedrals.shape}", flush=True)

    # Clean up checkpoint now that we're done
    if ckpt_path.exists():
        ckpt_path.unlink()
        print(f"  Removed checkpoint (run complete)", flush=True)

    return all_dihedrals


def save_starting_structures(path, structures, phi_psi):
    """Persist starting structures so restarts don't regenerate them."""
    np.savez(path, structures=np.array(structures), phi_psi=phi_psi)
    print(f"  Saved starting structures to {path}", flush=True)


def load_starting_structures(path):
    """Load previously generated starting structures."""
    data = np.load(path)
    structures = list(data['structures'])
    phi_psi = data['phi_psi']
    print(f"  Loaded {len(structures)} starting structures from {path}", flush=True)
    return structures, phi_psi


if __name__ == "__main__":
    if not HAS_OPENMM:
        print("OpenMM required. Install with: conda install -c conda-forge openmm")
        sys.exit(1)

    # Register signal handler for graceful preemption
    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGUSR1, handle_sigterm)  # some schedulers use SIGUSR1

    data_dir = Path(__file__).parent.parent / "data" / "alanine_short"
    data_dir.mkdir(parents=True, exist_ok=True)
    start_struct_path = data_dir / "starting_structures.npz"

    print("Phase 3: Alanine Dipeptide MD Generation", flush=True)
    print("=" * 50, flush=True)
    print(f"  Checkpoint-restart: ON (interval={CHECKPOINT_INTERVAL})", flush=True)
    print(f"  PID: {os.getpid()}", flush=True)
    print(f"  Time: {datetime.now().isoformat()}", flush=True)

    # Step 1: Build system (always needed for OpenMM context)
    print("\nStep 1: Building system...", flush=True)
    topology, system, positions = build_alanine_dipeptide_system()
    print(f"  Atoms: {topology.getNumAtoms()}", flush=True)

    # Step 2: Starting structures — load from cache if available (idempotent)
    if start_struct_path.exists():
        print("\nStep 2: Loading cached starting structures...", flush=True)
        starting_structures, starting_phi_psi = load_starting_structures(start_struct_path)
    else:
        print("\nStep 2: Generating starting structures...", flush=True)
        starting_structures, starting_phi_psi = generate_starting_structures(topology, system, positions)
        save_starting_structures(start_struct_path, starting_structures, starting_phi_psi)

    print(f"  Starting φ/ψ values:", flush=True)
    for i, (phi, psi) in enumerate(starting_phi_psi):
        print(f"    Structure {i+1}: φ={np.degrees(phi):.1f}°, ψ={np.degrees(psi):.1f}°", flush=True)

    # Step 3: Run simulations with checkpoint-restart
    print("\nStep 3: Running short simulations (11,388 × 20 ps)...", flush=True)
    dihedrals = run_short_simulations(topology, system, starting_structures)

    print(f"\nDone at {datetime.now().isoformat()}!", flush=True)
