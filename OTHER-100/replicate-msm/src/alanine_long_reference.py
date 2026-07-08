"""
Alanine Dipeptide — Long Reference Trajectories

Generate 10 × 100 ns trajectories to establish ground-truth implied timescales.
These serve as the "gold standard" to validate OOM correction from short data.

Target: t₂ ≈ 1400 ps, t₃ ≈ 70 ps (Nüske et al. 2017)

System:
- AMBER ff99SB-ILDN, TIP3P water, 300 K, PME
- Langevin thermostat, 2 fs timestep
- Save φ/ψ every 1 ps (= 500 steps)

Checkpoint-restart: saves per-trajectory progress.
Multi-GPU: distributes trajectories across available GPUs.
"""

import numpy as np
import os
import sys
import signal
import json
import multiprocessing as mp
from pathlib import Path
from datetime import datetime

SHUTDOWN_REQUESTED = False
N_TRAJS = 10
TRAJ_LENGTH_NS = 100.0        # 100 ns each
SAVE_INTERVAL_PS = 1.0        # save every 1 ps
TIMESTEP_FS = 2.0
STEPS_PER_SAVE = int(SAVE_INTERVAL_PS * 1000 / TIMESTEP_FS)  # 500
N_SAVES = int(TRAJ_LENGTH_NS * 1e3 / SAVE_INTERVAL_PS)       # 100,000
CHECKPOINT_INTERVAL = 10000   # checkpoint every 10K saves (~10 ns)


def handle_sigterm(signum, frame):
    global SHUTDOWN_REQUESTED
    SHUTDOWN_REQUESTED = True
    print(f"\n*** SIGTERM at {datetime.now().isoformat()} — checkpointing ***", flush=True)


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


