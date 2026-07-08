#!/usr/bin/env python3
"""score_unscored_3judge.py — 3-LLM-judge replication scorer.

Reads SCORE_TARGETS_LIST.txt (relative paths under REPLICATE-PROJECT root),
locates each replication's REPORT, queries 3 FREE Argo judges, takes the
median/majority, and appends rows to an additions CSV.

Standing policy (Rick, 2026-06-23):
  - 3-judge LLM scoring (no regex on author self-scores).
  - FREE Argo proxy only (http://localhost:44497/v1, key=stevens).
  - Honor 429/Retry-After; small concurrency.
  - Checkpoint additions CSV incrementally so partial work survives.
"""
from __future__ import annotations
import argparse
import csv
import json
import os
import re
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from statistics import median
from collections import Counter

import requests

ROOT = Path(os.path.expanduser("~/Dropbox/REPLICATE-PROJECT"))
TARGETS_FILE = ROOT / "SCORE_TARGETS_LIST.txt"
ADDITIONS_CSV = ROOT / "MASTER_SCORES_2026-06-23_additions.csv"

ARGO_URL = "http://localhost:44497/v1/chat/completions"
ARGO_KEY = "stevens"
JUDGES = ["argo:claude-sonnet-4.6", "argo:claude-opus-4.7", "argo:gpt-5"]

CSV_COLUMNS = [
    "paper_id", "verdict", "coverage_10", "agreement_10",
    "tools_top5", "datasets", "hardware",
    "runtime_gpu_h", "runtime_cpu_h", "repo",
    "judge_note", "judge_panel_json",
]

VALID_VERDICTS = ["REPLICATED", "PARTIAL", "SPOT-CHECK", "NO-GO", "FAILED"]
# Conservative ordering: most conservative = highest index (used for tie-break)
VERDICT_SEVERITY = {
    "REPLICATED": 0,
    "PARTIAL": 1,
    "SPOT-CHECK": 2,
    "NO-GO": 3,
    "FAILED": 4,
}

MAX_REPORT_CHARS = 60_000  # head+tail trim for very large reports

RUBRIC_PROMPT = """You are scoring a scientific paper REPLICATION REPORT for a curated benchmark.

Return STRICT JSON ONLY (no markdown fences, no prose outside JSON) with keys:
{{"coverage_10": <int 0-10>, "agreement_10": <int 0-10>, "verdict": "<one of REPLICATED|PARTIAL|SPOT-CHECK|NO-GO|FAILED>", "note": "<one or two sentences>"}}

Rubric (apply to the REPORT TEXT below, not your priors about the paper):
- coverage_10: How much of the paper's scope was actually attempted in this replication?
  10 = every major claim/figure/experiment attempted; 5 = roughly half; 0 = nothing.
- agreement_10: Of what WAS tested, how well does it match the paper's reported results?
  10 = bit-exact or numerically within tight tolerance on all tested items;
  5 = mixed agreement; 0 = could not test or strongly contradicts.
- verdict:
  - REPLICATED: broad coverage AND high agreement on what was tested.
  - PARTIAL: meaningful subset reproduced, some gaps or disagreements.
  - SPOT-CHECK: only one or a few claims tested, but those checked out.
  - NO-GO: could not attempt due to missing data/code/hardware, no real reproduction work done.
  - FAILED: attempt was made but did not reproduce, OR the report is a stub/empty/placeholder with no substantive content.
- note: one or two sentences citing concrete evidence from the report (figures reproduced, metrics, blockers).

Ground EVERY judgment in the actual report text. If the report contains author self-assigned scores, IGNORE those — re-score independently from the substantive content. If the report is essentially empty or a template, set coverage_10=0 and verdict=FAILED.

PAPER ID: {paper_id}

REPORT TEXT (may be truncated):
---
{report_text}
---

Return ONLY the JSON object."""


# ---------- I/O helpers ----------

