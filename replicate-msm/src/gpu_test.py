"""
Quick GPU/tile test: detect all OpenCL devices, run a tiny sim on each.
Verifies multi-GPU parallel works before committing to a production run.
"""
import os
import sys
import time
import multiprocessing as mp


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
    # Also try OPENMM_PLUGIN_DIR env var
    env_dir = os.environ.get('OPENMM_PLUGIN_DIR', '')
    if env_dir and os.path.exists(env_dir) and env_dir != plugin_dir:
        try:
            mm.Platform.loadPluginsFromDirectory(env_dir)
        except Exception:
            pass

def test_device(args):
    device_id, = args
    import openmm as mm
    from openmm import app, unit
    
    default_plat = os.environ.get('OPENMM_DEFAULT_PLATFORM', '')
    for name in ([default_plat] if default_plat else []) + ['CUDA', 'OpenCL', 'CPU']:
        try:
            platform = mm.Platform.getPlatformByName(name)
            if name == 'CUDA':
                props = {'DeviceIndex': str(device_id)}
            elif name == 'OpenCL':
                props = {'OpenCLDeviceIndex': str(device_id)}
            else:
                props = {}
            
            # Build tiny system: single particle in a box
            system = mm.System()
            system.addParticle(39.948)  # argon
            force = mm.NonbondedForce()
            force.addParticle(0.0, 0.3405, 0.996)
            system.addForce(force)
            system.setDefaultPeriodicBoxVectors(
                mm.Vec3(2, 0, 0) * unit.nanometers,
                mm.Vec3(0, 2, 0) * unit.nanometers,
                mm.Vec3(0, 0, 2) * unit.nanometers
            )
            
            integrator = mm.LangevinMiddleIntegrator(300*unit.kelvin, 1.0/unit.picoseconds, 2.0*unit.femtoseconds)
            
            top = app.Topology()
            chain = top.addChain()
            res = top.addResidue('AR', chain)
            top.addAtom('Ar', app.Element.getBySymbol('Ar'), res)
            
            sim = app.Simulation(top, system, integrator, platform, props)
            sim.context.setPositions([(1, 1, 1)] * unit.nanometers)
            sim.context.setVelocitiesToTemperature(300 * unit.kelvin)
            
            t0 = time.time()
            sim.step(1000)
            elapsed = time.time() - t0
            
            print(f"  Device {device_id}: {name} — OK ({elapsed:.3f}s for 1000 steps)", flush=True)
            return (device_id, name, True)
        except Exception as e:
            if 'CPU' not in name:
                continue
            print(f"  Device {device_id}: FAILED — {e}", flush=True)
            return (device_id, 'none', False)
    
    print(f"  Device {device_id}: no platform worked", flush=True)
    return (device_id, 'none', False)


def detect_max_devices():
    """Probe GPU device indices on all platforms by actually running a tiny sim on each."""
    import openmm as mm
    from openmm import app, unit
    default_plat = os.environ.get('OPENMM_DEFAULT_PLATFORM', '')
    
    candidates = []
    if default_plat:
        candidates.append(default_plat)
    candidates.extend(['CUDA', 'OpenCL', 'CPU'])
    
    for plat_name in candidates:
        try:
            platform = mm.Platform.getPlatformByName(plat_name)
        except:
            continue
        
        if plat_name == 'CPU':
            return 1, 'CPU'
        
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
                sim.step(10)  # actually run it to confirm device works
                del sim
                count += 1
            except Exception as e:
                if count == 0:
                    print(f"  {plat_name} device {i}: {e}", flush=True)
                break
        
        if count > 0:
            return count, plat_name
        print(f"  {plat_name}: platform exists but 0 working devices, trying next...", flush=True)
    
    print("  No GPU platform found, CPU only", flush=True)
    return 1, 'CPU'


if __name__ == "__main__":
    print(f"=== GPU/Tile Detection Test ===", flush=True)
    print(f"  Host: {os.uname().nodename}", flush=True)
    print(f"  OPENMM_DEFAULT_PLATFORM: {os.environ.get('OPENMM_DEFAULT_PLATFORM', '(not set)')}", flush=True)
    
    load_openmm_plugins()
    
    import openmm as mm
    print(f"  Available platforms: {[mm.Platform.getPlatform(i).getName() for i in range(mm.Platform.getNumPlatforms())]}", flush=True)
    
    n_devices, plat_name = detect_max_devices()
    print(f"  Detected {n_devices} {plat_name} device(s)", flush=True)
    
    if n_devices == 0:
        print("  ERROR: No devices found!", flush=True)
        sys.exit(1)
    
    print(f"\nTesting each device with a tiny sim...", flush=True)
    
    # Test all devices in parallel
    with mp.Pool(n_devices) as pool:
        results = pool.map(test_device, [(i,) for i in range(n_devices)])
    
    ok = sum(1 for _, _, success in results if success)
    print(f"\n=== Result: {ok}/{n_devices} devices working ===", flush=True)
    
    if ok == n_devices:
        print(f"All clear — safe to run production with {n_devices} parallel workers.", flush=True)
    else:
        print(f"WARNING: {n_devices - ok} devices failed!", flush=True)
        sys.exit(1)
