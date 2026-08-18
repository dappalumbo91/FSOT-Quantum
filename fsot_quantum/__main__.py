"""
Field entry: python -m fsot_quantum [cmd]

  check      pin/seed/D_eff vs Lean clone
  status     wrap snapshot pointer (docs/STATUS.md)
  accuracy   hired QC/QM jobs (Python/GPU)
  ask        run QC question battery (DJ/BV/Grover/Shor/Ising/G1/chem)
  hard       hard questions via FSOT math (K-scale; not foreign circuits)
  fold       domain-fold architecture on GPU (35 pin + Lean atlas)
  observe    typical questions + how the compute substrate is looked at
  mind       query: how genuine intelligence emerges (not an LLM)
  forward    architecture + known-answer checks + questions people want QC for
  harder     harder QC-for questions (CKM, Ising, nuclear, Gset, fabric)
  qi         physics + quantum-information rung (after graphs)
  push       physics + QI push II (CKM/Higgs/nuclear/Casimir/CHSH)
  push3      physics + QI push III (leftover CKM/LEP/BBN/cosmo)
  audit      stale vendor targets vs PDG/YR4
  family     Gset G1–G5 + G14–G17 + G22–G23 (<1% aspiration)
  open       diagnosis: wrong-object scoring (not living exclusive / SH0ES)
  vcb        |V_cb| puzzle: inclusive QM vs exclusive HEP
  h0         Hubble tension: Lean BH→WH bubble-bleed
  contested  Lean contested sectors (H0/S8/BBN/Higgs/σ8)
  leftovers  remaining opens: DE dual lane, alpha_s, V_cb, G17
  hire       expand hired QC questions (factor / dlog / Simon / SAT / HHL)
  hire2      climb higher: 7-digit factor / Simon-16 / SAT-16 / TSP / 1e7 search
  branch     probability as multiverse branching (no Born, no free param)
  gencode    genetics codon / 7-trit branching (law copied; genetics repo untouched)
  orf        ORF climb: start-to-stop as codon-fold product
  hire3      climb 3: 8-digit factor / dlog p=1e5
  hire4      climb 4: 9-digit factor / SAT-20 / TSP-8 / HHL 5×5 / MIS
  hire5      climb 5: 10-digit factor / SAT-24 / TSP-9 / HHL 6×6
  hire6      climb 6: 11-digit factor / SAT-28 / TSP-10 / HHL 7×7
  hire7      climb 7: 13-digit factor / SAT-32 / TSP-11 / HHL 8×8
  heights    G17 + far-prime (RSA-shaped) factoring — the written heights
  heights2   G17 close + p−1 log-N factor
  heights3   log-N: p−1 + p+1 + kN Fermat
  formulas   formula list — what each formula solves
  organ      export S/κ/QI JSON for neuron-zig
  stamp      Lean · Coq · Isabelle · F* · Python multiprover
  atlas      full Lean solved atlas
  expand     Lean chem + extra QM
  predict    print preregistered predictions
  qemu       remind / run QEMU OS (Windows)
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _cmd() -> str:
    return (sys.argv[1] if len(sys.argv) > 1 else "help").lower()


def main() -> int:
    c = _cmd()
    if c in ("help", "-h", "--help"):
        print(__doc__)
        print("Usable on an ordinary PC. Metal: .\\run_qemu.ps1")
        return 0
    if c == "check":
        from fsot_quantum.crosscheck import main as m
        return m()
    if c == "status":
        from fsot_quantum.status import main as m
        return m()
    if c == "accuracy":
        from fsot_quantum.qc_accuracy import main as m
        return m()
    if c == "ask":
        from fsot_quantum.ask_qc import main as m
        return m()
    if c == "hard":
        from fsot_quantum.hard_questions import main as m
        return m()
    if c == "fold":
        from fsot_quantum.fold_architecture import main as m
        return m()
    if c == "observe":
        from fsot_quantum.observe_emerge import main as m
        return m()
    if c == "mind":
        from fsot_quantum.emerge_mind import main as m
        return m()
    if c == "forward":
        from fsot_quantum.forward_ask import main as m
        return m()
    if c == "harder":
        from fsot_quantum.harder_qc import main as m
        return m()
    if c in ("qi", "physics"):
        from fsot_quantum.physics_qi import main as m
        return m()
    if c in ("push", "qi2"):
        from fsot_quantum.physics_qi2 import main as m
        return m()
    if c in ("push3", "qi3"):
        from fsot_quantum.physics_qi3 import main as m
        return m()
    if c == "audit":
        from fsot_quantum.stale_targets import main as m
        return m()
    if c == "family":
        from fsot_quantum.gset_family import main as m
        return m()
    if c in ("open", "objects"):
        from fsot_quantum.open_objects import main as m
        return m()
    if c == "vcb":
        from fsot_quantum.vcb_puzzle import main as m
        return m()
    if c == "h0":
        from fsot_quantum.h0_tension import main as m
        return m()
    if c in ("contested", "sectors"):
        from fsot_quantum.contested_sectors import main as m
        return m()
    if c in ("leftovers", "remaining"):
        from fsot_quantum.open_remaining import main as m
        return m()
    if c in ("hire", "hire_expand", "jobs"):
        from fsot_quantum.hire_expand import main as m
        return m()
    if c in ("hire2", "climbhire", "hire_climb"):
        from fsot_quantum.hire_climb import main as m
        return m()
    if c in ("branch", "prob", "probability"):
        from fsot_quantum.probability_branch import main as m
        return m()
    if c in ("gencode", "genetics", "codon"):
        from fsot_quantum.genetics_branch import main as m
        return m()
    if c in ("orf", "orf_branch"):
        from fsot_quantum.orf_branch import main as m
        return m()
    if c in ("hire3", "hire_climb3"):
        from fsot_quantum.hire_climb3 import main as m
        return m()
    if c in ("hire4", "hire_climb4"):
        from fsot_quantum.hire_climb4 import main as m
        return m()
    if c in ("hire5", "hire_climb5"):
        from fsot_quantum.hire_climb5 import main as m
        return m()
    if c in ("hire6", "hire_climb6"):
        from fsot_quantum.hire_climb6 import main as m
        return m()
    if c in ("hire7", "hire_climb7"):
        from fsot_quantum.hire_climb7 import main as m
        return m()
    if c in ("heights", "height"):
        from fsot_quantum.heights import main as m
        return m()
    if c in ("heights2", "height2"):
        from fsot_quantum.heights_next import main as m
        return m()
    if c in ("heights3", "height3"):
        from fsot_quantum.heights3 import main as m
        return m()
    if c in ("formulas", "catalog"):
        from fsot_quantum.formula_catalog import main as m
        return m()
    if c == "organ":
        from fsot_quantum.organ_export import main as m
        return m()
    if c == "stamp":
        return subprocess.call(
            [sys.executable, str(ROOT / "scripts" / "run_multiprover_verification.py")],
            cwd=str(ROOT),
        )
    if c == "atlas":
        from fsot_quantum.lean_full_atlas import main as m
        return m()
    if c == "expand":
        from fsot_quantum.expand_sim import main as m
        return m()
    if c == "predict":
        p = ROOT / "predictions" / "qc_preregistered.json"
        print(p.read_text(encoding="utf-8"))
        return 0
    if c == "qemu":
        script = ROOT / "run_qemu.ps1"
        if not script.is_file():
            print("run_qemu.ps1 missing")
            return 1
        return subprocess.call(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script)],
            cwd=str(ROOT),
        )
    print("unknown cmd:", c)
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
