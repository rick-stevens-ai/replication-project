"""
Alanine Dipeptide — Medium-Length Ensemble (200 ps trajectories)

Same protocol as the 20 ps ensemble but 10× longer per trajectory.
5,000 trajectories × 200 ps, save every 0.5 ps.
This gives OOM more data per trajectory to correct bias.

Paper used 20 ps × 11,388 trajs. We compare:
  - 20 ps  × 11,388 (original — already done)
  - 200 ps × 5,000  (this run — more data per traj)

Multi-GPU, checkpoint-restart, SIGTERM-safe.
"""

import numpy as np
import os
import sys
import signal
import multiprocessing as mp
from pathlib import Path
from datetime import datetime

SHUTDOWN_REQUESTED = False
N_TOTAL = 5000
TRAJ_LENGTH_PS = 200.0
SAVE_INTERVAL_FS = 500.0     # 0.5 ps per save
TIMESTEP_FS = 2.0
STEPS_PER_SAVE = int(SAVE_INTERVAL_FS / TIMESTEP_FS)  # 250
N_SAVES = int(TRAJ_LENGTH_PS * 1000 / SAVE_INTERVAL_FS)  # 400
START_PROBS = np.array([0.05, 0.05, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1])
CHECKPOINT_INTERVAL = 100


def handle_sigterm(signum, frame):
    global SHUTDOWN_REQUESTED
    SHUTDOWN_REQUESTED = True
    print(f"\n*** SIGTERM at {datetime.now().isoformat()} ***", flush=True)


def load_openmm_plugins():
    import openmm as mm
    site_packages = os.path.dirname(os.path.dirname(mm.__file__))
    plugin_dir = os.path.join(site_packages, 'OpenMM.libs', 'lib', 'plugins')
    if os.path.exists(plugin_dir):
        try:
            mm.Platform.loadPluginsFromDirectory(plugin_dir)
        except Exception:
            pass


def build_system():
    import openmm as mm
    from openmm import app, unit
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
        mod.addSolvent(ff, model='tip3p', boxSize=mm.Vec3(2.3222, 2.3222, 2.3222)*unit.nanometers)
        sys_obj = ff.createSystem(mod.topology, nonbondedMethod=PME,
                                  nonbondedCutoff=0.9*unit.nanometers, constraints=app.HBonds)
        return mod.topology, sys_obj, mod.positions
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
    mod.addSolvent(ff, model='tip3p', boxSize=mm.Vec3(2.3222, 2.3222, 2.3222)*unit.nanometers)
    sys_obj = ff.createSystem(mod.topology, nonbondedMethod=PME,
                              nonbondedCutoff=0.9*unit.nanometers, constraints=app.HBonds)
    return mod.topology, sys_obj, mod.positions


def compute_sim_assignments():
    n_per_struct = np.round(START_PROBS * N_TOTAL).astype(int)
    n_per_struct[-1] = N_TOTAL - n_per_struct[:-1].sum()
    assignments = []
    for struct_idx, count in enumerate(n_per_struct):
        assignments.extend([struct_idx] * count)
    return assignments, n_per_struct


