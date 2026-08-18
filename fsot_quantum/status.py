"""
Print the wrap snapshot pointer and the locked headline numbers.

Does not recompute physics. The living ledgers are the docs.
python -m fsot_quantum.status
python -m fsot_quantum status
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    snap = {
        "suite": "status",
        "pin": "D1D38A",
        "wrap": "docs/STATUS.md",
        "ladder": "docs/LADDER.md",
        "index": "docs/INDEX.md",
        "reproduce": "docs/REPRODUCE.md",
        "headlines": {
            "audit": "20/20 fold vs YR4/PDG @0.5%",
            "harder": "20/20 @0.5%",
            "physics_qi": "16/16 + 326/326 Lean",
            "physics_qi2": "22/22 + 126/126 Lean",
            "physics_qi3": "41/41 + 212/212 Lean",
            "gset_family": "10/11 under 1%; G17 1.017%",
            "hire_expand": "29/29 factor/dlog/Simon/SAT/HHL/search",
            "hire_climb": "32/32 through 2196323 / Simon-16 / 1e7",
            "probability_branch": "19/19 |S| folds, no Born",
            "genetics_branch": "15/15 codon/7-trit on Biology",
            "orf_branch": "11/11 ORF product of codon folds",
            "hire_climb3": "17/17 through 20937233 / dlog p=1e5",
            "hire_climb4": "22/22 through 144216077 / SAT-20 / TSP-8",
            "chemistry": "68/68 @0.5%",
            "S_QM": "+0.9555 emergence",
            "S_QC": "-0.1477 damping",
            "V_cb": "inclusive 0.002%; exclusive B→D 0.15%",
            "H0": "Planck 0.024%; SH0ES 1.00% Lean BH→WH",
            "alpha_s": "0.68% inside vendor 0.9% band",
            "open": [
                "Gset G17 1.017% (31 edges)",
                "Gset champions unmatched (aspiration <1% landed except G17)",
                "vendor BR_H_gg field still stale; fold matches YR4",
            ],
            "claims": "docs/CLAIMS.md",
        },
        "comparison": "hired question, not their stack",
        "replaces": [
            "cryogenic QPU / Hilbert 2^n / QAOA box / FCI sales pitch",
        ],
        "jobs_current": {
            "factor_Shor": "tiny N 3/3 and 4/4 — same job, larger moduli still to climb",
            "MaxCut": "10/11 under 1%; G17 1.017%",
            "chemistry": "68/68 @0.5% (pin formulas, not Hilbert FCI)",
        },
        "refuse": [
            "replay a foreign circuit as the answer",
            "invent a coefficient",
            "blend disagreeing extractions",
            "chatbot as mind",
        ],
    }
    print(json.dumps(snap, indent=2))
    print()
    print((ROOT / "docs" / "STATUS.md").resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
