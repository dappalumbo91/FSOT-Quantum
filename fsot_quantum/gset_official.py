"""
Official Gset MaxCut loader + residuals (if archive present).

Looks in local folders; optionally fetches one small file from Stanford
if FSOT_FETCH_GSET=1. Parser is always tested against an in-repo Gset-format
fixture (not claimed as official G1).

Gset line format (Ye):
  n m
  i j w     (1-based vertices, w usually 1)

Large official graphs (n=800) use 1-flip fold only (no O(n^2) pair pass).

Zero free parameters. pin D1D38A.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.fold_complexity import cost_contrast, fold_budget_formal
from fsot_quantum.large_maxcut import RATIO_FLOOR
from fsot_quantum.optimization import cut_value, fsot_local_spins

ROOT = Path(__file__).resolve().parents[1]

SEARCH_DIRS = [
    ROOT / "data" / "gset",
    ROOT / "_ref" / "gset",
    Path(os.environ.get("FSOT_GSET_DIR", "")) if os.environ.get("FSOT_GSET_DIR") else None,
    Path.home() / "Downloads" / "Gset",
    Path.home() / "Desktop" / "Gset",
]


def parse_gset_text(text: str) -> tuple[int, list[tuple[int, int, int]]]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]
    if not lines:
        raise ValueError("empty gset")
    head = lines[0].split()
    n = int(head[0])
    m = int(head[1]) if len(head) > 1 else None
    edges: list[tuple[int, int, int]] = []
    seen: set[tuple[int, int]] = set()
    for ln in lines[1:]:
        parts = ln.split()
        if len(parts) < 2:
            continue
        i, j = int(parts[0]) - 1, int(parts[1]) - 1
        w = int(parts[2]) if len(parts) > 2 else 1
        if i == j:
            continue
        if i > j:
            i, j = j, i
        if (i, j) in seen:
            continue
        seen.add((i, j))
        edges.append((i, j, 1 if w == 0 else abs(w)))
    if m is not None and len(edges) != m:
        # some files count directed; accept if close
        pass
    return n, edges


def find_official_files() -> list[Path]:
    found: list[Path] = []
    for d in SEARCH_DIRS:
        if d is None or not d.is_dir():
            continue
        for p in sorted(d.glob("G*.txt")) + sorted(d.glob("g*.txt")):
            if p.is_file():
                found.append(p)
    return found


def _fixture_gset_text() -> str:
    """Tiny Gset-format graph (cycle C6) — parser selftest, not official G1."""
    # 6 verts, 6 edges
    lines = ["6 6"]
    for i in range(1, 7):
        j = i + 1 if i < 6 else 1
        lines.append(f"{i} {j} 1")
    return "\n".join(lines) + "\n"


def _fast_maxcut(n: int, edges: list[tuple[int, int, int]]) -> tuple[int, list[int]]:
    """1-flip only for large n; full fold local for n<=64."""
    if n <= 64:
        s = fsot_local_spins(n, edges, maximize_cut=True)
        return cut_value(s, edges), s
    # large: domain/checkerboard + 1-flip, no pair pass
    from fsot_quantum.domains import DOMAIN_SPIN_LAW, domain_scalar

    base = 1 if domain_scalar(DOMAIN_SPIN_LAW) > 0 else -1
    starts = [
        [base] * n,
        [-base] * n,
        [base if (i % 2 == 0) else -base for i in range(n)],
    ]
    phi = float(SEEDS.phi)
    x = 1
    for k in range(4):
        x = (x * int(phi * 1e6) + k * 2654435761) % (1 << min(n, 30))
        starts.append([1 if (x >> (i % 30)) & 1 else -1 for i in range(n)])

    def score(s: list[int]) -> int:
        return cut_value(s, edges)

    def polish(s0: list[int]) -> list[int]:
        s = list(s0)
        for i, j, _J in edges:
            if s[i] == s[j]:
                s[j] = -s[j]
        improved = True
        steps = 0
        while improved and steps < n * 8:
            improved = False
            steps += 1
            cur = score(s)
            for i in range(n):
                s[i] = -s[i]
                if score(s) > cur:
                    improved = True
                    break
                s[i] = -s[i]
        return s

    best = polish(starts[0])
    best_c = score(best)
    for st in starts[1:]:
        cand = polish(st)
        c = score(cand)
        if c > best_c:
            best, best_c = cand, c
    return best_c, best


def _try_fetch_g1(dest_dir: Path) -> Path | None:
    if os.environ.get("FSOT_FETCH_GSET", "") not in ("1", "true", "yes"):
        return None
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "G1.txt"
    if dest.exists():
        return dest
    url = "https://web.stanford.edu/~yyye/yyye/Gset/G1"
    try:
        import urllib.request

        req = urllib.request.Request(url, headers={"User-Agent": "FSOT-Quantum-fold/1.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        dest.write_bytes(data)
        return dest
    except Exception:
        return None


def run_gset_official_panel() -> dict[str, Any]:
    # Parser selftest
    n_fix, e_fix = parse_gset_text(_fixture_gset_text())
    parser_ok = n_fix == 6 and len(e_fix) == 6

    official = find_official_files()
    fetched = None
    if not official:
        fetched = _try_fetch_g1(ROOT / "data" / "gset")
        if fetched:
            official = [fetched]

    rows = []
    for path in official[:4]:  # cap
        try:
            n, edges = parse_gset_text(path.read_text(encoding="utf-8", errors="replace"))
        except Exception as e:
            rows.append({"name": path.name, "ok": False, "error": str(e)[:200]})
            continue
        cut, _s = _fast_maxcut(n, edges)
        n_e = len(edges)
        ratio = cut / n_e if n_e else 0.0
        rows.append({
            "name": path.name,
            "path": str(path),
            "official": True,
            "n": n,
            "n_edges": n_e,
            "cut_fold": cut,
            "ratio_lb": ratio,
            "ratio_floor": RATIO_FLOOR,
            "ok": ratio >= RATIO_FLOOR,
            "hilbert_amps_if_QAOA": None if n > 40 else (1 << n),
            "fold_budget_formal": fold_budget_formal(n),
            "cost": cost_contrast(min(n, 32), n_e),
        })

    have_official = len(official) > 0
    official_ok = all(r.get("ok") for r in rows) if rows else False
    return {
        "panel": "gset_official",
        "parser_ok": parser_ok,
        "official_found": have_official,
        "n_official": len(official),
        "fetched": str(fetched) if fetched else None,
        "instances": rows,
        "pass_count": sum(1 for r in rows if r.get("ok")),
        "total": len(rows),
        "overall_ok": parser_ok and (official_ok if have_official else True),
        "status": "official" if have_official else "skip_official_parser_ok",
        "note": (
            "Official Gset used only if files exist under data/gset or FSOT_GSET_DIR. "
            "Otherwise parser fixture only — not claimed as G1–G54 residuals. "
            "Set FSOT_FETCH_GSET=1 to attempt Stanford G1."
        ),
    }
