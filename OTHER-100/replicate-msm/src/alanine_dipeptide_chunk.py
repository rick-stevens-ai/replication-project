"""
Phase 3: Alanine Dipeptide MD — Chunked Parallel Generation

Each job runs a slice of the 11,388 simulations independently.
Usage: python alanine_dipeptide_chunk.py <chunk_id> <n_chunks>

Example: 8 parallel jobs → chunk 0..7, each runs ~1424 sims
Results merged by alanine_merge_chunks.py after all complete.

Checkpoint-restart: each chunk saves its own checkpoint.
"""

import numpy as np
import os
import sys
import signal
import json
from pathlib import Path
from datetime import datetime

try:
    import openmm as mm
    from openmm import app, unit
except ImportError:
    print("OpenMM required.")
    sys.exit(1)

CHECKPOINT_INTERVAL = 200
SHUTDOWN_REQUESTED = False
N_TOTAL = 11388
START_PROBS = np.array([0.05, 0.05, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1])


def handle_sigterm(signum, frame):
    global SHUTDOWN_REQUESTED
    SHUTDOWN_REQUESTED = True
    print(f"\n  *** SIGTERM — checkpointing after current sim ***", flush=True)


def get_platform():
    default_plat = os.environ.get('OPENMM_DEFAULT_PLATFORM', '')
    for name in ([default_plat] if default_plat else []) + ['CUDA', 'OpenCL', 'CPU']:
        try:
            p = mm.Platform.getPlatformByName(name)
            print(f"  Using {name} platform", flush=True)
            return p
        except:
            continue
    return mm.Platform.getPlatformByName('CPU')


def build_system():
    """Build alanine dipeptide in explicit TIP3P water."""
    from openmm.app import ForceField, Modeller, PME, PDBFile

    try:
        from openmmtools.testsystems import AlanineDipeptideExplicit
        t = AlanineDipeptideExplicit(constraints=app.HBonds, nonbondedMethod=PME,
                                     nonbondedCutoff=0.9*unit.nanometers)
        return t.topology, t.system, t.positions
    except ImportError:
        pass

    pdb_path = '/tmp/ala_dipeptide_correct.pdb'
    try:
        from pdbfixer import PDBFixer
        import urllib.request
        url = "https://raw.githubusercontent.com/openmm/openmm/master/wrappers/python/tests/systems/alanine-dipeptide-implicit.pdb"
        urllib.request.urlretrieve(url, pdb_path)
        fixer = PDBFixer(filename=pdb_path)
        fixer.findMissingResidues(); fixer.findMissingAtoms()
        fixer.addMissingAtoms(); fixer.addMissingHydrogens(7.0)
        ff = ForceField('amber99sbildn.xml', 'tip3p.xml')
        mod = Modeller(fixer.topology, fixer.positions)
        mod.addSolvent(ff, model='tip3p', boxSize=mm.Vec3(2.3222,2.3222,2.3222)*unit.nanometers)
        sys = ff.createSystem(mod.topology, nonbondedMethod=PME,
                              nonbondedCutoff=0.9*unit.nanometers, constraints=app.HBonds)
        return mod.topology, sys, mod.positions
    except ImportError:
        pass

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
    ff = ForceField('amber99sbildn.xml', 'tip3p.xml')
    mod = Modeller(pdb.topology, pdb.positions)
    mod.addSolvent(ff, model='tip3p', boxSize=mm.Vec3(2.3222,2.3222,2.3222)*unit.nanometers)
    sys = ff.createSystem(mod.topology, nonbondedMethod=PME,
                          nonbondedCutoff=0.9*unit.nanometers, constraints=app.HBonds)
    return mod.topology, sys, mod.positions


def compute_sim_assignments():
    """Return flat list: for each sim index 0..N_TOTAL-1, which starting structure it uses."""
    n_per_struct = np.round(START_PROBS * N_TOTAL).astype(int)
    n_per_struct[-1] = N_TOTAL - n_per_struct[:-1].sum()
    assignments = []
    for struct_idx, count in enumerate(n_per_struct):
        assignments.extend([struct_idx] * count)
    return assignments, n_per_struct


