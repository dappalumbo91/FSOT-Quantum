"""
Quantum computing *questions* battery — stress FSOT-QC against real problem classes.

Compares:
  - FSOT path answers
  - Classical exact / full-enumeration truth (n small)
  - Optional tiny complex-amplitude baseline for 1–2 qubit structure checks

No free parameters. Writes results/question_battery.json + QUESTION_BATTERY.md
"""

from __future__ import annotations

import json
import math
import random
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_lib.seeds import COLLAPSE_THRESHOLD, SEEDS
from fsot_lib.trinary import collapse
from fsot_quantum.algorithms import (
    bernstein_vazirani_fsot,
    deutsch_jozsa_fsot,
    grover_fsot_search,
    make_balanced_parity_oracle,
    oracle_constant_one,
    oracle_constant_zero,
)
from fsot_quantum.circuit import Circuit, run_circuit
from fsot_quantum.domains import DOMAIN_COMPUTE, DOMAIN_SPIN_LAW, domain_scalar
from fsot_quantum.gates import apply_cx, h_analog, neg
from fsot_quantum.gpu_parallel import batch_grover_search, prefer_device
from fsot_quantum.measure import measure_register
from fsot_quantum.optimization import (
    cut_value,
    energy_ising,
    exact_ising_ground,
    exact_maxcut,
    fsot_local_spins,
    instance_bank,
    run_instance,
)
from fsot_quantum.register import TritRegister

# Seed RNG from FSOT constant only (reproducible, not a free fit param)
_RNG = random.Random(int(abs(SEEDS.k * 1e12)) % (2**31 - 1))


@dataclass
class QResult:
    id: str
    category: str
    question: str
    expected: Any
    got: Any
    ok: bool
    notes: str = ""


def _bool_stats(rows: list[QResult]) -> dict[str, Any]:
    n = len(rows)
    p = sum(1 for r in rows if r.ok)
    return {"pass": p, "total": n, "accuracy": p / n if n else 0.0}


# ---------------------------------------------------------------------------
# Q1 Deutsch–Jozsa stress
# ---------------------------------------------------------------------------

def q_deutsch_jozsa() -> list[QResult]:
    rows: list[QResult] = []
    # constants
    for n in (2, 4, 6, 8, 10):
        for name, ora in (("const0", oracle_constant_zero), ("const1", oracle_constant_one)):
            r = deutsch_jozsa_fsot(n, ora)
            rows.append(QResult(
                id=f"DJ_{name}_n{n}",
                category="deutsch_jozsa",
                question=f"Is f constant or balanced? (n={n}, {name})",
                expected=r.expected,
                got=r.got,
                ok=r.ok,
                notes="probe-set FSOT class",
            ))
    # balanced parity family
    for n in (3, 5, 8, 12):
        for trial in range(8):
            mask = _RNG.randrange(1, 1 << n)
            r = deutsch_jozsa_fsot(n, make_balanced_parity_oracle(mask))
            rows.append(QResult(
                id=f"DJ_parity_n{n}_m{mask}",
                category="deutsch_jozsa",
                question=f"Classify parity oracle mask={mask:#x} (n={n})",
                expected="balanced",
                got=r.got,
                ok=r.ok and r.got == "balanced",
                notes="parity balanced",
            ))
    # adversarial: almost-constant (only one point differs) — hard for incomplete probes
    def almost_const(n: int, flip_x: int) -> Callable:
        def f(bits):
            x = sum(int(b) << i for i, b in enumerate(bits))
            return 1 if x == flip_x else 0
        return f

    for n in (4, 6):
        flip = _RNG.randrange(0, 1 << n)
        # truth is balanced if not constant — almost-const with one 1 is balanced
        r = deutsch_jozsa_fsot(n, almost_const(n, flip))
        # full truth
        vals = {almost_const(n, flip)([(x >> i) & 1 for i in range(n)]) for x in range(1 << n)}
        truth = "constant" if len(vals) == 1 else "balanced"
        rows.append(QResult(
            id=f"DJ_almost_const_n{n}_flip{flip}",
            category="deutsch_jozsa_adversarial",
            question=f"Classify almost-constant (one flip at {flip}, n={n})",
            expected=truth,
            got=r.got,
            ok=r.got == truth,
            notes="ADVERSARIAL: probe set may miss single flip — expected weak point",
        ))
    return rows


# ---------------------------------------------------------------------------
# Q2 Bernstein–Vazirani
# ---------------------------------------------------------------------------

