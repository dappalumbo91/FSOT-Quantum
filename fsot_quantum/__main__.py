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
  open       open objects: exclusive V_cb, H0 tension, alpha_s
  vcb        |V_cb| puzzle: inclusive QM vs exclusive HEP
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
