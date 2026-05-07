#!/usr/bin/env python3
"""
Efficient runner: parallelizes examples across GPUs.
Usage: python3 run_efficient.py
"""
import subprocess
import sys
import os
import time
import json

WORKDIR = '/data/stevens/projects-active/zhang2019-replication/code'

# Run tasks in parallel across GPUs
tasks = [
    ('CUDA_VISIBLE_DEVICES=0', 'example1_advection.py', 'DO'),
    ('CUDA_VISIBLE_DEVICES=1', 'example1_advection.py', 'BO'),
    ('CUDA_VISIBLE_DEVICES=2', 'example2_burgers.py', 'DO'),
    ('CUDA_VISIBLE_DEVICES=3', 'example2_burgers.py', 'BO'),
    ('CUDA_VISIBLE_DEVICES=4', 'example3_reaction_diffusion.py', 'forward'),
    ('CUDA_VISIBLE_DEVICES=5', 'example3_reaction_diffusion.py', 'inverse'),
]

procs = []
for gpu_env, script, arg in tasks:
    cmd = f'{gpu_env} python3 -u {script} {arg}'
    log_name = f'{script.replace(".py", "")}_{arg}.log'
    log_path = os.path.join(WORKDIR, '..', 'results', log_name)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    print(f"Launching: {cmd} -> {log_path}")
    log_f = open(log_path, 'w')
    p = subprocess.Popen(cmd, shell=True, stdout=log_f, stderr=subprocess.STDOUT,
                         cwd=WORKDIR)
    procs.append((p, log_f, cmd, log_path))

print(f"\n{len(procs)} tasks launched in parallel. Waiting...")

for p, log_f, cmd, log_path in procs:
    p.wait()
    log_f.close()
    status = "OK" if p.returncode == 0 else f"FAIL (rc={p.returncode})"
    print(f"  [{status}] {cmd}")
    # Print last 10 lines of log
    with open(log_path) as f:
        lines = f.readlines()
        print("  Last lines:")
        for line in lines[-10:]:
            print(f"    {line.rstrip()}")
    print()

print("All tasks complete.")
