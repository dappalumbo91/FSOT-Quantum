"""
Keep going: concepts live + fridge/hits probe + more Lean QI/math jobs.

python -m fsot_quantum.keep_going
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.medium_strings import run_medium_strings_panel
from fsot_quantum.entangle_qi_jobs import run_entangle_qi_panel
from fsot_quantum.thermal_hits import run_thermal_hits_panel


def main() -> int:
    t0 = time.perf_counter()
    med = run_medium_strings_panel()
    qi = run_entangle_qi_panel()
    therm = run_thermal_hits_panel()
    concepts = (ROOT / "docs" / "CONCEPTS.md").exists()

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "keep_going",
        "pin": "D1D38A",
        "concepts_doc": "docs/CONCEPTS.md",
        "concepts_ok": concepts,
        "medium_ok": med["overall_ok"],
        "entangle_qi": {
            "ok": qi["overall_ok"],
            "replayed": qi.get("n_replayed"),
            "green": f"{qi.get('n_green_0_5')}/{qi.get('n_replayed')}",
            "band5": f"{qi.get('n_band_5')}/{qi.get('n_replayed')}",
            "skipped": qi.get("n_skipped_broken"),
        },
        "thermal_hits": {
            "ok": therm["overall_ok"],
            "fridge_pattern_ok": therm["fridge_pattern_ok"],
            "frac_super_cold": therm["frac_super_cold"],
            "frac_super_hot": therm["frac_super_hot"],
            "ladder": [
                {"hits": r["hits"], "frac_super": r["frac_superposed"]}
                for r in therm["instances"]
            ],
        },
        "overall_ok": (
            concepts
            and med["overall_ok"]
            and qi["overall_ok"]
            and therm["overall_ok"]
        ),
        "wall_seconds": time.perf_counter() - t0,
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "thermal_hits.json").write_text(json.dumps(therm, indent=2), encoding="utf-8")
    (out / "keep_going.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Keep going",
        "",
        f"**overall_ok:** `{report['overall_ok']}`",
        f"**wall_s:** `{report['wall_seconds']:.2f}`",
        "",
        "Concepts (traceable): `docs/CONCEPTS.md` (C1–C6).",
        "",
        f"- medium / three strings: `{report['medium_ok']}`",
        f"- Lean entanglement+QI+math replay: {report['entangle_qi']['green']} @0.5% "
        f"(skipped broken {report['entangle_qi']['skipped']})",
        f"- fridge/hits: cold super={report['thermal_hits']['frac_super_cold']:.3f} "
        f"→ hot super={report['thermal_hits']['frac_super_hot']:.3f} "
        f"pattern_ok={report['thermal_hits']['fridge_pattern_ok']}",
        "",
        "## Reproduce",
        "",
        "```powershell",
        'cd "C:\\Users\\damia\\Desktop\\fsot quantum"',
        "$env:PYTHONPATH = (Get-Location).Path",
        "python -m fsot_quantum.keep_going",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "KEEP_GOING.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "KEEP_GOING.md").write_text(text, encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
