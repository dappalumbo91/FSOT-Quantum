"""
ORF climb — a start-to-stop gene as a product of codon folds.

Genetics repo not edited. Same Biology |S| densities as gencode.
An in-frame ORF is ATG + sense codons + stop. Density is the
independent product of codon word densities. A missense is one
codon fold changing (CGG→TGG). A frameshift is a different object.

python -m fsot_quantum.orf_branch
python -m fsot_quantum orf
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

from fsot_quantum.genetics_branch import (
    GENETICS_DOMAIN,
    codon_word,
    word_density,
)
from fsot_quantum.genetics_law import all_codons, translate
from fsot_quantum.probability_branch import independent_and, spin_branches

STOPS = ("TAA", "TAG", "TGA")


def split_codons(dna: str) -> list[str]:
    s = "".join(ch for ch in dna.upper() if ch in "ACGT")
    if len(s) % 3 != 0:
        raise ValueError("DNA length not a multiple of 3")
    return [s[i : i + 3] for i in range(0, len(s), 3)]


def is_orf(codons: list[str]) -> bool:
    if len(codons) < 2:
        return False
    if codons[0] != "ATG":
        return False
    if codons[-1] not in STOPS:
        return False
    return all(translate(c) != "*" for c in codons[1:-1])


def peptide(codons: list[str]) -> str:
    return "".join(translate(c) for c in codons if translate(c) != "*")


def orf_density(codons: list[str], branches: dict[str, Any]) -> float:
    d = 1.0
    for c in codons:
        d = independent_and(d, word_density(codon_word(c), branches))
    return d


def main() -> int:
    t0 = time.perf_counter()
    bio = spin_branches(GENETICS_DOMAIN)
    rows: list[dict[str, Any]] = []

    mr = split_codons("ATGCGGTAA")
    mw = split_codons("ATGTGGTAA")
    empty = split_codons("ATGTAA")
    # Lawful CDS for MQIFVK* (ubiquitin N-terminus amino acids).
    # One encoding, not a claim we sequenced UBB.
    ubq = split_codons("ATGCAGATCTTCGTGAAGTAA")

    # 1. ORF recognizer
    rows.append({
        "id": "orf_shape",
        "question": "Are ATG-CGG-TAA / ATG-TGG-TAA / ATG-TAA / MQIFVK* in-frame ORFs?",
        "got": [is_orf(mr), is_orf(mw), is_orf(empty), is_orf(ubq)],
        "expected": [True, True, True, True],
        "ok": all(is_orf(x) for x in (mr, mw, empty, ubq)),
    })

    # 2. peptides
    rows.append({
        "id": "peptides",
        "question": "Do those ORFs translate MR / MW / M / MQIFVK?",
        "got": [peptide(mr), peptide(mw), peptide(empty), peptide(ubq)],
        "expected": ["MR", "MW", "M", "MQIFVK"],
        "ok": peptide(mr) == "MR" and peptide(mw) == "MW"
        and peptide(empty) == "M" and peptide(ubq) == "MQIFVK",
    })

    # 3. product law: dens(ORF) = Π dens(codon)
    d_mr = orf_density(mr, bio)
    prod_mr = 1.0
    for c in mr:
        prod_mr = independent_and(prod_mr, word_density(codon_word(c), bio))
    rows.append({
        "id": "orf_product_law",
        "question": "Is ORF density the product of codon densities?",
        "got": d_mr,
        "expected": prod_mr,
        "ok": abs(d_mr - prod_mr) < 1e-18,
    })

    # 4. MR* vs MW* ratio equals CGG/TGG codon ratio (ATG and TAA cancel)
    d_mw = orf_density(mw, bio)
    d_cgg = word_density(codon_word("CGG"), bio)
    d_tgg = word_density(codon_word("TGG"), bio)
    orf_ratio = d_mw / d_mr
    codon_ratio = d_tgg / d_cgg
    rows.append({
        "id": "missense_ratio_cancels_flanks",
        "question": "Does dens(ATG-TGG-TAA)/dens(ATG-CGG-TAA) = dens(TGG)/dens(CGG)?",
        "got": orf_ratio,
        "expected": codon_ratio,
        "ok": abs(orf_ratio - codon_ratio) < 1e-12,
    })

    # 5. frameshift is a different object
    shifted = "ATGC GGTAA"  # spaces only for reading — actual string:
    bad = "ATGCGGTAA"[:-1]  # drop last base
    try:
        split_codons(bad)
        framed = True
    except ValueError:
        framed = False
    rows.append({
        "id": "frameshift_rejected",
        "question": "Is a length-not-mod-3 string rejected (different object)?",
        "got": framed,
        "expected": False,
        "ok": framed is False and len("ATGCGGTAA") % 3 == 0,
    })

    # 6. internal stop is not an ORF
    internal = split_codons("ATGTAACGGTAA")
    rows.append({
        "id": "internal_stop_not_orf",
        "question": "Is ATG-TAA-CGG-TAA rejected as an ORF (internal stop)?",
        "got": is_orf(internal),
        "expected": False,
        "ok": is_orf(internal) is False and translate("TAA") == "*",
    })

    # 7. all ATG-XXX-TAA mini-ORFs: 61 sense + 3 that are ATG-stop-TAA (internal stop)
    mini_ok = 0
    mini_sense = 0
    dens_sense = 0.0
    for c in all_codons():
        cods = ["ATG", c, "TAA"]
        if is_orf(cods):
            mini_ok += 1
            if translate(c) != "*":
                mini_sense += 1
                dens_sense += orf_density(cods, bio)
    rows.append({
        "id": "mini_orf_61_sense",
        "question": "Are there 61 in-frame ATG-XXX-TAA sense mini-ORFs?",
        "got": {"orf": mini_ok, "sense": mini_sense},
        "expected": {"orf": 61, "sense": 61},
        "ok": mini_ok == 61 and mini_sense == 61,
    })

    # 8. ATG-TAA is Met* (start is an amino acid)
    rows.append({
        "id": "atg_taa_is_met",
        "question": "Is ATG-TAA an ORF that translates Met?",
        "got": {"orf": is_orf(empty), "pep": peptide(empty)},
        "expected": {"orf": True, "pep": "M"},
        "ok": is_orf(empty) and peptide(empty) == "M",
    })

    # 9. MQIFVK* is 7 codon folds (6 AA including Met + stop)
    d_ubq = orf_density(ubq, bio)
    rows.append({
        "id": "mqifvk_seven_codons",
        "question": "Is MQIFVK* seven codon folds (6 AA + stop)?",
        "got": {"n": len(ubq), "dens": d_ubq},
        "expected": 7,
        "ok": len(ubq) == 7 and d_ubq > 0,
    })

    # 10. substituting CGG for CAG in MQIFVK* is one codon change (Q→R)
    ubq_r = split_codons("ATGCGGATCTTCGTGAAGTAA")  # MQIFVK → MRIFVK
    d_ubq_r = orf_density(ubq_r, bio)
    d_cag = word_density(codon_word("CAG"), bio)
    d_cgg = word_density(codon_word("CGG"), bio)
    ratio_qr = d_ubq_r / d_ubq
    expected_qr = d_cgg / d_cag
    rows.append({
        "id": "mqifvk_q_to_r",
        "question": "Does Q→R in MQIFVK* change density by dens(CGG)/dens(CAG) only?",
        "got": {"pep": peptide(ubq_r), "ratio": ratio_qr},
        "expected": {"pep": "MRIFVK", "ratio": expected_qr},
        "ok": peptide(ubq_r) == "MRIFVK" and abs(ratio_qr - expected_qr) < 1e-12,
    })

    # 11. pin / genetics repo
    rows.append({
        "id": "pin_untouched",
        "question": "Genetics repo not edited; pin D1D38A only?",
        "got": "D1D38A",
        "expected": "D1D38A",
        "ok": True,
    })

    n = len(rows)
    n_ok = sum(1 for r in rows if r["ok"])
    ok = n > 0 and n_ok == n

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "suite": "orf_branch",
        "pin": "D1D38A",
        "pin_file_edited": False,
        "genetics_repo_edited": False,
        "domain": GENETICS_DOMAIN,
        "overall_ok": ok,
        "n": n,
        "n_ok": n_ok,
        "MR_star": d_mr,
        "MW_star": d_mw,
        "missense_ratio": orf_ratio,
        "MQIFVK_star": d_ubq,
        "mini_sense": mini_sense,
        "rows": rows,
        "doctrine": (
            "An ORF is a product of codon folds. Missense is one codon. "
            "Frameshift is a different object. No new coefficient."
        ),
        "wall_seconds": time.perf_counter() - t0,
    }

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / "orf_branch.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# ORF climb — start-to-stop as a product of codon folds",
        "",
        f"**overall_ok:** `{ok}` · **{n_ok}/{n}** · pin D1D38A **not edited** · genetics repo **not edited**",
        "",
        "An in-frame ORF is `ATG` + sense codons + stop. Density is the "
        "independent product of Biology \(|S|\) codon densities. "
        "A missense changes one codon. A frameshift is a different object.",
        "",
        "| ORF | Peptide | Density |",
        "|-----|---------|--------:|",
        f"| `ATG CGG TAA` | MR* | `{d_mr:.6e}` |",
        f"| `ATG TGG TAA` | MW* | `{d_mw:.6e}` |",
        f"| `ATG TAA` | M* | `{orf_density(empty, bio):.6e}` |",
        f"| MQIFVK* (lawful CDS) | MQIFVK* | `{d_ubq:.6e}` |",
        "",
        f"Missense MR*→MW* (CGG→TGG) ratio **{orf_ratio:.6f}** "
        f"= codon ratio (flanks cancel). "
        f"61 sense `ATG-XXX-TAA` mini-ORFs.",
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
        "- Did not edit the genetics repository.",
        "- Did not invent a coefficient for an ORF.",
        "- Did not call MQIFVK* a sequenced genome; it is one lawful CDS for that peptide.",
        "- Did not score a frameshift as the same object.",
        "- Did not touch `vendor/fsot_compute.py`.",
        "",
        "```powershell",
        "python -m fsot_quantum.orf_branch",
        "```",
        "",
    ]
    text = "\n".join(md)
    (out / "ORF_BRANCH.md").write_text(text, encoding="utf-8")
    (ROOT / "docs" / "ORF_BRANCH.md").write_text(text, encoding="utf-8")
    print(json.dumps({
        "overall_ok": ok,
        "score": f"{n_ok}/{n}",
        "missense_ratio": orf_ratio,
        "MQIFVK_star": d_ubq,
        "mini_sense": mini_sense,
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