def find_report(rep_dir: Path) -> tuple[Path | None, str]:
    """Locate the canonical REPORT for a replication directory.

    Preference order:
      1. <dir>/REPORT.md  (or any *REPORT*.md at top level)
      2. <dir>/report/REPORT.md
      3. <dir>/report/*.md (largest)
      4. <dir>/*.md (largest)
    """
    if not rep_dir.exists():
        return None, "missing-dir"
    # 1. top-level REPORT*.md
    top = sorted(rep_dir.glob("*REPORT*.md"))
    if top:
        return top[0], "top-REPORT"
    # 2. report/REPORT.md
    for cand in [rep_dir / "report" / "REPORT.md", rep_dir / "report" / "report.md"]:
        if cand.exists():
            return cand, "report-REPORT"
    # 3. report/*.md largest (prefer *REPORT* if present)
    report_dir = rep_dir / "report"
    if report_dir.exists():
        mds = list(report_dir.glob("*.md"))
        rep_named = [m for m in mds if "REPORT" in m.name.upper()]
        pool = rep_named or mds
        if pool:
            best = max(pool, key=lambda p: p.stat().st_size)
            return best, f"report-dir:{best.name}"
    # 4. top-level *.md largest
    mds = [m for m in rep_dir.glob("*.md") if m.name.upper() not in {"README.MD"}]
    if mds:
        best = max(mds, key=lambda p: p.stat().st_size)
        return best, f"top-md:{best.name}"
    # 5. fallback: any *.md anywhere (shallow)
    mds = list(rep_dir.glob("**/*.md"))
    if mds:
        best = max(mds, key=lambda p: p.stat().st_size)
        return best, f"deep-md:{best.relative_to(rep_dir)}"
    return None, "no-md"


def read_report(path: Path, limit: int = MAX_REPORT_CHARS) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"[ERROR reading report: {e}]"
    if len(text) <= limit:
        return text
    head = text[: int(limit * 0.7)]
    tail = text[-int(limit * 0.3) :]
    return head + "\n\n[... middle truncated to fit judge window ...]\n\n" + tail


# ---------- Light keyword extraction (NOT judged) ----------

TOOL_PATTERNS = [
    "Python", "R ", "Julia", "C++", "Fortran", "MATLAB",
    "PyTorch", "TensorFlow", "JAX", "scikit-learn", "scikit-image",
    "NumPy", "SciPy", "pandas", "matplotlib", "seaborn",
    "RDKit", "Biopython", "BLAST", "DIAMOND", "MMseqs2", "MAFFT", "MUSCLE",
    "PROKKA", "Prokka", "BUSCO", "QUAST", "SPAdes",
    "TOPAS", "Geant4", "Geant", "MEDRAS", "MCNP",
    "Quantum ESPRESSO", "VASP", "LAMMPS", "GROMACS", "OpenMM",
    "Snakemake", "Nextflow", "Docker", "Singularity",
    "NetworkX", "GraphBLAS",
    "Claude", "GPT-4", "GPT-5", "Anthropic", "OpenAI",
    "BV-BRC", "BVBRC", "PATRIC",
]

DATASET_PATTERNS = [
    r"PRJNA\d+", r"GSE\d+", r"PDB\s?\d[A-Z0-9]{3}", r"NCBI",
    r"UniProt", r"Ensembl", r"Refseq", r"RefSeq",
    r"BV-?BRC", r"PATRIC", r"KEGG", r"GenBank",
]

HW_PATTERNS = [
    "A100", "H100", "H200", "V100", "T4", "MI250", "MI300", "PVC",
    "GPU", "TPU", "CPU-only", "uicgpu", "Aurora", "Polaris", "Sophia",
    "Spark", "DGX",
]

def extract_light(text: str) -> dict[str, str]:
    out = {"tools_top5": "", "datasets": "", "hardware": ""}
    if not text:
        return out
    low = text
    found_tools = []
    for tok in TOOL_PATTERNS:
        if tok.lower() in low.lower() and tok not in found_tools:
            found_tools.append(tok)
        if len(found_tools) >= 5:
            break
    out["tools_top5"] = ", ".join(found_tools[:5])
    ds = set()
    for pat in DATASET_PATTERNS:
        for m in re.findall(pat, text):
            ds.add(m if isinstance(m, str) else " ".join(m))
        if len(ds) >= 8:
            break
    out["datasets"] = ", ".join(sorted(ds)[:8])
    hw = []
    for tok in HW_PATTERNS:
        if tok.lower() in low.lower() and tok not in hw:
            hw.append(tok)
        if len(hw) >= 4:
            break
    out["hardware"] = ", ".join(hw)
    return out


# ---------- Argo judge call ----------

_session_lock = threading.Lock()