def run_chunk(args):
    """Worker: run a chunk of simulations on a specific GPU."""
    chunk_id, n_chunks, gpu_id, data_dir = args

    load_openmm_plugins()
    import openmm as mm
    from openmm import app, unit
    import mdtraj as md

    assignments, _ = compute_sim_assignments()
    total = len(assignments)
    chunk_size = total // n_chunks
    start_idx = chunk_id * chunk_size
    end_idx = start_idx + chunk_size if chunk_id < n_chunks - 1 else total
    my_count = end_idx - start_idx

    data_dir = Path(data_dir)
    ckpt_path = data_dir / f"checkpoint_chunk{chunk_id}.npz"
    final_path = data_dir / f"dihedrals_chunk{chunk_id}.npz"

    print(f"  [chunk {chunk_id}] GPU {gpu_id}, sims [{start_idx},{end_idx}) = {my_count}", flush=True)

    if final_path.exists():
        print(f"  [chunk {chunk_id}] Already complete", flush=True)
        return chunk_id

    # Load checkpoint
    completed = 0
    all_dihedrals = []
    if ckpt_path.exists():
        try:
            d = np.load(ckpt_path, allow_pickle=True)
            completed = int(d['completed'])
            all_dihedrals = list(d['dihedrals'])
            print(f"  [chunk {chunk_id}] Resuming: {completed}/{my_count}", flush=True)
        except:
            completed = 0; all_dihedrals = []

    if completed >= my_count:
        return chunk_id

    # Platform
    platform = None
    platform_props = {}
    for name in ['CUDA', 'OpenCL', 'CPU']:
        try:
            platform = mm.Platform.getPlatformByName(name)
            if name == 'CUDA':
                platform_props = {'DeviceIndex': str(gpu_id)}
            elif name == 'OpenCL':
                platform_props = {'OpenCLDeviceIndex': str(gpu_id)}
            print(f"  [chunk {chunk_id}] {name} device {gpu_id}", flush=True)
            break
        except:
            continue

    # Load starting structures (from the original 20ps run)
    ss_short = Path(__file__).parent.parent / "data" / "alanine_short" / "starting_structures.npz"
    ss_data = np.load(ss_short)
    starting_structures = list(ss_data['structures'])

    topology, system, _ = build_system()
    top_md = md.Topology.from_openmm(topology)
    dummy = md.Trajectory(np.zeros((1, top_md.n_atoms, 3)), top_md)
    phi_indices = md.compute_phi(dummy)[0]
    psi_indices = md.compute_psi(dummy)[0]

    last_ckpt = completed

    for i in range(my_count):
        if i < completed:
            continue

        if SHUTDOWN_REQUESTED:
            print(f"  [chunk {chunk_id}] Shutdown at {i}/{my_count}", flush=True)
            np.savez(ckpt_path, completed=i,
                     dihedrals=np.array(all_dihedrals) if all_dihedrals else np.array([]))
            return chunk_id

        struct_idx = assignments[start_idx + i]

        integrator = mm.LangevinMiddleIntegrator(
            300*unit.kelvin, 1.0/unit.picoseconds, TIMESTEP_FS*unit.femtoseconds
        )

        if platform_props:
            sim = app.Simulation(topology, system, integrator, platform, platform_props)
        else:
            sim = app.Simulation(topology, system, integrator, platform)

        sim.context.setPositions(starting_structures[struct_idx] * unit.nanometers)
        sim.context.setVelocitiesToTemperature(300 * unit.kelvin)

        traj = np.zeros((N_SAVES + 1, 2), dtype=np.float32)

        # Initial frame
        state = sim.context.getState(getPositions=True)
        pos = state.getPositions(asNumpy=True).value_in_unit(unit.nanometers)
        frame = md.Trajectory(pos.reshape(1, -1, 3), top_md)
        traj[0, 0] = md.compute_dihedrals(frame, phi_indices)[0, 0]
        traj[0, 1] = md.compute_dihedrals(frame, psi_indices)[0, 0]

        for s in range(N_SAVES):
            sim.step(STEPS_PER_SAVE)
            state = sim.context.getState(getPositions=True)
            pos = state.getPositions(asNumpy=True).value_in_unit(unit.nanometers)
            frame = md.Trajectory(pos.reshape(1, -1, 3), top_md)
            traj[s+1, 0] = md.compute_dihedrals(frame, phi_indices)[0, 0]
            traj[s+1, 1] = md.compute_dihedrals(frame, psi_indices)[0, 0]

        all_dihedrals.append(traj)
        done = i + 1

        if done % 100 == 0:
            print(f"  [chunk {chunk_id}] {done}/{my_count}", flush=True)

        if (done - last_ckpt) >= CHECKPOINT_INTERVAL:
            np.savez(ckpt_path, completed=done, dihedrals=np.array(all_dihedrals))
            last_ckpt = done

    # Save final
    arr = np.array(all_dihedrals)
    np.savez(final_path, dihedrals=arr, chunk_id=chunk_id, start_idx=start_idx, end_idx=end_idx)
    print(f"  [chunk {chunk_id}] Done: {arr.shape}", flush=True)
    if ckpt_path.exists():
        ckpt_path.unlink()
    return chunk_id