def q_bernstein_vazirani() -> list[QResult]:
    rows: list[QResult] = []
    for n in (4, 8, 12, 16, 20):
        for trial in range(10):
            secret = [_RNG.randint(0, 1) for _ in range(n)]
            r = bernstein_vazirani_fsot(secret)
            rows.append(QResult(
                id=f"BV_n{n}_t{trial}",
                category="bernstein_vazirani",
                question=f"Recover secret s (n={n}): {secret}",
                expected=secret,
                got=r.got,
                ok=r.ok,
            ))
    return rows


# ---------------------------------------------------------------------------
# Q3 Grover / unstructured search
# ---------------------------------------------------------------------------

def q_grover() -> list[QResult]:
    rows: list[QResult] = []
    for N in (16, 64, 256, 1024, 4096, 16384):
        for trial in range(12):
            marked = _RNG.randrange(0, N)
            r = grover_fsot_search(N, marked)
            rows.append(QResult(
                id=f"GROVER_N{N}_m{marked}",
                category="grover_search",
                question=f"Find marked index in N={N} (marked={marked})",
                expected=marked,
                got=r.got,
                ok=r.ok,
                notes="collapse marked pole",
            ))
    # batch GPU
    for N, B in ((512, 200), (2048, 100), (8192, 50)):
        marked_list = [_RNG.randrange(0, N) for _ in range(B)]
        br = batch_grover_search(N, marked_list)
        rows.append(QResult(
            id=f"GROVER_BATCH_N{N}_B{B}",
            category="grover_batch_gpu",
            question=f"Batch find {B} marked items in N={N} on GPU",
            expected=B,
            got=br.get("correct"),
            ok=bool(br.get("ok")),
            notes=f"acc={br.get('accuracy')} ips={br.get('instances_per_sec')}",
        ))
    return rows


# ---------------------------------------------------------------------------
# Q4 Bell / GHZ structure
# ---------------------------------------------------------------------------

def q_entanglement_structure() -> list[QResult]:
    rows: list[QResult] = []
    # Bell agreement rate
    trials = 200
    agree = 0
    for _ in range(trials):
        reg = TritRegister.from_bits([0, 0], domain=DOMAIN_COMPUTE)
        out = run_circuit(reg, Circuit(2).h(0).cx(0, 1).measure(0, 1))
        if out.spins[0] == out.spins[1]:
            agree += 1
    rate = agree / trials
    rows.append(QResult(
        id="BELL_AGREE_200",
        category="entanglement",
        question="Bell-analog: after H·CX·measure, do spins agree? (200 trials)",
        expected=1.0,
        got=rate,
        ok=rate >= 0.99,
        notes="deterministic domain resolve",
    ))
    # GHZ-3: all measured same class
    reg = TritRegister.from_bits([0, 0, 0], domain=DOMAIN_COMPUTE)
    out = run_circuit(reg, Circuit(3).h(0).cx(0, 1).cx(1, 2).measure(0, 1, 2))
    same = out.spins[0] == out.spins[1] == out.spins[2]
    rows.append(QResult(
        id="GHZ3_STRUCTURE",
        category="entanglement",
        question="GHZ-3 analog: all three measured spins equal?",
        expected=True,
        got=same,
        ok=same,
        notes=f"spins={out.spins}",
    ))
    # CX truth table on eigenstates (classical reversible fragment)
    cases = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    cx_ok = 0
    for c, t in cases:
        # control +1 flips, -1 holds, 0 super
        nt = apply_cx(c, t)
        if c == 1:
            exp = -t
        elif c == -1:
            exp = t
        else:
            exp = 0
        if nt == exp:
            cx_ok += 1
    rows.append(QResult(
        id="CX_TRUTH_TABLE",
        category="gates",
        question="CX truth table on ±1 eigenstates",
        expected=4,
        got=cx_ok,
        ok=cx_ok == 4,
    ))
    return rows


# ---------------------------------------------------------------------------
# Q5 Phase / domain S questions (FSOT-native QC observables)
# ---------------------------------------------------------------------------

def q_phase_domain() -> list[QResult]:
    rows: list[QResult] = []
    s_qm = domain_scalar(DOMAIN_SPIN_LAW)
    s_qc = domain_scalar(DOMAIN_COMPUTE)
    rows.append(QResult(
        id="PHASE_S_QM_POSITIVE",
        category="phase_class",
        question="Is S(Quantum_Mechanics) positive (emergence under observation)?",
        expected=True,
        got=s_qm > 0,
        ok=s_qm > 0,
        notes=f"S_QM={s_qm}",
    ))
    rows.append(QResult(
        id="PHASE_S_QC_NEGATIVE",
        category="phase_class",
        question="Is S(Quantum_Computing) negative (compute substrate damping)?",
        expected=True,
        got=s_qc < 0,
        ok=s_qc < 0,
        notes=f"S_QC={s_qc}",
    ))
    rows.append(QResult(
        id="COLLAPSE_THRESHOLD_RANGE",
        category="phase_class",
        question="Is Θ=C_eff·P_var in (0,1)?",
        expected=True,
        got=0 < COLLAPSE_THRESHOLD < 1,
        ok=0 < COLLAPSE_THRESHOLD < 1,
        notes=f"Θ={COLLAPSE_THRESHOLD}",
    ))
    return rows


