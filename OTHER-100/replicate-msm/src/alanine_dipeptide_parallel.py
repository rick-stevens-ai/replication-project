"""
Phase 3: Alanine Dipeptide MD — Multi-GPU Parallel Generation

Runs N_CHUNKS in parallel across GPUs on a single node.
Each chunk runs on a separate OpenCL device (GPU/tile).

Usage: python alanine_dipeptide_parallel.py [n_chunks] [n_gpus]
  Defaults: n_chunks=8, n_gpus=auto-detect

Each chunk has its own checkpoint; preemption-safe.
"""

import numpy as np
import os
import sys
import signal
import multiprocessing as mp
from pathlib import Path
from datetime import datetime

def load_openmm_plugins():
    """Load OpenMM plugins from openmm-cuda/openmm-opencl pip packages if available."""
    import openmm as mm
    site_packages = os.path.dirname(os.path.dirname(mm.__file__))
    plugin_dir = os.path.join(site_packages, 'OpenMM.libs', 'lib', 'plugins')
    if os.path.exists(plugin_dir):
        try:
            mm.Platform.loadPluginsFromDirectory(plugin_dir)
        except Exception:
            pass
    env_dir = os.environ.get('OPENMM_PLUGIN_DIR', '')
    if env_dir and os.path.exists(env_dir) and env_dir != plugin_dir:
        try:
            mm.Platform.loadPluginsFromDirectory(env_dir)
        except Exception:
            pass

# Shared flag for shutdown
shutdown_event = mp.Event()


def signal_handler(signum, frame):
    print(f"\n*** SIGTERM/SIGUSR1 received — signaling all workers to checkpoint ***", flush=True)
    shutdown_event.set()


def get_n_devices():
    """Detect number of GPU devices by running a tiny sim on each."""
    import openmm as mm
    from openmm import app, unit
    default_plat = os.environ.get('OPENMM_DEFAULT_PLATFORM', '')
    
    candidates = []
    if default_plat:
        candidates.append(default_plat)
    candidates.extend(['CUDA', 'OpenCL'])
    
    for plat_name in candidates:
        try:
            platform = mm.Platform.getPlatformByName(plat_name)
        except:
            continue
        
        count = 0
        for i in range(32):
            try:
                system = mm.System()
                system.addParticle(39.948)
                force = mm.NonbondedForce()
                force.addParticle(0.0, 0.3405, 0.996)
                system.addForce(force)
                system.setDefaultPeriodicBoxVectors(
                    mm.Vec3(2,0,0)*unit.nanometers,
                    mm.Vec3(0,2,0)*unit.nanometers,
                    mm.Vec3(0,0,2)*unit.nanometers)
                integrator = mm.VerletIntegrator(0.001)
                top = app.Topology()
                chain = top.addChain(); res = top.addResidue('AR', chain)
                top.addAtom('Ar', app.Element.getBySymbol('Ar'), res)
                if plat_name == 'CUDA':
                    props = {'DeviceIndex': str(i)}
                elif plat_name == 'OpenCL':
                    props = {'OpenCLDeviceIndex': str(i)}
                else:
                    props = {}
                sim = app.Simulation(top, system, integrator, platform, props)
                sim.context.setPositions([(1,1,1)] * unit.nanometers)
                sim.step(10)
                del sim
                count += 1
            except:
                break
        
        if count > 0:
            print(f"  Detected {count} {plat_name} device(s)", flush=True)
            return count
    
    print("  No GPU devices found, using 1 CPU worker", flush=True)
    return 1


def build_system():
    """Build alanine dipeptide in explicit TIP3P water."""
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
        mod.addSolvent(ff, model='tip3p', boxSize=mm.Vec3(2.3222,2.3222,2.3222)*unit.nanometers)
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
    mod.addSolvent(ff, model='tip3p', boxSize=mm.Vec3(2.3222,2.3222,2.3222)*unit.nanometers)
    sys_obj = ff.createSystem(mod.topology, nonbondedMethod=PME,
                          nonbondedCutoff=0.9*unit.nanometers, constraints=app.HBonds)
    return mod.topology, sys_obj, mod.positions


