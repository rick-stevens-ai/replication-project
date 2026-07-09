# Brief

Independent replication of Mohan, Sundararaj & Thiagarajan (2019), "Numerical
simulation of flow over buildings using OpenFOAM®", AIP Conf. Proc. 2112,
020149 (DOI 10.1063/1.5112334). The paper is a qualitative CFD
demonstration: steady incompressible RANS with the standard k-ε model, solved
by simpleFoam, on a group of buildings of varying height inside a rectangular
domain, with inlet U=10 m/s, TI=0.1, ν=1.5e-5 m²/s. The authors explicitly
state their configuration is "an example case available in OpenFOAM";
inspection of the OpenFOAM v1906 distribution shows this to be the
`simpleFoam/windAroundBuildings` tutorial, whose every hard-coded value
(nu=1.5e-05, Uinlet=(10 0 0), kInlet=1.5 with comment "k=1.5*(I·U)²; I=0.1",
kEpsilon RASModel, simpleFoam application) matches the paper verbatim.
We ran that identical case on uicgpu (OpenFOAM 1906 Debian package,
`/usr/share/doc/openfoam-examples/examples/incompressible/simpleFoam/windAroundBuildings`)
to completion (400 SIMPLE iterations, 185,237-cell snappyHexMesh, 6-way MPI),
extracted global field extrema and line profiles, and verified all five
qualitative claims (convergence, roof acceleration, recirculation behind
buildings, 3D wake, undisturbed upstream flow). Verdict: **REPLICATED**.
