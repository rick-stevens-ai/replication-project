#!/usr/bin/env python3
"""Parse Table 3 (LDFR 4x0.5 Gy vs single-dose 2 Gy ± CPL/PTX chemopotentiation
clonogenic SF for 40 HNSCC fibroblast lines) into a tidy CSV.

Output columns:
  patient_id, patient_label, hrs_status, condition, SF_mean, SF_sem
Conditions: 2Gy, 4x0.5Gy, CPL, CPL+2Gy, CPL+4x0.5Gy, PTX, PTX+2Gy, PTX+4x0.5Gy

Source: artifacts/europepmc_fullText.xml (Table 3)
"""
from __future__ import annotations
import csv, re, sys
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent.parent
XML = HERE / 'artifacts' / 'europepmc_fullText.xml'
OUT = HERE / 'artifacts' / 'table3_chemopotentiation.csv'

CONDITIONS = ['2Gy', '4x0.5Gy', 'CPL', 'CPL+2Gy', 'CPL+4x0.5Gy', 'PTX', 'PTX+2Gy', 'PTX+4x0.5Gy']


def text_of(el):
    return ''.join(el.itertext())


def parse_cell(s):
    if s is None:
        return None
    s = s.replace('\xa0', ' ').strip()
    if s == '-' or s == '':
        return None
    m = re.match(r'^([0-9]*\.?[0-9]+)\s*±\s*([0-9]*\.?[0-9]+)$', s)
    return (float(m.group(1)), float(m.group(2))) if m else None


def main():
    root = ET.parse(XML).getroot()
    tables = list(root.iter('table-wrap'))
    if len(tables) < 3:
        print('ERROR: <3 tables', file=sys.stderr); return 1
    tbl = tables[2].find('table')
    rows = []
    for tr in tbl.iter('tr'):
        cells = [text_of(c).strip() for c in tr if c.tag in ('td', 'th')]
        if not cells:
            continue
        label = cells[0].rstrip('.').strip()
        m = re.match(r'^(H?)(\d+)$', label)
        if not m:
            continue
        hrs = 'HRS' if m.group(1) == 'H' else 'NON'
        pid = int(m.group(2))
        data_cells = cells[1:1 + len(CONDITIONS)]
        if len(data_cells) != len(CONDITIONS):
            print(f'warn pid={pid} ncells={len(data_cells)}', file=sys.stderr)
            continue
        for cond, cell in zip(CONDITIONS, data_cells):
            parsed = parse_cell(cell)
            if parsed is None:
                rows.append({'patient_id': pid, 'patient_label': label, 'hrs_status': hrs,
                             'condition': cond, 'SF_mean': '', 'SF_sem': ''})
            else:
                rows.append({'patient_id': pid, 'patient_label': label, 'hrs_status': hrs,
                             'condition': cond, 'SF_mean': parsed[0], 'SF_sem': parsed[1]})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['patient_id', 'patient_label', 'hrs_status', 'condition', 'SF_mean', 'SF_sem'])
        w.writeheader(); w.writerows(rows)
    npat = len({r['patient_id'] for r in rows})
    nnan = sum(1 for r in rows if r['SF_mean'] == '')
    print(f'wrote {OUT} rows={len(rows)} patients={npat} blanks={nnan}')


if __name__ == '__main__':
    sys.exit(main())
