#!/usr/bin/env python3
"""
Extract absolute SSB/DSB yields per energy from dnadamage1 SDD output + ROOT phys-stage edep.

For Mokari et al. 2018 (Geant4-DNA, electrons in liquid water -> DNA damage),
yield convention is Y = N_breaks / (D[Gy] * M_DNA[Gbp]) per event-averaged.

Inputs (one set per energy):
  <rundir>/output.root       # has ntuple/ntuple_1 (physical), ntuple_2 (chemical), edep per hit
  <rundir>/sdd_mokari.txt    # SDD output from scandamages_mokari.C (Essb=17.5 eV, POH=0.13)
  <rundir>/scandamages.log   # contains the printed "Summary of results" #SSB/#DSB lines

DNA mass per event (from dnadamage1 VoxelStraight chromatin-fiber geometry):
  - The voxel is 40 nm cube containing chromatin fiber (Tran/Le 2017).
  - Total DNA inside: 24,460 bp (read from molecule.C / SDD field 4 max copyNb).
  - 1 bp ~= 650 g/mol DNA mass / 1 Gbp = 1e9 bp / molecule.

Dose per event:
  D[Gy] = (totalEdep[J]) / (mass_target[kg])
  where mass_target = volume_water * rho_water (1 g/cm^3) for the irradiated voxel.
  Voxel = 40 nm cube = (4e-6 cm)^3 = 6.4e-17 cm^3 -> 6.4e-17 g = 6.4e-20 kg.

Usage:
  python3 extract_yields.py <rundir>
Prints JSON line with yields per energy.
"""
import os, sys, json, re, math
from pathlib import Path

# Physical constants
eV_to_J = 1.602176634e-19
N_BP_VOXEL = None  # filled per run from max copyNb
RHO_WATER = 1.0    # g/cm^3
# Voxel: 40 nm cube (per SDD header Volumes record)
VOXEL_EDGE_NM = 40.0
VOXEL_VOLUME_CM3 = (VOXEL_EDGE_NM * 1e-7)**3        # nm -> cm
VOXEL_MASS_G = VOXEL_VOLUME_CM3 * RHO_WATER
VOXEL_MASS_KG = VOXEL_MASS_G * 1e-3

def parse_sdd(path):
    """Parse SDD file -> list of (eventID, strand, copyNb, cause)."""
    events = []
    max_copyNb = 0
    with open(path) as f:
        in_data = False
        for line in f:
            line = line.strip()
            if not in_data:
                if "EndOfHeader" in line:
                    in_data = True
                continue
            if not line:
                continue
            # SDD record: "newPrimary, ?; pos x,y,z, chrom_id; copyNb; ?, ?, ?; cause(0=dir,1=indir), strand(0/1), ?;"
            # From observed file: "2, 0; 0, 0, 0, 0; 506; 0, 0, 0; 0, 1, 0;"
            # Fields separated by ';'. Field0 = "newEventFlag,eventID", Field2 = copyNb, Field5 = "cause, strand, dmgType"
            parts = [p.strip() for p in line.rstrip(';').split(';')]
            if len(parts) < 6:
                continue
            try:
                ne_evtID = parts[0].split(',')
                eventID = int(ne_evtID[1].strip()) if len(ne_evtID) > 1 else 0
                copyNb = int(parts[2].strip())
                cause_strand = parts[5].split(',')
                cause = int(cause_strand[0].strip())
                strand = int(cause_strand[1].strip())
            except (ValueError, IndexError):
                continue
            events.append((eventID, strand, copyNb, cause))
            if copyNb > max_copyNb:
                max_copyNb = copyNb
    return events, max_copyNb

def classify(events, cluster_distance=10):
    """Classify into SSB/DSB the same way as scandamages.C does:
       sort damages within each event by copyNb, then group consecutive ones with gap < cluster_distance bp.
       Cluster has DSB if both strands appear, else SSB."""
    by_event = {}
    for eid, strand, cn, cause in events:
        by_event.setdefault(eid, []).append((cn, strand, cause))
    nSSB = 0; nDSB = 0; nsDSB = 0; ncDSB = 0
    for eid, dmgs in by_event.items():
        dmgs.sort(key=lambda x: x[0])
        clusters = []
        prev_cn = None
        for cn, strand, cause in dmgs:
            if not clusters or (cn - prev_cn) >= cluster_distance:
                clusters.append({'first': cn, 'left': False, 'right': False, 'dmgs': []})
            clusters[-1]['dmgs'].append((cn, strand, cause))
            if strand == 0: clusters[-1]['left'] = True
            if strand == 1: clusters[-1]['right'] = True
            prev_cn = cn
        for c in clusters:
            if c['left'] and c['right']:
                nDSB += 1
                if len(c['dmgs']) > 2: ncDSB += 1
                else: nsDSB += 1
            else:
                nSSB += 1
    return nSSB, nDSB, nsDSB, ncDSB

