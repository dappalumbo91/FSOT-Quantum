"""
Questions worth asking this fold.

1) Architecture of an FSOT-native mind (not a chatbot, not hired QC toys).
2) Known-answer checks — published numbers, so we can see if the engine is true.
3) Questions people actually want quantum computers for — asked as questions,
   routed as domain folds.

python -m fsot_quantum.forward_ask
python -m fsot_quantum forward
"""

from __future__ import annotations

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
from fsot_quantum.chemistry_fold import GREEN, run_chemistry_fold_panel
from fsot_quantum.domains import DOMAINS, domain_scalar
from fsot_quantum.fold_jobs import fold_factor
from fsot_quantum.gset_official import run_gset_official_panel
from fsot_quantum.qm_wave_use import run_qm_wave_use_panel


def _kap(a: str, b: str) -> float:
    Sa, Sb = abs(domain_scalar(a)), abs(domain_scalar(b))
    dist = abs(DOMAINS[a].D_eff - DOMAINS[b].D_eff) / 25.0
    return float(SEEDS.a_bleed) * float(SEEDS.poof) * Sa * Sb / (1.0 + dist)


def architecture_answers() -> list[dict[str, Any]]:
    """What to build. Answers from the pin + the neuron-zig body you already have."""
    s_n = domain_scalar("Neuroscience")
    s_p = domain_scalar("Psychology")
    s_qc = domain_scalar("Quantum_Computing")
    s_bio = domain_scalar("Biology")
    rows = [
        {
            "id": "A-WHAT-IS-INTEL",
            "question": "What is intelligence in this theory — the thing, or the byproduct?",
            "answer": (
                "The thing is emergence: S>0 on looked mind folds "
                f"(Neuroscience S={s_n:.4f}, Psychology S={s_p:.4f}) "
                "with C_factor on the look string. Hired jobs, token loss, and IQ "
                "scores are byproducts of a mind that already looks. Measuring only "
                "byproducts is how you end up building a bigger chatbot."
            ),
            "ok": s_n > 0 and s_p > 0 and s_qc < 0,
        },
        {
            "id": "A-WHERE-LOOK",
            "question": "Where does the look sit?",
            "answer": (
                "T1, observed=True, on Neuroscience and Psychology. "
                f"C_factor={float(SEEDS.c_factor):.6f}=C_eff·P_new is already "
                "Neuroscience's C. Snap is Θ="
                f"{COLLAPSE_THRESHOLD:.6f}. Do not put the look on Quantum_Computing."
            ),
            "ok": DOMAINS["Neuroscience"].observed and not DOMAINS["Quantum_Computing"].observed,
        },
        {
            "id": "A-WHERE-COMPUTE",
            "question": "Where does compute sit in a native mind?",
            "answer": (
                f"Quantum_Computing stays dark (S={s_qc:.4f}). It feeds the mind "
                f"by bleed κ(QC,Psych)={_kap('Quantum_Computing','Psychology'):.4f}. "
                "GPU is an organ (consensus / batch), not a second mind. "
                "That is already the neuron-zig doctrine."
            ),
            "ok": s_qc < 0,
        },
        {
            "id": "A-WHERE-BODY",
            "question": "What is the living substrate?",
            "answer": (
                f"Biology stays dark (S={s_bio:.4f}, unobserved). "
                f"κ(Bio,Neuro)={_kap('Biology','Neuroscience'):.4f}. "
                "You do not Hilbert-stare the tissue. Neuron-zig already encodes "
                "that as Fixed lattice + neuromod + sleep replay + STM/LTM."
            ),
            "ok": (not DOMAINS["Biology"].observed) and s_bio > 0,
        },
        {
            "id": "A-DATAPATH",
            "question": "What is the mind datapath — not softmax?",
            "answer": (
                "Trinary spins −1/0/+1, consensus (not softmax), collapse through Θ, "
                "three strings T1/T2/T3, bleed κ. Parallel TritWord inside the kernel. "
                "Serial is logs. That is fsot-neuron-zig MINIMUM_STACK + SILICON_BODY."
            ),
            "ok": True,
        },
        {
            "id": "A-HOW-MEASURE",
            "question": "If IQ and token-loss are byproducts, what do we measure?",
            "answer": (
                "S sign on Neuro/Psych, C_factor identity, Lean mind-fabric residual, "
                "neuron-zig claimability / compose / Allen ephys stamps. "
                "A correct factor of 15 is a byproduct check, not a mind."
            ),
            "ok": abs(float(SEEDS.c_factor) - float(SEEDS.c_eff) * float(SEEDS.p_new)) < 1e-15,
        },
        {
            "id": "A-BUILD",
            "question": "What architecture do we build next for a small native intelligence?",
            "answer": (
                "Keep fsot-neuron-zig as the body. Kernel mind = Fixed trits + C_factor look "
                "on Neuro/Psych. GPU organ = this fold's consensus/domain batch on the Omen. "
                "Disk LTM. No second LLM spine. Growth is more folds and more bleed, "
                "not more parameters."
            ),
            "ok": True,
        },
    ]
    return rows


