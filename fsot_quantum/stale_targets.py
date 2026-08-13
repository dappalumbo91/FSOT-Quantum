"""
Stale-target audit: pin formulas vs vendor stored targets vs current literature.

Does not edit vendor/fsot_compute.py (pin D1D38A).
If vendor measured disagrees with YR4/PDG, score the fold against literature
and mark the vendor field stale.

python -m fsot_quantum.stale_targets
python -m fsot_quantum audit
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

from fsot_quantum.chemistry_fold import BAND_5, GREEN

# Only entries we can cite. Values are SM / PDG / YR4 recommendations.
# Sources noted per row. Not a fit.
LITERATURE: dict[str, dict[str, Any]] = {
    "BR_H_gg": {
        "value": 0.08187,
        "source": "LHCHWG YR4 SM BR(H→gg) MH≈125.09 GeV",
    },
    "BR_H_bb": {
        "value": 0.5809,
        "source": "LHCHWG YR4 SM BR(H→bb) MH≈125.09 GeV",
    },
    "BR_H_WW": {
        "value": 0.2152,
        "source": "LHCHWG YR4 SM BR(H→WW) MH≈125.09 GeV",
    },
    "BR_H_ZZ": {
        "value": 0.02643,
        "source": "LHCHWG YR4 SM BR(H→ZZ) MH≈125.09 GeV",
    },
    "BR_H_cc": {
        "value": 0.02891,
        "source": "LHCHWG YR4 SM BR(H→cc) MH≈125.09 GeV",
    },
    "BR_H_gamgam": {
        "value": 0.002270,
        "source": "LHCHWG YR4 SM BR(H→γγ) MH≈125.09 GeV",
    },
    "BR_H_Zgam": {
        "value": 0.001541,
        "source": "LHCHWG YR4 SM BR(H→Zγ) MH≈125.09 GeV",
    },
    "1/alpha_em": {
        "value": 137.035999084,
        "source": "CODATA / PDG inverse fine-structure constant",
    },
    "sin2_theta_W": {
        "value": 0.23122,
        "source": "PDG Weinberg angle (on-shell / common SM table)",
    },
    "|V_ud|": {
        "value": 0.97373,
        "source": "PDG CKM |V_ud|",
    },
    "|V_us|": {
        "value": 0.2243,
        "source": "PDG CKM |V_us|",
    },
    "|V_ub|": {
        "value": 0.00382,
        "source": "PDG CKM |V_ub|",
    },
    "|V_cd|": {
        "value": 0.221,
        "source": "PDG CKM |V_cd|",
    },
    "|V_cs|": {
        "value": 0.975,
        "source": "PDG CKM |V_cs|",
    },
    "|V_cb|": {
        "value": 0.0411,
        "source": "PDG CKM |V_cb| (exclusive/inclusive average ~0.041)",
    },
    "|V_tb|": {
        "value": 0.9991,
        "source": "PDG CKM |V_tb|",
    },
    "Deuteron_binding_MeV": {
        "value": 2.224566,
        "source": "CODATA / nuclear data deuteron binding",
    },
    "He4_binding_MeV": {
        "value": 28.29566,
        "source": "nuclear data ⁴He binding (MeV)",
    },
    "m_mu/m_e": {
        "value": 206.768283,
        "source": "CODATA m_μ/m_e",
    },
    "(g-2)/2_electron": {
        "value": 0.00115965218046,
        "source": "CODATA electron anomaly a_e",
    },
}


def _collect_vendor() -> list[Any]:
    from vendor import fsot_compute as f

    rows = []
    for name in (
        "validation_suite",
        "wave1",
        "wave2",
        "wave3",
        "wave4",
        "wave5",
        "wave6",
        "wave7",
        "wave8",
        "wave9",
        "wave10",
        "lepton_ratios",
    ):
        fn = getattr(f, name, None)
        if fn is None:
            continue
        for r in fn():
            rows.append((name, r))
    return rows


def main() -> int:
    t0 = time.perf_counter()
    vendor_rows = _collect_vendor()
    seen: set[str] = set()
    audits: list[dict[str, Any]] = []
    for wave, r in vendor_rows:
        if r.measured is None:
            continue
        if r.name in seen:
            continue
        seen.add(r.name)
        c = float(r.computed)
        vm = float(r.measured)
        lit = LITERATURE.get(r.name)
        if lit:
            lm = float(lit["value"])
            vendor_vs_lit = abs(vm - lm) / abs(lm) * 100 if lm else None
            fold_vs_lit = abs(c - lm) / abs(lm) * 100 if lm else None
            fold_vs_vendor = abs(c - vm) / abs(vm) * 100 if vm else None
            stale = vendor_vs_lit is not None and vendor_vs_lit > 0.5
            audits.append({
                "name": r.name,
                "wave": wave,
                "formula": getattr(r, "formula_str", ""),
                "computed": c,
                "vendor_measured": vm,
                "literature": lm,
                "literature_source": lit["source"],
                "vendor_vs_lit_pct": vendor_vs_lit,
                "fold_vs_lit_pct": fold_vs_lit,
                "fold_vs_vendor_pct": fold_vs_vendor,
                "stale_vendor": stale,
                "fold_ok_lit": fold_vs_lit is not None and fold_vs_lit <= GREEN,
                "fold_ok_vendor": fold_vs_vendor is not None and fold_vs_vendor <= GREEN,
            })
        else:
            fold_vs_vendor = abs(c - vm) / abs(vm) * 100 if vm else None
            audits.append({
                "name": r.name,
                "wave": wave,
                "formula": getattr(r, "formula_str", ""),
                "computed": c,
                "vendor_measured": vm,
                "literature": None,
                "literature_source": None,
                "vendor_vs_lit_pct": None,
                "fold_vs_lit_pct": None,
                "fold_vs_vendor_pct": fold_vs_vendor,
                "stale_vendor": False,
                "fold_ok_lit": None,
                "fold_ok_vendor": fold_vs_vendor is not None and fold_vs_vendor <= GREEN,
            })

    cited = [a for a in audits if a["literature"] is not None]
    stale = [a for a in cited if a["stale_vendor"]]
    fold_lit_ok = [a for a in cited if a["fold_ok_lit"]]
    ok = bool(cited) and all(a["fold_ok_lit"] for a in cited)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "stale_targets",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "wall_seconds": time.perf_counter() - t0,
        "n_vendor_scored": len(audits),
        "n_cited": len(cited),
        "n_stale_vendor": len(stale),
        "n_fold_ok_lit": len(fold_lit_ok),
        "stale": stale,
        "cited": cited,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "stale_targets.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Stale-target audit — vendor table vs current literature",
        "",
        f"**overall_ok:** `{ok}` · pin D1D38A **not edited**",
        f"Cited rows **{len(fold_lit_ok)}/{len(cited)}** fold-vs-literature @0.5% · "
        f"stale vendor fields **{len(stale)}**",
        "",
        "Same method as `docs/BR_H_GG.md`. If the stored vendor target is old and the "
        "formula already matches YR4/PDG, that is not a formula miss.",
        "",
        "## Stale vendor fields (vendor vs literature > 0.5%)",
        "",
        "| Name | vendor | literature | vendor vs lit | fold | fold vs lit |",
        "|------|--------|------------|--------------:|------|------------:|",
    ]
    if not stale:
        md.append("| — | — | — | — | — | — |")
    for a in stale:
        md.append(
            f"| {a['name']} | `{a['vendor_measured']}` | `{a['literature']}` "
            f"({a['literature_source']}) | {a['vendor_vs_lit_pct']:.3f}% | "
            f"`{a['computed']}` | {a['fold_vs_lit_pct']:.4f}% |"
        )
    md += [
        "",
        "## All cited rows",
        "",
        "| Name | fold vs lit | fold vs vendor | stale vendor? | 0.5% vs lit |",
        "|------|------------:|---------------:|:-------------:|:-----------:|",
    ]
    for a in cited:
        md.append(
            f"| {a['name']} | {a['fold_vs_lit_pct']:.4f}% | {a['fold_vs_vendor_pct']:.4f}% | "
            f"{a['stale_vendor']} | {a['fold_ok_lit']} |"
        )
    md += [
        "",
        "```powershell",
        "python -m fsot_quantum.stale_targets",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "STALE_TARGETS.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "STALE_TARGETS.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "cited": f"{len(fold_lit_ok)}/{len(cited)}",
        "stale_vendor": len(stale),
        "stale_names": [a["name"] for a in stale],
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
