"""
Scale / throughput scoreboard — GPU parallel FSOT-QC.

Sweeps N and batch sizes; writes results/scale_scoreboard.json.
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fsot_quantum.gpu_parallel import (
    batch_consensus_coupling,
    batch_grover_search,
    batch_oracle_parity,
    batch_pack_stress,
    prefer_device,
)

ROOT = Path(__file__).resolve().parents[1]


def run_scale_scoreboard() -> dict[str, Any]:
    device = prefer_device()
    report: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "device": device,
        "panel": "scale_throughput",
        "rows": [],
        "overall_ok": True,
    }

    # Pack scale
    for groups in (1024, 8192, 32768, 131072, 524288):
        r = batch_pack_stress(groups)
        report["rows"].append({"kind": "pack", **r})
        if not r.get("ok"):
            report["overall_ok"] = False

    # Grover search scale
    for n_items, batch in ((64, 256), (256, 512), (1024, 512), (4096, 256), (16384, 128)):
        marked = [(i * 31 + 7) % n_items for i in range(batch)]
        r = batch_grover_search(n_items, marked)
        report["rows"].append({"kind": "grover", **r})
        if not r.get("ok"):
            report["overall_ok"] = False

    # BV scale
    for n, batch in ((8, 256), (12, 128), (16, 64)):
        secrets = []
        for i in range(batch):
            secrets.append([(i >> b) & 1 for b in range(n)])
        r = batch_oracle_parity(n, secrets)
        report["rows"].append({"kind": "bv", **r})
        if not r.get("ok"):
            report["overall_ok"] = False

    # Consensus scale
    for seq, dim, batch in ((32, 32, 32), (64, 64, 16), (128, 64, 8), (256, 32, 4)):
        r = batch_consensus_coupling(batch=batch, seq=seq, dim=dim)
        report["rows"].append({"kind": "consensus", **r})
        if not r.get("ok"):
            report["overall_ok"] = False

    # Best throughputs
    pack_rows = [r for r in report["rows"] if r["kind"] == "pack" and r.get("ok")]
    grover_rows = [r for r in report["rows"] if r["kind"] == "grover" and r.get("ok")]
    report["highlights"] = {
        "device": device,
        "max_trits_packed": max((r.get("trits", 0) for r in pack_rows), default=0),
        "fastest_pack_trits_per_s": max(
            (r["trits"] / r["seconds"] for r in pack_rows if r.get("seconds")),
            default=0,
        ),
        "best_grover_instances_per_s": max(
            (r.get("instances_per_sec") or 0 for r in grover_rows),
            default=0,
        ),
        "largest_grover_N": max((r.get("n_items", 0) for r in grover_rows), default=0),
    }

    out = ROOT / "results" / "scale_scoreboard.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# FSOT-QC scale scoreboard",
        "",
        f"**device:** `{device}`",
        f"**overall_ok:** `{report['overall_ok']}`",
        "",
        "## Highlights",
        "",
        f"- max trits packed: **{report['highlights']['max_trits_packed']:,}**",
        f"- pack throughput: **{report['highlights']['fastest_pack_trits_per_s']:.0f}** trits/s",
        f"- best Grover batch: **{report['highlights']['best_grover_instances_per_s']:.0f}** instances/s",
        f"- largest search N: **{report['highlights']['largest_grover_N']}**",
        "",
        "## Rows",
        "",
        "| kind | key | ok | seconds |",
        "|------|-----|----|---------|",
    ]
    for r in report["rows"]:
        key = r.get("trits") or r.get("n_items") or r.get("n") or r.get("seq")
        md.append(f"| {r['kind']} | {key} | {r.get('ok')} | {r.get('seconds', 0):.6f} |")
    (ROOT / "results" / "SCALE_SCOREBOARD.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return report