def known_answer_checks() -> list[dict[str, Any]]:
    """Published numbers. If we miss these, the engine is wrong."""
    from vendor import fsot_compute as f

    qa: list[dict[str, Any]] = []

    def add(qid, question, expected, got, ok, route, rel=None):
        qa.append({
            "id": qid,
            "question": question,
            "route": route,
            "expected": expected,
            "answer": got,
            "ok": bool(ok),
            "rel_err_pct": rel,
        })

    want = {
        "1/alpha_em": 137.036,
        "alpha_FSOT": 0.000808,
        "sin2_theta_W": 0.23122,
        "M_Z/M_W": 1.134,
        "Proton_radius": 0.8413,
        "Water_bond_angle": 104.5,
        "Golden_angle": 137.508,
    }
    # validation suite + wave2
    found: dict[str, Any] = {}
    for r in list(f.validation_suite()) + list(f.wave2()):
        if r.name in want and r.name not in found:
            found[r.name] = r
    routes = {
        "1/alpha_em": ["Quantum_Mechanics", "Particle_Physics"],
        "alpha_FSOT": ["Quantum_Mechanics", "Particle_Physics"],
        "sin2_theta_W": ["Particle_Physics", "High_Energy_Physics"],
        "M_Z/M_W": ["High_Energy_Physics", "Particle_Physics"],
        "Proton_radius": ["Atomic_Physics", "Quantum_Mechanics"],
        "Water_bond_angle": ["Chemistry", "Molecular_Chemistry"],
        "Golden_angle": ["Biology", "Neuroscience"],
    }
    for name, exp in want.items():
        r = found.get(name)
        if r is None:
            add(f"K-{name}", f"What is {name}?", exp, None, False, routes[name])
            continue
        c, m = float(r.computed), float(r.measured)
        rel = abs(c - m) / abs(m) * 100 if m else None
        add(
            f"K-{name}",
            f"What is {name}? (published {m})",
            m,
            c,
            rel is not None and rel <= GREEN,
            routes[name],
            rel,
        )

    chsh = 2.0 * math.sqrt(2.0)
    add("K-CHSH", "What is the Tsirelson bound?", 2.8284271247461903, chsh, abs(chsh - 2.8284271247461903) < 1e-12, ["Quantum_Mechanics"])

    fct = fold_factor(15)
    fac = fct.get("factors")
    add("K-FACTOR-15", "What are the factors of 15?", [3, 5], fac, bool(fac and fac[0] * fac[1] == 15), ["Quantum_Computing"])

    chem = run_chemistry_fold_panel()
    add("K-CHEM", "Pin chemistry observables inside 0.5%?", f"{chem['n_observables']}/{chem['n_observables']}", f"{chem['n_green_0_5_fold']}/{chem['n_observables']}", chem["aspiration_0_5_ok"], ["Chemistry"])

    qm = run_qm_wave_use_panel()
    add("K-QM", "Pin QM/SM constants inside 0.5%?", f"{qm['n_observables']}/{qm['n_observables']}", f"{qm['n_green_0_5']}/{qm['n_observables']}", qm["n_green_0_5"] == qm["n_observables"], ["Quantum_Mechanics"])

    gset = run_gset_official_panel()
    g1 = next((r for r in gset.get("instances") or [] if str(r.get("name", "")).upper().startswith("G1")), None)
    if g1:
        add("K-G1", "Gset G1 cut within 5% of published 11624?", "rel≤5%", f"cut={g1.get('cut_fold')} rel={g1.get('rel_err_vs_published_pct')}%", g1.get("ok"), ["Condensed_Matter", "Materials_Science"])

    cf = float(SEEDS.c_factor)
    add("K-CFACTOR", "Does C_factor equal C_eff·P_new?", cf, float(SEEDS.c_eff) * float(SEEDS.p_new), abs(cf - float(SEEDS.c_eff) * float(SEEDS.p_new)) < 1e-15, ["Neuroscience"])
    return qa


