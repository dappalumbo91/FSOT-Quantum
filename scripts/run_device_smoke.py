#!/usr/bin/env python3
"""FSOT-owned device smoke (torch if present — no nvcc)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.device import backend_info, smoke_device


def main() -> int:
    info = backend_info()
    report = smoke_device(n_groups=4096)
    out = {"backend": info, "smoke": report}
    path = ROOT / "results" / "device_smoke.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    print("overall_ok:", report.get("overall_ok"))
    return 0 if report.get("overall_ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