def merge_chunks(n_chunks, data_dir):
    data_dir = Path(data_dir)
    chunks = []
    for i in range(n_chunks):
        p = data_dir / f"dihedrals_chunk{i}.npz"
        if not p.exists():
            print(f"  Missing chunk {i}")
            return False
        d = np.load(p)
        chunks.append(d['dihedrals'])
        print(f"  chunk {i}: {d['dihedrals'].shape[0]} sims")

    merged = np.concatenate(chunks, axis=0)
    n_per_struct = np.round(START_PROBS * N_TOTAL).astype(int)
    n_per_struct[-1] = N_TOTAL - n_per_struct[:-1].sum()

    out = data_dir / "dihedrals_medium.npz"
    np.savez(out, dihedrals=merged, start_probs=START_PROBS, n_per_struct=n_per_struct,
             traj_length_ps=TRAJ_LENGTH_PS, save_interval_fs=SAVE_INTERVAL_FS)
    print(f"\nMerged {merged.shape[0]} sims → {out} — shape {merged.shape}")
    return True


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGUSR1, handle_sigterm)

    data_dir = Path(__file__).parent.parent / "data" / "alanine_medium"
    data_dir.mkdir(parents=True, exist_ok=True)

    n_chunks = int(sys.argv[1]) if len(sys.argv) > 1 else 4

    load_openmm_plugins()
    print("=" * 60)
    print("Alanine Dipeptide — Medium Ensemble (200 ps × 5000)")
    print(f"  {N_TOTAL} trajectories × {TRAJ_LENGTH_PS} ps")
    print(f"  Save every {SAVE_INTERVAL_FS} fs → {N_SAVES+1} frames/traj")
    print(f"  Chunks: {n_chunks}")
    print(f"  PID: {os.getpid()}")
    print(f"  Time: {datetime.now().isoformat()}")
    print("=" * 60, flush=True)

    # Detect GPUs
    import openmm as mm
    from openmm import app, unit
    n_gpus = 0
    for name in ['CUDA', 'OpenCL']:
        try:
            p = mm.Platform.getPlatformByName(name)
            for i in range(8):
                try:
                    sys_test = mm.System(); sys_test.addParticle(1.0)
                    f = mm.NonbondedForce(); f.addParticle(0,0.3,0.0); sys_test.addForce(f)
                    sys_test.setDefaultPeriodicBoxVectors(
                        mm.Vec3(2,0,0)*unit.nanometers,
                        mm.Vec3(0,2,0)*unit.nanometers,
                        mm.Vec3(0,0,2)*unit.nanometers)
                    integ = mm.VerletIntegrator(0.001)
                    top = app.Topology(); ch = top.addChain(); res = top.addResidue('A', ch)
                    top.addAtom('X', app.Element.getBySymbol('Ar'), res)
                    props = {'DeviceIndex': str(i)} if name == 'CUDA' else {'OpenCLDeviceIndex': str(i)}
                    s = app.Simulation(top, sys_test, integ, p, props)
                    s.context.setPositions([(1,1,1)]*unit.nanometers); s.step(1); del s
                    n_gpus += 1
                except:
                    break
            if n_gpus > 0: break
        except:
            continue
    n_gpus = max(n_gpus, 1)
    print(f"  GPUs: {n_gpus}", flush=True)

    # Check starting structures exist
    ss_path = Path(__file__).parent.parent / "data" / "alanine_short" / "starting_structures.npz"
    if not ss_path.exists():
        print("ERROR: Starting structures not found. Run alanine_dipeptide_gen.py first.")
        sys.exit(1)

    worker_args = [(i, n_chunks, i % n_gpus, str(data_dir)) for i in range(n_chunks)]

    ctx = mp.get_context("spawn")
    n_workers = min(n_chunks, n_gpus)
    print(f"  Launching {n_workers} workers...", flush=True)

    with ctx.Pool(n_workers) as pool:
        pool.map(run_chunk, worker_args)

    print(f"\nMerging chunks...", flush=True)
    merge_chunks(n_chunks, data_dir)
    print(f"Finished at {datetime.now().isoformat()}")
