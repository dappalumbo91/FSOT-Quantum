"""
Living formula list — every pin / derived formula and what it solves.

python -m fsot_quantum.formula_catalog
python -m fsot_quantum formulas
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

WAVES = (
    "validation_suite",
    "wave1", "wave2", "wave3", "wave4", "wave5",
    "wave6", "wave7", "wave8", "wave9", "wave10",
    "lepton_ratios",
)

# Formulas we built on this fold (not in vendor wave tables).
DERIVED: list[dict[str, Any]] = [
    {
        "name": "K",
        "formula": "φ·(γ/e)·√2/ln(π)·99/100",
        "solves": "universal scale in S=K(T1+T2+T3)",
        "kind": "engine",
    },
    {
        "name": "S",
        "formula": "K(T1+T2+T3)",
        "solves": "domain scalar; sign is identity",
        "kind": "engine",
    },
    {
        "name": "Theta",
        "formula": "C_eff·P_var",
        "solves": "collapse threshold (no softmax)",
        "kind": "engine",
    },
    {
        "name": "C_factor",
        "formula": "C_eff·P_new",
        "solves": "consciousness / look factor on T1",
        "kind": "engine",
    },
    {
        "name": "kappa",
        "formula": "A_bleed·POOF·|Si||Sj|/(1+|ΔD|/25)",
        "solves": "bleed between named domains",
        "kind": "engine",
    },
    {
        "name": "V_cb_inclusive",
        "formula": "S(QM)·(1/C_eff−1)",
        "solves": "inclusive |V_cb| (PDG 0.0422)",
        "kind": "tension",
        "published": 0.0422,
    },
    {
        "name": "V_cb_exclusive",
        "formula": "S(HEP)·(1/C_eff−1)",
        "solves": "exclusive |V_cb| (combined 0.0398, 1.1σ)",
        "kind": "tension",
        "published": 0.0398,
    },
    {
        "name": "H0_global",
        "formula": "100·(1+S_cosm·A_bleed/A_in)",
        "solves": "single fluid Hubble rate (wave1 Cosmology)",
        "kind": "tension",
    },
    {
        "name": "H0_Planck_CMB",
        "formula": "H0_global·(1+(−1)·bleed)",
        "solves": "Planck CMB — BH→WH depleted sector",
        "kind": "tension",
        "published": 67.4,
    },
    {
        "name": "H0_SH0ES",
        "formula": "H0_global·(1+5.05·bleed)",
        "solves": "SH0ES local ladder — BH→WH inflated sector",
        "kind": "tension",
        "published": 73.04,
    },
    {
        "name": "bleed_frac",
        "formula": "H0_global/67.4 − 1",
        "solves": "bubble-bleed amplitude (0.015431, not a fit)",
        "kind": "tension",
    },
    {
        "name": "w0_cmb",
        "formula": "−P_new·π/G",
        "solves": "dark-energy w0 CMB lane",
        "kind": "tension",
        "published": -1.03,
    },
    {
        "name": "wa_cmb",
        "formula": "−γ·e·φ/π",
        "solves": "dark-energy wa CMB lane",
        "kind": "tension",
        "published": -0.8081,
    },
    {
        "name": "w0_bao",
        "formula": "w0_cmb·(1−G/π)",
        "solves": "DESI DR2 w0 BAO lane",
        "kind": "tension",
        "published": -0.727,
    },
    {
        "name": "wa_bao",
        "formula": "wa_cmb + w0_bao·(G/π)",
        "solves": "DESI DR2 wa BAO lane",
        "kind": "tension",
        "published": -1.018,
    },
    {
        "name": "r_c_Fornax",
        "formula": "η_eff·φ − POOF",
        "solves": "dwarf core radius (Fornax 0.6 kpc)",
        "kind": "tension",
        "published": 0.6,
    },
    {
        "name": "Lithium_factor",
        "formula": "π·C_eff",
        "solves": "BBN lithium underproduction factor (~3)",
        "kind": "tension",
        "published": 3.0,
    },
    {
        "name": "m_H",
        "formula": "(θ_S + e³)/C_factor⁷ / 1000",
        "solves": "Higgs mass (125.20 vs 125.25 GeV)",
        "kind": "tension",
        "published": 125.25,
    },
]


def _eval_derived() -> list[dict[str, Any]]:
    from fsot_quantum.open_remaining import _de_readouts, _v_from_S
    from fsot_quantum.h0_tension import _h0_global, _bleed_frac, _tool, DENSITY_PLANCK, DENSITY_SHOES

    s = SEEDS
    h0g = _h0_global()
    bleed = _bleed_frac(h0g)
    de = _de_readouts()
    out = []
    values = {
        "K": float(s.k),
        "S": None,
        "Theta": float(s.c_eff * s.p_var),
        "C_factor": float(s.c_factor),
        "kappa": None,
        "V_cb_inclusive": _v_from_S(domain_scalar("Quantum_Mechanics")),
        "V_cb_exclusive": _v_from_S(domain_scalar("High_Energy_Physics")),
        "H0_global": h0g,
        "H0_Planck_CMB": _tool(h0g, bleed, DENSITY_PLANCK),
        "H0_SH0ES": _tool(h0g, bleed, DENSITY_SHOES),
        "bleed_frac": bleed,
        "w0_cmb": de["w0_cmb"],
        "wa_cmb": de["wa_cmb"],
        "w0_bao": de["w0_bao"],
        "wa_bao": de["wa_bao"],
        "r_c_Fornax": float(s.eta_eff) * float(s.phi) - float(s.poof),
        "Lithium_factor": float(s.pi) * float(s.c_eff),
        "m_H": (float(s.theta_s) + float(s.e) ** 3) / (float(s.c_factor) ** 7) / 1000.0,
    }
    for row in DERIVED:
        item = dict(row)
        v = values.get(row["name"])
        item["computed"] = v
        pub = row.get("published")
        if v is not None and pub is not None and pub != 0:
            item["rel_pct"] = abs(float(v) - float(pub)) / abs(float(pub)) * 100
        out.append(item)
    return out


def _collect_vendor() -> list[dict[str, Any]]:
    from vendor import fsot_compute as f

    seen: set[str] = set()
    rows: list[dict[str, Any]] = []
    for w in WAVES:
        fn = getattr(f, w, None)
        if fn is None:
            continue
        for r in fn():
            if r.name in seen or r.measured is None:
                continue
            seen.add(r.name)
            c = float(r.computed)
            m = float(r.measured)
            rel = abs(c - m) / abs(m) * 100 if m else None
            rows.append({
                "name": r.name,
                "wave": w,
                "formula": getattr(r, "formula_str", ""),
                "computed": c,
                "published": m,
                "rel_pct": rel,
                "solves": r.name.replace("_", " "),
                "kind": "pin-wave",
            })
    return rows


def main() -> int:
    t0 = time.perf_counter()
    derived = _eval_derived()
    vendor = _collect_vendor()
    n_v = len(vendor)
    n_v05 = sum(1 for r in vendor if r.get("rel_pct") is not None and r["rel_pct"] <= GREEN)
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "formula_catalog",
        "pin": "D1D38A",
        "n_engine_and_tension": len(derived),
        "n_pin_wave": n_v,
        "n_pin_wave_0_5": n_v05,
        "derived": derived,
        "pin_wave": vendor,
        "wall_seconds": time.perf_counter() - t0,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "formula_catalog.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# FSOT formula list — what each formula solves",
        "",
        f"**Pin:** D1D38A · **{len(derived)}** engine/tension formulas · "
        f"**{n_v05}/{n_v}** pin-wave rows @0.5% vs their stored object",
        "",
        "Generated. Do not hand-edit — `python -m fsot_quantum formulas`.",
        "",
        "## Engine (closed)",
        "",
        "| Name | Formula | Solves |",
        "|------|---------|--------|",
    ]
    for r in derived:
        if r["kind"] != "engine":
            continue
        md.append(f"| {r['name']} | `${r['formula']}$` | {r['solves']} |")
    md += [
        "",
        "## Tension / dual-object solvers (this fold)",
        "",
        "Change domain or lane, not a coefficient. Lean BH→WH + Catalan/π bleed.",
        "",
        "| Name | Formula | Solves | Fold | Published | rel% |",
        "|------|---------|--------|------|-----------|-----:|",
    ]
    for r in derived:
        if r["kind"] != "tension":
            continue
        fold = r.get("computed")
        fold_s = f"`{fold}`" if fold is not None else "—"
        pub = r.get("published")
        pub_s = f"`{pub}`" if pub is not None else "—"
        rel = r.get("rel_pct")
        rel_s = f"{rel:.4f}" if rel is not None else "—"
        md.append(
            f"| {r['name']} | `{r['formula']}` | {r['solves']} | {fold_s} | {pub_s} | {rel_s} |"
        )
    md += [
        "",
        "## Pin-wave inventory (vendor, first occurrence)",
        "",
        "Stored measured field is the object the wave was written against. "
        "Some stored fields are stale (see `docs/STALE_TARGETS.md`).",
        "",
        "| Name | Wave | Formula | Fold | Stored | rel% |",
        "|------|------|---------|------|--------|-----:|",
    ]
    for r in vendor:
        rel = r.get("rel_pct")
        rel_s = f"{rel:.4f}" if rel is not None else "—"
        md.append(
            f"| {r['name']} | {r['wave']} | `{r['formula']}` | `{r['computed']}` | "
            f"`{r['published']}` | {rel_s} |"
        )
    md += [
        "",
        "```powershell",
        "python -m fsot_quantum.formula_catalog",
        "python -m fsot_quantum stamp",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "FORMULA_LIST.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "FORMULA_LIST.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "engine_tension": len(derived),
        "pin_wave": f"{n_v05}/{n_v}",
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