# ---------------------------------------------------------------------------
# Q6 Optimization (Ising / MaxCut) random + bank
# ---------------------------------------------------------------------------

def q_optimization() -> list[QResult]:
    rows: list[QResult] = []
    for inst in instance_bank():
        r = run_instance(inst)
        rows.append(QResult(
            id=f"OPT_{inst.name}",
            category="optimization_bank",
            question=f"Solve {inst.kind} instance {inst.name} exactly?",
            expected=r.get("E_exact", r.get("cut_exact")),
            got=r.get("E_fsot", r.get("cut_fsot")),
            ok=bool(r.get("ok")),
            notes=f"residual%={r.get('residual_pct')}",
        ))
    # random Ising n=8
    for trial in range(15):
        n = 8
        edges = []
        for i in range(n):
            j = (i + 1) % n
            J = 1 if _RNG.random() < 0.5 else -1
            edges.append((i, j, J))
        # a few chords
        for _ in range(3):
            a, b = _RNG.sample(range(n), 2)
            if a > b:
                a, b = b, a
            edges.append((a, b, 1 if _RNG.random() < 0.5 else -1))
        from fsot_quantum.optimization import solve_ising

        exact_e, _ = exact_ising_ground(n, edges)
        spins, got_e, method = solve_ising(n, edges)
        rows.append(QResult(
            id=f"ISING_RAND8_t{trial}",
            category="optimization_random",
            question=f"Random Ising n=8 ground energy (trial {trial})",
            expected=exact_e,
            got=got_e,
            ok=got_e == exact_e,
            notes=f"Δ={got_e - exact_e} method={method}",
        ))
    # random MaxCut n=10
    for trial in range(10):
        n = 10
        edges = []
        for i in range(n):
            edges.append((i, (i + 1) % n, 1))
        for _ in range(5):
            a, b = _RNG.sample(range(n), 2)
            if a > b:
                a, b = b, a
            edges.append((a, b, 1))
        from fsot_quantum.optimization import solve_maxcut

        exact_c, _ = exact_maxcut(n, edges)
        spins, got_c, method = solve_maxcut(n, edges)
        rows.append(QResult(
            id=f"MAXCUT_RAND10_t{trial}",
            category="optimization_random",
            question=f"Random MaxCut n=10 (trial {trial})",
            expected=exact_c,
            got=got_c,
            ok=got_c == exact_c,
            notes=f"gap={exact_c - got_c} method={method}",
        ))
    return rows


# ---------------------------------------------------------------------------
# Q7 Gate algebra / circuit questions
# ---------------------------------------------------------------------------

def q_gate_algebra() -> list[QResult]:
    rows: list[QResult] = []
    # X twice = I
    ok_x2 = all(neg(neg(t)) == t for t in (-1, 0, 1))
    rows.append(QResult("GATE_X2_I", "gates", "Does X·X = I on trits?", True, ok_x2, ok_x2))
    # H maps poles to super
    ok_h = all(h_analog(t, DOMAIN_SPIN_LAW) == 0 for t in (-1, 1))
    rows.append(QResult("GATE_H_POLE", "gates", "Does H send ±1 → superposed?", True, ok_h, ok_h))
    # H on super: domain S sign (QM >0 → +1, QC <0 → −1)
    h_qm = h_analog(0, DOMAIN_SPIN_LAW)
    h_qc = h_analog(0, DOMAIN_COMPUTE)
    rows.append(QResult(
        "GATE_H_SUPER_QM", "gates",
        "H(0) under Quantum_Mechanics → +1 (emergence)?",
        1, h_qm, h_qm == 1,
    ))
    rows.append(QResult(
        "GATE_H_SUPER_QC", "gates",
        "H(0) under Quantum_Computing → −1 (damping)?",
        -1, h_qc, h_qc == -1,
    ))
    # Toffoli: both up flips target
    from fsot_quantum.gates import apply_ccx
    rows.append(QResult(
        "GATE_CCX", "gates",
        "CCX(1,1,-1) → +1?",
        1, apply_ccx(1, 1, -1), apply_ccx(1, 1, -1) == 1,
    ))
    return rows


# ---------------------------------------------------------------------------
# Q8 Collapse numerics (quantum measurement analog)
# ---------------------------------------------------------------------------