def run_long_traj(args):
    """Run one long trajectory on a specific GPU."""
    traj_id, gpu_id, data_dir = args

    load_openmm_plugins()
    import openmm as mm
    from openmm import app, unit
    import mdtraj as md

    data_dir = Path(data_dir)
    ckpt_path = data_dir / f"long_traj_{traj_id}_ckpt.npz"
    final_path = data_dir / f"long_traj_{traj_id}.npz"

    if final_path.exists():
        print(f"  [traj {traj_id}] Already complete", flush=True)
        return traj_id

    # Load checkpoint
    completed_saves = 0
    dihedrals = np.zeros((N_SAVES + 1, 2), dtype=np.float32)
    sim_state_xml = None
    if ckpt_path.exists():
        try:
            d = np.load(ckpt_path, allow_pickle=True)
            completed_saves = int(d['completed_saves'])
            dihedrals[:completed_saves+1] = d['dihedrals'][:completed_saves+1]
            sim_state_xml = str(d['sim_state_xml']) if 'sim_state_xml' in d else None
            print(f"  [traj {traj_id}] Resuming from save {completed_saves}/{N_SAVES} "
                  f"({completed_saves * SAVE_INTERVAL_PS / 1000:.1f} ns)", flush=True)
        except Exception as e:
            print(f"  [traj {traj_id}] Corrupt checkpoint, restarting: {e}", flush=True)
            completed_saves = 0
            sim_state_xml = None

    if completed_saves >= N_SAVES:
        np.savez(final_path, dihedrals=dihedrals, traj_id=traj_id)
        return traj_id

    # Build system
    topology, system, positions = build_system()

    # Select platform
    platform = None
    platform_props = {}
    for name in ['CUDA', 'OpenCL', 'CPU']:
        try:
            platform = mm.Platform.getPlatformByName(name)
            if name == 'CUDA':
                platform_props = {'DeviceIndex': str(gpu_id)}
            elif name == 'OpenCL':
                platform_props = {'OpenCLDeviceIndex': str(gpu_id)}
            print(f"  [traj {traj_id}] GPU {gpu_id}, {name}", flush=True)
            break
        except:
            continue

    integrator = mm.LangevinMiddleIntegrator(
        300 * unit.kelvin, 1.0 / unit.picoseconds, TIMESTEP_FS * unit.femtoseconds
    )

    if platform_props:
        simulation = app.Simulation(topology, system, integrator, platform, platform_props)
    else:
        simulation = app.Simulation(topology, system, integrator, platform)

    # Initialize or restore state
    if sim_state_xml and completed_saves > 0:
        simulation.context.setState(mm.XmlSerializer.deserialize(sim_state_xml))
        print(f"  [traj {traj_id}] Restored simulation state", flush=True)
    else:
        simulation.context.setPositions(positions)
        simulation.minimizeEnergy()
        simulation.context.setVelocitiesToTemperature(300 * unit.kelvin)
        # 100 ps equilibration
        simulation.step(50000)
        print(f"  [traj {traj_id}] Equilibrated (100 ps)", flush=True)

        # Record initial frame
        top_md = md.Topology.from_openmm(topology)
        state = simulation.context.getState(getPositions=True)
        pos = state.getPositions(asNumpy=True).value_in_unit(unit.nanometers)
        frame = md.Trajectory(pos.reshape(1, -1, 3), top_md)
        phi_i = md.compute_phi(frame)[0]
        psi_i = md.compute_psi(frame)[0]
        dihedrals[0, 0] = md.compute_dihedrals(frame, phi_i)[0, 0]
        dihedrals[0, 1] = md.compute_dihedrals(frame, psi_i)[0, 0]

    # Setup dihedral computation
    top_md = md.Topology.from_openmm(topology)
    dummy = md.Trajectory(np.zeros((1, top_md.n_atoms, 3)), top_md)
    phi_indices = md.compute_phi(dummy)[0]
    psi_indices = md.compute_psi(dummy)[0]

    last_ckpt = completed_saves
    start_from = max(completed_saves, 1) if completed_saves > 0 else 1

    for save_idx in range(start_from, N_SAVES + 1):
        if SHUTDOWN_REQUESTED:
            # Save checkpoint with simulation state for exact restart
            state_xml = mm.XmlSerializer.serialize(
                simulation.context.getState(getPositions=True, getVelocities=True)
            )
            np.savez(ckpt_path,
                     completed_saves=save_idx - 1,
                     dihedrals=dihedrals,
                     sim_state_xml=state_xml,
                     traj_id=traj_id)
            print(f"  [traj {traj_id}] Checkpointed at save {save_idx-1}/{N_SAVES}", flush=True)
            return traj_id

        simulation.step(STEPS_PER_SAVE)

        state = simulation.context.getState(getPositions=True)
        pos = state.getPositions(asNumpy=True).value_in_unit(unit.nanometers)
        frame = md.Trajectory(pos.reshape(1, -1, 3), top_md)
        dihedrals[save_idx, 0] = md.compute_dihedrals(frame, phi_indices)[0, 0]
        dihedrals[save_idx, 1] = md.compute_dihedrals(frame, psi_indices)[0, 0]

        if save_idx % 10000 == 0:
            ns_done = save_idx * SAVE_INTERVAL_PS / 1000
            print(f"  [traj {traj_id}] {ns_done:.0f}/{TRAJ_LENGTH_NS:.0f} ns", flush=True)

        # Periodic checkpoint
        if (save_idx - last_ckpt) >= CHECKPOINT_INTERVAL:
            state_xml = mm.XmlSerializer.serialize(
                simulation.context.getState(getPositions=True, getVelocities=True)
            )
            np.savez(ckpt_path,
                     completed_saves=save_idx,
                     dihedrals=dihedrals,
                     sim_state_xml=state_xml,
                     traj_id=traj_id)
            last_ckpt = save_idx

    # Save final
    np.savez(final_path, dihedrals=dihedrals, traj_id=traj_id)
    print(f"  [traj {traj_id}] Complete: {TRAJ_LENGTH_NS} ns, {N_SAVES+1} frames", flush=True)
    if ckpt_path.exists():
        ckpt_path.unlink()
    return traj_id