N_TOTAL = 11388
START_PROBS = np.array([0.05, 0.05, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1])
CHECKPOINT_INTERVAL = 200


def compute_sim_assignments():
    n_per_struct = np.round(START_PROBS * N_TOTAL).astype(int)
    n_per_struct[-1] = N_TOTAL - n_per_struct[:-1].sum()
    assignments = []
    for struct_idx, count in enumerate(n_per_struct):
        assignments.extend([struct_idx] * count)
    return assignments, n_per_struct


def run_chunk_worker(args):
    """Worker function for one chunk. Runs on assigned GPU device."""
    chunk_id, n_chunks, gpu_id, data_dir, shutdown_event_flag = args
    
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
            print(f"  [chunk {chunk_id}] Resuming: {completed}/{my_count} done", flush=True)
        except:
            completed = 0; all_dihedrals = []

    if completed >= my_count:
        return chunk_id

    # Select platform and pin to GPU
    default_plat = os.environ.get('OPENMM_DEFAULT_PLATFORM', '')
    platform = None
    platform_props = {}
    for name in ([default_plat] if default_plat else []) + ['CUDA', 'OpenCL', 'CPU']:
        try:
            platform = mm.Platform.getPlatformByName(name)
            if name == 'CUDA':
                platform_props = {'DeviceIndex': str(gpu_id)}
            elif name == 'OpenCL':
                platform_props = {'OpenCLDeviceIndex': str(gpu_id)}
            print(f"  [chunk {chunk_id}] Using {name} device {gpu_id}", flush=True)
            break
        except:
            continue
    if platform is None:
        platform = mm.Platform.getPlatformByName('CPU')

    # Load starting structures
    ss_data = np.load(data_dir / "starting_structures.npz")
    starting_structures = list(ss_data['structures'])

    # Build system (each worker needs its own copy)
    topology, system, _ = build_system()
    top_md = md.Topology.from_openmm(topology)
    dummy = md.Trajectory(np.zeros((1, top_md.n_atoms, 3)), top_md)
    phi_indices = md.compute_phi(dummy)[0]
    psi_indices = md.compute_psi(dummy)[0]

    steps_per_save = 25
    n_saves = 400
    last_ckpt = completed

    for i in range(my_count):
        if i < completed:
            continue

        if shutdown_event_flag.is_set():
            print(f"  [chunk {chunk_id}] Shutdown at {i}/{my_count}", flush=True)
            np.savez(ckpt_path, completed=i, dihedrals=np.array(all_dihedrals) if all_dihedrals else np.array([]))
            return chunk_id

        struct_idx = assignments[start_idx + i]

        integrator = mm.LangevinMiddleIntegrator(300*unit.kelvin, 1.0/unit.picoseconds, 2.0*unit.femtoseconds)
        
        if platform_props:
            sim = app.Simulation(topology, system, integrator, platform, platform_props)
        else:
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
    """Merge all chunk results into final output."""
    data_dir = Path(data_dir)
    chunks = []
    for i in range(n_chunks):
        p = data_dir / f"dihedrals_chunk{i}.npz"
        if not p.exists():
            print(f"  Missing chunk {i}, cannot merge yet")
            return False
        d = np.load(p)
        chunks.append(d['dihedrals'])
        print(f"  chunk {i}: {d['dihedrals'].shape[0]} sims")

    merged = np.concatenate(chunks, axis=0)
    n_per_struct = np.round(START_PROBS * N_TOTAL).astype(int)
    n_per_struct[-1] = N_TOTAL - n_per_struct[:-1].sum()

    out = data_dir / "dihedrals_short.npz"
    np.savez(out, dihedrals=merged, start_probs=START_PROBS, n_per_struct=n_per_struct)
    print(f"\nMerged {merged.shape[0]} sims → {out} — shape {merged.shape}")
    return True


