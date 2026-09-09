"""
GPU / law organ export for fsot-neuron-zig.

Not a second mind. JSON a Zig skill can read:
  pin, S(domain), bleed κ, look-path law, living hired-job scores.

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
        "look_law": {
            "observe": "QC dark → Quantum_Optics look → QM measure",
            "do_not_observe": ["Quantum_Computing", "Biology"],
            "why": (
                "Forcing observed=True on QC flips S from damping to emergence "
                "and the compute identity is gone. That is the Hilbert move."
            ),
        },
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
                "emergence": True,
            },
            {
                "id": "S_QC",
                "question": "Is S(Quantum_Computing) damping?",
                "answer": S["Quantum_Computing"],
                "emergence": False,
            },
        ],
        "hired_jobs": [
            {
                "hire": "Shor factor",
                "question": "Factor N=pq (RSA-shaped, similar-bit primes)",
                "score": "119-bit 8/8 (60-bit rho); 64-bit 0/8 ECM",
                "command": "python -m fsot_quantum heights17",
            },
            {
                "hire": "QAOA MaxCut",
                "question": "Gset unweighted MaxCut vs published BKS",
                "score": "11/11 under 1%; G17 13 short; G22 89; G23 50",
                "command": "python -m fsot_quantum family",
            },
            {
                "hire": "Grover search",
                "question": "Find a marked item",
                "score": "exact through 1e7",
                "command": "python -m fsot_quantum known",
            },
            {
                "hire": "chemistry / FCI observables",
                "question": "pin chemistry set",
                "score": "68/68 @ 0.5%; H2 De 0.25%; Kolos 0.75% written; LiH not invented",
                "command": "python -m fsot_quantum vqe",
            },
            {
                "hire": "CKM / H0 / V_cb",
                "question": "published SM / cosmology objects",
                "score": "audit 20/20; inclusive V_cb 0.002%; exclusive B→D 0.15%; Planck H0 0.024%",
                "command": "python -m fsot_quantum audit",
            },
        ],
        "doctrine": (
            "Zig Fixed lattice is the mind. This JSON is an organ readout: "
            "domain S, bleed κ, look-path law, and living hired-job scores. "
            "Do not softmax. Do not spawn an LLM. Do not look at QC."
        ),
        "metal": {
            "qc_os": "FSOT-QC-OS v0.3.0 under QEMU — 13 integer jobs, subset of the Python host",
            "python_host": "python -m fsot_quantum — living wrap, 44/44 known, heights17, family",
        },
        "wrap": {
            "quantum_status": "https://github.com/dappalumbo91/FSOT-Quantum/blob/main/docs/STATUS.md",
            "claims": "https://github.com/dappalumbo91/FSOT-Quantum/blob/main/docs/CLAIMS.md",
            "audit": "20/20 vs YR4/PDG @0.5%",
            "physics_qi3": "41/41 + 212/212 Lean",
            "gset_family": "11/11 under 1%; G17 13 edges; G22 89; G23 50",
            "factor": "RSA-shaped 119-bit 8/8; 64-bit 0/8 ECM",
            "known_qc": "44/44",
            "stamp": "FSOT_QUANTUM_MULTIPROVER_OK",
            "vcb": "inclusive 0.002%; exclusive B→D 0.15%",
            "h0": "Planck 0.024%; SH0ES 1.00% Lean BH→WH",
            "open": [
                "G17 13 edges / G22 89 (champions unmatched)",
                "64-bit ECM 0/8; rho ~2^32 wall",
                "RSA-2048 not run",
                "vendor BR_H_gg field still stale",
            ],
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
    zig_organ = (
        ROOT / "_ref" / "fsot-neuron-zig" / "data" / "organs" / "fsot_quantum_organ.json"
    )
    if zig_organ.parent.is_dir():
        zig_organ.write_text(text, encoding="utf-8")
    md = [
        "# Law organ — living wrap for neuron-zig",
        "",
        f"**pin:** `{organ['pin']}` · **pin_ok:** `{organ['pin_ok']}`",
        "",
        "Not a second mind. Zig remains mind authority. This JSON is the "
        "law readout: \(S\), \(\kappa\), look-path, hired-job scores.",
        "",
        "## Look law",
        "",
        f"- Observe: {organ['look_law']['observe']}",
        f"- Do not observe: `{', '.join(organ['look_law']['do_not_observe'])}`",
        f"- {organ['look_law']['why']}",
        "",
        "## Hired jobs (living)",
        "",
        "| Hire | Score | Command |",
        "|------|-------|---------|",
    ]
    for j in organ["hired_jobs"]:
        md.append(f"| {j['hire']} | {j['score']} | `{j['command']}` |")
    md += [
        "",
        f"Metal: {organ['metal']['qc_os']}",
        "",
        "```powershell",
        "python -m fsot_quantum organ",
        "```",
        "",
    ]
    (out / "ORGAN.md").write_text("\n".join(md), encoding="utf-8")
    (ROOT / "docs" / "ORGAN.md").write_text("\n".join(md), encoding="utf-8")
    print(json.dumps({
        "pin_ok": organ["pin_ok"],
        "pin": organ["pin"],
        "n_domains": len(organ["S"]),
        "n_bleed": len(organ["bleed"]),
        "n_hired": len(organ["hired_jobs"]),
        "S_QM": organ["S"]["Quantum_Mechanics"],
        "S_QC": organ["S"]["Quantum_Computing"],
        "path": str(out / "organ_export.json"),
    }, indent=2))
    return 0 if organ["pin_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
