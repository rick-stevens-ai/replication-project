#!/usr/bin/env python3
"""Minimal Affymetrix Command Console (AGCC, CEL v1 / Calvin) header sniffer.

We do NOT decode probe intensities here -- full RMA + limma DE requires
oligo/affy/limma from Bioconductor, which we run on uicgpu (see RUN_PLAN.md).

This script just verifies that downloaded CELs are well-formed AGCC v1 files
with the expected magic, version, and array-design metadata. That is enough
of a 'smoke' to confirm the artifact harvest is real and the upstream RMA
pipeline is feasible from the public ArrayExpress raw data.

References:
  Affymetrix Command Console File Format spec
  https://media.affymetrix.com/support/developer/powertools/changelog/gcos-agcc/cel.html
"""
from __future__ import annotations
import struct
import sys
from pathlib import Path


def read_string(f) -> str:
    n = struct.unpack(">i", f.read(4))[0]
    if n <= 0:
        return ""
    return f.read(n).decode("ascii", errors="replace")


def read_wstring(f) -> str:
    n = struct.unpack(">i", f.read(4))[0]
    if n <= 0:
        return ""
    return f.read(n * 2).decode("utf-16-be", errors="replace")


def read_value_type_pair(f) -> tuple[str, bytes, str]:
    name = read_wstring(f)
    val_len = struct.unpack(">i", f.read(4))[0]
    val = f.read(val_len)
    mime = read_wstring(f)
    return name, val, mime


def decode_value(val: bytes, mime: str) -> object:
    try:
        if "text/plain" in mime:
            return val.decode("utf-16-be", errors="replace").rstrip("\x00")
        if "text/ascii" in mime:
            return val.decode("ascii", errors="replace").rstrip("\x00")
        if "x-calvin-integer-32" in mime:
            return struct.unpack(">i", val)[0]
        if "x-calvin-unsigned-integer-32" in mime:
            return struct.unpack(">I", val)[0]
        if "x-calvin-integer-16" in mime:
            return struct.unpack(">h", val)[0]
        if "x-calvin-integer-8" in mime:
            return struct.unpack(">b", val)[0]
        if "x-calvin-float" in mime:
            return struct.unpack(">f", val)[0]
        return val.hex()
    except Exception as e:
        return f"<decode-err {e}>"


def sniff(path: Path) -> dict:
    with path.open("rb") as f:
        magic, version = struct.unpack(">BB", f.read(2))
        if magic != 59:  # 0x3B
            raise ValueError(f"{path}: not a Calvin/AGCC CEL (magic={magic})")
        n_groups = struct.unpack(">i", f.read(4))[0]
        first_group_pos = struct.unpack(">I", f.read(4))[0]

        # DataHeader
        data_type_id = read_string(f)
        file_id = read_string(f)
        timestamp = read_wstring(f)
        locale = read_wstring(f)
        n_params = struct.unpack(">i", f.read(4))[0]
        params = {}
        for _ in range(n_params):
            name, val, mime = read_value_type_pair(f)
            params[name] = decode_value(val, mime)

        return {
            "file": str(path),
            "size_bytes": path.stat().st_size,
            "magic": magic,
            "version": version,
            "n_data_groups": n_groups,
            "first_group_pos": first_group_pos,
            "data_type_id": data_type_id,
            "file_id": file_id[:80],
            "timestamp": timestamp,
            "locale": locale,
            "n_header_params": n_params,
            "array_type": params.get("affymetrix-array-type")
            or params.get("affymetrix-cel-array-type"),
            "algorithm": params.get("affymetrix-algorithm-name"),
            "scanner_id": params.get("affymetrix-scanner-id"),
            "scan_date": params.get("affymetrix-scan-date"),
            "n_rows": params.get("affymetrix-cel-rows"),
            "n_cols": params.get("affymetrix-cel-cols"),
        }


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: cel_header_sniff.py CEL [CEL ...]", file=sys.stderr)
        return 2

    paths = [Path(p) for p in sys.argv[1:]]
    results = [sniff(p) for p in paths]

    # Pretty table
    cols = [
        "file",
        "size_bytes",
        "array_type",
        "n_rows",
        "n_cols",
        "scan_date",
        "scanner_id",
    ]
    widths = {c: max(len(c), max(len(str(r.get(c, ""))) for r in results)) for c in cols}
    line = " | ".join(c.ljust(widths[c]) for c in cols)
    print(line)
    print("-" * len(line))
    for r in results:
        r["file"] = Path(r["file"]).name
        widths["file"] = max(widths["file"], len(r["file"]))
        print(" | ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols))

    # Sanity assertions
    array_types = {r["array_type"] for r in results}
    if len(array_types) != 1:
        print(f"\nWARN: heterogeneous array types: {array_types}", file=sys.stderr)
        return 1
    print(f"\nOK: all {len(results)} CELs share array_type={array_types.pop()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
