#!/usr/bin/env python3
"""Parse Table 1 (single-dose clonogenic SF for 40 HNSCC patient fibroblast lines)
from the JATS XML extracted from EuropePMC and emit a tidy CSV.

Source: artifacts/europepmc_fullText.xml (PMC13027110)
Output: artifacts/table1_singledose_SF.csv

Columns: patient_label, hrs_status (HRS|NON), dose_Gy, SF_mean, SF_sem
Doses (Gy): 0.1, 0.15, 0.2, 0.25, 0.3, 0.5, 1, 2, 4
"""
from __future__ import annotations
import csv, re, sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
XML = HERE / "artifacts" / "europepmc_fullText.xml"
OUT = HERE / "artifacts" / "table1_singledose_SF.csv"

DOSES = [0.1, 0.15, 0.2, 0.25, 0.3, 0.5, 1.0, 2.0, 4.0]


def text_of(el) -> str:
    return ''.join(el.itertext())


def parse_cell(s: str) -> tuple[float, float] | None:
    """Parse strings like '0.86 ± 0.01' (also tolerates spacing/typos like '0.41± 0.03')."""
    if s is None:
        return None
    s = s.replace('\xa0', ' ').strip()
    m = re.match(r'^([0-9]*\.?[0-9]+)\s*[±+\-]\s*([0-9]*\.?[0-9]+)$', s)
    if not m:
        # tolerate joint form '0.41± 0.03'
        m = re.match(r'^([0-9]*\.?[0-9]+)\s*±\s*([0-9]*\.?[0-9]+)$', s.replace('+/-', '±'))
    if not m:
        return None
    return float(m.group(1)), float(m.group(2))


def main() -> int:
    root = ET.parse(XML).getroot()
    rows: list[dict] = []
    tables = list(root.iter('table-wrap'))
    if len(tables) < 1:
        print('ERROR: no tables in XML', file=sys.stderr)
        return 1
    tbl = tables[0].find('table')
    for tr in tbl.iter('tr'):
        cells = [text_of(c).strip() for c in tr if c.tag in ('td', 'th')]
        if not cells:
            continue
        label = cells[0].rstrip('.').strip()
        # Skip the header row
        if re.fullmatch(r'PatientsNo\.?', label):
            continue
        # Patient labels are '1'..'40' optionally prefixed with 'H'
        m = re.match(r'^(H?)(\d+)$', label)
        if not m:
            continue
        hrs = 'HRS' if m.group(1) == 'H' else 'NON'
        pid = int(m.group(2))
        # 9 dose cells expected after the patient label
        data_cells = cells[1:1 + len(DOSES)]
        if len(data_cells) != len(DOSES):
            print(f'warn: patient {label} has {len(data_cells)} dose cells', file=sys.stderr)
            continue
        for d, cell in zip(DOSES, data_cells):
            parsed = parse_cell(cell)
            if parsed is None:
                print(f'warn: unparseable cell pid={pid} dose={d}: {cell!r}', file=sys.stderr)
                continue
            mean, sem = parsed
            rows.append({
                'patient_id': pid,
                'patient_label': label,
                'hrs_status': hrs,
                'dose_Gy': d,
                'SF_mean': mean,
                'SF_sem': sem,
            })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['patient_id', 'patient_label', 'hrs_status', 'dose_Gy', 'SF_mean', 'SF_sem'])
        w.writeheader()
        w.writerows(rows)
    print(f'wrote {OUT} rows={len(rows)} patients={len({r["patient_id"] for r in rows})} '
          f'HRS+={len({r["patient_id"] for r in rows if r["hrs_status"] == "HRS"})}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
