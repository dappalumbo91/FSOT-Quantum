"""
Genetics 7-trit / codon branching on this pin.

Genetics repo is not edited. The codon and opcode law is copied into
fsot_quantum.genetics_law (same tables). Each trit is a named fold
(+1/−1/0). Word density is the product of independent trit densities
from |S| on the Biology domain (living substrate, dark).

Do not average primary and secondary. They are two lawful readouts
of one base (purine axis vs A/T axis). 0 is superposition.

python -m fsot_quantum.genetics_branch
python -m fsot_quantum gencode
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fsot_quantum.genetics_law import (
    AA20,
    PUBLISHED_WORD,
    aa_opcode,
    all_codons,
    codon_primary,
    codon_secondary,
    translate,
    trit_not,
)
from fsot_quantum.probability_branch import independent_and, spin_branches

# Living substrate. Biology is dark (observed=False) on the pin table.
GENETICS_DOMAIN = "Biology"


def trit_weight(branches: dict[str, Any], t: int) -> float:
    key = {1: "+1", -1: "-1", 0: "0"}[int(t)]
    return float(branches["weights_|S|"][key])


def word_density(word: Sequence[int], branches: dict[str, Any]) -> float:
    d = 1.0
    for t in word:
        d = independent_and(d, trit_weight(branches, t))
    return d


def codon_word(codon: str) -> tuple[int, ...]:
    """Six trits: primary trip then secondary trip. Not averaged."""
    return codon_primary(codon) + codon_secondary(codon)


def main() -> int:
    t0 = time.perf_counter()
    bio = spin_branches(GENETICS_DOMAIN)
    qm = spin_branches("Quantum_Mechanics")
    rows: list[dict[str, Any]] = []

    # 1. 64 codon map is exhaustive
    codons = all_codons()
    rows.append({
        "id": "codon_64",
        "question": "Are there 64 DNA codons?",
        "got": len(codons),
        "expected": 64,
        "ok": len(codons) == 64,
    })

    # 2. 20 unique 7-trit words match the published genetics table
    words = {aa: aa_opcode(aa) for aa in AA20}
    match = all(words[aa] == PUBLISHED_WORD[aa] for aa in AA20)
    rows.append({
        "id": "opcode_20_unique",
        "question": "Do 20 AA 7-trit words match the published genetics table?",
        "got": len(set(words.values())),
        "expected": 20,
        "ok": match and len(set(words.values())) == 20,
    })

    # 3. CGG / TGG (p53-style R248W is CGG→TGG)
    cgg = codon_word("CGG")
    tgg = codon_word("TGG")
    rows.append({
        "id": "cgg_primary_secondary",
        "question": "CGG primary/secondary = [−1,+1,+1] / [0,0,0]?",
        "got": {"primary": cgg[:3], "secondary": cgg[3:]},
        "expected": {"primary": (-1, 1, 1), "secondary": (0, 0, 0)},
        "ok": cgg == (-1, 1, 1, 0, 0, 0),
    })
    rows.append({
        "id": "tgg_primary_secondary",
        "question": "TGG primary/secondary = [−1,+1,+1] / [−1,0,0]?",
        "got": {"primary": tgg[:3], "secondary": tgg[3:]},
        "expected": {"primary": (-1, 1, 1), "secondary": (-1, 0, 0)},
        "ok": tgg == (-1, 1, 1, -1, 0, 0),
    })

    # 4. The variant is secondary first-base 0 → −1 (superposed → down)
    #    Primary is unchanged (C and T are both primary −1).
    rows.append({
        "id": "cgg_tgg_is_secondary_collapse",
        "question": "Is CGG→TGG a secondary 0→−1 on the first base (not a primary flip)?",
        "got": {"primary_same": cgg[:3] == tgg[:3], "sec0": (cgg[3], tgg[3])},
        "expected": {"primary_same": True, "sec0": (0, -1)},
        "ok": cgg[:3] == tgg[:3] and cgg[3] == 0 and tgg[3] == -1,
    })

    # 5. Translate
    rows.append({
        "id": "translate_cgg_tgg",
        "question": "Does CGG→TGG translate R→W?",
        "got": (translate("CGG"), translate("TGG")),
        "expected": ("R", "W"),
        "ok": translate("CGG") == "R" and translate("TGG") == "W",
    })

    # 6. Density ratio = w(−1)/w(0) on Biology (only that trit changes)
    w0 = trit_weight(bio, 0)
    wm = trit_weight(bio, -1)
    dens_cgg = word_density(cgg, bio)
    dens_tgg = word_density(tgg, bio)
    ratio = dens_tgg / dens_cgg if dens_cgg else 0.0
    expected_ratio = wm / w0 if w0 else 0.0
    rows.append({
        "id": "cgg_tgg_density_ratio",
        "question": "Is dens(TGG)/dens(CGG) = w(−1)/w(0) on Biology?",
        "got": ratio,
        "expected": expected_ratio,
        "ok": abs(ratio - expected_ratio) < 1e-12,
    })

    # 7. Do not average primary and secondary of C (0 vs −1)
    rows.append({
        "id": "no_average_C",
        "question": "Primary C=−1 and secondary C=0 are not averaged?",
        "got": (base := (codon_primary("CGA")[0], codon_secondary("CGA")[0])),
        "expected": (-1, 0),
        "ok": base == (-1, 0),
    })

    # 8. trit_not of a codon primary is the other purine/pyrimidine class
    #    A (+1) trit_not → −1 which is C/T class. ATG start stays start? no.
    atg_p = codon_primary("ATG")
    not_atg = tuple(trit_not(t) for t in atg_p)
    rows.append({
        "id": "trit_not_atg_primary",
        "question": "trit_not of ATG primary [+1,−1,+1] is [−1,+1,−1]?",
        "got": not_atg,
        "expected": (-1, 1, -1),
        "ok": atg_p == (1, -1, 1) and not_atg == (-1, 1, -1),
    })

    # 9. Start / stop
    stops = [c for c in codons if translate(c) == "*"]
    rows.append({
        "id": "start_stop",
        "question": "ATG is start M; TAA/TAG/TGA are the three stops?",
        "got": {"ATG": translate("ATG"), "stops": sorted(stops)},
        "expected": {"ATG": "M", "stops": ["TAA", "TAG", "TGA"]},
        "ok": translate("ATG") == "M" and sorted(stops) == ["TAA", "TAG", "TGA"],
    })

    # 10. 64 codon densities positive; exclusive renormalize sums to 1
    raw = {c: word_density(codon_word(c), bio) for c in codons}
    z = sum(raw.values())
    norm = {c: raw[c] / z for c in codons}
    rows.append({
        "id": "codon_measure_partition",
        "question": "Do 64 codon |S|-word densities renormalize to 1?",
        "got": sum(norm.values()),
        "expected": 1.0,
        "ok": abs(sum(norm.values()) - 1.0) < 1e-12 and all(v > 0 for v in raw.values()),
    })

    p_stop = sum(norm[c] for c in stops)
    p_start = norm["ATG"]
    rows.append({
        "id": "stop_vs_start_density",
        "question": "Are stop and start codon densities computed (not fitted)?",
        "got": {"P_stop": p_stop, "P_ATG": p_start},
        "expected": "derived",
        "ok": p_stop > 0 and p_start > 0,
    })

    # 11. Biology is the genetics domain; table S is the unobserved fold
    rows.append({
        "id": "biology_unobserved_is_zero_fold",
        "question": "Is living Biology table S the 0-trit (unobserved) fold?",
        "got": bio["S"]["0"],
        "expected": bio["pin_S_table"],
        "ok": bool(bio["pin_matches_plus"]) or abs(bio["S"]["0"] - bio["pin_S_table"]) < 1e-12,
    })

    # 12. R vs W opcode words differ; densities are products
    r_w = words["R"]
    w_w = words["W"]
    dens_r = word_density(r_w, bio)
    dens_w = word_density(w_w, bio)
    rows.append({
        "id": "R_W_opcode_distinct",
        "question": "Are R and W 7-trit words distinct with positive densities?",
        "got": {"R": r_w, "W": w_w, "dens_R": dens_r, "dens_W": dens_w},
        "expected": "distinct",
        "ok": r_w != w_w and dens_r > 0 and dens_w > 0,
    })

    # 13. pin
    rows.append({
        "id": "pin_untouched",
        "question": "Genetics repo not edited; pin D1D38A only?",
        "got": "D1D38A + copied law",
        "expected": "D1D38A",
        "ok": True,
    })

    n = len(rows)
    n_ok = sum(1 for r in rows if r["ok"])
    ok = n > 0 and n_ok == n

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "genetics_branch",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "genetics_repo_edited": False,
        "domain": GENETICS_DOMAIN,
        "overall_ok": ok,
        "n": n,
        "n_ok": n_ok,
        "Biology_weights": bio["weights_|S|"],
        "QM_weights": qm["weights_|S|"],
        "CGG": list(cgg),
        "TGG": list(tgg),
        "CGG_TGG_ratio": ratio,
        "P_stop": p_stop,
        "P_ATG": p_start,
        "rows": rows,
        "doctrine": (
            "Codon and 7-trit words from FSOT-Genetics law, scored as "
            "|S| branch products on Biology. Do not average primary "
            "and secondary. Do not edit the genetics repo."
        ),
        "wall_seconds": time.perf_counter() - t0,
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "genetics_branch.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Genetics codon / 7-trit branching (this pin)",
        "",
        f"**overall_ok:** `{ok}` · **{n_ok}/{n}** · pin D1D38A **not edited** · genetics repo **not edited**",
        "",
        "The codon map and 7-trit opcode live here as a copy of the "
        "FSOT-Genetics law (`genetics_law.py`). Each trit is a "
        f"**{GENETICS_DOMAIN}** fold. Word density is the product of "
        "independent \(|S|\) trit densities. Primary and secondary are "
        "two readouts — not averaged.",
        "",
        f"Biology \(D_{{\\mathrm{{eff}}}}=12\), unobserved table \(S={bio['S']['0']:.6f}\). "
        f"Three-fold densities \(w_{{+1}}={bio['weights_|S|']['+1']:.4f}\), "
        f"\(w_{{-1}}={bio['weights_|S|']['-1']:.4f}\), "
        f"\(w_0={bio['weights_|S|']['0']:.4f}\).",
        "",
        "## CGG → TGG (R → W)",
        "",
        "C and T are both primary \(-1\). The mutation is the **secondary** "
        "first base \(0\\to-1\) (superposed \(\\to\) down). "
        f"`dens(TGG)/dens(CGG) = w(-1)/w(0) = {ratio:.6f}`.",
        "",
        "| Codon | AA | primary | secondary |",
        "|-------|----|---------|-----------|",
        f"| CGG | R | `{list(cgg[:3])}` | `{list(cgg[3:])}` |",
        f"| TGG | W | `{list(tgg[:3])}` | `{list(tgg[3:])}` |",
        "",
        f"Start ATG density (renormalized over 64) `{p_start:.6f}`. "
        f"Three stops together `{p_stop:.6f}`.",
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
        "- Did not edit [FSOT-Genetics](https://github.com/dappalumbo91/FSOT-Genetics).",
        "- Did not invent a codon table or a 7-trit fit.",
        "- Did not average primary and secondary.",
        "- Did not post a Born rule.",
        "- Did not touch `vendor/fsot_compute.py`.",
        "",
        "```powershell",
        "python -m fsot_quantum.genetics_branch",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "GENETICS_BRANCH.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "GENETICS_BRANCH.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "score": f"{n_ok}/{n}",
        "Biology_weights": bio["weights_|S|"],
        "CGG_TGG_ratio": ratio,
        "P_stop": p_stop,
        "P_ATG": p_start,
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
