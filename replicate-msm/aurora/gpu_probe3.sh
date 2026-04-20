#!/bin/bash
#PBS -N gpu_probe3
#PBS -l select=1
#PBS -l walltime=00:10:00
#PBS -q debug
#PBS -A datascience
#PBS -l filesystems=home

cd ~/projects/replicate-msm
source ~/envs/replicate/bin/activate
export OPENMM_DEFAULT_PLATFORM=OpenCL

# Key: make OpenMM use the SYSTEM OpenCL, not its bundled one
# The system has Intel OpenCL ICD at /usr/lib64/intel-opencl/libigdrcl.so
export OCL_ICD_VENDORS=/etc/OpenCL/vendors

echo "=== Checking system OpenCL devices ==="
clinfo -l 2>/dev/null || echo "clinfo not available"

echo "=== Check what libOpenCL OpenMM links to ==="
SITE_PKG=$(python -c "import openmm, os; print(os.path.dirname(os.path.dirname(openmm.__file__)))")
echo "OpenMM site-packages: $SITE_PKG"
ls $SITE_PKG/OpenMM.libs/lib/plugins/libOpenMMOpenCL.so 2>/dev/null
ldd $SITE_PKG/OpenMM.libs/lib/plugins/libOpenMMOpenCL.so 2>/dev/null | grep -i opencl

echo "=== Check system libOpenCL ==="
ls -la /usr/lib64/libOpenCL* 2>/dev/null
ldd /usr/lib64/libOpenCL.so 2>/dev/null | head -10

echo "=== Try LD_PRELOAD system OpenCL ==="
export LD_PRELOAD="/usr/lib64/libOpenCL.so.1"
python -c "
import openmm as mm
import os

# Load plugins
site_packages = os.path.dirname(os.path.dirname(mm.__file__))
plugin_dir = os.path.join(site_packages, 'OpenMM.libs', 'lib', 'plugins')
if os.path.exists(plugin_dir):
    mm.Platform.loadPluginsFromDirectory(plugin_dir)

print('Platforms:', [mm.Platform.getPlatform(i).getName() for i in range(mm.Platform.getNumPlatforms())])

# Try OpenCL
try:
    p = mm.Platform.getPlatformByName('OpenCL')
    from openmm import app, unit
    system = mm.System()
    system.addParticle(39.948)
    force = mm.NonbondedForce()
    force.addParticle(0.0, 0.3405, 0.996)
    system.addForce(force)
    system.setDefaultPeriodicBoxVectors(
        mm.Vec3(2,0,0)*unit.nanometers, mm.Vec3(0,2,0)*unit.nanometers, mm.Vec3(0,0,2)*unit.nanometers)
    integrator = mm.VerletIntegrator(0.001)
    top = app.Topology()
    chain = top.addChain(); res = top.addResidue('AR', chain)
    top.addAtom('Ar', app.Element.getBySymbol('Ar'), res)
    
    # Try each device index
    for i in range(12):
        try:
            sim = app.Simulation(top, system, mm.VerletIntegrator(0.001), p, {'OpenCLDeviceIndex': str(i)})
            sim.context.setPositions([(1,1,1)] * unit.nanometers)
            sim.step(10)
            print(f'  Device {i}: OK')
            del sim
        except Exception as e:
            print(f'  Device {i}: {e}')
            break
except Exception as e:
    print(f'OpenCL failed: {e}')
" 2>&1
