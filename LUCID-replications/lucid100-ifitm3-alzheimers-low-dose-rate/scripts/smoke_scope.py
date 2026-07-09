#!/usr/bin/env python3
"""Smoke script for LUCID100 slot 31 — re-verifies that the paper is
still paywalled and supplement-free. Exits non-zero if anything has
flipped (paper becomes OA, gains a PMC mirror, or registers a
supplement), so this row can be re-evaluated.

Usage:
    python3 scripts/smoke_scope.py
"""

import json
import subprocess
import sys
import urllib.request

DOI = "10.1080/09553002.2023.2211142"
PMID = "37162420"


def get_s2_key() -> str | None:
    try:
        out = subprocess.run(
            ["security", "find-generic-password",
             "-a", "rick-stevens-ai",
             "-s", "semantic-scholar-api-key", "-w"],
            check=True, capture_output=True, text=True,
        )
        return out.stdout.strip()
    except Exception:
        return None


def http_json(url: str, headers: dict | None = None) -> dict:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def main() -> int:
    failures: list[str] = []

    # 1. Unpaywall
    up = http_json(f"https://api.unpaywall.org/v2/{DOI}?email=rick.stevens.ai@anl.gov")
    print(f"[unpaywall] is_oa={up.get('is_oa')!r} status={up.get('oa_status')!r}")
    if up.get("is_oa"):
        failures.append("Unpaywall now reports is_oa=True; full text may be available.")

    # 2. EuropePMC
    epmc = http_json(
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
        f"query=EXT_ID:{PMID}%20AND%20SRC:MED&format=json&resultType=core"
    )
    results = epmc.get("resultList", {}).get("result", [])
    if not results:
        failures.append("EuropePMC returned no record for the PMID.")
    else:
        rec = results[0]
        print(
            f"[europepmc] inPMC={rec.get('inPMC')!r} "
            f"hasPDF={rec.get('hasPDF')!r} "
            f"hasSuppl={rec.get('hasSuppl')!r} "
            f"isOpenAccess={rec.get('isOpenAccess')!r}"
        )
        if rec.get("inPMC") == "Y":
            failures.append("EuropePMC now shows inPMC=Y; full text mirrored in PMC.")
        if rec.get("hasSuppl") == "Y":
            failures.append("EuropePMC now lists supplementary material.")

    # 3. Semantic Scholar (best-effort; rate-limit tolerant)
    key = get_s2_key()
    headers = {"x-api-key": key} if key else {}
    try:
        s2 = http_json(
            f"https://api.semanticscholar.org/graph/v1/paper/DOI:{DOI}"
            "?fields=title,openAccessPdf,externalIds",
            headers=headers,
        )
        oa = (s2.get("openAccessPdf") or {}).get("status")
        print(f"[s2] openAccessPdf.status={oa!r} title={s2.get('title')!r}")
        if oa and oa != "CLOSED":
            failures.append(f"Semantic Scholar openAccessPdf.status flipped to {oa!r}.")
    except urllib.error.HTTPError as e:
        # Don't fail the smoke run for transient rate limits / S2 outages.
        print(f"[s2] HTTPError {e.code}: skipped (best-effort)")
    except Exception as e:
        print(f"[s2] error: {e!r}: skipped (best-effort)")

    print()
    if failures:
        print("STATUS-CHANGE DETECTED — re-evaluate this row:")
        for f in failures:
            print("  *", f)
        return 1

    print("STATUS UNCHANGED — paper remains closed, no PMC mirror, no supplement. NO-GO stands.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
