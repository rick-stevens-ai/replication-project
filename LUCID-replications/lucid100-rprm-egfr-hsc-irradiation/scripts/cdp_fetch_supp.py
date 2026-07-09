#!/usr/bin/env python3
"""Fetch PMC9804513 supplementary files through the already-running Chrome
controlled by OpenClaw browser tool. PMC requires a proof-of-work cookie
that the live Chrome session already holds; we re-use it.

Strategy: connect to Chrome's CDP page websocket, call Runtime.evaluate
to fetch each supp URL with credentials, return as base64 in slices small
enough to fit in a CDP response (~1MB safe), reassemble + write to disk.
"""

import base64
import json
import os
import sys
import urllib.request
from websockets.sync.client import connect

CDP_HTTP = "http://127.0.0.1:18800"
ARTICLE_URL_SUFFIX = "PMC9804513/"
SUPP_FILES = [
    ("CBIN-46-2158-s001.pdf", "/articles/instance/9804513/bin/CBIN-46-2158-s001.pdf"),
    ("CBIN-46-2158-s002.docx", "/articles/instance/9804513/bin/CBIN-46-2158-s002.docx"),
    ("CBIN-46-2158-s003.pdf", "/articles/instance/9804513/bin/CBIN-46-2158-s003.pdf"),
    ("CBIN-46-2158-s004.pdf", "/articles/instance/9804513/bin/CBIN-46-2158-s004.pdf"),
    ("CBIN-46-2158-s005.pdf", "/articles/instance/9804513/bin/CBIN-46-2158-s005.pdf"),
    ("CBIN-46-2158-s006.pdf", "/articles/instance/9804513/bin/CBIN-46-2158-s006.pdf"),
]
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "source", "supplementary")
CHUNK = 524288  # 512KB base64 chunk


def get_ws_url():
    with urllib.request.urlopen(f"{CDP_HTTP}/json") as r:
        tabs = json.loads(r.read())
    for t in tabs:
        if t.get("url", "").endswith(ARTICLE_URL_SUFFIX):
            return t["webSocketDebuggerUrl"]
    # fallback: navigate the first page-type tab there
    for t in tabs:
        if t.get("type") == "page":
            return t["webSocketDebuggerUrl"]
    raise RuntimeError("no PMC9804513 tab open in Chrome")


def evaluate(ws, msg_id, expression):
    payload = {
        "id": msg_id,
        "method": "Runtime.evaluate",
        "params": {
            "expression": expression,
            "awaitPromise": True,
            "returnByValue": True,
            "timeout": 60000,
        },
    }
    ws.send(json.dumps(payload))
    while True:
        msg = json.loads(ws.recv())
        if msg.get("id") == msg_id:
            if "error" in msg:
                raise RuntimeError(msg["error"])
            return msg["result"]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    ws_url = get_ws_url()
    print(f"[cdp] tab ws: {ws_url}", flush=True)
    with connect(ws_url, max_size=64 * 1024 * 1024) as ws:
        msg_id = 0
        # Step 1: fetch each file fully, stash base64 string into window.__bufs
        for fname, path in SUPP_FILES:
            msg_id += 1
            expr = (
                "(async () => {"
                f" const r = await fetch('{path}', {{credentials:'include'}});"
                " const buf = await r.arrayBuffer();"
                " const bytes = new Uint8Array(buf);"
                " let s=''; const CHUNK=8192;"
                " for (let i=0;i<bytes.length;i+=CHUNK){"
                "   s += String.fromCharCode.apply(null, bytes.slice(i,i+CHUNK));"
                " }"
                " const b64 = btoa(s);"
                " window.__lastBuf = b64;"
                " return {status:r.status, size:buf.byteLength, b64len:b64.length};"
                "})()"
            )
            res = evaluate(ws, msg_id, expr)
            info = res["result"]["value"]
            print(f"[fetch] {fname} status={info['status']} size={info['size']} b64len={info['b64len']}", flush=True)

            b64_full = ""
            # Step 2: slice window.__lastBuf in chunks
            offset = 0
            total = info["b64len"]
            while offset < total:
                msg_id += 1
                slice_expr = f"window.__lastBuf.substr({offset},{CHUNK})"
                r = evaluate(ws, msg_id, slice_expr)
                slc = r["result"]["value"]
                if not slc:
                    break
                b64_full += slc
                offset += len(slc)
            data = base64.b64decode(b64_full)
            assert len(data) == info["size"], f"size mismatch {len(data)} != {info['size']}"
            out = os.path.join(OUT_DIR, fname)
            with open(out, "wb") as f:
                f.write(data)
            print(f"[saved] {out} ({len(data)} bytes)", flush=True)

        # clear stash
        msg_id += 1
        evaluate(ws, msg_id, "delete window.__lastBuf; 1")


if __name__ == "__main__":
    main()
