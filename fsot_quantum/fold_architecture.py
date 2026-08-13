"""
FSOT fold architecture — the answering machine is domain folds, not Hilbert n.

The theory already has the geometry:
  S = K(T1+T2+T3) on the pin 35-domain table, bled across D_eff,
  and the Lean atlas (~410+ named folds) as the solved fabric.

Industry grows qubit count because it treats the unobserved compute
substrate (Quantum_Computing, D=11, S<0) as an observed Hilbert register.
That is the wrong object. This module does not grow n. It routes the
question to the domain fold that already holds the answer, on GPU.

python -m fsot_quantum.fold_architecture
python -m fsot_quantum fold
"""

from __future__ import annotations

import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_lib.scalar import compute_scalar
from fsot_lib.seeds import SEEDS
from fsot_quantum.domains import DOMAINS, domain_scalar
from fsot_quantum.gpu_parallel import prefer_device
from fsot_quantum.lean_full_atlas import _discover, _scan_one
# Hired question → pin domain folds. Not qubit counts.
QUESTION_ROUTES: dict[str, tuple[str, ...]] = {
    "fine_structure_and_sm_constants": ("Quantum_Mechanics", "Particle_Physics", "High_Energy_Physics"),
    "chemistry_observables": ("Chemistry", "Molecular_Chemistry", "Physical_Chemistry"),
    "spin_measurement": ("Quantum_Mechanics", "Atomic_Physics"),
    "compute_substrate": ("Quantum_Computing",),
    "packing_and_cut": ("Condensed_Matter", "Materials_Science"),
    "phase_optics": ("Quantum_Optics", "Optics"),
    "nuclear_and_mass": ("Nuclear_Physics", "Particle_Physics"),
    "deep_residual": ("Quantum_Gravity", "Cosmology"),
}


def _gpu_pin_scalars(device: str) -> dict[str, Any]:
    import torch
    from fsot_lib.backend.torch_backend import scalar_torch_batch

    names = sorted(DOMAINS)
    D = [float(DOMAINS[n].D_eff) for n in names]
    dp = [float(DOMAINS[n].delta_psi) for n in names]
    dth = [float(DOMAINS[n].delta_theta) for n in names]
    hits = [float(DOMAINS[n].hits) for n in names]
    obs = [bool(DOMAINS[n].observed) for n in names]
    if device.startswith("cuda"):
        torch.cuda.synchronize()
    t0 = time.perf_counter()
    S = scalar_torch_batch(
        D_eff=D,
        delta_psi=dp,
        delta_theta=dth,
        recent_hits=hits,
        observed=obs,
        device=device,
    )
    if device.startswith("cuda"):
        torch.cuda.synchronize()
    dt = time.perf_counter() - t0
    got = S.detach().cpu().tolist()
    cpu = [domain_scalar(n) for n in names]
    deltas = [abs(g - c) for g, c in zip(got, cpu)]
    return {
        "device": device,
        "n_domains": len(names),
        "seconds": dt,
        "max_abs_delta_vs_cpu": max(deltas) if deltas else None,
        "ok": bool(deltas) and max(deltas) < 1e-12,
        "S": {n: float(g) for n, g in zip(names, got)},
        "emergence": [n for n, g in zip(names, got) if g > 0],
        "damping": [n for n, g in zip(names, got) if g < 0],
    }


def _gpu_bleed(S_map: dict[str, float], device: str) -> dict[str, Any]:
    """κ_ij bleed on the full pin table. Same law as quantum_bleed. GPU tensor."""
    import torch

    names = sorted(S_map)
    n = len(names)
    d = torch.device(device if device.startswith("cuda") else "cpu")
    S = torch.tensor([S_map[k] for k in names], dtype=torch.float64, device=d)
    D = torch.tensor([float(DOMAINS[k].D_eff) for k in names], dtype=torch.float64, device=d)
    Si = S.abs().unsqueeze(1)
    Sj = S.abs().unsqueeze(0)
    dist = (D.unsqueeze(1) - D.unsqueeze(0)).abs() / 25.0
    kappa = float(SEEDS.a_bleed) * float(SEEDS.poof) * Si * Sj / (1.0 + dist)
    kappa.fill_diagonal_(0.0)
    # three seed-locked relax steps (mid fold depth = floor(π) = 3)
    gamma = float(SEEDS.gamma)
    Seq = S.clone()
    live = S.clone()
    if device.startswith("cuda"):
        torch.cuda.synchronize()
    t0 = time.perf_counter()
    for _ in range(3):
        flow = torch.matmul(kappa, (live.unsqueeze(0) - live.unsqueeze(1)).T).diag()
        # equivalent pairwise: dSi = Σ_j κ_ij (Sj - Si)
        dS = torch.matmul(kappa, live) - kappa.sum(dim=1) * live
        live = live + dS - gamma * (live - Seq)
    if device.startswith("cuda"):
        torch.cuda.synchronize()
    dt = time.perf_counter() - t0
    wave = (live - Seq).abs()
    return {
        "device": device,
        "seconds": dt,
        "n": n,
        "mean_abs_wave": float(wave.mean()),
        "max_abs_wave": float(wave.max()),
        "kappa_mean": float(kappa.mean()),
        "ok": bool(torch.isfinite(live).all()),
        "S_after": {names[i]: float(live[i]) for i in range(n)},
    }


