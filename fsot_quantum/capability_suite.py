"""
FSOT-QC capability suite — what industry quantum computing claims, on GPU.

Writes results/capability_suite.json + CAPABILITY_REPORT.md
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

from fsot_lib.seeds import COLLAPSE_THRESHOLD
from fsot_quantum.algorithms import (
    AlgoResult,
    bell_correlation_fsot,
    bernstein_vazirani_fsot,
    deutsch_jozsa_fsot,
    grover_fsot_search,
    ising_ground_fsot,
    make_balanced_parity_oracle,
    oracle_constant_one,
    oracle_constant_zero,
    phase_class_estimation_fsot,
    qft_role_fsot,
)
from fsot_quantum.domains import domain_scalar
from fsot_quantum.gpu_parallel import (
    batch_consensus_coupling,
    batch_grover_search,
    batch_oracle_parity,
    batch_pack_stress,
    prefer_device,
)


def _algo_dict(r: AlgoResult) -> dict[str, Any]:
    return {
        "name": r.name,
        "ok": r.ok,
        "expected": r.expected,
        "got": r.got,
        "detail": r.detail,
    }


def run_suite() -> dict[str, Any]:
    t0 = time.perf_counter()
    device = prefer_device()
    report: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "goal": (
            "FSOT quantum capability on GPU/CPU — answers without quantum hardware "
            "infrastructure; parallel interface = GPU"
        ),
        "implementation": "fsot_lib (FSOT-GPU) + fsot_quantum domain fold",
        "pin": "D1D38A",
        "collapse_threshold": COLLAPSE_THRESHOLD,
        "device": device,
        "S_Quantum_Mechanics": domain_scalar("Quantum_Mechanics"),
        "S_Quantum_Computing": domain_scalar("Quantum_Computing"),
        "algorithms": [],
        "gpu_parallel": {},
        "summary": {},
    }

    algos: list[AlgoResult] = []

    # Deutsch–Jozsa family
    algos.append(deutsch_jozsa_fsot(4, oracle_constant_zero))
    algos.append(deutsch_jozsa_fsot(4, oracle_constant_one))
    algos.append(deutsch_jozsa_fsot(4, make_balanced_parity_oracle(0b1011)))
    algos.append(deutsch_jozsa_fsot(8, make_balanced_parity_oracle(0b11001101)))

    # Bernstein–Vazirani
    for secret in ([1, 0, 1, 1], [1, 1, 0, 0, 1, 0, 1, 1], [1] * 12):
        algos.append(bernstein_vazirani_fsot(secret))

    # Grover-like search
    for N, m in [(16, 7), (64, 41), (256, 200), (1024, 777)]:
        algos.append(grover_fsot_search(N, m))

    # Bell
    algos.append(bell_correlation_fsot(128))

    # Phase class
    algos.append(phase_class_estimation_fsot())

    # Ising small
    # ring ferromagnetic n=6
    n = 6
    coup = [(i, (i + 1) % n, 1) for i in range(n)]
    algos.append(ising_ground_fsot(coup, n))
    # frustrated triangle + chain
    coup2 = [(0, 1, 1), (1, 2, 1), (2, 0, -1), (2, 3, 1), (3, 4, -1)]
    algos.append(ising_ground_fsot(coup2, 5))

    # QFT role
    algos.append(qft_role_fsot(32, 64))

    report["algorithms"] = [_algo_dict(a) for a in algos]

    # GPU parallel stress / throughput
    report["gpu_parallel"] = {
        "pack_stress": batch_pack_stress(32768),
        "grover_batch": batch_grover_search(
            512, marked_list=[(i * 17 + 3) % 512 for i in range(256)]
        ),
        "bv_batch": batch_oracle_parity(
            8,
            secrets=[[(i >> b) & 1 for b in range(8)] for i in range(128)],
        ),
        "consensus_batch": batch_consensus_coupling(batch=16, seq=48, dim=48),
    }

    algo_ok = sum(1 for a in algos if a.ok)
    gpu_ok = all(v.get("ok") for v in report["gpu_parallel"].values())
    report["summary"] = {
        "algorithms_pass": algo_ok,
        "algorithms_total": len(algos),
        "algorithms_accuracy": algo_ok / len(algos),
        "gpu_parallel_all_ok": gpu_ok,
        "overall_ok": algo_ok == len(algos) and gpu_ok,
        "wall_seconds": time.perf_counter() - t0,
        "device": device,
    }

    # What industry QC costs vs this path (narrative facts for report)
    report["path_forward"] = {
        "industry_requires": [
            "cryogenic dilution refrigerators",
            "error-corrected logical qubits (huge physical overhead)",
            "specialty fabs / trapped-ion / photonic lines",
            "closed vendor stacks",
        ],
        "fsot_requires": [
            "consumer/server GPU (or CPU for pure path)",
            "fsot_lib owned operators (collapse, consensus, pack)",
            "pin-locked seeds — zero free parameters",
            "domain routes Quantum_Mechanics / Quantum_Computing",
        ],
        "honest_scope": [
            "Not claiming full Hilbert-space equivalence to arbitrary unitaries",
            "Claiming: same *jobs* (oracle class, secret recover, search, coupling, optimization) with seed-locked accuracy ledgers on GPU",
            "Scale path: batch more instances / longer registers on same GPU",
        ],
        "next_builds": [
            "Larger Ising / MaxCut panels with residual gates vs public benchmarks",
            "Circuit depth library mapped 1:1 to industry textbook algorithms",
            "Zig/QEMU twin of quantum register (same as neuron/genetics multi-lang)",
            "Publish capability ledger + skeptic kit",
        ],
    }

    out_dir = ROOT / "results"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "capability_suite.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    md = _markdown(report)
    (out_dir / "CAPABILITY_REPORT.md").write_text(md, encoding="utf-8")
    (ROOT / "docs" / "CAPABILITY_AND_PATH_FORWARD.md").write_text(
        _path_forward_doc(report), encoding="utf-8"
    )
    return report


def _markdown(report: dict[str, Any]) -> str:
    s = report["summary"]
    lines = [
        "# FSOT-QC Capability Report",
        "",
        f"**overall_ok:** `{s['overall_ok']}`",
        f"**device:** `{s['device']}`",
        f"**algorithms:** {s['algorithms_pass']}/{s['algorithms_total']} "
        f"({100*s['algorithms_accuracy']:.1f}%)",
        f"**gpu_parallel_all_ok:** `{s['gpu_parallel_all_ok']}`",
        f"**wall_s:** `{s['wall_seconds']:.4f}`",
        f"**Θ:** `{report['collapse_threshold']}`",
        "",
        "## Algorithms",
        "",
        "| Name | OK | Expected | Got |",
        "|------|----|----------|-----|",
    ]
    for a in report["algorithms"]:
        lines.append(
            f"| {a['name']} | {a['ok']} | `{a['expected']}` | `{a['got']}` |"
        )
    lines += ["", "## GPU parallel", ""]
    for k, v in report["gpu_parallel"].items():
        lines.append(f"- **{k}:** ok={v.get('ok')} device={v.get('device')} detail=`{ {kk:v[kk] for kk in v if kk not in ('ok',)} }`")
    lines += ["", "## Goal", "", report["goal"], ""]
    return "\n".join(lines) + "\n"


def _path_forward_doc(report: dict[str, Any]) -> str:
    s = report["summary"]
    pf = report["path_forward"]
    return f"""# Capability and path forward — FSOT quantum computing

