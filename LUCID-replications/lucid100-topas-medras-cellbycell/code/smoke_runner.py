import sys, os, time
sys.path.insert(0, '.')
from main_assembler import main
for cfg, outdir in [
    ("alpha_config.json",   "Alpha_Simulation"),
    ("proton_config.json",  "Proton_Simulation"),
    ("electron_config_time.json", "Electron_Sim"),
]:
    print(f"\n===== {cfg} =====")
    # clear prior output
    if os.path.isdir(outdir):
        for f in os.listdir(outdir):
            p = os.path.join(outdir, f)
            if os.path.isfile(p): os.remove(p)
    t0 = time.time()
    main(cfg)
    print(f"--> elapsed {time.time()-t0:.2f}s; produced {len(os.listdir(outdir))} files in {outdir}")
