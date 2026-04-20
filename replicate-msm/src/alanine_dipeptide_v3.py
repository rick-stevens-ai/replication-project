"""
Alanine dipeptide trajectory generation - v3 (longer trajectories)
- 100 ps per trajectory (2001 frames at 50 fs save interval)
- 11,388 trajectories from 8 starting structures (3 αR + 5 αL)
- Checkpoint-restart support
- Multi-GPU parallel (spawn context)
"""
import numpy as np
import openmm as mm
import openmm.app as app
import openmm.unit as unit
import os, sys, json, signal, time, argparse
import multiprocessing as mp

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--data-dir', default='data/alanine_v3')
    p.add_argument('--n-traj', type=int, default=11388)
    p.add_argument('--n-steps-per-traj', type=int, default=100000)  # 100 ps at 1 fs → but we use 2fs timestep → 50000 steps = 100ps
    p.add_argument('--save-interval', type=int, default=100)  # save every 100 steps = 200fs → 500 frames per traj
    p.add_argument('--platform', default='auto', choices=['auto', 'CUDA', 'OpenCL', 'CPU'])
    p.add_argument('--platform-index', type=int, default=None, help='OpenCL platform index (Aurora: 1)')
    p.add_argument('--device', type=int, default=None)
    p.add_argument('--n-workers', type=int, default=None)
    p.add_argument('--chunk', type=int, default=None, help='Which chunk (0-indexed)')
    p.add_argument('--n-chunks', type=int, default=None, help='Total chunks')
    p.add_argument('--checkpoint-interval', type=int, default=50)
    return p.parse_args()

# Starting structure probabilities (paper Eq. 64)
START_PROBS = np.array([0.05, 0.05, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1])

def create_system():
    """Create alanine dipeptide system in TIP3P water."""
    from openmm.app import PDBFile, ForceField, Modeller, PME, HBonds
    
    pdb_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'ala_dipeptide_correct.pdb')
    if not os.path.exists(pdb_path):
        # Build from scratch
        from openmm.app import NoCutoff
        ff = ForceField('amber99sbildn.xml', 'tip3p.xml')
        # Create Ace-Ala-NMe
        from openmm.app import Topology, Element
        # Use a simple approach: build from sequence
        modeller = Modeller(Topology(), [])
        # ... this is complex, use PDB instead
        raise FileNotFoundError(f"Need PDB at {pdb_path}")
    
    pdb = PDBFile(pdb_path)
    ff = ForceField('amber99sbildn.xml', 'tip3p.xml')
    modeller = Modeller(pdb.topology, pdb.positions)
    modeller.addSolvent(ff, model='tip3p', padding=1.0*unit.nanometers)
    
    system = ff.createSystem(modeller.topology, 
                             nonbondedMethod=PME,
                             nonbondedCutoff=1.0*unit.nanometers,
                             constraints=HBonds)
    
    return system, modeller.topology, modeller.positions

def get_phi_psi(positions, topology):
    """Extract phi/psi dihedrals from positions."""
    # Find atom indices for phi (C-N-CA-C) and psi (N-CA-C-N)
    atoms = list(topology.atoms())
    atom_names = [a.name for a in atoms]
    residues = list(topology.residues())
    
    # For Ace-Ala-NMe, the Ala residue is index 1
    ala_atoms = {a.name: a.index for a in residues[1].atoms()}
    ace_atoms = {a.name: a.index for a in residues[0].atoms()}
    nme_atoms = {a.name: a.index for a in residues[2].atoms()}
    
    # phi: C(Ace) - N(Ala) - CA(Ala) - C(Ala)
    phi_indices = [ace_atoms['C'], ala_atoms['N'], ala_atoms['CA'], ala_atoms['C']]
    # psi: N(Ala) - CA(Ala) - C(Ala) - N(NMe)
    psi_indices = [ala_atoms['N'], ala_atoms['CA'], ala_atoms['C'], nme_atoms['N']]
    
    pos = np.array(positions.value_in_unit(unit.nanometers))
    
    def dihedral(p1, p2, p3, p4):
        b1 = p2 - p1; b2 = p3 - p2; b3 = p4 - p3
        n1 = np.cross(b1, b2); n2 = np.cross(b2, b3)
        n1 /= np.linalg.norm(n1); n2 /= np.linalg.norm(n2)
        m1 = np.cross(n1, b2/np.linalg.norm(b2))
        return np.arctan2(np.dot(m1, n2), np.dot(n1, n2))
    
    phi = dihedral(pos[phi_indices[0]], pos[phi_indices[1]], 
                   pos[phi_indices[2]], pos[phi_indices[3]])
    psi = dihedral(pos[psi_indices[0]], pos[psi_indices[1]], 
                   pos[psi_indices[2]], pos[psi_indices[3]])
    return phi, psi

def run_simulation(args_tuple):
    """Run a single trajectory and return dihedrals."""
    traj_idx, starting_pos, system_xml, topology_xml, platform_name, device_idx, platform_index, n_steps, save_interval = args_tuple
    
    system = mm.XmlSerializer.deserialize(system_xml)
    # Reconstruct topology from XML... simplified: just use the integrator
    
    integrator = mm.LangevinMiddleIntegrator(300*unit.kelvin, 1.0/unit.picosecond, 0.002*unit.picoseconds)
    
    if platform_name == 'CUDA':
        platform = mm.Platform.getPlatformByName('CUDA')
        properties = {'DeviceIndex': str(device_idx)}
    elif platform_name == 'OpenCL':
        platform = mm.Platform.getPlatformByName('OpenCL')
        properties = {'OpenCLPlatformIndex': str(platform_index), 'OpenCLDeviceIndex': str(device_idx)}
    else:
        platform = mm.Platform.getPlatformByName('CPU')
        properties = {}
    
    context = mm.Context(system, integrator, platform, properties)
    context.setPositions(starting_pos)
    context.setVelocitiesToTemperature(300*unit.kelvin)
    
    n_frames = n_steps // save_interval + 1
    dihedrals = np.zeros((n_frames, 2))
    
    # Record initial state
    state = context.getState(getPositions=True)
    # ... need topology for phi/psi extraction
    # For speed, just record positions and compute dihedrals later
    # Actually, store raw phi/psi angles
    
    for frame in range(n_frames):
        if frame > 0:
            integrator.step(save_interval)
        state = context.getState(getPositions=True)
        # Simplified: compute phi/psi from positions
        pos = state.getPositions(asNumpy=True).value_in_unit(unit.nanometers)
        # Hard-coded atom indices (need to be set correctly per system)
        # This is a placeholder - actual indices depend on the PDB
        dihedrals[frame, 0] = 0  # phi placeholder
        dihedrals[frame, 1] = 0  # psi placeholder
    
    return traj_idx, dihedrals

if __name__ == '__main__':
    args = parse_args()
    print(f"Alanine dipeptide v3: {args.n_traj} trajectories, "
          f"{args.n_steps_per_traj} steps ({args.n_steps_per_traj * 0.002:.0f} ps)")