def parse_run_log_edep(path):
    """Return total energy deposit (eV) summed across all events from the dnadamage1 run.log.
       The log doesn't directly report this; we'll need to extract from output.root via ROOT.
       Fallback: scan log for any 'EdepTotal' lines (none in default dnadamage1)."""
    return None

def edep_from_root(rootfile):
    """Use ROOT (via pyroot or root -l -b -q TFile macro) to sum edep in ntuple_1.
       Returns total_edep_eV, total_events, n_unique_eventIDs."""
    import subprocess
    macro = f'''
{{
TFile* f = TFile::Open("{rootfile}");
TDirectoryFile* d = (TDirectoryFile*)f->Get("ntuple");
TTree* t = (TTree*)d->Get("ntuple_1");
double edep; int eid;
t->SetBranchAddress("edep", &edep);
t->SetBranchAddress("EventID", &eid);
double tot=0; std::set<int> evts;
for (long long i=0; i<t->GetEntries(); ++i) {{
  t->GetEntry(i);
  tot += edep;
  evts.insert(eid);
}}
cout << "EDEP_TOTAL_EV=" << tot << endl;
cout << "EDEP_NHITS=" << t->GetEntries() << endl;
cout << "EDEP_NEVENTS=" << evts.size() << endl;
f->Close();
}}
'''
    macro_path = rootfile + ".sumedep.C"
    with open(macro_path, "w") as fh:
        fh.write(macro)
    out = subprocess.check_output(["root", "-l", "-b", "-q", macro_path], stderr=subprocess.STDOUT).decode()
    total_eV = nhits = nevts = None
    for line in out.splitlines():
        if line.startswith("EDEP_TOTAL_EV="):
            total_eV = float(line.split("=")[1])
        elif line.startswith("EDEP_NHITS="):
            nhits = int(line.split("=")[1])
        elif line.startswith("EDEP_NEVENTS="):
            nevts = int(line.split("=")[1])
    return total_eV, nhits, nevts

def compute_yields(rundir):
    rundir = Path(rundir)
    sdd_path = rundir / "sdd_mokari.txt"
    if not sdd_path.exists():
        # fall back to default scandamages output name
        for cand in ["SDD.txt", "sdd.txt", "SDD_mokari.txt"]:
            if (rundir / cand).exists():
                sdd_path = rundir / cand
                break
    events, max_cn = parse_sdd(sdd_path)
    nSSB, nDSB, nsDSB, ncDSB = classify(events, cluster_distance=10)
    edep_eV, nhits, nevts = edep_from_root(str(rundir / "output.root"))

    # Yields: per Gy per Gbp
    total_edep_J = edep_eV * eV_to_J
    dose_Gy = total_edep_J / VOXEL_MASS_KG if VOXEL_MASS_KG > 0 else 0.0
    # DNA mass per event: max_cn bp -> max_cn / 1e9 Gbp
    n_bp_in_voxel = max_cn if max_cn > 0 else 24460  # observed dnadamage1 voxel default
    # Total DNA "exposure" = N_events * (DNA Gbp per voxel) integrated; yield convention is
    # Y = N_breaks / (dose * DNA_mass_Gbp). Since each event sees the same DNA, and dose is total:
    DNA_Gbp_per_event = n_bp_in_voxel / 1e9
    # Y_SSB = nSSB / (dose_Gy * DNA_Gbp_per_event * N_events) — but dose_Gy is total over N events;
    # if we average per-event, dose_per_event = dose_Gy / N_events, and yields cancel:
    # Y = nSSB / (dose_Gy_total * DNA_Gbp_per_event)
    # Because each event re-irradiates the same DNA volume.
    Y_SSB = nSSB / (dose_Gy * DNA_Gbp_per_event) if dose_Gy > 0 else 0.0
    Y_DSB = nDSB / (dose_Gy * DNA_Gbp_per_event) if dose_Gy > 0 else 0.0
    ratio = nSSB / nDSB if nDSB > 0 else None

    return {
        "rundir": str(rundir),
        "n_events": nevts,
        "n_hits": nhits,
        "max_copyNb_bp": max_cn,
        "n_bp_in_voxel_used": n_bp_in_voxel,
        "DNA_Gbp_per_event": DNA_Gbp_per_event,
        "voxel_mass_kg": VOXEL_MASS_KG,
        "edep_total_eV": edep_eV,
        "dose_Gy_total": dose_Gy,
        "dose_Gy_per_event": dose_Gy / nevts if nevts else None,
        "nSSB": nSSB,
        "nDSB": nDSB,
        "nsDSB": nsDSB,
        "ncDSB": ncDSB,
        "Y_SSB_per_Gy_per_Gbp": Y_SSB,
        "Y_DSB_per_Gy_per_Gbp": Y_DSB,
        "SSB_over_DSB": ratio,
    }

if __name__ == "__main__":
    rundir = sys.argv[1] if len(sys.argv) > 1 else "."
    res = compute_yields(rundir)
    print(json.dumps(res, indent=2))
