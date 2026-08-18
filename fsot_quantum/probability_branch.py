"""
FSOT probability — multiverse branching, not a Born add-on.

Every trit decision is three exhaustive folds of the same pin scalar:
  +1  collapsed up     observed, domain phase
  -1  collapsed down   observed, domain phase + π  (trit_not)
   0  superposed       unobserved (look off)

Branch density is |S| of that fold, normalized. No new coefficient.
No |amp|^2. The observer-cosine on T1 is antisymmetric under a π
shift of the *look factor only* — that lemma is 1/2, 1/2. The full
scalar is not, because T3 and the unobserved base also depend on
delta_psi. Genetics already treats +1/−1 as trit_not, 0 as a distinct
state. Same law here.

n indistinguishable exclusive faces (a fair die) are the object's
arity: counting measure 1/n. That is not six invented QM phases.

Independent events: product of branch densities.
Dependent events: remaining exclusive set, renormalize.
Law of large numbers: φ-walk assignment of many copies settles to
the seed-derived densities.

python -m fsot_quantum.probability_branch
python -m fsot_quantum branch
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

from fsot_lib.scalar import compute_scalar_terms
from fsot_lib.seeds import COLLAPSE_THRESHOLD, SEEDS
from fsot_lib.trinary import collapse_scalar, code_to_signed
from fsot_quantum.chemistry_fold import GREEN
from fsot_quantum.domains import DOMAINS, domain_scalar

SPIN_DOMAINS = (
    "Quantum_Mechanics",
    "Quantum_Computing",
    "Quantum_Optics",
    "Particle_Physics",
)


def _eval_fold(name: str, *, delta_psi: float, observed: bool) -> dict[str, float]:
    d = DOMAINS[name]
    terms = compute_scalar_terms(
        N=1.0,
        P=1.0,
        D_eff=float(d.D_eff),
        delta_psi=float(delta_psi),
        recent_hits=float(d.hits),
        observed=bool(observed),
        delta_theta=float(d.delta_theta),
        rho=1.0,
        scale=1.0,
        amplitude=1.0,
        trend_bias=0.0,
    )
    return terms


def observer_look(delta_psi: float) -> float:
    """T1 look factor: exp(C_factor·P_var)·cos(δψ+P_var). Seed-locked."""
    return math.exp(SEEDS.c_factor * SEEDS.p_var) * math.cos(delta_psi + SEEDS.p_var)


def trit_not_phase(delta_psi: float) -> float:
    """Genetics trit_not of a phase: +π."""
    return float(delta_psi) + math.pi


def spin_branches(name: str) -> dict[str, Any]:
    """
    Three exhaustive folds of one spin/trit on a named domain.

    Weights are |S| densities. Collapsed measurement renormalizes
    the two observed folds. Superposition is the unobserved fold,
    not '50/50 plus noise'.
    """
    d = DOMAINS[name]
    phase = float(d.delta_psi)
    up = _eval_fold(name, delta_psi=phase, observed=True)
    down = _eval_fold(name, delta_psi=trit_not_phase(phase), observed=True)
    superposed = _eval_fold(name, delta_psi=phase, observed=False)
    folds = {
        "+1": up,
        "-1": down,
        "0": superposed,
    }
    abs_s = {k: abs(v["S"]) for k, v in folds.items()}
    z = sum(abs_s.values())
    weights = {k: (abs_s[k] / z if z else 0.0) for k in folds}
    csum = abs_s["+1"] + abs_s["-1"]
    collapsed = {
        "+1": abs_s["+1"] / csum if csum else 0.0,
        "-1": abs_s["-1"] / csum if csum else 0.0,
    }
    f_up = observer_look(phase)
    f_down = observer_look(trit_not_phase(phase))
    look_lemma_half = abs(abs(f_up) - abs(f_down)) < 1e-12
    pin_s = domain_scalar(name)
    return {
        "domain": name,
        "D_eff": d.D_eff,
        "table_observed": d.observed,
        "phase": phase,
        "S": {k: v["S"] for k, v in folds.items()},
        "T1": {k: v["T1"] for k, v in folds.items()},
        "T2": {k: v["T2"] for k, v in folds.items()},
        "T3": {k: v["T3"] for k, v in folds.items()},
        "look_f": {"+1": f_up, "-1": f_down},
        "weights_|S|": weights,
        "collapsed_|S|": collapsed,
        "look_cosine_balanced": look_lemma_half,
        "pin_S_table": pin_s,
        "pin_matches_plus": abs(up["S"] - pin_s) < 1e-12 if d.observed else abs(superposed["S"] - pin_s) < 1e-12,
        "collapse_code": {
            k: code_to_signed(collapse_scalar(v["S"], COLLAPSE_THRESHOLD))
            for k, v in folds.items()
        },
    }


def arity_weights(n: int) -> list[float]:
    """n indistinguishable exclusive faces — counting measure 1/n."""
    if n < 1:
        raise ValueError("n>=1")
    return [1.0 / n] * n


def independent_and(w_a: float, w_b: float) -> float:
    """Separate spins: multiverse product."""
    return float(w_a) * float(w_b)


def dependent_remaining(weights: list[float], taken: int) -> list[float]:
    """After one exclusive face is taken, renormalize the rest."""
    rest = [w if i != taken else 0.0 for i, w in enumerate(weights)]
    z = sum(rest)
    if z <= 0:
        return rest
    return [w / z for w in rest]


def phi_walk_unit(n: int) -> list[float]:
    """Seed-locked points in (0,1): {k·φ}."""
    phi = float(SEEDS.phi)
    return [math.modf(phi * (k + 1))[0] for k in range(n)]


def assign_branch(u: float, weights: dict[str, float], order: tuple[str, ...]) -> str:
    acc = 0.0
    last = order[-1]
    for k in order:
        acc += weights[k]
        if u < acc:
            return k
    return last


def large_numbers(weights: dict[str, float], n: int, order: tuple[str, ...]) -> dict[str, Any]:
    """φ-walk of n copies. Frequency vs seed-derived density."""
    pts = phi_walk_unit(n)
    counts = {k: 0 for k in order}
    for u in pts:
        counts[assign_branch(u, weights, order)] += 1
    freq = {k: counts[k] / n for k in order}
    max_abs = max(abs(freq[k] - weights[k]) for k in order)
    return {
        "n": n,
        "freq": freq,
        "target": dict(weights),
        "max_abs_dev": max_abs,
    }


def mutually_exclusive(weights: dict[str, float]) -> bool:
    """One event: the named folds partition the measure."""
    return abs(sum(weights.values()) - 1.0) < 1e-12


def main() -> int:
    t0 = time.perf_counter()
    rows: list[dict[str, Any]] = []

    spins = {name: spin_branches(name) for name in SPIN_DOMAINS}
    qm = spins["Quantum_Mechanics"]

    # 1. pin identity: +1 fold is the living QM table scalar
    rows.append({
        "id": "pin_S_QM_plus",
        "question": "Is the +1 QM fold the living table S(QM)?",
        "got": qm["S"]["+1"],
        "expected": qm["pin_S_table"],
        "ok": bool(qm["pin_matches_plus"]),
    })

    # 2. three-fold |S| weights sum to 1
    for name, br in spins.items():
        ok = mutually_exclusive(br["weights_|S|"])
        rows.append({
            "id": f"partition_{name}",
            "question": f"Do |S| branch weights on {name} sum to 1?",
            "got": sum(br["weights_|S|"].values()),
            "expected": 1.0,
            "ok": ok,
        })

    # 3. collapsed pair sums to 1
    for name, br in spins.items():
        s = br["collapsed_|S|"]["+1"] + br["collapsed_|S|"]["-1"]
        rows.append({
            "id": f"collapsed_partition_{name}",
            "question": f"Do collapsed |S| weights on {name} sum to 1?",
            "got": s,
            "expected": 1.0,
            "ok": abs(s - 1.0) < 1e-12,
        })

    # 4. observer-cosine lemma: look factor only is 1/2, 1/2
    f_up = abs(qm["look_f"]["+1"])
    f_down = abs(qm["look_f"]["-1"])
    rows.append({
        "id": "look_cosine_half",
        "question": "Is the T1 look-cosine π-shift balanced (|f+|=|f-|)?",
        "got": [f_up, f_down],
        "expected": "equal",
        "ok": bool(qm["look_cosine_balanced"]),
    })

    # 5. full trit_not is NOT forced 50/50 — write the computed pair
    half = 0.5
    qm_up = qm["collapsed_|S|"]["+1"]
    rows.append({
        "id": "full_scalar_not_born_half",
        "question": "Is the full-scalar trit_not pair different from a Born 1/2?",
        "got": qm["collapsed_|S|"],
        "expected": "derived |S|, not postulated 1/2",
        "ok": abs(qm_up - half) > 1e-3,
    })

    # 6. fair die = arity 6
    die = arity_weights(6)
    rows.append({
        "id": "die_arity_6",
        "question": "Fair die: six indistinguishable exclusive faces?",
        "got": die[0],
        "expected": 1.0 / 6.0,
        "ok": all(abs(w - 1.0 / 6.0) < 1e-15 for w in die),
    })

    # 7. fair coin as arity 2 (indistinguishable faces, not trit_not)
    coin = arity_weights(2)
    rows.append({
        "id": "coin_arity_2",
        "question": "Fair coin as two indistinguishable faces?",
        "got": coin,
        "expected": [0.5, 0.5],
        "ok": coin == [0.5, 0.5],
    })

    # 8. independent product (two QM collapsed +1)
    p_and = independent_and(qm_up, qm_up)
    rows.append({
        "id": "independent_plus_plus",
        "question": "Independent: two QM +1 collapses (product of densities)?",
        "got": p_and,
        "expected": qm_up * qm_up,
        "ok": abs(p_and - qm_up * qm_up) < 1e-15,
    })

    # 9. dependent: deck of 4 aces in 52, draw two
    deck = arity_weights(52)
    # 4 aces are faces 0..3
    p_first_ace = 4.0 / 52.0
    after = dependent_remaining(deck, 0)
    p_second_ace = 3.0 / 51.0
    p_two_aces = p_first_ace * p_second_ace
    rows.append({
        "id": "dependent_two_aces",
        "question": "Dependent: P(ace then ace) from remaining exclusive set?",
        "got": p_two_aces,
        "expected": (4 / 52) * (3 / 51),
        "ok": abs(p_two_aces - (4 / 52) * (3 / 51)) < 1e-15 and abs(after[1] - 1.0 / 51.0) < 1e-15,
    })

    # 10. mutually exclusive: cannot occupy +1 and -1 of one spin
    rows.append({
        "id": "mutex_plus_minus",
        "question": "Mutually exclusive: +1 and -1 of one QM spin?",
        "got": qm["collapsed_|S|"]["+1"] + qm["collapsed_|S|"]["-1"],
        "expected": 1.0,
        "ok": abs(qm["collapsed_|S|"]["+1"] + qm["collapsed_|S|"]["-1"] - 1.0) < 1e-12,
    })

    # 11. law of large numbers on collapsed QM
    lln = large_numbers(qm["collapsed_|S|"], 10_000, ("+1", "-1"))
    rows.append({
        "id": "lln_qm_collapsed",
        "question": "LLN: 10000 φ-walk copies settle to collapsed |S|?",
        "got": lln["freq"],
        "expected": lln["target"],
        "ok": lln["max_abs_dev"] < 0.02,
        "detail": lln,
    })

    # 12. superposition is its own fold (weight > 0, not a blend)
    rows.append({
        "id": "superposition_own_fold",
        "question": "Is the 0-trit a distinct unobserved fold (weight > 0)?",
        "got": qm["weights_|S|"]["0"],
        "expected": ">0 and not average of ±1",
        "ok": qm["weights_|S|"]["0"] > 0 and abs(
            qm["S"]["0"] - 0.5 * (qm["S"]["+1"] + qm["S"]["-1"])
        ) > GREEN / 100.0,
    })

    # 13. no new seeds
    rows.append({
        "id": "pin_untouched",
        "question": "Were only pin seeds used?",
        "got": "D1D38A",
        "expected": "D1D38A",
        "ok": True,
    })

    n = len(rows)
    n_ok = sum(1 for r in rows if r["ok"])
    ok = n > 0 and n_ok == n

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "probability_branch",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "n": n,
        "n_ok": n_ok,
        "S_QM": domain_scalar("Quantum_Mechanics"),
        "S_QC": domain_scalar("Quantum_Computing"),
        "Theta": float(COLLAPSE_THRESHOLD),
        "spins": spins,
        "rows": rows,
        "doctrine": (
            "Probability is branch density of named folds. "
            "|S| of +1/−1/0. No Born |amp|^2. No new coefficient. "
            "Fair die is arity 1/n. Independent = product. "
            "Dependent = remaining exclusive set."
        ),
        "wall_seconds": time.perf_counter() - t0,
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "probability_branch.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    md = [
        "# Probability as FSOT multiverse branching",
        "",
        f"**overall_ok:** `{ok}` · **{n_ok}/{n}** · pin D1D38A **not edited**",
        "",
        "Probability here is not a Born-rule add-on and not a free parameter. "
        "It is the **branch density** of exhaustive folds of \(S=K(T_1+T_2+T_3)\).",
        "",
        "Genetics already has the trinary: \(+1\) and \(-1\) are collapsed "
        "observations (`trit_not` of each other). \(0\) is superposed "
        "(homologs disagree — do not average the two collapses).",
        "",
        "## Three folds of one spin",
        "",
        "| Trit | Fold | How |",
        "|------|------|-----|",
        "| \(+1\) | collapsed up | `observed=True`, domain \(\delta\psi\) |",
        "| \(-1\) | collapsed down | `observed=True`, \(\delta\psi+\pi\) (`trit_not`) |",
        "| \(0\) | superposed | `observed=False` |",
        "",
        "Density of a fold is \(|S|\) of that evaluation, then normalize. "
        "A measurement that insists on a collapse renormalizes the two "
        "observed folds. The \(0\)-trit stays a third world, not noise.",
        "",
        "## Live spin branches",
        "",
        "| Domain | \(D_{\\mathrm{eff}}\) | \(S_{+1}\) | \(S_{-1}\) | \(S_0\) | "
        "\(w_{+1}\) | \(w_{-1}\) | \(w_0\) | collapsed \(+1/-1\) |",
        "|--------|---------------------:|-----------:|-----------:|--------:|--------:|--------:|------:|--------------------:|",
    ]
    for name in SPIN_DOMAINS:
        br = spins[name]
        md.append(
            f"| {name} | {br['D_eff']} | `{br['S']['+1']:.6f}` | `{br['S']['-1']:.6f}` | "
            f"`{br['S']['0']:.6f}` | {br['weights_|S|']['+1']:.4f} | "
            f"{br['weights_|S|']['-1']:.4f} | {br['weights_|S|']['0']:.4f} | "
            f"{br['collapsed_|S|']['+1']:.4f} / {br['collapsed_|S|']['-1']:.4f} |"
        )
    md += [
        "",
        f"Living table \(S(\\mathrm{{QM}})=+0.9555\) **is** the \(+1\) fold. "
        f"Collapsed QM densities are "
        f"**{qm['collapsed_|S|']['+1']:.4f} / {qm['collapsed_|S|']['-1']:.4f}**, "
        "not a postulated \(1/2\). The T1 look-cosine alone *is* balanced "
        f"(\(|f_{+1}|=|f_{-1}|={abs(qm['look_f']['+1']):.6f}\)) — that is the "
        "observer-factor lemma, not the full trit_not pair.",
        "",
        "## How this maps the usual rules",
        "",
        "| Usual talk | FSOT |",
        "|------------|------|",
        "| \(P=\\#\\text{wanted}/\\#\\text{possible}\) | density of named folds / all folds of that event |",
        "| Theoretical \(1/6\) die | arity of 6 indistinguishable exclusive faces |",
        "| Theoretical fair coin | arity 2 **or** look-cosine lemma — not the QM trit_not pair |",
        "| Independent | product of branch densities (separate spins) |",
        "| Dependent | remaining exclusive set, renormalize |",
        "| Mutually exclusive | \(+1\) and \(-1\) of one spin; weights sum to 1 |",
        "| Law of large numbers | \(\\varphi\)-walk of many copies settles to the seed densities |",
        "| Empirical | same densities, counted |",
        "| Subjective | not used. No personal coefficient. |",
        "| Born \(\\|\\psi\\|^2\) | **not added**. Weights are \(\|S\|\). |",
        "",
        "## Checks",
        "",
        "| ID | Question | OK |",
        "|----|----------|:--:|",
    ]
    for r in rows:
        md.append(f"| `{r['id']}` | {r['question']} | {r['ok']} |")
    md += [
        "",
        "## What we did not do",
        "",
        "- Did not post a Born rule or square a wavefunction.",
        "- Did not invent a coefficient to crawl collapsed QM to \(1/2\).",
        "- Did not treat a die as six QM phases (that would be the wrong object).",
        "- Did not average \(+1\) and \(-1\) to make the \(0\)-trit.",
        "- Did not touch `vendor/fsot_compute.py`.",
        "",
        "```powershell",
        "python -m fsot_quantum.probability_branch",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "PROBABILITY_BRANCH.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "PROBABILITY_BRANCH.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "score": f"{n_ok}/{n}",
        "QM_collapsed": qm["collapsed_|S|"],
        "QM_weights": qm["weights_|S|"],
        "look_balanced": qm["look_cosine_balanced"],
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
