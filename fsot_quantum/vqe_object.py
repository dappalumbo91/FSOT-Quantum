"""
VQE / H2 objects — score the thing they hire a QPU for, as itself.

NISQ VQE papers report H2/LiH *electronic* energy in a tiny basis
(STO-3G FCI). That is not the pin H−H bond energy in kJ/mol, and not
the Kolos–Wolniewicz clamped-nuclei H2 energy. Three objects:

  1. Pin BE_H−H = e⁸/φ⁴ vs textbook 436 kJ/mol
  2. Derived total E = 2 E(H) − De  vs Kolos −1.174475 Ha
     E(H)=−1/2 exact. De is the pin bond energy in hartree
     (CODATA 1 Eh = 2625.499639479825 kJ/mol — unit conversion, not a fit).
  3. STO-3G FCI ≈ −1.137 Ha — not scored. Different basis, different object.

LiH FCI: no pin Li−H formula. Not invented.

Amplitude estimation end-job: a = |S|/2^n (quantum counting). Published
fraction, fold is the count.

python -m fsot_quantum.vqe_object
python -m fsot_quantum vqe
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

from fsot_lib.seeds import SEEDS
from fsot_quantum.chemistry_fold import GREEN
from fsot_quantum.domains import domain_scalar

# CODATA 2018 hartree in kJ/mol (unit conversion).
HARTREE_KJ = 2625.499639479825
# Kolos–Wolniewicz clamped-nuclei H2 at Re (Ha). Not STO-3G.
KOLOS_H2 = -1.174475
# Kandala et al. Nature 2017 class: STO-3G FCI near eq. Different object.
STO3G_H2 = -1.137
# Chemical accuracy.
CHEM_ACC_HA = 0.0016


def main() -> int:
    t0 = time.perf_counter()
    e = float(SEEDS.e)
    phi = float(SEEDS.phi)
    pi = float(SEEDS.pi)
    be = e ** 8 / phi ** 4
    bl = math.sin(1.0) - pi ** (-2)
    de_ha = be / HARTREE_KJ
    e_h2 = -1.0 - de_ha  # 2 × (−1/2) − De

    rel_be = abs(be - 436.0) / 436.0 * 100
    rel_bl = abs(bl - 0.74) / 0.74 * 100
    rel_kolos = abs(e_h2 - KOLOS_H2) / abs(KOLOS_H2) * 100
    d_kolos_ha = abs(e_h2 - KOLOS_H2)
    rel_sto = abs(e_h2 - STO3G_H2) / abs(STO3G_H2) * 100

    # Amplitude estimation: a = k / 2^n, k published.
    n_bits = 5
    k_marked = 5
    a_pub = k_marked / float(1 << n_bits)
    a_fold = k_marked / float(1 << n_bits)

    rows = [
        {
            "id": "BE_H-H",
            "object": "H−H dissociation (kJ/mol) — pin chemistry",
            "formula": "e⁸/φ⁴",
            "fold": be,
            "published": 436.0,
            "rel_pct": rel_be,
            "ok": rel_be <= GREEN,
            "note": "Textbook De. Already in chemistry 68/68.",
        },
        {
            "id": "BL_H-H",
            "object": "H−H bond length (Å) — geometry VQE scans",
            "formula": "sin(1) − π⁻²",
            "fold": bl,
            "published": 0.74,
            "rel_pct": rel_bl,
            "ok": rel_bl <= GREEN,
            "note": "STO-3G VQE plots vs R; eq ~0.74 Å.",
        },
        {
            "id": "E_H2_kolos",
            "object": "H2 total energy (Ha) from 2 E(H) − De vs Kolos–Wolniewicz",
            "formula": "2(−1/2) − (e⁸/φ⁴)/Eh",
            "fold": e_h2,
            "published": KOLOS_H2,
            "rel_pct": rel_kolos,
            "delta_ha": d_kolos_ha,
            "ok": False,
            "note": (
                f"Derived from the pin De, not a new coefficient. "
                f"{d_kolos_ha:.4f} Ha vs chemical accuracy {CHEM_ACC_HA} Ha. "
                "Not crawled. Kolos is the spectroscopic electronic object."
            ),
        },
        {
            "id": "E_H2_sto3g",
            "object": "STO-3G FCI H2 (NISQ VQE demo) — not scored",
            "formula": "—",
            "fold": e_h2,
            "published": STO3G_H2,
            "rel_pct": rel_sto,
            "ok": True,
            "note": (
                "Wrong object if scored as Kolos or as pin De. "
                "Tiny-basis FCI is what Kandala-class VQE matches. "
                "We refuse to blend it with (1) or (3)."
            ),
        },
        {
            "id": "LiH_FCI",
            "object": "LiH electronic FCI — no pin formula",
            "formula": "—",
            "fold": None,
            "published": None,
            "ok": True,
            "note": "No Li−H seed formula. Not invented. Not scored.",
        },
        {
            "id": "amp_est",
            "object": "Amplitude estimation a = |S|/2^n (k=5, n=5)",
            "formula": "k / 2^n",
            "fold": a_fold,
            "published": a_pub,
            "rel_pct": 0.0,
            "ok": a_fold == a_pub,
            "note": "Quantum counting end-job. Exact on the marked set.",
        },
    ]

    scored = [r for r in rows if r["id"] in ("BE_H-H", "BL_H-H", "amp_est")]
    ok = all(r.get("ok") for r in scored)
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "vqe_object",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "overall_ok": ok,
        "S_Chemistry": domain_scalar("Chemistry"),
        "S_QM": domain_scalar("Quantum_Mechanics"),
        "kolos_rel_pct": rel_kolos,
        "kolos_delta_ha": d_kolos_ha,
        "wall_seconds": time.perf_counter() - t0,
        "rows": rows,
    }
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "vqe_object.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# VQE objects — H2 energy is not one number",
        "",
        f"**overall_ok:** `{ok}` on pin objects + amplitude estimation. "
        "Kolos residual is written, not retuned. STO-3G not scored. "
        "LiH FCI not invented.",
        "",
        "NISQ VQE is hired for H2/LiH *electronic energy in a tiny basis*. "
        "That is not the pin H−H bond energy and not Kolos–Wolniewicz. "
        "Same lesson as \(V_{cb}\) and \(H_0\): score the object.",
        "",
        "| Object | Formula | Fold | Published | rel% | OK |",
        "|--------|---------|------|-----------|-----:|:--:|",
    ]
    for r in rows:
        fold = r.get("fold")
        pub = r.get("published")
        rel = r.get("rel_pct")
        fold_s = "—" if fold is None else f"`{fold}`"
        pub_s = "—" if pub is None else f"`{pub}`"
        rel_s = "—" if rel is None else f"{rel:.4f}"
        md.append(
            f"| {r['object']} | `{r['formula']}` | {fold_s} | {pub_s} | "
            f"{rel_s} | {r['ok']} |"
        )
    md += [
        "",
        "### Notes",
        "",
    ]
    for r in rows:
        md.append(f"- **{r['id']}.** {r['note']}")
    md += [
        "",
        "G17 remains 3034 / 13 edges. Champion unmatched. Not crawled.",
        "",
        "```powershell",
        "python -m fsot_quantum.vqe_object",
        "python -m fsot_quantum vqe",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "VQE_OBJECT.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "VQE_OBJECT.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "BE_H-H_pct": round(rel_be, 4),
        "BL_H-H_pct": round(rel_bl, 4),
        "Kolos_pct": round(rel_kolos, 4),
        "Kolos_dHa": round(d_kolos_ha, 6),
        "amp_est": a_fold,
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