def call_judge(model: str, paper_id: str, report_text: str, max_retries: int = 5) -> dict:
    """Call one Argo judge. Returns dict with parsed score or error info.

    Always returns a dict; never raises.
    """
    prompt = RUBRIC_PROMPT.format(paper_id=paper_id, report_text=report_text)
    headers = {"Authorization": f"Bearer {ARGO_KEY}", "Content-Type": "application/json"}
    is_gpt5 = "gpt-5" in model
    # gpt-5 burns ~128-512 tokens on hidden reasoning; need extra headroom for actual JSON.
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4000 if is_gpt5 else 800,
    }
    # gpt-5 family rejects temperature override (only default 1 allowed); Claude accepts 0.
    if not is_gpt5:
        payload["temperature"] = 0
    backoff = 4.0
    last_err = None
    for attempt in range(max_retries):
        try:
            r = requests.post(ARGO_URL, headers=headers, json=payload, timeout=180)
        except Exception as e:
            last_err = f"net:{e}"
            time.sleep(backoff)
            backoff = min(backoff * 1.6, 30)
            continue
        if r.status_code == 429:
            ra = r.headers.get("Retry-After")
            try:
                wait = float(ra) if ra else backoff
            except Exception:
                wait = backoff
            time.sleep(min(wait, 60))
            backoff = min(backoff * 1.6, 60)
            last_err = "429"
            continue
        if r.status_code >= 500:
            last_err = f"http:{r.status_code}"
            time.sleep(backoff)
            backoff = min(backoff * 1.6, 30)
            continue
        if r.status_code != 200:
            return {"judge": model, "error": f"http:{r.status_code}", "body": r.text[:300]}
        try:
            content = r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return {"judge": model, "error": f"parse_resp:{e}", "body": r.text[:300]}
        # Strip code fences if present
        c = content.strip()
        if c.startswith("```"):
            c = re.sub(r"^```[a-zA-Z]*", "", c).strip()
            if c.endswith("```"):
                c = c[:-3].strip()
        # Try direct parse; else extract first {...}
        try:
            parsed = json.loads(c)
        except Exception:
            m = re.search(r"\{.*\}", c, re.DOTALL)
            if not m:
                return {"judge": model, "error": "no_json", "raw": content[:400]}
            try:
                parsed = json.loads(m.group(0))
            except Exception as e:
                return {"judge": model, "error": f"json:{e}", "raw": content[:400]}
        # Normalize
        try:
            cov = int(parsed.get("coverage_10"))
            agr = int(parsed.get("agreement_10"))
            verdict = str(parsed.get("verdict", "")).upper().strip()
            note = str(parsed.get("note", "")).strip()
        except Exception as e:
            return {"judge": model, "error": f"norm:{e}", "raw": content[:400]}
        if verdict not in VALID_VERDICTS:
            # try to coerce
            up = verdict.replace("_", "-").replace(" ", "-")
            if up in VALID_VERDICTS:
                verdict = up
            elif "REPLIC" in verdict:
                verdict = "REPLICATED"
            elif "PARTIAL" in verdict:
                verdict = "PARTIAL"
            elif "SPOT" in verdict:
                verdict = "SPOT-CHECK"
            elif "NO" in verdict and "GO" in verdict:
                verdict = "NO-GO"
            else:
                verdict = "FAILED"
        cov = max(0, min(10, cov))
        agr = max(0, min(10, agr))
        return {
            "judge": model,
            "coverage_10": cov,
            "agreement_10": agr,
            "verdict": verdict,
            "note": note[:500],
        }
    return {"judge": model, "error": f"giveup:{last_err}"}


def aggregate_panel(panel: list[dict]) -> tuple[int | None, int | None, str | None]:
    """Median coverage/agreement, majority verdict (tie -> more conservative)."""
    covs = [p["coverage_10"] for p in panel if "coverage_10" in p]
    agrs = [p["agreement_10"] for p in panel if "agreement_10" in p]
    verds = [p["verdict"] for p in panel if "verdict" in p]
    if not covs or not agrs or not verds:
        return None, None, None
    cov = int(round(median(covs)))
    agr = int(round(median(agrs)))
    counts = Counter(verds)
    top = counts.most_common()
    top_n = top[0][1]
    tied = [v for v, n in top if n == top_n]
    if len(tied) == 1:
        verdict = tied[0]
    else:
        # Most conservative
        verdict = max(tied, key=lambda v: VERDICT_SEVERITY.get(v, 99))
    return cov, agr, verdict


# ---------- Per-paper processing ----------

