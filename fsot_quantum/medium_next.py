"""
Next step: water/three-string/observe medium + Lean entanglement/QI jobs.

python -m fsot_quantum.medium_next
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.medium_strings import run_medium_strings_panel
from fsot_quantum.entangle_qi_jobs import run_entangle_qi_panel
from fsot_quantum.quantum_bleed import coupled_equilibrium as bleed_eq


def main() -> int:
    t0 = time.perf_counter()
    med = run_medium_strings_panel()
    qi = run_entangle_qi_panel()
    eq = bleed_eq()

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "medium_next",
        "pin": "D1D38A",
        "thesis": (
            "Quantum side = water body of the medium. Three strings T1/T2/T3 "
            "strum (T3 bleed). Observation (C_factor) snaps collapse Θ. "
            "Entanglement/QI jobs replayed from FSOT-2.1-Lean material records."
        ),
        "medium": {
            "ok": med["overall_ok"],
            "S_match": med["S_match_domain_scalar"],
            "chsh": med["chsh"],
            "observe_agree": med["observe_pair"]["agree"],
            "strum_ok": med["strum"].get("ok"),
            "T1_QM": med["strings_QM"]["T1_observe_string"],
            "T3_QM": med["strings_QM"]["T3_strum_string"],
            "T1_QC": med["strings_QC"]["T1_observe_string"],
            "T3_QC": med["strings_QC"]["T3_strum_string"],
        },
        "entangle_qi": {
            "ok": qi["overall_ok"],
            "replayed": qi.get("n_replayed"),
            "green": f"{qi.get('n_green_0_5')}/{qi.get('n_replayed')}",
            "band5": f"{qi.get('n_band_5')}/{qi.get('n_replayed')}",
            "skipped_broken": qi.get("n_skipped_broken"),
            "worst": qi.get("worst"),
        },
        "bleed_still": {
            "dS_QM": eq["coupled_S"]["QM"] - eq["bare_S"]["QM"],
            "dS_QC": eq["coupled_S"]["QC"] - eq["bare_S"]["QC"],
        },
        "overall_ok": med["overall_ok"] and qi["overall_ok"],
        "wall_seconds": time.perf_counter() - t0,
        "plain": (
            "The water is the continuum. The three strings are T1 (look), "
            "T2 (body), T3 (strum). Looking turns the observer valve on QM. "
            "Strum is the bleed vibration. Snap is collapse. Bonds agreeing "
            "after a look is consensus. We did not add a new knob."
        ),
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "medium_strings.json").write_text(json.dumps(med, indent=2), encoding="utf-8")
    (out / "entangle_qi_jobs.json").write_text(json.dumps(qi, indent=2), encoding="utf-8")
    (out / "medium_next.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Medium next — water, three strings, look, snap",
        "",
        f"**overall_ok:** `{report['overall_ok']}`",
        f"**wall_s:** `{report['wall_seconds']:.2f}`",
        "",
        report["plain"],
        "",
        "## Three strings",
        "",
        f"- QM (look ON): T1={med['strings_QM']['T1_observe_string']:.6g} "
        f"T3={med['strings_QM']['T3_strum_string']:.6g} S={med['strings_QM']['S']:.4f}",
        f"- QC (look OFF): T1={med['strings_QC']['T1_observe_string']:.6g} "
        f"T3={med['strings_QC']['T3_strum_string']:.6g} S={med['strings_QC']['S']:.4f}",
        f"- S matches domain_scalar: `{med['S_match_domain_scalar']}`",
        f"- observe-pair agree: `{med['observe_pair']['agree']}`",
        f"- strum+collapse ok: `{med['strum'].get('ok')}`",
        f"- CHSH classical 2, Tsirelson {med['chsh']['chsh_tsirelson']:.6f}",
        "",
        "## Entanglement / QI jobs (Lean replay)",
        "",
        f"- replayed **{qi.get('n_replayed')}** · 5% band **{report['entangle_qi']['band5']}** "
        f"· 0.5% **{report['entangle_qi']['green']}**",
        f"- skipped broken (computed=0): {qi.get('n_skipped_broken')}",
        "",
        "## Reproduce",
        "",
        "```powershell",
        'cd "C:\\Users\\damia\\Desktop\\fsot quantum"',
        "$env:PYTHONPATH = (Get-Location).Path",
        "python -m fsot_quantum.medium_next",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "MEDIUM_NEXT.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "MEDIUM_NEXT.md").write_text(text, encoding="utf-8")

    print(json.dumps({
        "overall_ok": report["overall_ok"],
        "medium": report["medium"],
        "entangle_qi": report["entangle_qi"],
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if report["overall_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
