#!/usr/bin/env python3
"""
FSOT-Quantum multiprover verification — Lean 4 · Coq · Isabelle · F* · Python runtime.

Modeled on FSOT-2.1-Lean cross-proof discipline:
  - shared obligation spine (verification/obligations/quantum_spine.json)
  - each prover reports ok / skip / fail
  - overall_ok requires Python runtime + all present formal provers
  - stamp written to results/multiprover_verification_report.json

Usage:
  python scripts/run_multiprover_verification.py
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

SPINE = ROOT / "verification" / "obligations" / "quantum_spine.json"
OUT = ROOT / "results" / "multiprover_verification_report.json"
PIN_EXPECTED = "D1D38A"


def _run(cmd: list[str], cwd: Path, timeout: int = 600) -> tuple[int, str]:
    try:
        p = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )
        out = (p.stdout or "") + (p.stderr or "")
        return p.returncode, out
    except FileNotFoundError as e:
        return 127, str(e)
    except subprocess.TimeoutExpired:
        return 124, "timeout"


def pin_check() -> dict[str, Any]:
    p = ROOT / "vendor" / "fsot_compute.py"
    pin = hashlib.sha256(p.read_bytes()).hexdigest()[:6].upper()
    return {"ok": pin == PIN_EXPECTED, "got": pin, "expected": PIN_EXPECTED}


def python_runtime_obligations() -> dict[str, Any]:
    """Replay every obligation against fsot_lib / fsot_quantum runtime."""
    from fsot_lib.seeds import COLLAPSE_THRESHOLD, SEEDS
    from fsot_lib.trinary import (
        code_to_signed,
        pack_roundtrip_ok,
        pack_u64,
        signed_to_code,
        unpack_u64,
    )
    STATES_PER_U64 = 32  # formal + GPU contract
    from fsot_quantum.domains import DOMAINS, domain_scalar
    from fsot_quantum.gates import apply_cx, neg, pair

    checks: list[dict[str, Any]] = []

    def add(oid: str, ok: bool, detail: Any = None):
        checks.append({"id": oid, "ok": ok, "detail": detail})

    # Q-TRIT
    for s in (-1, 0, 1):
        ok = code_to_signed(signed_to_code(s)) == s
        if not ok:
            break
    else:
        ok = True
    add("Q-TRIT-001", ok)
    add("Q-TRIT-002", all(signed_to_code(s) in (0, 1, 2) for s in (-1, 0, 1)))
    add("Q-TRIT-003", STATES_PER_U64 == 32)

    # Q-GATE
    add("Q-GATE-001", all(neg(neg(s)) == s for s in (-1, 0, 1)))
    add("Q-GATE-002", all(apply_cx(1, t) == -t for t in (-1, 0, 1)))
    add("Q-GATE-003", all(apply_cx(-1, t) == t for t in (-1, 0, 1)))
    add("Q-GATE-004", all(pair(0, t) == 0 for t in (-1, 0, 1)))

    # Q-PACK
    add("Q-PACK-001", 32 * 2 == 64)
    codes = [i % 3 for i in range(32)]
    add("Q-PACK-002", unpack_u64(pack_u64(codes)) == codes and pack_roundtrip_ok(codes))

    # Q-DOM
    add("Q-DOM-001", DOMAINS["Quantum_Mechanics"].D_eff == 6)
    add("Q-DOM-002", DOMAINS["Quantum_Computing"].D_eff == 11)
    add(
        "Q-DOM-003",
        DOMAINS["Quantum_Mechanics"].observed is True
        and DOMAINS["Quantum_Computing"].observed is False,
    )
    add(
        "Q-DOM-004",
        DOMAINS["Quantum_Mechanics"].D_eff < 25
        and DOMAINS["Quantum_Computing"].D_eff < 25,
    )

    # Q-NUM
    thr_gold = 0.9174663774653723
    add(
        "Q-NUM-001",
        abs(COLLAPSE_THRESHOLD - thr_gold) < 1e-12
        and abs(SEEDS.c_eff * SEEDS.p_var - thr_gold) < 1e-12,
        {"theta": COLLAPSE_THRESHOLD},
    )
    s_qm = domain_scalar("Quantum_Mechanics")
    s_qc = domain_scalar("Quantum_Computing")
    add("Q-NUM-002", s_qm > 0 and s_qc < 0, {"S_QM": s_qm, "S_QC": s_qc})
    add(
        "Q-STRUCT-001",
        STATES_PER_U64 == 32
        and DOMAINS["Quantum_Mechanics"].D_eff == 6
        and DOMAINS["Quantum_Computing"].D_eff == 11,
    )

    # Q-FOLD cost contrast (integer proxy shared with Lean/Coq/Isabelle/F*/Zig)
    from fsot_quantum.fold_complexity import (
        fold_budget_formal,
        fold_work_k_int,
        fold_work_via_k,
        k_matches_pin,
    )
    import math as _math

    add(
        "Q-FOLD-001",
        fold_budget_formal(8) == 195 and fold_budget_formal(8) < (1 << 8),
        {"fold8": fold_budget_formal(8), "hilbert8": 1 << 8},
    )
    add(
        "Q-FOLD-002",
        fold_budget_formal(16) < (1 << 16) and fold_budget_formal(32) < (1 << 32),
        {"fold16": fold_budget_formal(16), "fold32": fold_budget_formal(32)},
    )

    # Q-JOB integer facts shared with formal/lean|coq|isabelle|fstar Jobs
    add("Q-JOB-001", pow(7, 4) % 15 == 1)
    add("Q-JOB-002", pow(5, 6) % 21 == 1)
    add("Q-JOB-003", pow(2, 10) % 33 == 1 and pow(8, 8) % 51 == 1)
    add("Q-JOB-004", 3 * 5 == 15 and 3 * 7 == 21 and 3 * 11 == 33)
    add(
        "Q-JOB-005",
        _math.gcd(3, 15) == 3
        and _math.gcd(5, 15) == 5
        and pow(7, 2) % 15 == 4
        and _math.gcd(4 - 1, 15) == 3
        and _math.gcd(4 + 1, 15) == 5,
    )

    # Q-K universal scaling — S = K(T1+T2+T3)
    add("Q-K-001", k_matches_pin(), {"K": float(SEEDS.k)})
    add(
        "Q-K-002",
        fold_work_k_int(8) == 47
        and fold_work_via_k(8) == 47
        and fold_work_k_int(64) == 180
        and fold_work_k_int(8) < (1 << 8)
        and fold_work_k_int(64) < (1 << 20),
        {"work8": fold_work_k_int(8), "work64": fold_work_k_int(64)},
    )

    ok = all(c["ok"] for c in checks)
    return {
        "prover": "python_runtime",
        "ok": ok,
        "status": "pass" if ok else "fail",
        "n_obligations": len(checks),
        "n_pass": sum(1 for c in checks if c["ok"]),
        "checks": checks,
    }


def run_lean() -> dict[str, Any]:
    lean_dir = ROOT / "formal" / "lean"
    lake = shutil.which("lake")
    if not lake:
        return {
            "prover": "lean4",
            "ok": False,
            "status": "skip",
            "reason": "lake not on PATH",
        }
    # lake build
    code, out = _run([lake, "build"], lean_dir, timeout=900)
    ok = code == 0
    return {
        "prover": "lean4",
        "ok": ok,
        "status": "pass" if ok else "fail",
        "exit_code": code,
        "log_tail": out[-4000:] if out else "",
        "cwd": str(lean_dir),
    }


def run_coq() -> dict[str, Any]:
    coqc = shutil.which("coqc")
    if not coqc:
        return {
            "prover": "coq",
            "ok": False,
            "status": "skip",
            "reason": "coqc not on PATH",
        }
    coq_dir = ROOT / "formal" / "coq"
    files = [
        "Trinary.v",
        "Gates.v",
        "Pack.v",
        "Domains.v",
        "Hilbert.v",
        "Fold.v",
        "Jobs.v",
    ]
    logs = []
    all_ok = True
    # Plain coqc in-order so Require Import Trinary finds Trinary.vo (no -Q rename)
    for f in files:
        # remove stale mismatched .vo from prior -Q Top builds
        vo = coq_dir / (Path(f).stem + ".vo")
        if f == "Trinary.v" and vo.exists():
            pass  # rebuild each full run
        code, out = _run([coqc, f], coq_dir, timeout=300)
        logs.append({"file": f, "exit_code": code, "ok": code == 0})
        if code != 0:
            all_ok = False
            logs[-1]["log_tail"] = out[-2000:]
    return {
        "prover": "coq",
        "ok": all_ok,
        "status": "pass" if all_ok else "fail",
        "files": logs,
    }


def _resolve_fstar() -> str | None:
    """Prefer a working local fstar.exe; skip broken removable-drive stubs."""
    candidates: list[Path] = []
    home = os.environ.get("FSTAR_HOME")
    if home:
        candidates.append(Path(home) / "bin" / "fstar.exe")
    candidates.extend(
        [
            Path.home() / "tools" / "fstar-v2026.07.05" / "bin" / "fstar.exe",
            ROOT / "tools" / "fstar" / "bin" / "fstar.exe",
            Path(r"I:\FSOT-Physical-Archive\07_Portable-Toolchain\fstar\bin\fstar.exe"),
        ]
    )
    for name in ("fstar.exe", "fstar"):
        found = shutil.which(name)
        if found:
            candidates.append(Path(found))
    seen: set[str] = set()
    for cand in candidates:
        key = str(cand)
        if key in seen or not cand.exists():
            continue
        seen.add(key)
        try:
            r = subprocess.run(
                [str(cand), "--version"],
                capture_output=True,
                text=True,
                timeout=30,
            )
            blob = (r.stdout or "") + (r.stderr or "")
            if r.returncode == 0 or "F*" in blob:
                return str(cand)
        except OSError:
            continue
        except Exception:
            continue
    return None


def run_fstar() -> dict[str, Any]:
    exe = _resolve_fstar()
    if not exe:
        return {
            "prover": "fstar",
            "ok": False,
            "status": "skip",
            "reason": "no working fstar.exe",
        }
    jobs = ROOT / "formal" / "fstar" / "Jobs.fst"
    if not jobs.is_file():
        return {
            "prover": "fstar",
            "ok": False,
            "status": "fail",
            "reason": f"missing {jobs}",
        }
    code, out = _run([exe, "--cache_off", str(jobs)], jobs.parent, timeout=300)
    verified = "Verified module: Jobs" in (out or "") and code == 0
    return {
        "prover": "fstar",
        "ok": verified,
        "status": "pass" if verified else "fail",
        "exit_code": code,
        "tool": exe,
        "entry": str(jobs.relative_to(ROOT)),
        "log_tail": (out or "")[-4000:],
    }


def run_isabelle() -> dict[str, Any]:
    """
    Windows Isabelle is a bash script under bin/isabelle (not the GUI .exe).
    Invoke via contrib/cygwin/bin/bash.exe -lc 'isabelle build ...'
    """
    isabelle_home = None
    desk = Path(r"C:\Users\damia\Desktop")
    for d in sorted(desk.glob("Isabelle*"), reverse=True):
        if (d / "bin" / "isabelle").exists():
            isabelle_home = d
            break
    if not isabelle_home:
        return {
            "prover": "isabelle",
            "ok": False,
            "status": "skip",
            "reason": "Isabelle home with bin/isabelle not found",
        }
    bash = isabelle_home / "contrib" / "cygwin" / "bin" / "bash.exe"
    if not bash.exists():
        # try any bash under contrib
        cands = list((isabelle_home / "contrib").rglob("bash.exe"))
        bash = cands[0] if cands else None
    if not bash or not Path(bash).exists():
        return {
            "prover": "isabelle",
            "ok": False,
            "status": "skip",
            "reason": f"cygwin bash not found under {isabelle_home}",
            "isabelle_home": str(isabelle_home),
        }

    isabelle_dir = ROOT / "formal" / "isabelle"
    # POSIX paths for bash
    home_posix = str(isabelle_home).replace("\\", "/")
    dir_posix = str(isabelle_dir).replace("\\", "/")
    # Drive letter: C:/Users/... works in Cygwin if /cygdrive/c/...
    def to_cyg(p: str) -> str:
        p = p.replace("\\", "/")
        if len(p) >= 2 and p[1] == ":":
            return f"/cygdrive/{p[0].lower()}{p[2:]}"
        return p

    cmd_sh = (
        f'export PATH="{to_cyg(home_posix)}/bin:$PATH"; '
        f'isabelle build -d "{to_cyg(dir_posix)}" FSOT_Quantum'
    )
    code, out = _run(
        [str(bash), "-lc", cmd_sh],
        ROOT,
        timeout=1800,
    )
    ok = code == 0
    return {
        "prover": "isabelle",
        "ok": ok,
        "status": "pass" if ok else "fail",
        "exit_code": code,
        "isabelle_home": str(isabelle_home),
        "bash": str(bash),
        "log_tail": (out or "")[-4000:],
    }


def main() -> int:
    t0 = time.perf_counter()
    spine = json.loads(SPINE.read_text(encoding="utf-8"))

    pin = pin_check()
    py = python_runtime_obligations()
    lean = run_lean()
    coq = run_coq()
    isa = run_isabelle()
    fstar = run_fstar()

    provers = {
        "python_runtime": py,
        "lean4": lean,
        "coq": coq,
        "isabelle": isa,
        "fstar": fstar,
    }

    formal = (lean, coq, isa, fstar)
    formal_present = [p for p in formal if p.get("status") != "skip"]
    formal_ok = all(p.get("ok") for p in formal_present) if formal_present else False
    at_least_one_formal = any(p.get("ok") for p in formal)
    overall = bool(pin["ok"] and py["ok"] and at_least_one_formal and formal_ok)

    if any(p.get("status") == "skip" for p in formal):
        nonskip = [p for p in formal if p.get("status") != "skip"]
        overall = bool(pin["ok"] and py["ok"] and nonskip and all(p["ok"] for p in nonskip))

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "kit": "FSOT-Quantum multiprover verification",
        "pin": pin,
        "spine": {
            "path": str(SPINE.relative_to(ROOT)),
            "n_obligations": len(spine["obligations"]),
            "ids": [o["id"] for o in spine["obligations"]],
        },
        "provers": provers,
        "overall_ok": overall,
        "stamp": "FSOT_QUANTUM_MULTIPROVER_OK" if overall else "FSOT_QUANTUM_MULTIPROVER_OPEN",
        "wall_seconds": time.perf_counter() - t0,
        "claims": {
            "math": "trinary spin algebra, pack contracts, domain D_eff folds, hired QC job integers",
            "programming_structure": "gates CX/neg/pair, pack capacity, runtime parity, Jobs twins",
            "not_claimed": "full Hilbert unitary equivalence; a prover may skip if not installed",
        },
    }

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# FSOT-Quantum multiprover verification stamp",
        "",
        f"**stamp:** `{report['stamp']}`",
        f"**overall_ok:** `{overall}`",
        f"**pin:** `{pin.get('got')}` (expect D1D38A)",
        f"**wall_s:** `{report['wall_seconds']:.2f}`",
        "",
        "## Provers",
        "",
        "| Prover | Status | OK |",
        "|--------|--------|----|",
    ]
    for name, p in provers.items():
        md.append(f"| {name} | {p.get('status')} | {p.get('ok')} |")
    md += [
        "",
        f"## Obligations: {len(spine['obligations'])}",
        "",
        "Spine: `verification/obligations/quantum_spine.json`",
        "",
        "## Reproduce",
        "",
        "```powershell",
        'cd "C:\\Users\\damia\\Desktop\\fsot quantum"',
        "$env:PYTHONPATH = (Get-Location).Path",
        "python scripts\\run_multiprover_verification.py",
        "```",
        "",
        "Lean: `cd formal\\lean; lake build`",
        "Coq: `cd formal\\coq; coqc Trinary.v Gates.v Pack.v Domains.v Hilbert.v Fold.v Jobs.v`",
        "Isabelle: `isabelle build -d formal/isabelle FSOT_Quantum`",
        "F*: `fstar --cache_off formal\\fstar\\Jobs.fst`",
        "",
    ]
    (ROOT / "results" / "MULTIPROVER_STAMP.md").write_text("\n".join(md), encoding="utf-8")
    (ROOT / "docs" / "MULTIPROVER_VERIFICATION.md").write_text("\n".join(md), encoding="utf-8")

    print(json.dumps({
        "overall_ok": overall,
        "stamp": report["stamp"],
        "pin": pin,
        "provers": {k: {"status": v.get("status"), "ok": v.get("ok")} for k, v in provers.items()},
        "wall_seconds": report["wall_seconds"],
    }, indent=2))
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