## Goal

Apply Fluid Spacetime Omni-Theory to **quantum computing as a field**:  
get **usable, accurate answers** to the jobs QC is sold for, **without** cryogenic quantum hardware — using **GPU parallel processing** as the physical interface.

## Live ledger (this machine)

| Metric | Value |
|--------|------:|
| overall_ok | `{s['overall_ok']}` |
| algorithms | {s['algorithms_pass']}/{s['algorithms_total']} |
| GPU parallel | `{s['gpu_parallel_all_ok']}` |
| device | `{s['device']}` |
| Θ = C_eff·P_var | `{report['collapse_threshold']}` |
| S(QM) | `{report['S_Quantum_Mechanics']}` |
| S(QC) | `{report['S_Quantum_Computing']}` |

Regenerate: `python -m fsot_quantum.capability_suite`

## What industry QC “does” vs FSOT-QC here

| Industry job | FSOT path (this repo) | GPU role |
|--------------|----------------------|----------|
| Deutsch–Jozsa (constant vs balanced) | Oracle class via seed-locked structure + domain routes | Batch many oracles |
| Bernstein–Vazirani (learn secret) | Parity oracle basis probes (exact) | Vectorized secrets |
| Grover search | Marked pole + `fsot_lib.collapse` | Batch searches `[B,N]` |
| Entanglement / correlations | H+CX+measure trinary circuit | Many pairs in parallel |
| Phase estimation | Domain `S` class (emergence/damping) | Scalar on device optional |
| QFT / phase ladder | `apply_phase_rotation` + consensus (FSOT-GPU) | Large seq×dim |
| Optimization (Ising) | Pair couplings + local FSOT search | Later: batched graphs |
| Memory packing | 2-bit trit pack (4× denser than u8) | VRAM banks |

## Infrastructure contrast

**Industry requires**

{chr(10).join('- ' + x for x in pf['industry_requires'])}

**FSOT path requires**

{chr(10).join('- ' + x for x in pf['fsot_requires'])}

## Honesty (non-negotiable)

{chr(10).join('- ' + x for x in pf['honest_scope'])}

## Next builds

{chr(10).join('1. ' + x for x in pf['next_builds'])}

## How to run

```powershell
cd "C:\\Users\\damia\\Desktop\\fsot quantum"
$env:PYTHONPATH = (Get-Location).Path
python -m fsot_lib.smoke_owned
python -m fsot_quantum.verify
python -m fsot_quantum.capability_suite
```

Ledgers: `results/capability_suite.json`, `results/CAPABILITY_REPORT.md`
"""


def main() -> int:
    report = run_suite()
    print(json.dumps(report["summary"], indent=2))
    print("overall_ok:", report["summary"]["overall_ok"])
    print("wrote results/capability_suite.json")
    print("wrote results/CAPABILITY_REPORT.md")
    print("wrote docs/CAPABILITY_AND_PATH_FORWARD.md")
    return 0 if report["summary"]["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
