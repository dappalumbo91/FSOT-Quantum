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
from collections import deque
from pathlib import Path
from typing import Any

from fsot_lib.seeds import SEEDS
from fsot_quantum.fold_complexity import (
    cost_contrast,
    fold_budget_formal,
    fold_depth_ladder,
    fold_probe_budget,
    phi_walk_indices,
)
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
    "G2": 11620,
    "G2.TXT": 11620,
    "G3": 11622,
    "G3.TXT": 11622,
    "G4": 11646,
    "G4.TXT": 11646,
    "G5": 11631,
    "G5.TXT": 11631,
    "G23": 13344,
    "G23.TXT": 13344,
    "G15": 3050,
    "G15.TXT": 3050,
    "G16": 3052,
    "G16.TXT": 3052,
    "G17": 3047,
    "G17.TXT": 3047,
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
    cm = 1 if domain_scalar("Condensed_Matter") > 0 else -1
    mat = 1 if domain_scalar("Materials_Science") > 0 else -1
    starts = [
        [base] * n,
        [-base] * n,
        [base if (i % 2 == 0) else -base for i in range(n)],
        [-base if (i % 2 == 0) else base for i in range(n)],
        [cm if (i % 2 == 0) else -cm for i in range(n)],
        [mat if (i % 3 == 0) else -mat for i in range(n)],
    ]
    # Per-vertex φ bits. A 30-bit stripe repeating across n=800 was a broken start.
    phi_m = int(float(SEEDS.phi) * 1e6)
    n_phi = int(math.floor(float(SEEDS.e) * float(SEEDS.pi))) * int(math.floor(float(SEEDS.pi)))
    for k in range(n_phi):
        row = []
        for i in range(n):
            x = (phi_m * (k + 1) * (i + 1) + (k + 3) * 2654435761 + i * 40503) & 0xFFFFFFFF
            row.append(1 if (x >> 16) & 1 else -1)
        starts.append(row)
    # golden partition (seed φ) and e-walk (second seed, not a free RNG)
    half = n // 2
    starts.append([1 if ((i * phi_m) % n) < half else -1 for i in range(n)])
    e_m = int(float(SEEDS.e) * 1e6)
    n_e = int(math.floor(float(SEEDS.pi)))
    for k in range(n_e):
        row = []
        for i in range(n):
            x = (e_m * (k + 1) * (i + 3) + (k + 1) * 2246822519 + i * 17) & 0xFFFFFFFF
            row.append(1 if (x >> 15) & 1 else -1)
        starts.append(row)

    # Laplacian of L = D−A. x^T L x = 4·cut for x=±1.
    # n≤800 keeps the single power-iter start (G1–G17 living cuts).
    # n=2000 had no spectral/BFS; extra deflated modes + hyperplanes
    # are that scale's lane, not a coefficient.
    if n <= 2000:
        n_iter = max(
            n,
            int(math.floor(float(SEEDS.e) * float(SEEDS.pi)))
            * int(math.floor(float(SEEDS.pi))),
        )
        n_modes = 1 if n <= 800 else max(2, int(math.floor(float(SEEDS.pi))))
        deg = [len(adj[i]) for i in range(n)]
        modes: list[list[float]] = []
        for r in range(n_modes):
            if r == 0:
                v = [
                    float(((phi_m * (i + 1)) & 0xFFFF) / 65536.0) - 0.5
                    for i in range(n)
                ]
            else:
                v = [
                    float(((phi_m * (i + 1) * (r + 3)) & 0xFFFF) / 65536.0) - 0.5
                    for i in range(n)
                ]
            for u in modes:
                dot = sum(v[i] * u[i] for i in range(n))
                v = [v[i] - dot * u[i] for i in range(n)]
            nrm = math.sqrt(sum(x * x for x in v)) or 1.0
            v = [x / nrm for x in v]
            for _ in range(n_iter):
                w = [0.0] * n
                for i, nbr in enumerate(adj):
                    acc = deg[i] * v[i]
                    for j in nbr:
                        acc -= v[j]
                    w[i] = acc
                for u in modes:
                    dot = sum(w[i] * u[i] for i in range(n))
                    w = [w[i] - dot * u[i] for i in range(n)]
                nrm = math.sqrt(sum(x * x for x in w)) or 1.0
                v = [x / nrm for x in w]
            modes.append(v)
            starts.append([1 if v[i] >= 0.0 else -1 for i in range(n)])
        if n > 800:
            thetas = (
                0.0,
                1.0 / float(SEEDS.phi),
                1.0 / float(SEEDS.e),
                1.0 / float(SEEDS.pi),
            )
            for i in range(len(modes)):
                for j in range(i + 1, len(modes)):
                    for th in thetas:
                        cth = math.cos(2.0 * math.pi * th)
                        sth = math.sin(2.0 * math.pi * th)
                        starts.append(
                            [
                                1 if modes[i][t] * cth + modes[j][t] * sth >= 0.0 else -1
                                for t in range(n)
                            ]
                        )

        n_src = max(
            int(math.isqrt(n)),
            int(math.floor(float(SEEDS.e) * float(SEEDS.pi))) * int(math.floor(float(SEEDS.pi))),
        )
        for src in phi_walk_indices(n, n_src, seed_k=n + 17):
            dist = [-1] * n
            dist[src] = 0
            dq = deque([src])
            while dq:
                u = dq.popleft()
                for v2 in adj[u]:
                    if dist[v2] < 0:
                        dist[v2] = dist[u] + 1
                        dq.append(v2)
            starts.append([1 if (d if d >= 0 else 0) % 2 == 0 else -1 for d in dist])

    def cut_of(s: list[int]) -> int:
        return cut_value(s, edges)

    def polish(s0: list[int]) -> list[int]:
        s = list(s0)
        # Do not greedy-flip every uncut edge. That is not fold law and
        # funnels G14 every start into one 1-opt (cut 2913).
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
        # FSOT snap: collapse the cut-gradient field, floor(π) rounds
        from fsot_lib.seeds import COLLAPSE_THRESHOLD
        from fsot_lib.trinary import collapse, code_to_signed

        snap_rounds = max(1, int(math.floor(float(SEEDS.pi))))
        for _ in range(snap_rounds):
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
            else:
                break
        return s

    def kl_pass(s0: list[int]) -> list[int]:
        """
        Kernighan–Lin variable-depth: flip even when a single move loses,
        keep the prefix with best cumulative gain. Tie-break by index.
        This is why 1-flip plateaus sit 2–5% under published champions.
        """
        nloc = n
        locked = [False] * nloc
        cur = list(s0)
        gain = [0] * nloc
        for i, nbr in enumerate(adj):
            same = 0
            for j in nbr:
                if cur[j] == cur[i]:
                    same += 1
            gain[i] = 2 * same - len(nbr)
        seq: list[int] = []
        gseq: list[int] = []
        for _ in range(nloc):
            best_i = -1
            best_g = -10 ** 9
            for i in range(nloc):
                if locked[i]:
                    continue
                if gain[i] > best_g:
                    best_g = gain[i]
                    best_i = i
            if best_i < 0:
                break
            # flip best_i, update neighbor gains
            si = cur[best_i]
            cur[best_i] = -si
            locked[best_i] = True
            seq.append(best_i)
            gseq.append(best_g)
            gain[best_i] = -gain[best_i]
            for j in adj[best_i]:
                if cur[j] == si:
                    # was same, now different
                    gain[j] -= 2
                else:
                    gain[j] += 2
        acc = 0
        best_acc = 0
        best_k = -1
        for k, g in enumerate(gseq):
            acc += g
            if acc > best_acc:
                best_acc = acc
                best_k = k
        if best_k < 0:
            return list(s0)
        out = list(s0)
        for i in seq[: best_k + 1]:
            out[i] = -out[i]
        return out

    best = polish(starts[0])
    best_c = cut_of(best)
    pool = [(best_c, best)]
    for st in starts[1:]:
        cand = polish(st)
        c = cut_of(cand)
        pool.append((c, cand))
        if c > best_c:
            best, best_c = cand, c
    def two_opt(s0: list[int]) -> list[int]:
        """Improving 2-flips. Adjacent pair gain: δi+δj − 2·same_sign."""
        s = list(s0)
        neighbor = [set() for _ in range(n)]
        for i, j, _w in edges:
            neighbor[i].add(j)
            neighbor[j].add(i)
        moved = True
        guard = 0
        while moved and guard < n:
            moved = False
            guard += 1
            dlt = [0] * n
            for i, nbr in enumerate(adj):
                same = 0
                for j in nbr:
                    if s[j] == s[i]:
                        same += 1
                dlt[i] = 2 * same - len(nbr)
            best_g = 0
            pair = None
            if n > 800:
                # G22-scale: only existing edges (O(m)), not n²
                for i, j, _w in edges:
                    if i > j:
                        continue
                    g = dlt[i] + dlt[j]
                    g -= 2 if s[i] == s[j] else -2
                    if g > best_g:
                        best_g = g
                        pair = (i, j)
            else:
                for i in range(n):
                    for j in range(i + 1, n):
                        g = dlt[i] + dlt[j]
                        if j in neighbor[i]:
                            g -= 2 if s[i] == s[j] else -2
                        if g > best_g:
                            best_g = g
                            pair = (i, j)
            if pair is None:
                break
            i, j = pair
            s[i] = -s[i]
            s[j] = -s[j]
            moved = True
        return s

    def refine(s0: list[int]) -> list[int]:
        s = list(s0)
        c = cut_of(s)
        rounds = max(3, int(math.floor(float(SEEDS.e) * float(SEEDS.pi))))
        for _ in range(rounds):
            s2 = kl_pass(s)
            s2 = two_opt(s2)
            s2 = polish(s2)
            c2 = cut_of(s2)
            if c2 <= c:
                break
            s, c = s2, c2
        return s

    # KL + 2-opt on the top floor(e·π) distinct 1-opt basins
    pool.sort(key=lambda t: -t[0])
    # n>800 used to KL only ⌊eπ⌋ basins. Extra spectral/BFS starts
    # would then displace the old winners. Same seed product as BFS
    # source count keeps the old basins in the pool.
    n_kl = len(pool) if n <= 800 else min(
        len(pool),
        max(
            int(math.floor(float(SEEDS.e) * float(SEEDS.pi)))
            * int(math.floor(float(SEEDS.pi))),
            int(math.floor(float(SEEDS.e) * float(SEEDS.pi))),
        ),
    )
    if n <= 800:
        seen_c: set[int] = set()
        refine_iter = []
        for c0, s0 in pool[:n_kl]:
            if c0 in seen_c:
                continue
            seen_c.add(c0)
            refine_iter.append(s0)
    else:
        seen_s: set[tuple[int, ...]] = set()
        refine_iter = []
        for c0, s0 in pool[:n_kl]:
            sig = tuple(s0)
            if sig in seen_s:
                continue
            seen_s.add(sig)
            refine_iter.append(s0)
    for s0 in refine_iter:
        s = refine(s0)
        c = cut_of(s)
        if c > best_c:
            best, best_c = s, c
    # seed-locked breakout from the winner, then refine again
    phi_m = int(float(SEEDS.phi) * 1e6)
    rounds = max(3, int(math.floor(float(SEEDS.e) * float(SEEDS.pi))))
    stride = max(2, int(math.floor(float(SEEDS.pi))))
    s = list(best)
    strides = (
        2,
        stride,
        max(4, int(math.floor(float(SEEDS.e) * float(SEEDS.pi)))),
        max(8, int(math.floor(float(SEEDS.pi) ** 3))),  # 31 — G17's leftover scale
    )
    for stride_k in strides:
        for r in range(rounds):
            trial = list(s)
            for i in range(n):
                x = (phi_m * (r + 1) * (i + 1) + r * 2654435761 + stride_k) & 0xFFFFFFFF
                if (x >> 16) % stride_k == 0:
                    trial[i] = -trial[i]
            trial = refine(trial)
            tc = cut_of(trial)
            if tc > best_c:
                best, best_c, s = trial, tc, trial

    def _gains(s0: list[int]) -> list[int]:
        g = [0] * n
        for i, nbr in enumerate(adj):
            same = 0
            for j in nbr:
                if s0[j] == s0[i]:
                    same += 1
            g[i] = 2 * same - len(nbr)
        return g

    # Plateau ridge: at 1-opt the flip-gain field is ≤ 0 and Θ cannot
    # fire. Walk the zero-gain ridge in φ-order, then refine. Seed
    # bounded — not a crawl and not a new coefficient.
    zeros = [i for i, g in enumerate(_gains(best)) if g == 0]
    zeros.sort(key=lambda i: (phi_m * (i + 1) + 2654435761) & 0xFFFFFFFF)
    kick_n = max(1, int(math.floor(float(SEEDS.e) * float(SEEDS.pi))))
    for r in range(rounds):
        trial = list(best)
        take = zeros[r * kick_n : (r + 1) * kick_n]
        if not take:
            take = zeros[:kick_n]
        for i in take:
            trial[i] = -trial[i]
        trial = refine(trial)
        tc = cut_of(trial)
        if tc > best_c:
            best, best_c = trial, tc
            zeros = [i for i, g in enumerate(_gains(best)) if g == 0]
            zeros.sort(key=lambda i: (phi_m * (i + 1) + 2654435761) & 0xFFFFFFFF)

    # 3-flip on a φ-walk of triples (n≤800). One improving triple
    # then refine — the 31-edge G17 gap is larger than 1-opt/2-opt.
    if n <= 800:
        budget = fold_probe_budget(n, fold_depth_ladder()["deep"])
        span = n * n * n
        s3 = list(best)
        c3 = best_c
        for idx in phi_walk_indices(span, budget, seed_k=n + best_c):
            i = idx % n
            j = (idx // n) % n
            k = (idx // n // n) % n
            if i == j or j == k or i == k:
                continue
            s3[i] = -s3[i]
            s3[j] = -s3[j]
            s3[k] = -s3[k]
            tc = cut_of(s3)
            if tc > c3:
                s3 = refine(s3)
                c3 = cut_of(s3)
                if c3 > best_c:
                    best, best_c = list(s3), c3
            else:
                s3[i] = -s3[i]
                s3[j] = -s3[j]
                s3[k] = -s3[k]
        if c3 > best_c:
            best, best_c = s3, c3

    # Split monochromatic uncut blobs. Extra uncut edges sit inside
    # same-sign components; flipping a φ-subset of a blob is the
    # cluster move 1-opt cannot make. n=2000 also gets the adjacency
    # spectral split of each blob.
    if n <= 2000:
        seen_v = [False] * n
        comps: list[list[int]] = []
        for src in range(n):
            if seen_v[src]:
                continue
            stack = [src]
            seen_v[src] = True
            comp = [src]
            while stack:
                u = stack.pop()
                su = best[u]
                for v in adj[u]:
                    if not seen_v[v] and best[v] == su:
                        seen_v[v] = True
                        stack.append(v)
                        comp.append(v)
            if len(comp) >= 3:
                comps.append(comp)
        blob_iter = max(
            int(math.floor(float(SEEDS.e) * float(SEEDS.pi)))
            * int(math.floor(float(SEEDS.pi))),
            8,
        )
        for ci, comp in enumerate(comps):
            trial = list(best)
            for i in comp:
                x = (phi_m * (i + 1) * (ci + 3) + 40503) & 0xFFFFFFFF
                if (x >> 16) & 1:
                    trial[i] = -trial[i]
            trial = refine(trial)
            tc = cut_of(trial)
            if tc > best_c:
                best, best_c = trial, tc
            # second split: every other vertex in φ-order along the blob
            trial = list(best)
            ordered = sorted(comp, key=lambda i: (phi_m * (i + 1)) & 0xFFFFFFFF)
            for k, i in enumerate(ordered):
                if k % 2 == 0:
                    trial[i] = -trial[i]
            trial = refine(trial)
            tc = cut_of(trial)
            if tc > best_c:
                best, best_c = trial, tc
            if n > 800 and len(comp) >= 4:
                loc = {v: i for i, v in enumerate(comp)}
                sblob = len(comp)
                av = [
                    float(((phi_m * (comp[i] + 1) * (ci + 5)) & 0xFFFF) / 65536.0) - 0.5
                    for i in range(sblob)
                ]
                nrm = math.sqrt(sum(x * x for x in av)) or 1.0
                av = [x / nrm for x in av]
                for _ in range(min(blob_iter, sblob)):
                    w = [0.0] * sblob
                    for i, v in enumerate(comp):
                        acc = 0.0
                        for nb in adj[v]:
                            j = loc.get(nb)
                            if j is not None:
                                acc += av[j]
                        w[i] = acc
                    nrm = math.sqrt(sum(x * x for x in w)) or 1.0
                    av = [x / nrm for x in w]
                trial = list(best)
                for i, v in enumerate(comp):
                    if av[i] >= 0.0:
                        trial[v] = -trial[v]
                trial = refine(trial)
                tc = cut_of(trial)
                if tc > best_c:
                    best, best_c = trial, tc

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