if __name__ == "__main__":
    n_chunks = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    n_gpus = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGUSR1, signal_handler)

    data_dir = Path(__file__).parent.parent / "data" / "alanine_short"
    data_dir.mkdir(parents=True, exist_ok=True)

    load_openmm_plugins()
    print(f"=== Multi-GPU Parallel Generation ===", flush=True)
    print(f"  PID: {os.getpid()}", flush=True)
    print(f"  Time: {datetime.now().isoformat()}", flush=True)
    print(f"  Chunks: {n_chunks}", flush=True)

    # Auto-detect GPUs if not specified
    if n_gpus == 0:
        n_gpus = get_n_devices()
    print(f"  GPUs detected: {n_gpus}", flush=True)

    # Check starting structures exist
    ss_path = data_dir / "starting_structures.npz"
    if not ss_path.exists():
        print("Generating starting structures first...", flush=True)
        topology, system, positions = build_system()
        # Quick equilibration to generate diverse starts
        import openmm as mm
        from openmm import app, unit
        import mdtraj as md
        
        default_plat = os.environ.get('OPENMM_DEFAULT_PLATFORM', '')
        platform = None
        for name in ([default_plat] if default_plat else []) + ['CUDA', 'OpenCL', 'CPU']:
            try:
                platform = mm.Platform.getPlatformByName(name)
                break
            except:
                continue
        
        integrator = mm.LangevinMiddleIntegrator(300*unit.kelvin, 1.0/unit.picoseconds, 2.0*unit.femtoseconds)
        sim = app.Simulation(topology, system, integrator, platform)
        sim.context.setPositions(positions)
        sim.minimizeEnergy()
        sim.context.setVelocitiesToTemperature(300*unit.kelvin)
        
        top_md = md.Topology.from_openmm(topology)
        all_pos = []; all_pp = []
        for _ in range(200):
            sim.step(5000)
            state = sim.context.getState(getPositions=True)
            pos = state.getPositions(asNumpy=True).value_in_unit(unit.nanometers)
            all_pos.append(pos.copy())
            frame = md.Trajectory(pos.reshape(1,-1,3), top_md)
            phi_i = md.compute_phi(frame)[0]; psi_i = md.compute_psi(frame)[0]
            p = md.compute_dihedrals(frame, phi_i)[0,0] if len(phi_i) else 0
            s = md.compute_dihedrals(frame, psi_i)[0,0] if len(psi_i) else 0
            all_pp.append([p, s])
        
        all_pp = np.array(all_pp)
        from sklearn.cluster import KMeans
        km = KMeans(n_clusters=8, random_state=42, n_init=10).fit(all_pp)
        structs = []; struct_pp = []
        for k in range(8):
            mask = km.labels_ == k
            dists = np.linalg.norm(all_pp[mask] - km.cluster_centers_[k], axis=1)
            best = np.where(mask)[0][np.argmin(dists)]
            structs.append(all_pos[best]); struct_pp.append(all_pp[best])
        np.savez(ss_path, structures=np.array(structs), phi_psi=np.array(struct_pp))
        print(f"  Saved starting structures", flush=True)

    # Assign chunks to GPUs round-robin
    worker_args = []
    for chunk_id in range(n_chunks):
        gpu_id = chunk_id % n_gpus
        worker_args.append((chunk_id, n_chunks, gpu_id, str(data_dir), shutdown_event))

    # Run in parallel — one process per chunk, pinned to GPUs
    n_workers = min(n_chunks, n_gpus)
    print(f"  Launching {n_workers} parallel workers...", flush=True)

    with mp.Pool(n_workers) as pool:
        results = pool.map(run_chunk_worker, worker_args)

    print(f"\nAll workers done. Attempting merge...", flush=True)
    merge_chunks(n_chunks, data_dir)
    print(f"Finished at {datetime.now().isoformat()}", flush=True)
