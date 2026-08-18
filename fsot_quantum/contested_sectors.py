"""
Contested sectors — FSOT-2.1-Lean open-science panel, computed on this pin.

Hubble, S8, BBN lithium, cusp-core, Higgs mass, w0/N_eff/σ8, BH→WH
bubble-bleed tools. Same D1D38A. No new coefficient.

Authority: https://github.com/dappalumbo91/FSOT-2.1-Lean
  data/contested_observables_closure.json
  predictions/reports/CONTESTED_SECTOR_WATCH.md

python -m fsot_quantum.contested_sectors
python -m fsot_quantum contested
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

from fsot_quantum.chemistry_fold import GREEN
from fsot_quantum.domains import domain_scalar
from fsot_lib.seeds import SEEDS

PLANCK_H0 = 67.4
SHOES_H0 = 73.04
CARNEGIE_H0 = 69.8
DENSITY_PLANCK = -1.0
DENSITY_SHOES = 5.05
DENSITY_CARNEGIE = 2.04


def _h0_global() -> float:
    s = domain_scalar("Cosmology")
    return 100.0 * (1.0 + float(s) * float(SEEDS.a_bleed) / float(SEEDS.a_in))


def _bleed(h0g: float) -> float:
    return h0g / PLANCK_H0 - 1.0


def _tool(h0g: float, bleed: float, density: float) -> float:
    return h0g * (1.0 + density * bleed)


def _vendor(wave: str, name: str):
    from vendor import fsot_compute as f

    for r in getattr(f, wave)():
        if r.name == name:
            return r
    return None


def _row(name: str, formula: str, fold: float, published: float, *,
         gate: float = GREEN, source: str = "pin") -> dict[str, Any]:
    rel = abs(fold - published) / abs(published) * 100 if published else None
    return {
        "name": name,
        "formula": formula,
        "fold": fold,
        "published": published,
        "rel_pct": rel,
        "gate_pct": gate,
        "ok": rel is not None and rel <= gate,
        "source": source,
    }


def main() -> int:
    t0 = time.perf_counter()
    s = SEEDS
    h0g = _h0_global()
    bleed = _bleed(h0g)
    h_planck = _tool(h0g, bleed, DENSITY_PLANCK)
    h_shoes = _tool(h0g, bleed, DENSITY_SHOES)
    h_carn = _tool(h0g, bleed, DENSITY_CARNEGIE)

    r_c = float(s.eta_eff) * float(s.phi) - float(s.poof)
    lithium = float(s.pi) * float(s.c_eff)
    # Lean overlay: (θ_S + e³)/C_factor⁷ is MeV; /1000 → GeV (125.200).
    m_h = (float(s.theta_s) + float(s.e) ** 3) / (float(s.c_factor) ** 7) / 1000.0
    s8 = float(s.psi_con) / math.sqrt(float(s.gamma))

    rows = [
        _row("H0_Planck_CMB", "H0_global·(1 − bleed)", h_planck, PLANCK_H0,
             source="BH→WH depleted"),
        _row("H0_SH0ES", "H0_global·(1 + 5.05·bleed)", h_shoes, SHOES_H0,
             gate=2.5, source="BH→WH inflated"),
        _row("H0_Carnegie", "H0_global·(1 + 2.04·bleed)", h_carn, CARNEGIE_H0,
             gate=2.5, source="BH→WH intermediate"),
        _row("r_c_Fornax_kpc", "η_eff·φ − POOF", r_c, 0.6,
             source="Lean cusp-core"),
        _row("Lithium_problem_factor", "π·C_eff", lithium, 3.0,
             source="Lean BBN"),
        _row("m_H_GeV", "(θ_S + e³)/C_factor⁷ / 1000", m_h, 125.25,
             source="Lean hierarchy"),
        _row("S_8", "ψ_con/√γ", s8, 0.832, source="vendor wave8"),
    ]

    for wave, name in (
        ("wave2", "N_eff"),
        ("wave2", "Omega_Lambda"),
        ("wave2", "sigma_8"),
        ("wave2", "tau_reion"),
        ("wave5", "D_H_ratio"),
        ("wave4", "w0"),
        ("wave1", "alpha_s(M_Z)"),
    ):
        r = _vendor(wave, name)
        if r is None or r.measured is None:
            rows.append({"name": name, "ok": False, "reason": "missing"})
            continue
        gate = 0.9 if name == "alpha_s(M_Z)" else GREEN
        rows.append(_row(
            name,
            getattr(r, "formula_str", ""),
            float(r.computed),
            float(r.measured),
            gate=gate,
            source=f"vendor {wave}",
        ))

    n = sum(1 for r in rows if "rel_pct" in r)
    n_ok = sum(1 for r in rows if r.get("ok"))
    ok = n > 0 and n_ok == n

    lean_path = ROOT / "_ref" / "FSOT-2.1-Lean" / "data" / "contested_observables_closure.json"
    lean_ok = None
    if lean_path.is_file():
        lean = json.loads(lean_path.read_text(encoding="utf-8"))
        lean_ok = lean.get("verdict")

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "contested_sectors",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "wall_seconds": time.perf_counter() - t0,
        "n": n,
        "n_ok": n_ok,
        "h0_global": h0g,
        "bubble_bleed_fraction": bleed,
        "lean_closure_present": lean_path.is_file(),
        "lean_verdict": lean_ok,
        "authority": "FSOT-2.1-Lean contested + BH→WH bubble-bleed",
        "rows": rows,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "contested_sectors.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Contested sectors — aligned with FSOT-2.1-Lean",
        "",
        f"**overall_ok:** `{ok}` · **{n_ok}/{n}** · pin D1D38A **not edited**",
        "",
        "These are the open-science tensions Lean already monitors "
        "([CONTESTED_SECTOR_WATCH](https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/predictions/reports/CONTESTED_SECTOR_WATCH.md)). "
        "Computed here from the same pin. Hubble tools use BH→WH bubble-bleed.",
        "",
        "| Name | Formula | Fold | Published | rel% | gate | OK |",
        "|------|---------|------|-----------|-----:|-----:|:--:|",
    ]
    for r in rows:
        if "rel_pct" not in r:
            md.append(f"| {r.get('name')} | missing | — | — | — | — | False |")
            continue
        md.append(
            f"| {r['name']} | `{r['formula']}` | `{r['fold']}` | `{r['published']}` | "
            f"{r['rel_pct']:.4f} | {r['gate_pct']}% | {r['ok']} |"
        )
    md += [
        "",
        "α_s(M_Z) keeps the vendor 0.9% band (PDG 1σ edge). "
        "SH0ES / Carnegie keep Lean’s 2.5% contested-sector band.",
        "",
        "```powershell",
        "python -m fsot_quantum.contested_sectors",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "CONTESTED_SECTORS.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "CONTESTED_SECTORS.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "scored": f"{n_ok}/{n}",
        "h0_global": h0g,
        "misses": [r["name"] for r in rows if not r.get("ok")],
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
