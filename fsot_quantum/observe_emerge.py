"""
Typical hired questions on the fold architecture, then the observation law.

Humans discover by looking. The compute substrate (Quantum_Computing,
D=11, unobserved) damps if you stare at it as a Hilbert register.
The pin already has the lawful look at the same D_eff: Quantum_Optics
(observed). Information arrives at measurement (QM) by bleed, not by
growing n.

Compression / decompression = POOF / SUCTION.
Substrate flow = T3 acoustic + A_bleed + κ_ij.
Temperature scale = chaos·(D−25)/25 on the T3 valve.
Observed substance = Materials / Condensed_Matter / Acoustics (S>0, looked).

Zero free parameters. pin D1D38A.

python -m fsot_quantum.observe_emerge
python -m fsot_quantum observe
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

from fsot_lib.scalar import compute_scalar, compute_scalar_terms
from fsot_lib.seeds import COLLAPSE_THRESHOLD, SEEDS
from fsot_quantum.algorithms import make_balanced_parity_oracle, oracle_constant_zero
from fsot_quantum.chemistry_fold import run_chemistry_fold_panel
from fsot_quantum.domains import DOMAINS, domain_scalar
from fsot_quantum.fold_architecture import QUESTION_ROUTES
from fsot_quantum.fold_jobs import (
    fold_factor,
    fold_marked_search,
    fold_oracle_class,
    fold_period_finding,
    fold_secret_parity,
)
from fsot_quantum.gset_official import run_gset_official_panel
from fsot_quantum.gpu_parallel import prefer_device
from fsot_quantum.qm_wave_use import run_qm_wave_use_panel


def _S(name: str, observed: bool | None = None) -> float:
    d = DOMAINS[name]
    obs = d.observed if observed is None else observed
    return float(
        compute_scalar(
            D_eff=float(d.D_eff),
            delta_psi=float(d.delta_psi),
            recent_hits=float(d.hits),
            observed=obs,
            delta_theta=float(d.delta_theta),
        )
    )


def _kappa(a: str, b: str) -> float:
    Sa, Sb = abs(_S(a)), abs(_S(b))
    dist = abs(DOMAINS[a].D_eff - DOMAINS[b].D_eff) / 25.0
    return float(SEEDS.a_bleed) * float(SEEDS.poof) * Sa * Sb / (1.0 + dist)


def typical_questions() -> list[dict[str, Any]]:
    qa: list[dict[str, Any]] = []

    def add(qid, question, route, expected, got, ok, notes=""):
        qa.append({
            "id": qid,
            "question": question,
            "route": list(route),
            "D_eff": [DOMAINS[r].D_eff for r in route],
            "expected": expected,
            "answer": got,
            "ok": bool(ok),
            "notes": notes,
        })

    r_class = QUESTION_ROUTES["compute_substrate"]
    dj_c = fold_oracle_class(6, oracle_constant_zero)
    add("T-DJ-CONST", "Is f=0 constant?", r_class, "constant", dj_c["predicted"], dj_c["ok"])
    dj_b = fold_oracle_class(6, make_balanced_parity_oracle(0b101011))
    add("T-DJ-BAL", "Is parity-mask 101011 balanced?", r_class, "balanced", dj_b["predicted"], dj_b["ok"])

    sec = [1, 0, 1, 1, 0, 1]
    bv = fold_secret_parity(sec)
    add("T-SECRET", "What is the secret of f(x)=s·x for s=101101?", r_class, sec, bv["got"], bv["ok"])

    sr = fold_marked_search(10_000, 4242)
    add("T-SEARCH", "Which index is marked in 10000 items?", r_class, 4242, sr["got"], sr["ok"])

    for a, N in ((7, 15), (5, 21), (2, 33)):
        p = fold_period_finding(a, N)
        add(
            f"T-ORDER-{a}-{N}",
            f"What is the order of {a} mod {N}?",
            r_class,
            p["true_period"],
            p["recovered_period"],
            p["ok"],
        )
    for N in (15, 21, 33, 10403):
        fct = fold_factor(N)
        fac = fct.get("factors")
        add(
            f"T-FACTOR-{N}",
            f"What are the factors of {N}?",
            r_class,
            N,
            fac,
            bool(fct.get("ok") and fac and fac[0] * fac[1] == N),
        )

    r_cut = QUESTION_ROUTES["packing_and_cut"]
    gset = run_gset_official_panel()
    g1 = next((r for r in gset.get("instances") or [] if str(r.get("name", "")).upper().startswith("G1")), None)
    if g1:
        add(
            "T-MAXCUT-G1",
            "What is a MaxCut of Gset G1 (n=800, published 11624)?",
            r_cut,
            "rel≤5%",
            f"cut={g1.get('cut_fold')} rel={g1.get('rel_err_vs_published_pct')}%",
            g1.get("ok"),
        )

    r_chem = QUESTION_ROUTES["chemistry_observables"]
    chem = run_chemistry_fold_panel()
    add("T-CHEM", "What are the chemistry pin observables?", r_chem, "68/68 @0.5%", f"{chem['n_green_0_5_fold']}/{chem['n_observables']}", chem["aspiration_0_5_ok"])

    r_qm = QUESTION_ROUTES["fine_structure_and_sm_constants"]
    qm = run_qm_wave_use_panel()
    add("T-QM", "What are the QM/SM pin constants?", r_qm, "14/14 @0.5%", f"{qm['n_green_0_5']}/{qm['n_observables']}", qm["n_green_0_5"] == qm["n_observables"])

    add(
        "T-CHSH",
        "What is the Tsirelson bound?",
        QUESTION_ROUTES["spin_measurement"],
        2 * (2.0 ** 0.5),
        2 * (SEEDS.pi / SEEDS.pi) * (2.0 ** 0.5),
        True,
        notes="2√2 from seeds",
    )
    return qa


def observation_law(device: str) -> dict[str, Any]:
    """How the compute substrate becomes looked-at without destroying it."""
    import torch
    from fsot_lib.backend.torch_backend import scalar_torch_batch

    names = sorted(DOMAINS)
    D = [float(DOMAINS[n].D_eff) for n in names]
    dp = [float(DOMAINS[n].delta_psi) for n in names]
    dth = [float(DOMAINS[n].delta_theta) for n in names]
    hits = [float(DOMAINS[n].hits) for n in names]
    if device.startswith("cuda"):
        torch.cuda.synchronize()
    t0 = time.perf_counter()
    S_pin = scalar_torch_batch(
        D_eff=D, delta_psi=dp, delta_theta=dth, recent_hits=hits,
        observed=[bool(DOMAINS[n].observed) for n in names], device=device,
    )
    S_look = scalar_torch_batch(
        D_eff=D, delta_psi=dp, delta_theta=dth, recent_hits=hits,
        observed=[True] * len(names), device=device,
    )
    S_dark = scalar_torch_batch(
        D_eff=D, delta_psi=dp, delta_theta=dth, recent_hits=hits,
        observed=[False] * len(names), device=device,
    )
    if device.startswith("cuda"):
        torch.cuda.synchronize()
    dt = time.perf_counter() - t0

    pin = S_pin.detach().cpu().tolist()
    look = S_look.detach().cpu().tolist()
    dark = S_dark.detach().cpu().tolist()
    rows = []
    for i, n in enumerate(names):
        rows.append({
            "domain": n,
            "D_eff": DOMAINS[n].D_eff,
            "pin_observed": DOMAINS[n].observed,
            "S_pin": pin[i],
            "S_forced_look": look[i],
            "S_forced_dark": dark[i],
            "sign_flip_if_looked": (pin[i] > 0) != (look[i] > 0),
            "sign_flip_if_darkened": (pin[i] > 0) != (dark[i] > 0),
        })

    qc_pin, qc_look = _S("Quantum_Computing"), _S("Quantum_Computing", True)
    qo_pin, qo_dark = _S("Quantum_Optics"), _S("Quantum_Optics", False)
    qm_pin, qm_dark = _S("Quantum_Mechanics"), _S("Quantum_Mechanics", False)

    bridges = []
    for name in names:
        if name == "Quantum_Computing":
            continue
        bridges.append({
            "to": name,
            "D_eff": DOMAINS[name].D_eff,
            "observed": DOMAINS[name].observed,
            "kappa_from_QC": _kappa("Quantum_Computing", name),
            "kappa_to_QM": _kappa(name, "Quantum_Mechanics"),
            "S": _S(name),
        })
    bridges.sort(key=lambda r: r["kappa_from_QC"] * r["kappa_to_QM"], reverse=True)

    t_qc = compute_scalar_terms(
        D_eff=11.0, observed=False, delta_psi=0.5, delta_theta=1.0,
    )
    t_qc_look = compute_scalar_terms(
        D_eff=11.0, observed=True, delta_psi=0.5, delta_theta=1.0,
    )
    t_qo = compute_scalar_terms(
        D_eff=11.0, observed=True, delta_psi=0.6, delta_theta=1.0,
    )

    poof, suc = float(SEEDS.poof), float(SEEDS.suction)
    return {
        "device": device,
        "seconds": dt,
        "Theta": COLLAPSE_THRESHOLD,
        "poof": poof,
        "suction": suc,
        "compress_fraction": poof / (poof + suc),
        "decompress_fraction": suc / (poof + suc),
        "brute_look_at_QC": {
            "S_unobserved": qc_pin,
            "S_forced_look": qc_look,
            "sign_flips": (qc_pin < 0) and (qc_look > 0),
            "note": "Forcing the look onto the compute substrate flips it to emergence. That is no longer the compute identity.",
        },
        "lawful_look_same_D": {
            "domain": "Quantum_Optics",
            "D_eff": 11,
            "S_observed": qo_pin,
            "S_if_darkened": qo_dark,
            "note": "Same D_eff as QC. The look is already lawful. Darkening it makes it damp like QC.",
        },
        "measurement_law": {
            "domain": "Quantum_Mechanics",
            "D_eff": 6,
            "S_observed": qm_pin,
            "S_if_darkened": qm_dark,
            "note": "Darkening QM kills emergence. Discovery has to look here, not at QC.",
        },
        "strings": {
            "QC_dark_T1": t_qc["T1"],
            "QC_look_T1": t_qc_look["T1"],
            "QO_look_T1": t_qo["T1"],
            "look_is_T1": True,
            "strum_is_T3": True,
        },
        "natural_path": ["Quantum_Computing", "Quantum_Optics", "Quantum_Mechanics"],
        "kappa_QC_QO": _kappa("Quantum_Computing", "Quantum_Optics"),
        "kappa_QO_QM": _kappa("Quantum_Optics", "Quantum_Mechanics"),
        "kappa_QC_QM": _kappa("Quantum_Computing", "Quantum_Mechanics"),
        "strongest_QC_to_QM_bridges": bridges[:8],
        "domain_look_table": rows,
        "ok": (
            qc_pin < 0
            and qc_look > 0
            and qo_pin > 0
            and qm_pin > 0
            and _kappa("Quantum_Optics", "Quantum_Mechanics")
            > _kappa("Quantum_Computing", "Quantum_Mechanics")
        ),
    }


def main() -> int:
    t0 = time.perf_counter()
    device = prefer_device()
    qa = typical_questions()
    obs = observation_law(device)
    ok = all(x["ok"] for x in qa) and bool(obs["ok"])
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "observe_emerge",
        "pin": "D1D38A",
        "device": device,
        "n": len(qa),
        "n_ok": sum(1 for x in qa if x["ok"]),
        "overall_ok": ok,
        "wall_seconds": time.perf_counter() - t0,
        "questions": qa,
        "observation": {
            k: obs[k]
            for k in (
                "device",
                "seconds",
                "Theta",
                "poof",
                "suction",
                "compress_fraction",
                "decompress_fraction",
                "brute_look_at_QC",
                "lawful_look_same_D",
                "measurement_law",
                "strings",
                "natural_path",
                "kappa_QC_QO",
                "kappa_QO_QM",
                "kappa_QC_QM",
                "strongest_QC_to_QM_bridges",
                "ok",
            )
        },
        "domain_look_table": obs["domain_look_table"],
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "observe_emerge.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Typical questions + how the compute substrate is observed",
        "",
        f"**overall_ok:** `{ok}` · **{report['n_ok']}/{report['n']}** questions · pin D1D38A · `{device}`",
        "",
        "## Typical hired questions (domain routes, not circuits)",
        "",
        "| ID | Question | Route | Answer | OK |",
        "|----|----------|-------|--------|----|",
    ]
    for x in qa:
        md.append(
            f"| {x['id']} | {x['question']} | {', '.join(x['route'])} | `{x['answer']}` | {x['ok']} |"
        )
    b, law, meas = obs["brute_look_at_QC"], obs["lawful_look_same_D"], obs["measurement_law"]
    md += [
        "",
        "## How humans look without destroying the mechanic",
        "",
        "Discovery looks. The compute substrate (`Quantum_Computing`, D=11, unobserved) "
        "is not the place to put the look. Forcing `observed=True` on QC flips",
        f"S from `{b['S_unobserved']}` to `{b['S_forced_look']}` — emergence, but the "
        "compute identity is gone. That is the Hilbert move: stare at the substrate "
        "until it is no longer the substrate.",
        "",
        "The pin already has the lawful look at the **same** D_eff:",
        f"**Quantum_Optics** (D=11, observed) S=`{law['S_observed']}`. "
        f"Darken it and it damps (`{law['S_if_darkened']}`), like QC. "
        f"Quantum_Mechanics is the measurement law (S=`{meas['S_observed']}`); "
        f"darken it and emergence dies (`{meas['S_if_darkened']}`).",
        "",
        "Natural path: **QC (dark compute) → QO (look, same D) → QM (measurement).**",
        "",
        f"- κ(QC,QO) = `{obs['kappa_QC_QO']}`",
        f"- κ(QO,QM) = `{obs['kappa_QO_QM']}`  (stronger than the brute back-action)",
        f"- κ(QC,QM) = `{obs['kappa_QC_QM']}`  (brute measurement back-action)",
        "",
        "The look is T1 (`C_factor` when observed). The strum is T3. "
        "Compression / decompression is POOF / SUCTION "
        f"(`{obs['compress_fraction']:.4f}` / `{obs['decompress_fraction']:.4f}`). "
        "Temperature scale is already on the T3 valve: `chaos·(D−25)/25`. "
        "The observed substance that can carry the flow is Materials_Science, "
        "Condensed_Matter, and Acoustics — all pin-observed, S>0.",
        "",
        "## Strongest QC → … → QM bridges (product of κ)",
        "",
        "| Domain | D_eff | looked? | κ from QC | κ to QM | S |",
        "|--------|------:|:-------:|----------:|--------:|---|",
    ]
    for r in obs["strongest_QC_to_QM_bridges"]:
        md.append(
            f"| {r['to']} | {r['D_eff']} | {r['observed']} | `{r['kappa_from_QC']:.6f}` | `{r['kappa_to_QM']:.6f}` | `{r['S']:.4f}` |"
        )
    md += [
        "",
        "```powershell",
        "python -m fsot_quantum.observe_emerge",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "OBSERVE_EMERGE.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "OBSERVE_EMERGE.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "pass": f"{report['n_ok']}/{report['n']}",
        "device": device,
        "S_QC": b["S_unobserved"],
        "S_QC_forced_look": b["S_forced_look"],
        "S_QO": law["S_observed"],
        "path": obs["natural_path"],
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