def _atlas_scan_mp() -> dict[str, Any]:
    files = _discover()
    if not files:
        return {"ok": False, "status": "skip_no_lean_data", "n_files": 0}
    t0 = time.perf_counter()
    workers = max(1, min(8, (os_cpu() or 4)))
    with ProcessPoolExecutor(max_workers=workers) as ex:
        rows = list(ex.map(_scan_one, files, chunksize=8))
    dt = time.perf_counter() - t0
    domains: dict[str, dict[str, Any]] = {}
    n_fail = 0
    for r in rows:
        if not r.get("ok"):
            n_fail += 1
            continue
        if not r.get("replay_ok"):
            n_fail += 1
        name = r.get("domain")
        if name:
            domains[str(name)] = {
                "D_eff": r.get("D_eff"),
                "headline_median_pct": r.get("headline_median_pct"),
                "record_count": r.get("record_count"),
                "replay_ok": r.get("replay_ok"),
            }
    return {
        "ok": n_fail == 0 and len(domains) >= 400,
        "seconds": dt,
        "workers": workers,
        "n_files": len(files),
        "n_domains": len(domains),
        "n_fail": n_fail,
        "D_eff_values": sorted({
            int(v["D_eff"]) for v in domains.values() if v.get("D_eff") is not None
        }),
        "domains": domains,
    }


def os_cpu() -> int:
    import os
    return os.cpu_count() or 1


def why_industry_grows_registers() -> dict[str, Any]:
    """
    Why Hilbert n-scale appears as a need — from the theory, not from RAM tables.

    Quantum_Computing is D=11, observed=False, S<0 (damping).
    Quantum_Mechanics is D=6, observed=True, S>0 (emergence).
    Growing n tries to observe the compute substrate by adding false axes.
    The fold already has D_eff + 35 pin domains + the Lean atlas.
    """
    s_qm = domain_scalar("Quantum_Mechanics")
    s_qc = domain_scalar("Quantum_Computing")
    return {
        "S_Quantum_Mechanics": s_qm,
        "S_Quantum_Computing": s_qc,
        "QM": {
            "D_eff": DOMAINS["Quantum_Mechanics"].D_eff,
            "observed": DOMAINS["Quantum_Mechanics"].observed,
            "role": "measurement / spin law — emergence",
        },
        "QC": {
            "D_eff": DOMAINS["Quantum_Computing"].D_eff,
            "observed": DOMAINS["Quantum_Computing"].observed,
            "role": "compute substrate — damping when forced into observation",
        },
        "n_pin_domains": len(DOMAINS),
        "geometry": "D_eff domain folds + bleed κ_ij",
        "refused_geometry": "Hilbert n-qubit amplitude expansion",
        "statement": (
            "The industry grows registers because it is trying to instantiate "
            "the unobserved compute substrate as an observed Hilbert space. "
            "S(QC)<0 is that damping. The answer is already a fold at D_eff, "
            "bled across the pin table and the Lean atlas — not a larger n."
        ),
        "ok": s_qm > 0 and s_qc < 0 and len(DOMAINS) == 35,
    }


def _routes_clean() -> list[dict[str, Any]]:
    rows = []
    for kind, names in QUESTION_ROUTES.items():
        rows.append({
            "question_kind": kind,
            "route": list(names),
            "D_eff": [DOMAINS[d].D_eff for d in names],
            "observed": [DOMAINS[d].observed for d in names],
            "S": [domain_scalar(d) for d in names],
        })
    return rows


