"""
Ingest FSOT-2.1-Lean quantum benchmark headlines (already solved there).

This fold does **not** re-fit those 177+50+21 formulas. It reads the
mother-repo ledgers so this granular QC field-of-use knows what the
full fabric already covers.

Looks in repo `_ref/FSOT-2.1-Lean/data/` (dev clone) — skip if absent.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEAN_DATA = ROOT / "_ref" / "FSOT-2.1-Lean" / "data"

ATLAS_FILES = (
    "quantum_computing_gap_fill_benchmark.json",
    "quantum_mechanics_gap_fill_benchmark.json",
    "quantum_optics_gap_fill_benchmark.json",
    "quantum_information_benchmark.json",
    "quantum_mechanics_entanglement_depth_panel_benchmark.json",
    "quantum_computing_math_depth_panel_benchmark.json",
    "quantum_materials_benchmark.json",
    "founding_quantum_vacuum_panel_benchmark.json",
)


def ingest_lean_quantum_atlas() -> dict[str, Any]:
    rows = []
    if not LEAN_DATA.is_dir():
        return {
            "panel": "lean_quantum_atlas",
            "ok": False,
            "status": "skip_no_local_lean_data",
            "instances": [],
            "note": "Clone FSOT-2.1-Lean under _ref to ingest atlas headlines.",
        }
    for name in ATLAS_FILES:
        p = LEAN_DATA / name
        if not p.is_file():
            rows.append({"file": name, "ok": False, "status": "missing"})
            continue
        try:
            blob = json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            rows.append({"file": name, "ok": False, "error": str(e)[:160]})
            continue
        rows.append({
            "file": name,
            "ok": True,
            "domain": blob.get("domain"),
            "D_eff": blob.get("D_eff"),
            "record_count": blob.get("record_count") or blob.get("observable_count"),
            "median_error_pct": blob.get("headline_median_error_pct")
            or blob.get("pooled_median_error_pct")
            or blob.get("median_error_pct"),
            "free_parameters": (blob.get("sota_comparison") or {}).get("fsot_free_parameters"),
        })
    ok_rows = [r for r in rows if r.get("ok")]
    return {
        "panel": "lean_quantum_atlas",
        "ok": len(ok_rows) >= 4,
        "status": "ingested" if ok_rows else "empty",
        "n_files": len(ok_rows),
        "instances": rows,
        "total_records": sum(int(r.get("record_count") or 0) for r in ok_rows),
        "note": (
            "Headlines from FSOT-2.1-Lean verification fabric — "
            "403+ domain interfaces live there. This fold is the QC/QM job layer."
        ),
    }
