#!/usr/bin/env python3
from pathlib import Path
import csv, math
p=Path(__file__).with_name("score_curve_checkpoints.tsv")
rows=list(csv.DictReader(p.open(), delimiter="	"))

def num(x):
    try:
        s=str(x).strip().replace('~','')
        if not s or s.startswith('TBD'): return None
        return float(s.split('_')[0])
    except Exception:
        return None
print(f"iterations	{len(rows)}")
for r in rows:
    cov=num(r.get('coverage_delta'))
    acc=num(r.get('accuracy_delta'))
    tok=num(r.get('tokens_total'))
    cpu=num(r.get('cpu_core_hours'))
    gpu=num(r.get('gpu_hours'))
    print("
"+r['iteration_id'])
    print("scope:", r['scope'])
    print("action:", r['action_type'])
    print("output:", r['output_state'])
    if cov is not None and tok:
        print("coverage_gain_per_100k_tokens", cov/(tok/100000))
    if acc is not None and tok:
        print("accuracy_gain_per_100k_tokens", acc/(tok/100000))
    if cov is not None and cpu:
        print("coverage_gain_per_cpu_hour", cov/cpu)
    if acc is not None and cpu:
        print("accuracy_gain_per_cpu_hour", acc/cpu)
    if cov is not None and gpu:
        print("coverage_gain_per_gpu_hour", cov/gpu)
    if acc is not None and gpu:
        print("accuracy_gain_per_gpu_hour", acc/gpu)
    print("tokens_total", r.get('tokens_total'))
    print("cpu_core_hours", r.get('cpu_core_hours'))
    print("gpu_hours", r.get('gpu_hours'))
