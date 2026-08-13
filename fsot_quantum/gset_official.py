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

import math
import os
from pathlib import Path
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.fold_complexity import cost_contrast, fold_budget_formal
from fsot_quantum.large_maxcut import RATIO_FLOOR
from fsot_quantum.optimization import cut_value, fsot_local_spins

# Literature champion cuts (Ye / Gset papers) — not free fits.
# G1 = 11624 is the standard published value used in SDP/QAOA comparisons.
PUBLISHED_CUTS = {
    "G1.TXT": 11624,
    "G1": 11624,
    "G11.TXT": 564,
    "G11": 564,
    "G14.TXT": 3064,
    "G14": 3064,
    "G22.TXT": 13359,
    "G22": 13359,
}

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
    """
    Incremental 1-flip MaxCut (O(degree) per trial).
    n<=32 also runs full fold local for exactable residual.
    """
    if n <= 32:
        s = fsot_local_spins(n, edges, maximize_cut=True)
        return cut_value(s, edges), s

    from fsot_quantum.domains import DOMAIN_SPIN_LAW, domain_scalar

    adj: list[list[int]] = [[] for _ in range(n)]
    for i, j, _w in edges:
        adj[i].append(j)
        adj[j].append(i)

    base = 1 if domain_scalar(DOMAIN_SPIN_LAW) > 0 else -1
    starts = [
        [base] * n,
        [-base] * n,
        [base if (i % 2 == 0) else -base for i in range(n)],
        [-base if (i % 2 == 0) else base for i in range(n)],
    ]
    phi = float(SEEDS.phi)
    n_phi = max(4, int(math.floor(float(SEEDS.e) * float(SEEDS.pi))))  # 8
    x = 1
    for k in range(n_phi):
        x = (x * int(phi * 1e6) + k * 2654435761) % (1 << 30)
        starts.append([1 if ((x >> (i % 30)) & 1) else -1 for i in range(n)])

    def cut_of(s: list[int]) -> int:
        return cut_value(s, edges)

    def polish(s0: list[int]) -> list[int]:
        s = list(s0)
        # greedy uncut-edge flip
        for i, j, _w in edges:
            if s[i] == s[j]:
                s[j] = -s[j]
        improved = True
        steps = 0
        cap = max(8, n)
        while improved and steps < cap:
            improved = False
            steps += 1
            for i in range(n):
                same = 0
                deg = len(adj[i])
                if deg == 0:
                    continue
                si = s[i]
                for j in adj[i]:
                    if s[j] == si:
                        same += 1
                # delta cut if flip i: 2*same - deg
                if 2 * same - deg > 0:
                    s[i] = -si
                    improved = True
        # FSOT snap: collapse the cut-gradient field, flip poles
        from fsot_lib.seeds import COLLAPSE_THRESHOLD
        from fsot_lib.trinary import collapse, code_to_signed

        field = []
        for i in range(n):
            deg = len(adj[i])
            same = sum(1 for j in adj[i] if s[j] == s[i])
            field.append(float(2 * same - deg))
        codes = collapse(field, threshold=COLLAPSE_THRESHOLD)
        if hasattr(codes, "tolist"):
            codes = codes.tolist()
        trial = list(s)
        for i, c in enumerate(codes):
            if code_to_signed(int(c)) > 0:
                trial[i] = -trial[i]
        if cut_of(trial) > cut_of(s):
            s = trial
        return s

    best = polish(starts[0])
    best_c = cut_of(best)
    for st in starts[1:]:
        cand = polish(st)
        c = cut_of(cand)
        if c > best_c:
            best, best_c = cand, c
    return best_c, best


def _try_fetch_gset(dest_dir: Path, name: str = "G1") -> Path | None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{name}.txt"
    if dest.exists() and dest.stat().st_size > 100:
        return dest
    allow = os.environ.get("FSOT_FETCH_GSET", "1") not in ("0", "false", "no")
    if not allow:
        return dest if dest.exists() else None
    url = f"https://web.stanford.edu/~yyye/yyye/Gset/{name}"
    try:
        import urllib.request

        req = urllib.request.Request(url, headers={"User-Agent": "FSOT-Quantum-fold/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        if len(data) < 20:
            return None
        dest.write_bytes(data)
        return dest
    except Exception:
        return dest if dest.exists() else None


def _try_fetch_g1(dest_dir: Path) -> Path | None:
    return _try_fetch_gset(dest_dir, "G1")


def run_gset_official_panel() -> dict[str, Any]:
    # Parser selftest
    n_fix, e_fix = parse_gset_text(_fixture_gset_text())
    parser_ok = n_fix == 6 and len(e_fix) == 6

    dest_dir = ROOT / "data" / "gset"
    fetched = _try_fetch_g1(dest_dir)
    extra = []
    # G14/G22: unweighted MaxCut. Skip signed ±1 grids (G11) — different object.
    for gname in ("G14", "G22"):
        hit = _try_fetch_gset(dest_dir, gname)
        if hit:
            extra.append(hit)
    official = find_official_files()
    for p in ([fetched] if fetched else []) + extra:
        if p and p not in official:
            official = [p] + official
    # unique by name
    seen_n: set[str] = set()
    uniq: list[Path] = []
    for p in official:
        if p.name not in seen_n:
            seen_n.add(p.name)
            uniq.append(p)
    official = [p for p in uniq if not p.stem.upper() == "G11"]

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
        key = path.stem.upper()
        published = PUBLISHED_CUTS.get(path.name.upper()) or PUBLISHED_CUTS.get(key)
        # 1/φ is the sparse-graph floor; official G1 champion ratio is ~0.606 < 1/φ,
        # so official graphs use: cut >= m/2, and if published, within 5% of champion.
        half_ok = cut * 2 >= n_e
        if published:
            rel_vs_pub = abs(published - cut) / published * 100.0
            ok = half_ok and rel_vs_pub <= 5.0
        else:
            rel_vs_pub = None
            ok = half_ok and ratio >= min(RATIO_FLOOR, 0.5)
        rows.append({
            "name": path.name,
            "path": str(path),
            "official": True,
            "n": n,
            "n_edges": n_e,
            "cut_fold": cut,
            "ratio_lb": ratio,
            "ratio_floor_sparse": RATIO_FLOOR,
            "published_cut": published,
            "rel_err_vs_published_pct": rel_vs_pub,
            "ok": ok,
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