def merge_and_analyze(data_dir):
    """Merge long trajectories and compute reference timescales."""
    from sklearn.cluster import KMeans
    from scipy import linalg

    data_dir = Path(data_dir)
    all_dihedrals = []
    for i in range(N_TRAJS):
        f = data_dir / f"long_traj_{i}.npz"
        if not f.exists():
            print(f"  Missing traj {i}")
            return
        d = np.load(f)
        all_dihedrals.append(d['dihedrals'])

    all_dihedrals = np.array(all_dihedrals)  # (10, 100001, 2)
    print(f"Loaded {all_dihedrals.shape[0]} trajectories, {all_dihedrals.shape[1]} frames each")

    # Concatenate all frames for clustering
    flat = all_dihedrals.reshape(-1, 2)
    features = np.column_stack([np.cos(flat[:,0]), np.sin(flat[:,0]),
                                 np.cos(flat[:,1]), np.sin(flat[:,1])])

    print("Clustering into 40 states...")
    km = KMeans(n_clusters=40, random_state=42, n_init=10)
    labels = km.fit_predict(features)
    assignments = labels.reshape(all_dihedrals.shape[0], all_dihedrals.shape[1])

    # Build MSM from concatenated long trajectories — standard reversible MSM
    n_states = 40
    lag_frames_list = [10, 50, 100, 500, 1000, 5000]  # 10 ps to 5 ns
    
    print(f"\nReference MSM from {TRAJ_LENGTH_NS*N_TRAJS:.0f} ns total data:")
    print(f"{'Lag (ps)':>10}  {'t₂ (ps)':>12}  {'t₃ (ps)':>12}")
    print("-" * 40)

    for lag in lag_frames_list:
        # Count transitions across all trajectories
        C = np.zeros((n_states, n_states), dtype=np.float64)
        for traj_assign in assignments:
            for t in range(len(traj_assign) - lag):
                C[traj_assign[t], traj_assign[t + lag]] += 1

        # Reversibilize: C_rev = (C + C.T) / 2
        C_rev = (C + C.T) / 2.0
        row_sums = C_rev.sum(axis=1)
        valid = row_sums > 0
        T = np.zeros_like(C_rev)
        T[valid] = C_rev[valid] / row_sums[valid, None]

        eigenvalues = np.sort(np.real(linalg.eigvals(T)))[::-1]
        # Implied timescales
        ts = []
        for ev in eigenvalues[1:4]:
            if ev > 0 and ev < 1:
                ts.append(-lag * SAVE_INTERVAL_PS / np.log(ev))
            else:
                ts.append(np.nan)

        lag_ps = lag * SAVE_INTERVAL_PS
        print(f"  {lag_ps:8.0f}  {ts[0]:12.1f}  {ts[1]:12.1f}")

    # Save merged data
    np.savez(data_dir / "long_reference_merged.npz",
             dihedrals=all_dihedrals,
             assignments=assignments,
             cluster_centers=km.cluster_centers_)
    print(f"\nSaved merged reference data to {data_dir / 'long_reference_merged.npz'}")


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGUSR1, handle_sigterm)

    data_dir = Path(__file__).parent.parent / "data" / "alanine_long"
    data_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Alanine Dipeptide — Long Reference Trajectories")
    print(f"  {N_TRAJS} × {TRAJ_LENGTH_NS} ns = {N_TRAJS * TRAJ_LENGTH_NS:.0f} ns total")
    print(f"  Save every {SAVE_INTERVAL_PS} ps → {N_SAVES+1} frames/traj")
    print(f"  PID: {os.getpid()}")
    print(f"  Time: {datetime.now().isoformat()}")
    print("=" * 60, flush=True)

    # Detect GPUs
    load_openmm_plugins()
    import openmm as mm
    from openmm import app, unit
    n_gpus = 0
    for name in ['CUDA', 'OpenCL']:
        try:
            p = mm.Platform.getPlatformByName(name)
            for i in range(8):
                try:
                    sys_test = mm.System()
                    sys_test.addParticle(1.0)
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
                    s.context.setPositions([(1,1,1)]*unit.nanometers)
                    s.step(1); del s
                    n_gpus += 1
                except:
                    break
            if n_gpus > 0:
                break
        except:
            continue
    n_gpus = max(n_gpus, 1)
    print(f"  GPUs: {n_gpus}", flush=True)

    if "--analyze" in sys.argv:
        merge_and_analyze(data_dir)
        sys.exit(0)

    # Distribute trajectories across GPUs
    worker_args = []
    for traj_id in range(N_TRAJS):
        gpu_id = traj_id % n_gpus
        worker_args.append((traj_id, gpu_id, str(data_dir)))

    # Run — use spawn context for CUDA safety
    ctx = mp.get_context("spawn")
    n_workers = min(N_TRAJS, n_gpus)
    print(f"  Launching {n_workers} workers for {N_TRAJS} trajectories...", flush=True)

    with ctx.Pool(n_workers) as pool:
        results = pool.map(run_long_traj, worker_args)

    print(f"\nAll trajectories done. Running analysis...", flush=True)
    merge_and_analyze(data_dir)
    print(f"Finished at {datetime.now().isoformat()}")