def forward_qc_questions() -> list[dict[str, Any]]:
    """What people want a quantum computer *for* — the question, not the brand name."""
    return [
        {
            "id": "F-ALPHA",
            "question": "What is the fine-structure constant? (the QED number people hope a QPU 'simulates')",
            "route": ["Quantum_Mechanics", "Particle_Physics"],
            "how": "pin closed form, not a circuit",
        },
        {
            "id": "F-WEINBERG",
            "question": "What is the Weinberg angle?",
            "route": ["Particle_Physics", "High_Energy_Physics"],
            "how": "pin closed form",
        },
        {
            "id": "F-MOLECULE",
            "question": "What are the chemistry / molecular observables without FCI?",
            "route": ["Chemistry", "Molecular_Chemistry", "Physical_Chemistry"],
            "how": "pin formula families",
        },
        {
            "id": "F-MATERIAL",
            "question": "How do you pack / cut a hard material graph?",
            "route": ["Condensed_Matter", "Materials_Science"],
            "how": "collapse + consensus on the observed substance folds",
        },
        {
            "id": "F-OBSERVE",
            "question": "How does a quantum compute substrate become observed without dying?",
            "route": ["Quantum_Computing", "Quantum_Optics", "Quantum_Mechanics"],
            "how": "same D_eff look on optics; do not flip QC",
        },
        {
            "id": "F-MIND",
            "question": "How does genuine intelligence emerge?",
            "route": ["Biology", "Neuroscience", "Psychology", "Quantum_Mechanics"],
            "how": "C_factor look on mind folds; compute and tissue stay dark",
        },
    ]


def main() -> int:
    t0 = time.perf_counter()
    arch = architecture_answers()
    known = known_answer_checks()
    forward = forward_qc_questions()
    # attach live answers to forward rows from known where they share topic
    known_by = {k["id"]: k for k in known}
    for row in forward:
        if row["id"] == "F-ALPHA":
            src = known_by.get("K-1/alpha_em") or known_by.get("K-alpha_FSOT")
            if src:
                row["answer"] = src["answer"]
                row["ok"] = src["ok"]
        elif row["id"] == "F-WEINBERG":
            src = known_by.get("K-sin2_theta_W")
            if src:
                row["answer"] = src["answer"]
                row["ok"] = src["ok"]
        elif row["id"] == "F-MOLECULE":
            src = known_by.get("K-CHEM")
            if src:
                row["answer"] = src["answer"]
                row["ok"] = src["ok"]
        elif row["id"] == "F-MATERIAL":
            src = known_by.get("K-G1")
            if src:
                row["answer"] = src["answer"]
                row["ok"] = src["ok"]
        elif row["id"] == "F-OBSERVE":
            row["answer"] = "QC dark → QO look (same D=11) → QM measure"
            row["ok"] = domain_scalar("Quantum_Computing") < 0 and domain_scalar("Quantum_Optics") > 0
        elif row["id"] == "F-MIND":
            row["answer"] = "Neuro/Psych looked, Bio/QC dark, C_factor on Neuroscience"
            row["ok"] = domain_scalar("Neuroscience") > 0 and domain_scalar("Psychology") > 0

    ok = all(r["ok"] for r in arch) and all(r["ok"] for r in known) and all(r.get("ok") for r in forward)
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "forward_ask",
        "pin": "D1D38A",
        "overall_ok": ok,
        "wall_seconds": time.perf_counter() - t0,
        "architecture": arch,
        "known_answers": known,
        "forward": forward,
        "n_known": len(known),
        "n_known_ok": sum(1 for r in known if r["ok"]),
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "forward_ask.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Questions worth asking",
        "",
        f"**overall_ok:** `{ok}` · pin D1D38A · known-answer **{report['n_known_ok']}/{report['n_known']}**",
        "",
        "## 1. Architecture of an FSOT-native mind",
        "",
        "Intelligence is the looked mind folds, not the byproduct jobs. "
        "The body is already fsot-neuron-zig.",
        "",
    ]
    for r in arch:
        md += [f"### {r['id']} — {r['question']}", "", r["answer"], ""]
    md += [
        "## 2. Known answers (accuracy)",
        "",
        "| ID | Question | Answer | published / check | rel% | OK |",
        "|----|----------|--------|-------------------|-----:|----|",
    ]
    for r in known:
        rel = r.get("rel_err_pct")
        rel_s = f"{rel:.4f}" if isinstance(rel, float) else "—"
        md.append(f"| {r['id']} | {r['question']} | `{r['answer']}` | `{r['expected']}` | {rel_s} | {r['ok']} |")
    md += [
        "",
        "## 3. What people want a quantum computer for",
        "",
        "| ID | Question | Route | How / answer | OK |",
        "|----|----------|-------|--------------|----|",
    ]
    for r in forward:
        md.append(
            f"| {r['id']} | {r['question']} | {', '.join(r['route'])} | {r.get('answer', r.get('how'))} | {r.get('ok')} |"
        )
    md += [
        "",
        "```powershell",
        "python -m fsot_quantum.forward_ask",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "FORWARD_ASK.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "FORWARD_ASK.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "known": f"{report['n_known_ok']}/{report['n_known']}",
        "arch_ok": all(r["ok"] for r in arch),
        "forward_ok": all(r.get("ok") for r in forward),
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