def run_chunk(chunk_id, n_chunks, topology, system, starting_structures, output_dir):
    """Run simulations for this chunk only."""
    global SHUTDOWN_REQUESTED
    import mdtraj as md

    assignments, n_per_struct = compute_sim_assignments()
    total = len(assignments)

    # Determine this chunk's slice
    chunk_size = total // n_chunks
    start_idx = chunk_id * chunk_size
    end_idx = start_idx + chunk_size if chunk_id < n_chunks - 1 else total
    my_count = end_idx - start_idx

    print(f"  Chunk {chunk_id}/{n_chunks}: sims [{start_idx}, {end_idx}) = {my_count} sims", flush=True)

    ckpt_path = output_dir / f"checkpoint_chunk{chunk_id}.npz"
    final_path = output_dir / f"dihedrals_chunk{chunk_id}.npz"

    # Check if already done
    if final_path.exists():
        print(f"  Chunk {chunk_id} already complete: {final_path}", flush=True)
        return

    # Load checkpoint
    completed = 0
    all_dihedrals = []
    if ckpt_path.exists():
        try:
            data = np.load(ckpt_path, allow_pickle=True)
            completed = int(data['completed'])
            all_dihedrals = list(data['dihedrals'])
            print(f"  Resuming from checkpoint: {completed}/{my_count} done", flush=True)
        except:
            print(f"  Corrupt checkpoint, starting fresh", flush=True)
            completed = 0; all_dihedrals = []

    if completed >= my_count:
        print(f"  Already complete!", flush=True)
        return

    platform = get_platform()
    top_md = md.Topology.from_openmm(topology)
    dummy = md.Trajectory(np.zeros((1, top_md.n_atoms, 3)), top_md)
    phi_indices = md.compute_phi(dummy)[0]
    psi_indices = md.compute_psi(dummy)[0]

    steps_per_save = 25  # 50 fs / 2 fs
    n_saves = 400         # 20 ps / 50 fs

    last_ckpt = completed
    for i in range(my_count):
        if i < completed:
            continue

        if SHUTDOWN_REQUESTED:
            print(f"  Shutting down at {i}/{my_count}", flush=True)
            np.savez(ckpt_path, completed=i, dihedrals=np.array(all_dihedrals))
            print(f"  [checkpoint] saved {i} sims", flush=True)
            sys.exit(0)

        struct_idx = assignments[start_idx + i]

        integrator = mm.LangevinMiddleIntegrator(300*unit.kelvin, 1.0/unit.picoseconds, 2.0*unit.femtoseconds)
        sim = app.Simulation(topology, system, integrator, platform)
        sim.context.setPositions(starting_structures[struct_idx] * unit.nanometers)
        sim.context.setVelocitiesToTemperature(300 * unit.kelvin)

        traj = np.zeros((n_saves + 1, 2))
        state = sim.context.getState(getPositions=True)
        pos = state.getPositions(asNumpy=True).value_in_unit(unit.nanometers)
        frame = md.Trajectory(pos.reshape(1, -1, 3), top_md)
        traj[0, 0] = md.compute_dihedrals(frame, phi_indices)[0, 0]
        traj[0, 1] = md.compute_dihedrals(frame, psi_indices)[0, 0]

        for s in range(n_saves):
            sim.step(steps_per_save)
            state = sim.context.getState(getPositions=True)
            pos = state.getPositions(asNumpy=True).value_in_unit(unit.nanometers)
            frame = md.Trajectory(pos.reshape(1, -1, 3), top_md)
            traj[s+1, 0] = md.compute_dihedrals(frame, phi_indices)[0, 0]
            traj[s+1, 1] = md.compute_dihedrals(frame, psi_indices)[0, 0]

        all_dihedrals.append(traj)
        done = i + 1

        if done % 200 == 0:
            print(f"    chunk {chunk_id}: {done}/{my_count}", flush=True)

        if (done - last_ckpt) >= CHECKPOINT_INTERVAL:
            np.savez(ckpt_path, completed=done, dihedrals=np.array(all_dihedrals))
            print(f"  [checkpoint] {done}/{my_count}", flush=True)
            last_ckpt = done

    # Done — save final, remove checkpoint
    arr = np.array(all_dihedrals)
    np.savez(final_path, dihedrals=arr, chunk_id=chunk_id, start_idx=start_idx, end_idx=end_idx)
    print(f"  Chunk {chunk_id} complete: {final_path} — shape {arr.shape}", flush=True)
    if ckpt_path.exists():
        ckpt_path.unlink()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <chunk_id> <n_chunks>")
        sys.exit(1)

    chunk_id = int(sys.argv[1])
    n_chunks = int(sys.argv[2])

    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGUSR1, handle_sigterm)

    data_dir = Path(__file__).parent.parent / "data" / "alanine_short"
    data_dir.mkdir(parents=True, exist_ok=True)
    start_struct_path = data_dir / "starting_structures.npz"

    print(f"=== Chunk {chunk_id}/{n_chunks} — PID {os.getpid()} — {datetime.now().isoformat()} ===", flush=True)

    # Build system
    topology, system, positions = build_system()
    print(f"  Atoms: {topology.getNumAtoms()}", flush=True)

    # Load starting structures (must exist — generated by prep step)
    if not start_struct_path.exists():
        print(f"ERROR: {start_struct_path} not found. Run alanine_dipeptide_gen.py first to generate starting structures.")
        sys.exit(1)
    data = np.load(start_struct_path)
    starting_structures = list(data['structures'])
    print(f"  Loaded {len(starting_structures)} starting structures", flush=True)

    run_chunk(chunk_id, n_chunks, topology, system, starting_structures, data_dir)
    print(f"Finished at {datetime.now().isoformat()}", flush=True)