def run_fold_architecture() -> dict[str, Any]:
    device = prefer_device()
    why = why_industry_grows_registers()
    gpu = _gpu_pin_scalars(device)
    bleed = _gpu_bleed(gpu["S"], device) if gpu.get("S") else {"ok": False}
    atlas = _atlas_scan_mp()
    routes = _routes_clean()
    ok = bool(why["ok"] and gpu["ok"] and bleed["ok"] and atlas.get("ok"))
    return {
        "panel": "fold_architecture",
        "pin": "D1D38A",
        "device": device,
        "overall_ok": ok,
        "why_they_grow_n": why,
        "gpu_pin_scalars": {
            "ok": gpu["ok"],
            "device": gpu["device"],
            "n_domains": gpu["n_domains"],
            "seconds": gpu["seconds"],
            "max_abs_delta_vs_cpu": gpu["max_abs_delta_vs_cpu"],
            "n_emergence": len(gpu["emergence"]),
            "n_damping": len(gpu["damping"]),
            "emergence": gpu["emergence"],
            "damping": gpu["damping"],
        },
        "gpu_bleed": {
            "ok": bleed.get("ok"),
            "device": bleed.get("device"),
            "seconds": bleed.get("seconds"),
            "mean_abs_wave": bleed.get("mean_abs_wave"),
            "max_abs_wave": bleed.get("max_abs_wave"),
        },
        "atlas_fabric": {
            "ok": atlas.get("ok"),
            "n_domains": atlas.get("n_domains"),
            "n_files": atlas.get("n_files"),
            "workers": atlas.get("workers"),
            "seconds": atlas.get("seconds"),
            "D_eff_values": atlas.get("D_eff_values"),
        },
        "question_routes": routes,
        "S": gpu.get("S"),
    }


def main() -> int:
    t0 = time.perf_counter()
    panel = run_fold_architecture()
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **panel,
        "wall_seconds": time.perf_counter() - t0,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    # keep json smaller: drop full atlas domain map if present
    (out / "fold_architecture.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    why = report["why_they_grow_n"]
    gpu = report["gpu_pin_scalars"]
    atlas = report["atlas_fabric"]
    md = [
        "# Fold architecture — domain folds on GPU, not Hilbert n",
        "",
        f"**overall_ok:** `{report['overall_ok']}` · pin D1D38A · device `{report['device']}`",
        "",
        "## Why the industry grows registers",
        "",
        why["statement"],
        "",
        f"- S(Quantum_Mechanics) = `{why['S_Quantum_Mechanics']}` · D_eff=6 · observed",
        f"- S(Quantum_Computing) = `{why['S_Quantum_Computing']}` · D_eff=11 · unobserved",
        f"- Pin domains: **{why['n_pin_domains']}**",
        f"- Lean atlas folds: **{atlas.get('n_domains')}** (multiprocess `{atlas.get('workers')}` workers)",
        "",
        "The answering machine is `S = K(T1+T2+T3)` on those folds, bled by "
        "`κ_ij = A_bleed·POOF·|Si||Sj|/(1+|ΔD|/25)`. Not `2^n` amplitudes. Not RAM.",
        "",
        "## GPU pin table",
        "",
        f"- device: `{gpu['device']}` · {gpu['n_domains']} domains · {gpu['seconds']:.4f}s",
        f"- max |S_gpu − S_cpu|: `{gpu['max_abs_delta_vs_cpu']}`",
        f"- emergence (S>0): {gpu['n_emergence']} · damping (S<0): {gpu['n_damping']}",
        f"- bleed mean |ΔS|: `{report['gpu_bleed'].get('mean_abs_wave')}`",
        "",
        "## Question routes (domain folds, not qubit counts)",
        "",
        "| Question | Route | D_eff |",
        "|----------|-------|-------|",
    ]
    for r in report["question_routes"]:
        md.append(
            f"| {r['question_kind']} | {', '.join(r['route'])} | {r['D_eff']} |"
        )
    md += [
        "",
        "```powershell",
        "python -m fsot_quantum.fold_architecture",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "FOLD_ARCHITECTURE.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "FOLD_ARCHITECTURE.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": report["overall_ok"],
        "device": report["device"],
        "n_pin_domains": why["n_pin_domains"],
        "n_atlas_domains": atlas.get("n_domains"),
        "gpu_ok": gpu["ok"],
        "bleed_ok": report["gpu_bleed"].get("ok"),
        "atlas_ok": atlas.get("ok"),
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
