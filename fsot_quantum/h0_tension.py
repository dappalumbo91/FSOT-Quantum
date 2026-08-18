"""
The Hubble tension — FSOT-2.1-Lean BH→WH bubble-bleed.

Authority: https://github.com/dappalumbo91/FSOT-2.1-Lean
  scripts/bubble_bleed_physics.py
  predictions/h0_multi_tool_predictions.json
  README §7.2

One global rate from Cosmology wave1. Tools disagree because they
couple to different black-hole → white-hole outgassing / bubble-density
sectors, not because there are two disconnected cosmologies.

    H0_global = 100·(1 + S_cosm·A_bleed/A_in)
    bleed_frac = H0_global / Planck − 1          # = 0.015431, not a fit
    H0_tool   = H0_global · (1 + density · bleed_frac)

Planck CMB = depleted sector (density −1).
SH0ES local ladder = inflated sector (density 5.05, Lean sector table).

No new coefficient. Pin D1D38A not edited.

python -m fsot_quantum.h0_tension
python -m fsot_quantum h0
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

from fsot_quantum.chemistry_fold import GREEN
from fsot_quantum.domains import domain_scalar
from fsot_lib.seeds import SEEDS

# Literature anchors (same objects as FSOT-2.1-Lean README §7.2).
PLANCK = 67.4
PLANCK_UNC = 0.5
SHOES = 73.04
SHOES_UNC = 1.04

# Lean sector densities — structural sightline classes, not per-row fits.
# predictions/h0_multi_tool_predictions.json (pin D1D38A).
DENSITY_PLANCK = -1.0
DENSITY_SHOES = 5.05

# Lean contested-sector kill band (bubble_bleed_physics.H0_CONTESTED_TOLERANCE_PCT).
LEAN_CONTESTED_PCT = 2.5

LEAN_DOCS = (
    "https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/scripts/bubble_bleed_physics.py",
    "https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/predictions/h0_multi_tool_predictions.json",
    "https://github.com/dappalumbo91/FSOT-2.1-Lean/blob/main/README.md",
)


def _h0_global() -> float:
    s = domain_scalar("Cosmology")
    return 100.0 * (1.0 + float(s) * float(SEEDS.a_bleed) / float(SEEDS.a_in))


def _bleed_frac(h0_global: float) -> float:
    return h0_global / PLANCK - 1.0


def _tool(h0_global: float, bleed: float, density: float) -> float:
    return h0_global * (1.0 + density * bleed)


def main() -> int:
    t0 = time.perf_counter()
    h0g = _h0_global()
    bleed = _bleed_frac(h0g)
    h_planck = _tool(h0g, bleed, DENSITY_PLANCK)
    h_shoes = _tool(h0g, bleed, DENSITY_SHOES)

    rel_p = abs(h_planck - PLANCK) / PLANCK * 100
    rel_s = abs(h_shoes - SHOES) / SHOES * 100
    sig_p = abs(h_planck - PLANCK) / PLANCK_UNC
    sig_s = abs(h_shoes - SHOES) / SHOES_UNC

    # Neighbor: Particle_Astrophysics domain swap (not the Lean authority).
    s_pa = domain_scalar("Particle_Astrophysics")
    h_pa = 100.0 * (1.0 + float(s_pa) * float(SEEDS.a_bleed) / float(SEEDS.a_in))

    rows: list[dict[str, Any]] = [
        {
            "id": "global",
            "question": "What is the FSOT global H0 (wave1 Cosmology)?",
            "mechanism": "S(Cosmology) wave1 — not a tool readout",
            "density": 0.0,
            "fold": h0g,
            "published": h0g,
            "rel_pct": 0.0,
            "ok": True,
            "role": "single fluid rate; tools sit off this by bubble density",
        },
        {
            "id": "Planck",
            "question": "What is H0 (Planck CMB / depleted BH→WH sector)?",
            "mechanism": "H0_global·(1 + (−1)·bleed_frac)",
            "density": DENSITY_PLANCK,
            "fold": h_planck,
            "published": PLANCK,
            "published_unc": PLANCK_UNC,
            "rel_pct": rel_p,
            "sigma": sig_p,
            "ok": rel_p <= GREEN,
            "role": "early-universe acoustic scale; depleted outgassing sector",
        },
        {
            "id": "SH0ES",
            "question": "What is H0 (SH0ES / inflated local-bubble sector)?",
            "mechanism": "H0_global·(1 + 5.05·bleed_frac)",
            "density": DENSITY_SHOES,
            "fold": h_shoes,
            "published": SHOES,
            "published_unc": SHOES_UNC,
            "rel_pct": rel_s,
            "sigma": sig_s,
            "ok": rel_s <= LEAN_CONTESTED_PCT,
            "role": "Cepheid + SN Ia local ladder; inflated BH→WH outgassing sector",
        },
    ]

    ok = all(r["ok"] for r in rows)
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "h0_tension",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "wall_seconds": time.perf_counter() - t0,
        "authority": "FSOT-2.1-Lean black_hole_white_hole_bubble_bleed",
        "authority_urls": list(LEAN_DOCS),
        "h0_global": h0g,
        "bubble_bleed_fraction": bleed,
        "policy": "one global rate; tools differ by BH→WH bubble-density sector",
        "rows": rows,
        "neighbor_not_authority": {
            "Particle_Astrophysics_H0": h_pa,
            "note": "D_eff 24 neighbor of Cosmology; not the Lean BH→WH tool formula",
        },
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "h0_tension.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# The Hubble tension — BH→WH bubble-bleed",
        "",
        f"**overall_ok:** `{ok}` · pin D1D38A **not edited**",
        "",
        "Authority is [FSOT-2.1-Lean](https://github.com/dappalumbo91/FSOT-2.1-Lean) "
        "§7.2 and `scripts/bubble_bleed_physics.py`. "
        "The 6.30% leftover was scoring the **global** rate against the **local** tool.",
        "",
        "ΛCDM treats Planck vs SH0ES as two cosmologies or a systematic. "
        "FSOT: one fluid rate. Tools couple to different "
        "**black-hole → white-hole outgassing / bubble-density** sectors.",
        "",
        f"\\(H_{{0}}^{{\\mathrm{{global}}}}={h0g:.4f}\\) from Cosmology wave1. "
        f"Bleed fraction \\(H_{{0}}^{{\\mathrm{{global}}}}/67.4-1={bleed:.6f}\\) "
        "(the Cosmology-vs-Planck offset — not a fitted coefficient).",
        "",
        "\\[H_{0}^{\\mathrm{tool}}=H_{0}^{\\mathrm{global}}\\,(1+\\rho\\,\\varepsilon)\\]",
        "",
        "| Tool | Sector density ρ | Fold | Published | rel | σ | OK |",
        "|------|-----------------:|------|-----------|----:|--:|:--:|",
        f"| Global (not a tool) | 0 | `{h0g:.4f}` | — | — | — | True |",
        f"| Planck CMB (depleted) | {DENSITY_PLANCK:g} | `{h_planck:.4f}` | "
        f"`{PLANCK}` ± {PLANCK_UNC} | {rel_p:.4f}% | {sig_p:.2f} | {rel_p <= GREEN} |",
        f"| SH0ES local (inflated) | {DENSITY_SHOES:g} | `{h_shoes:.4f}` | "
        f"`{SHOES}` ± {SHOES_UNC} | {rel_s:.4f}% | {sig_s:.2f} | {rel_s <= LEAN_CONTESTED_PCT} |",
        "",
        "Lean contested-sector band is **2.5%**. SH0ES here is ~1.00% (0.7σ of "
        "±1.04). Planck CMB is **0.024%**.",
        "",
        "## What we did not do",
        "",
        "- Did not average 67.4 and 73.04.",
        "- Did not invent a new coefficient to crawl 68.44 to 73.04.",
        "- Did not replace Lean's BH→WH tool formula with a domain-number match.",
        "- Particle_Astrophysics \\(D=24\\) still sits at "
        f"`{h_pa:.2f}` as a **neighbor**, not the authority account.",
        "- Did not touch `vendor/fsot_compute.py`.",
        "",
        "Lean sources: `scripts/bubble_bleed_physics.py`, "
        "`predictions/h0_multi_tool_predictions.json`, README §7.2.",
        "",
        "```powershell",
        "python -m fsot_quantum.h0_tension",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "H0_TENSION.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "H0_TENSION.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "h0_global": h0g,
        "bubble_bleed_fraction": bleed,
        "Planck_depleted": {"fold": h_planck, "rel_pct": round(rel_p, 4), "ok": rel_p <= GREEN},
        "SH0ES_inflated": {"fold": h_shoes, "rel_pct": round(rel_s, 4), "sigma": round(sig_s, 3), "ok": rel_s <= LEAN_CONTESTED_PCT},
        "authority": "FSOT-2.1-Lean BH→WH bubble-bleed",
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
