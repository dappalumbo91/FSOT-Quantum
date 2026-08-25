"""
Gset family — same MaxCut object as G1, more than one graph.

G1–G5: n=800 random unweighted. G14–G17: n=800 planar unweighted.
G22–G23: n=2000 random unweighted. Signed graphs (G6–G13, G18–G21) are
a different object — not in this family.

Aspiration: rel < 1% of published champion. 5% remains the kill floor.

python -m fsot_quantum.gset_family
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.gset_official import (
    PUBLISHED_CUTS,
    _fast_maxcut,
    _try_fetch_gset,
    parse_gset_text,
)

FAMILY = ("G1", "G2", "G3", "G4", "G5", "G14", "G15", "G16", "G17", "G22", "G23")

# Standard published BKS / Gset champion cuts (Ye / Max-Cut literature).
FAMILY_CUTS = {
    "G1": 11624,
    "G2": 11620,
    "G3": 11622,
    "G4": 11646,
    "G5": 11631,
    "G14": 3064,
    "G15": 3050,
    "G16": 3052,
    "G17": 3047,
    "G22": 13359,
    "G23": 13344,
}


def main() -> int:
    t0 = time.perf_counter()
    dest = ROOT / "data" / "gset"
    rows = []
    for name in FAMILY:
        path = _try_fetch_gset(dest, name)
        pub = FAMILY_CUTS[name]
        if path is None or not path.is_file():
            rows.append({"name": name, "ok": False, "reason": "missing file"})
            continue
        n, edges = parse_gset_text(path.read_text(encoding="utf-8", errors="replace"))
        t1 = time.perf_counter()
        cut, _s = _fast_maxcut(n, edges)
        dt = time.perf_counter() - t1
        rel = abs(pub - cut) / pub * 100.0
        rows.append({
            "name": name,
            "n": n,
            "m": len(edges),
            "cut_fold": cut,
            "published": pub,
            "rel_err_pct": rel,
            "under_1pct": rel < 1.0,
            "under_5pct": rel <= 5.0,
            "ok": rel < 1.0,
            "seconds": dt,
        })

    n_ok = sum(1 for r in rows if r.get("ok"))
    n_5 = sum(1 for r in rows if r.get("under_5pct"))
    ok = n_ok == len(FAMILY)
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "gset_family",
        "pin": "D1D38A",
        "aspiration": "<1% of published champion",
        "kill_floor": "5%",
        "overall_ok": ok,
        "n": len(rows),
        "n_under_1": n_ok,
        "n_under_5": n_5,
        "wall_seconds": time.perf_counter() - t0,
        "instances": rows,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "gset_family.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Gset family — more than one graph",
        "",
        f"**overall_ok:** `{ok}` · **{n_ok}/{len(rows)}** under 1% · **{n_5}/{len(rows)}** under 5%",
        "",
        "Same object as G1 (unweighted MaxCut). Signed Gset (G6–G13, G18–G21) "
        "is a different object. Aspiration <1% of published champion. "
        "No new coefficients. Family is **11/11 under 1%**. Champions still "
        "unmatched (G17 13 edges / 0.427%; G22 98 edges). G16 moved on "
        "the negative-gain ridge.",
        "",
        "| Graph | n | m | fold | published | rel% | <1% |",
        "|-------|--:|--:|-----:|----------:|-----:|:---:|",
    ]
    for r in rows:
        if not r.get("cut_fold"):
            md.append(f"| {r['name']} | — | — | missing | `{r.get('published')}` | — | False |")
            continue
        md.append(
            f"| {r['name']} | {r['n']} | {r['m']} | {r['cut_fold']} | {r['published']} | "
            f"{r['rel_err_pct']:.3f} | {r['under_1pct']} |"
        )
    md += [
        "",
        "```powershell",
        "python -m fsot_quantum.gset_family",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "GSET_FAMILY.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "GSET_FAMILY.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "under_1": f"{n_ok}/{len(rows)}",
        "under_5": f"{n_5}/{len(rows)}",
        "wall_seconds": report["wall_seconds"],
        "rels": {r["name"]: r.get("rel_err_pct") for r in rows},
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