def q_collapse() -> list[QResult]:
    rows: list[QResult] = []
    thr = COLLAPSE_THRESHOLD
    cases = [
        (thr + 0.01, 2, "just above Θ → up code"),
        (-(thr + 0.01), 0, "just below −Θ → down code"),
        (0.0, 1, "zero → superposed"),
        (thr * 0.5, 1, "half Θ → superposed"),
        (1.0, 2, "unit pole → up"),
        (-1.0, 0, "unit pole → down"),
    ]
    field = [c[0] for c in cases]
    codes = collapse(field)
    if hasattr(codes, "tolist"):
        codes = [int(x) for x in codes.tolist()]
    else:
        codes = [int(x) for x in codes]
    for i, (v, exp, desc) in enumerate(cases):
        rows.append(QResult(
            id=f"COLLAPSE_{i}",
            category="measurement",
            question=f"collapse({v:.6f}): {desc}",
            expected=exp,
            got=codes[i],
            ok=codes[i] == exp,
        ))
    return rows


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_question_battery() -> dict[str, Any]:
    t0 = time.perf_counter()
    all_rows: list[QResult] = []
    all_rows += q_deutsch_jozsa()
    all_rows += q_bernstein_vazirani()
    all_rows += q_grover()
    all_rows += q_entanglement_structure()
    all_rows += q_phase_domain()
    all_rows += q_optimization()
    all_rows += q_gate_algebra()
    all_rows += q_collapse()

    by_cat: dict[str, list[QResult]] = {}
    for r in all_rows:
        by_cat.setdefault(r.category, []).append(r)

    categories = {c: _bool_stats(rs) for c, rs in sorted(by_cat.items())}
    overall = _bool_stats(all_rows)

    # Refinement flags: categories below 100% or adversarial fails
    refine: list[str] = []
    for c, st in categories.items():
        if st["accuracy"] < 1.0:
            refine.append(f"{c}: {st['pass']}/{st['total']} ({100*st['accuracy']:.1f}%)")
    fails = [asdict(r) for r in all_rows if not r.ok]

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "device": prefer_device(),
        "pin": "D1D38A",
        "collapse_threshold": COLLAPSE_THRESHOLD,
        "S_QM": domain_scalar(DOMAIN_SPIN_LAW),
        "S_QC": domain_scalar(DOMAIN_COMPUTE),
        "overall": overall,
        "categories": categories,
        "failures": fails,
        "refine_priority": refine,
        "wall_seconds": time.perf_counter() - t0,
        "questions": [asdict(r) for r in all_rows],
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "question_battery.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# FSOT-QC Question Battery",
        "",
        f"**overall:** {overall['pass']}/{overall['total']} "
        f"({100*overall['accuracy']:.2f}%)",
        f"**device:** `{report['device']}`",
        f"**wall_s:** `{report['wall_seconds']:.3f}`",
        "",
        "## By category",
        "",
        "| Category | Pass | Total | Accuracy |",
        "|----------|-----:|------:|---------:|",
    ]
    for c, st in categories.items():
        md.append(f"| {c} | {st['pass']} | {st['total']} | {100*st['accuracy']:.1f}% |")
    md += ["", "## Failures (refine targets)", ""]
    if not fails:
        md.append("_None — full pass._")
    else:
        for f in fails:
            md.append(f"- **{f['id']}**: expected `{f['expected']}` got `{f['got']}` — {f['notes']}")
    md += ["", "## Refine priority", ""]
    if not refine:
        md.append("_No category below 100%._")
    else:
        for line in refine:
            md.append(f"- {line}")
    md += [
        "",
        "## Reproduce",
        "",
        "```powershell",
        'cd "C:\\Users\\damia\\Desktop\\fsot quantum"',
        "$env:PYTHONPATH = (Get-Location).Path",
        "python -m fsot_quantum.question_battery",
        "```",
        "",
    ]
    (out / "QUESTION_BATTERY.md").write_text("\n".join(md), encoding="utf-8")
    return report


def main() -> int:
    report = run_question_battery()
    print(json.dumps({
        "overall": report["overall"],
        "categories": report["categories"],
        "refine_priority": report["refine_priority"],
        "n_failures": len(report["failures"]),
        "wall_seconds": report["wall_seconds"],
        "device": report["device"],
    }, indent=2))
    if report["failures"]:
        print("\nFAILURES:")
        for f in report["failures"][:30]:
            print(f"  {f['id']}: exp={f['expected']} got={f['got']} | {f['notes']}")
    print("wrote results/question_battery.json")
    print("wrote results/QUESTION_BATTERY.md")
    return 0 if report["overall"]["accuracy"] == 1.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