def score_one(paper_id: str) -> dict:
    rep_dir = ROOT / paper_id
    report_path, how = find_report(rep_dir)
    if not report_path:
        return {
            "paper_id": paper_id,
            "error": f"no_report:{how}",
            "verdict": "FAILED",
            "coverage_10": 0,
            "agreement_10": 0,
            "tools_top5": "",
            "datasets": "",
            "hardware": "",
            "runtime_gpu_h": "",
            "runtime_cpu_h": "",
            "repo": "",
            "judge_note": f"NO REPORT FOUND ({how}); marked FAILED for scoring registry.",
            "judge_panel_json": json.dumps({"error": f"no_report:{how}"}),
        }
    text = read_report(report_path)
    if not text or text.strip() == "" or len(text.strip()) < 80:
        light = extract_light(text)
        return {
            "paper_id": paper_id,
            "error": "empty_report",
            "verdict": "FAILED",
            "coverage_10": 0,
            "agreement_10": 0,
            "tools_top5": light["tools_top5"],
            "datasets": light["datasets"],
            "hardware": light["hardware"],
            "runtime_gpu_h": "",
            "runtime_cpu_h": "",
            "repo": str(report_path.relative_to(ROOT)),
            "judge_note": f"Report at {report_path.name} is empty/stub ({len(text)} chars); FAILED.",
            "judge_panel_json": json.dumps({"error": "empty_report", "report": str(report_path.relative_to(ROOT)), "chars": len(text)}),
        }
    panel = []
    for j in JUDGES:
        result = call_judge(j, paper_id, text)
        panel.append(result)
    cov, agr, verdict = aggregate_panel(panel)
    light = extract_light(text)
    if cov is None:
        # All judges errored — record failure
        return {
            "paper_id": paper_id,
            "error": "all_judges_failed",
            "verdict": "FAILED",
            "coverage_10": 0,
            "agreement_10": 0,
            "tools_top5": light["tools_top5"],
            "datasets": light["datasets"],
            "hardware": light["hardware"],
            "runtime_gpu_h": "",
            "runtime_cpu_h": "",
            "repo": str(report_path.relative_to(ROOT)),
            "judge_note": "All 3 judges errored or returned unparseable output; marked FAILED.",
            "judge_panel_json": json.dumps({"panel": panel, "report": str(report_path.relative_to(ROOT))}),
        }
    # Compose judge_note from the median-most agreeable judge's note (prefer non-erroring)
    notes = [p.get("note", "") for p in panel if p.get("note")]
    composite = " | ".join(f"[{p['judge'].split(':')[-1]}] {p.get('note','')}" for p in panel if "note" in p)
    return {
        "paper_id": paper_id,
        "verdict": verdict,
        "coverage_10": cov,
        "agreement_10": agr,
        "tools_top5": light["tools_top5"],
        "datasets": light["datasets"],
        "hardware": light["hardware"],
        "runtime_gpu_h": "",
        "runtime_cpu_h": "",
        "repo": str(report_path.relative_to(ROOT)),
        "judge_note": composite[:1200],
        "judge_panel_json": json.dumps({"panel": panel, "report": str(report_path.relative_to(ROOT))}),
    }


# ---------- Driver ----------

def load_targets() -> list[str]:
    raw = TARGETS_FILE.read_text(encoding="utf-8").splitlines()
    return [ln.strip() for ln in raw if ln.strip() and not ln.startswith("#")]


def load_done(csv_path: Path) -> set[str]:
    if not csv_path.exists():
        return set()
    done = set()
    with csv_path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("paper_id"):
                done.add(row["paper_id"])
    return done


def write_header_if_needed(csv_path: Path):
    if csv_path.exists() and csv_path.stat().st_size > 0:
        return
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        w.writeheader()


_csv_lock = threading.Lock()


def append_row(csv_path: Path, row: dict):
    with _csv_lock:
        with csv_path.open("a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
            w.writerow({k: row.get(k, "") for k in CSV_COLUMNS})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--concurrency", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0, help="0=all")
    ap.add_argument("--resume", action="store_true", default=True)
    ap.add_argument("--csv", type=Path, default=ADDITIONS_CSV)
    args = ap.parse_args()

    targets = load_targets()
    if args.limit:
        targets = targets[: args.limit]
    write_header_if_needed(args.csv)
    done = load_done(args.csv) if args.resume else set()
    todo = [t for t in targets if t not in done]
    print(f"[score] targets={len(targets)} done={len(done)} todo={len(todo)} csv={args.csv}")
    t0 = time.time()
    completed = 0
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futs = {ex.submit(score_one, t): t for t in todo}
        for fut in as_completed(futs):
            t = futs[fut]
            try:
                row = fut.result()
            except Exception as e:
                row = {
                    "paper_id": t,
                    "verdict": "FAILED",
                    "coverage_10": 0,
                    "agreement_10": 0,
                    "tools_top5": "",
                    "datasets": "",
                    "hardware": "",
                    "runtime_gpu_h": "",
                    "runtime_cpu_h": "",
                    "repo": "",
                    "judge_note": f"driver exception: {e}",
                    "judge_panel_json": json.dumps({"error": f"driver:{e}"}),
                }
            append_row(args.csv, row)
            completed += 1
            err = row.get("error", "")
            print(f"[{completed}/{len(todo)}] {t} -> {row.get('verdict')} cov={row.get('coverage_10')} agr={row.get('agreement_10')} {('('+err+')') if err else ''}", flush=True)
    dt = time.time() - t0
    print(f"[score] done in {dt/60:.1f} min")


if __name__ == "__main__":
    main()
