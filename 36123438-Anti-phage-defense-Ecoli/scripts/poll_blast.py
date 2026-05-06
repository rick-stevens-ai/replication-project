#!/usr/bin/env python3
"""Poll NCBI BLAST RIDs and retrieve results when ready."""
import json, requests, time, os, sys, xml.etree.ElementTree as ET

BASEDIR = os.path.expanduser("~/Dropbox/REPLICATE-PROJECT/36123438-Anti-phage-defense-Ecoli")

with open(os.path.join(BASEDIR, "data/blast_rids.json")) as f:
    rids = json.load(f)

results_dir = os.path.join(BASEDIR, "analysis/blast_results")
os.makedirs(results_dir, exist_ok=True)

# Check which ones we already have
already_done = set()
for fname in os.listdir(results_dir):
    if fname.endswith(".xml"):
        already_done.add(fname.replace(".xml", "").replace("_", "-"))

status_counts = {"READY": 0, "WAITING": 0, "EXPIRED": 0}

for sys_name in sorted(rids.keys()):
    safe_name = sys_name.replace("-", "_")
    if sys_name in already_done or safe_name in already_done:
        print(f"{sys_name}: ALREADY RETRIEVED")
        status_counts["READY"] += 1
        continue
    
    rid = rids[sys_name]["rid"]
    try:
        r = requests.get(
            f"https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&FORMAT_OBJECT=SearchInfo&RID={rid}",
            timeout=30
        )
        if "Status=READY" in r.text:
            status = "READY"
            status_counts["READY"] += 1
            # Retrieve results as tabular
            print(f"{sys_name}: READY — retrieving...")
            r2 = requests.get(
                f"https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&FORMAT_TYPE=XML&RID={rid}",
                timeout=120
            )
            outfile = os.path.join(results_dir, f"{safe_name}.xml")
            with open(outfile, "w") as out:
                out.write(r2.text)
            
            # Also get tabular
            r3 = requests.get(
                f"https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&FORMAT_TYPE=Tabular&RID={rid}",
                timeout=120
            )
            outfile_tab = os.path.join(results_dir, f"{safe_name}.tab")
            with open(outfile_tab, "w") as out:
                out.write(r3.text)
            print(f"  Saved to {outfile}")
            
        elif "Status=WAITING" in r.text:
            status = "WAITING"
            status_counts["WAITING"] += 1
        elif "Status=UNKNOWN" in r.text:
            status = "EXPIRED"
            status_counts["EXPIRED"] += 1
        else:
            status = "OTHER"
            status_counts.setdefault("OTHER", 0)
            status_counts["OTHER"] = status_counts.get("OTHER", 0) + 1
        
        if status != "READY":
            print(f"{sys_name}: {status}")
    except Exception as e:
        print(f"{sys_name}: ERROR - {e}")
    
    time.sleep(1)

print(f"\nSummary: {status_counts}")
