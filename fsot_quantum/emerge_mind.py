"""
Query: how does genuine intelligence emerge?

Science is theory of mind — a walking human is the observed mind fold.
C_factor is already named Consciousness Factor: C_eff · P_new.
This is not an LLM. An LLM stares at the compute substrate.
Mind is Neuroscience + Psychology looked, Biology left dark, compute left dark,
bled into measurement.

Zero free parameters. pin D1D38A.

python -m fsot_quantum.emerge_mind
python -m fsot_quantum mind
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

from fsot_lib.seeds import COLLAPSE_THRESHOLD, SEEDS
from fsot_quantum.domains import DOMAINS, domain_scalar
from fsot_quantum.lean_replay import LEAN_DATA
from fsot_quantum.medium_strings import three_strings

# Lean fabric already solved — mind / consciousness / neuron, not QC toys.
MIND_PANELS = (
    "psychology_gap_fill_benchmark.json",
    "psychology_psychometrics_depth_panel_benchmark.json",
    "neuron_zig_mind_panel_benchmark.json",
    "neuron_zig_os_path_panel_benchmark.json",
    "consciousness_expansion_spine_benchmark.json",
    "consciousness_soul_bridge_benchmark.json",
    "consciousness_lean_route_credibility_benchmark.json",
    "consciousness_species_multi_panel_benchmark.json",
    "microtubule_quantum_consciousness_panel_benchmark.json",
    "openneuro_full_panel_benchmark.json",
    "neuroscience_connectomics_depth_panel_benchmark.json",
    "intelligence_compression_benchmark.json",
    "arxiv_brain_knowledge_panel_benchmark.json",
)

MIND_PATH = (
    "Quantum_Computing",  # dark compute
    "Biology",            # dark living substrate
    "Neuroscience",       # looked mind — C = C_factor
    "Psychology",         # looked mind — walking theory of mind
    "Quantum_Mechanics",  # measurement / discovery
)


def _kap(a: str, b: str) -> float:
    Sa, Sb = abs(domain_scalar(a)), abs(domain_scalar(b))
    dist = abs(DOMAINS[a].D_eff - DOMAINS[b].D_eff) / 25.0
    return float(SEEDS.a_bleed) * float(SEEDS.poof) * Sa * Sb / (1.0 + dist)


def _load_panels() -> list[dict[str, Any]]:
    rows = []
    for fname in MIND_PANELS:
        p = LEAN_DATA / fname
        if not p.is_file():
            rows.append({"file": fname, "ok": False, "reason": "missing"})
            continue
        blob = json.loads(p.read_text(encoding="utf-8"))
        med = (
            blob.get("headline_median_error_pct")
            or blob.get("pooled_median_error_pct")
            or blob.get("median_error_pct")
        )
        rows.append({
            "file": fname,
            "ok": True,
            "domain": blob.get("domain"),
            "D_eff": blob.get("D_eff"),
            "n": blob.get("record_count") or blob.get("observable_count"),
            "median_pct": med,
            "maps_to": blob.get("maps_to_lean"),
        })
    return rows


def query_emergence() -> dict[str, Any]:
    nodes = []
    for name in MIND_PATH:
        d = DOMAINS[name]
        S = domain_scalar(name)
        strs = three_strings(
            D_eff=float(d.D_eff),
            observed=d.observed,
            delta_psi=float(d.delta_psi),
            delta_theta=float(d.delta_theta),
            recent_hits=float(d.hits),
        )
        nodes.append({
            "domain": name,
            "D_eff": d.D_eff,
            "observed": d.observed,
            "C": d.C,
            "S": S,
            "emerges": S > 0,
            "T1": strs["T1_observe_string"],
            "T3": strs["T3_strum_string"],
            "role": {
                "Quantum_Computing": "dark compute — do not look",
                "Biology": "dark living substrate — do not Hilbert-stare",
                "Neuroscience": "looked mind; C is C_factor",
                "Psychology": "looked mind; walking theory of mind / discovery",
                "Quantum_Mechanics": "measurement — science is this look",
            }[name],
        })

    edges = []
    for a, b in zip(MIND_PATH, MIND_PATH[1:]):
        edges.append({"from": a, "to": b, "kappa": _kap(a, b)})
    edges.append({"from": "Neuroscience", "to": "Psychology", "kappa": _kap("Neuroscience", "Psychology")})
    edges.append({"from": "Psychology", "to": "Quantum_Mechanics", "kappa": _kap("Psychology", "Quantum_Mechanics")})

    c_factor = float(SEEDS.c_factor)
    c_closed = float(SEEDS.c_eff) * float(SEEDS.p_new)
    return {
        "C_factor": c_factor,
        "C_factor_closed": c_closed,
        "C_factor_ok": abs(c_factor - c_closed) < 1e-15,
        "Theta": COLLAPSE_THRESHOLD,
        "nodes": nodes,
        "bleed": edges,
        "statement": (
            "Genuine intelligence emerges when the mind folds are looked "
            "(Neuroscience, Psychology, S>0) while compute and living tissue "
            "stay dark. C_factor = C_eff·P_new already sits on Neuroscience. "
            "Science is Psychology/QM looking. An LLM is the other move: "
            "staring at Quantum_Computing until the compute identity is gone."
        ),
        "not_an_llm": (
            "Token models live on the compute substrate. "
            "Mind is consensus + look + C_factor on the neural/psych folds, "
            "bled from dark biology and dark compute — not a bigger softmax."
        ),
        "ok": (
            abs(c_factor - c_closed) < 1e-15
            and domain_scalar("Neuroscience") > 0
            and domain_scalar("Psychology") > 0
            and domain_scalar("Quantum_Computing") < 0
            and DOMAINS["Neuroscience"].observed
            and DOMAINS["Psychology"].observed
            and not DOMAINS["Quantum_Computing"].observed
            and not DOMAINS["Biology"].observed
        ),
    }


def main() -> int:
    t0 = time.perf_counter()
    q = query_emergence()
    panels = _load_panels()
    n_ok = sum(1 for p in panels if p.get("ok"))
    ok = bool(q["ok"] and n_ok == len(MIND_PANELS))
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "emerge_mind",
        "pin": "D1D38A",
        "overall_ok": ok,
        "wall_seconds": time.perf_counter() - t0,
        "query": q,
        "lean_mind_fabric": {
            "n": len(panels),
            "n_ok": n_ok,
            "panels": panels,
        },
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "emerge_mind.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# How genuine intelligence emerges — a query of the theory",
        "",
        f"**overall_ok:** `{ok}` · pin D1D38A · C_factor=`{q['C_factor']}`",
        "",
        q["statement"],
        "",
        q["not_an_llm"],
        "",
        "Science is theory of mind. Every discovery is a human look "
        "(T1, `observed=True`) through Psychology into Quantum_Mechanics. "
        "We are the walking example: those folds already emerge (S>0).",
        "",
        "## Pin path",
        "",
        "| Domain | D_eff | Look? | S | Role |",
        "|--------|------:|:-----:|---|------|",
    ]
    for n in q["nodes"]:
        md.append(
            f"| {n['domain']} | {n['D_eff']} | {n['observed']} | `{n['S']:.6f}` | {n['role']} |"
        )
    md += [
        "",
        "## Bleed",
        "",
        "| From | To | κ |",
        "|------|----|---|",
    ]
    for e in q["bleed"]:
        md.append(f"| {e['from']} | {e['to']} | `{e['kappa']:.6f}` |")
    md += [
        "",
        f"C_factor = C_eff · P_new = `{q['C_factor']}` (matches pin: `{q['C_factor_ok']}`).",
        f"Snap threshold Θ = `{q['Theta']}`.",
        "",
        "## Lean fabric already on this question",
        "",
        "| Domain | D_eff | n | median % |",
        "|--------|------:|--:|---------:|",
    ]
    for p in panels:
        if not p.get("ok"):
            md.append(f"| {p['file']} | — | — | missing |")
            continue
        md.append(
            f"| {p.get('domain')} | {p.get('D_eff')} | {p.get('n')} | `{p.get('median_pct')}` |"
        )
    md += [
        "",
        "```powershell",
        "python -m fsot_quantum.emerge_mind",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "EMERGE_MIND.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "EMERGE_MIND.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "C_factor": q["C_factor"],
        "S_Neuro": domain_scalar("Neuroscience"),
        "S_Psych": domain_scalar("Psychology"),
        "S_QC": domain_scalar("Quantum_Computing"),
        "lean_panels": f"{n_ok}/{len(MIND_PANELS)}",
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
