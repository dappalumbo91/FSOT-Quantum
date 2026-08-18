"""
GPU / law organ export for fsot-neuron-zig.

Not a second mind. JSON a Zig skill can read:
  pin, S(domain), bleed κ, one QI answer, look path.

python -m fsot_quantum.organ_export
python -m fsot_quantum organ
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_lib.seeds import COLLAPSE_THRESHOLD, SEEDS
from fsot_quantum.domains import DOMAINS, domain_scalar


def _kap(a: str, b: str) -> float:
    Sa, Sb = abs(domain_scalar(a)), abs(domain_scalar(b))
    dist = abs(DOMAINS[a].D_eff - DOMAINS[b].D_eff) / 25.0
    return float(SEEDS.a_bleed) * float(SEEDS.poof) * Sa * Sb / (1.0 + dist)


ORGAN_EDGES = (
    ("Quantum_Computing", "Quantum_Optics"),
    ("Quantum_Optics", "Quantum_Mechanics"),
    ("Quantum_Computing", "Psychology"),
    ("Biology", "Neuroscience"),
    ("Neuroscience", "Psychology"),
    ("Psychology", "Quantum_Mechanics"),
    ("Quantum_Computing", "Quantum_Mechanics"),
)


def build_organ() -> dict[str, Any]:
    pin_path = ROOT / "vendor" / "fsot_compute.py"
    pin = hashlib.sha256(pin_path.read_bytes()).hexdigest()[:6].upper()
    S = {name: domain_scalar(name) for name in sorted(DOMAINS)}
    bleed = [
        {"from": a, "to": b, "kappa": _kap(a, b)}
        for a, b in ORGAN_EDGES
    ]
    return {
        "organ": "fsot_quantum",
        "role": "GPU/law organ — not mind authority",
        "pin": pin,
        "pin_expected": "D1D38A",
        "pin_ok": pin == "D1D38A",
        "C_factor": float(SEEDS.c_factor),
        "Theta": float(COLLAPSE_THRESHOLD),
        "K": float(SEEDS.k),
        "S": S,
        "bleed": bleed,
        "look_path": ["Quantum_Computing", "Quantum_Optics", "Quantum_Mechanics"],
        "mind_path": ["Quantum_Computing", "Biology", "Neuroscience", "Psychology", "Quantum_Mechanics"],
        "qi": [
            {
                "id": "CHSH_TSIRELSON",
                "question": "What is the Tsirelson bound?",
                "answer": 2.0 * math.sqrt(2.0),
            },
            {
                "id": "S_QM",
                "question": "Is S(Quantum_Mechanics) emergence?",
                "answer": S["Quantum_Mechanics"],
            },
            {
                "id": "S_QC",
                "question": "Is S(Quantum_Computing) damping?",
                "answer": S["Quantum_Computing"],
            },
        ],
        "doctrine": (
            "Zig Fixed lattice is the mind. This JSON is an organ readout: "
            "domain S, bleed κ, and pin QI. Do not softmax. Do not spawn an LLM."
        ),
        "wrap": {
            "quantum_status": "https://github.com/dappalumbo91/FSOT-Quantum/blob/main/docs/STATUS.md",
            "audit": "20/20 vs YR4/PDG @0.5%",
            "physics_qi3": "41/41 + 212/212 Lean",
            "gset_family": "11/11 under 1%; G17 0.427%",
            "vcb": "inclusive 0.002%; exclusive B→D 0.15%",
            "h0": "Planck 0.024%; SH0ES 1.00% Lean BH→WH",
        },
    }


def main() -> int:
    t0 = time.perf_counter()
    organ = build_organ()
    organ["timestamp"] = datetime.now(timezone.utc).isoformat()
    organ["wall_seconds"] = time.perf_counter() - t0
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    text = json.dumps(organ, indent=2)
    (out / "organ_export.json").write_text(text, encoding="utf-8")
    # snapshot a copy the neuron-zig skill can vendor if the other repo is present
    snap = ROOT / "results" / "fsot_quantum_organ.json"
    snap.write_text(text, encoding="utf-8")
    print(json.dumps({
        "pin_ok": organ["pin_ok"],
        "pin": organ["pin"],
        "n_domains": len(organ["S"]),
        "n_bleed": len(organ["bleed"]),
        "S_QM": organ["S"]["Quantum_Mechanics"],
        "S_QC": organ["S"]["Quantum_Computing"],
        "path": str(out / "organ_export.json"),
    }, indent=2))
    return 0 if organ["pin_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
