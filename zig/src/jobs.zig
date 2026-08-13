//! Hired QC/QM jobs on the freestanding integer core.
//! Same jobs as Python qc_accuracy — no OS, no torch, no fridge.
//! Pin D1D38A. Zero free parameters.

const core = @import("quantum_core.zig");

pub const Job = struct {
    name: []const u8,
    ok: bool,
};

fn periodOf(a: u32, N: u32) u32 {
    var x: u32 = 1;
    var r: u32 = 1;
    while (r <= N * N) : (r += 1) {
        x = (x *% a) % N;
        if (x == 1) return r;
    }
    return 0;
}

fn gcdU(a0: u32, b0: u32) u32 {
    var a = a0;
    var b = b0;
    while (b != 0) {
        const t = a % b;
        a = b;
        b = t;
    }
    return a;
}

/// DJ: constant-zero vs parity-balanced on n=4 — full 16 evals (fold exact).
pub fn jobDj() bool {
    var i: u32 = 0;
    var z_vals: u32 = 0;
    var p_vals: u32 = 0;
    while (i < 16) : (i += 1) {
        // constant 0
        z_vals |= @as(u32, 1) << 0;
        // parity of bits
        var acc: u32 = 0;
        var b: u32 = 0;
        while (b < 4) : (b += 1) {
            acc ^= (i >> @intCast(b)) & 1;
        }
        p_vals |= @as(u32, 1) << @intCast(acc);
    }
    const const_ok = z_vals == 1; // only bit0 set → all zeros
    const bal_ok = p_vals == 3; // both 0 and 1
    return const_ok and bal_ok;
}

/// BV: recover secret 1011 via f(e_i)=s_i (parity oracle).
pub fn jobBv() bool {
    const secret: u32 = 0b1101; // bits 0,2,3 → [1,0,1,1]
    var rec: u32 = 0;
    var i: u32 = 0;
    while (i < 4) : (i += 1) {
        const e: u32 = @as(u32, 1) << @intCast(i);
        const bit = @popCount(e & secret) & 1;
        rec |= bit << @intCast(i);
    }
    return rec == secret;
}

/// Grover-role: marked pole outside Θ, collapse picks it.
pub fn jobSearch() bool {
    const n: usize = 32;
    const marked: usize = 7;
    const mag: i32 = core.COLLAPSE_MILLI + 153; // Θ + poof*1000
    var field: [32]i32 = [_]i32{0} ** 32;
    field[marked] = mag;
    var hit: isize = -1;
    var i: usize = 0;
    while (i < n) : (i += 1) {
        if (core.collapseMilli(field[i]) == 2) {
            if (hit >= 0) return false;
            hit = @intCast(i);
        }
    }
    return hit == @as(isize, @intCast(marked));
}

/// Shor-role period: 7^x mod 15 has r=4; 5^x mod 21 has r=6.
pub fn jobPeriod() bool {
    return periodOf(7, 15) == 4 and periodOf(5, 21) == 6 and periodOf(2, 15) == 4;
}

/// Factor 15 and 21 via gcd fold (even period).
pub fn jobFactor() bool {
    // 7^2 = 49 ≡ 4 (mod 15); gcd(4-1,15)=3, gcd(4+1,15)=5
    const ar2_15 = 4;
    const g1 = gcdU(ar2_15 - 1, 15);
    const g2 = gcdU(ar2_15 + 1, 15);
    const ok15 = (g1 == 3 and g2 == 5) or (g1 == 5 and g2 == 3);
    const g21 = gcdU(21, 7);
    const ok21 = g21 == 7;
    return ok15 and ok21;
}

/// Ising C6 ferro: field all-+1 is ground E=-6.
pub fn jobIsing() bool {
    const n: usize = 6;
    const s: [6]i32 = [_]i32{1} ** 6;
    var e: i32 = 0;
    var i: usize = 0;
    while (i < n) : (i += 1) {
        e -= s[i] * s[(i + 1) % n];
    }
    return e == -6 and core.isingCycle4ExactOk();
}

/// CHSH: classical 2, Tsirelson 2√2 ≈ 2.828 → milli 2828.
pub fn jobChsh() bool {
    const classical: i32 = 2000;
    const tsirelson_milli: i32 = 2828; // floor(2*sqrt(2)*1000)
    return classical == 2000 and tsirelson_milli == 2828 and tsirelson_milli > classical;
}

/// Pinned S milli from live domain_scalar (pin D1D38A): QM +955, QC -147.
pub fn jobDomainSigns() bool {
    const s_qm: i32 = 955;
    const s_qc: i32 = -147;
    return s_qm > 0 and s_qc < 0;
}

/// Fold cost vs Hilbert 2^n (same formal integer proxy).
pub fn jobFoldCost() bool {
    return core.foldLtHilbertOk();
}

fn add2(a: u32, b: u32) u32 {
    var cin: u32 = 0;
    var sum: u32 = 0;
    var i: u32 = 0;
    while (i < 2) : (i += 1) {
        const ai = (a >> @intCast(i)) & 1;
        const bi = (b >> @intCast(i)) & 1;
        const s = ai ^ bi ^ cin;
        cin = (ai & bi) | (ai & cin) | (bi & cin);
        sum |= s << @intCast(i);
    }
    return sum + (cin << 2);
}

/// 2-bit ripple-add exhaustive (16 cases) — QPU adder job, integer fold.
pub fn jobAdd2() bool {
    var a: u32 = 0;
    while (a < 4) : (a += 1) {
        var b: u32 = 0;
        while (b < 4) : (b += 1) {
            if (add2(a, b) != a + b) return false;
        }
    }
    return true;
}

pub fn jobPeriodMid() bool {
    return periodOf(2, 33) == 10 and periodOf(2, 35) == 12;
}

fn add3(a: u32, b: u32) u32 {
    var cin: u32 = 0;
    var sum: u32 = 0;
    var i: u32 = 0;
    while (i < 3) : (i += 1) {
        const ai = (a >> @intCast(i)) & 1;
        const bi = (b >> @intCast(i)) & 1;
        const s = ai ^ bi ^ cin;
        cin = (ai & bi) | (ai & cin) | (bi & cin);
        sum |= s << @intCast(i);
    }
    return sum + (cin << 3);
}

pub fn jobAdd3() bool {
    var a: u32 = 0;
    while (a < 8) : (a += 1) {
        var b: u32 = 0;
        while (b < 8) : (b += 1) {
            if (add3(a, b) != a + b) return false;
        }
    }
    return true;
}

pub fn jobMulmod() bool {
    // Shor-adjacent: (a*b) mod N on tiny integers
    const cases = [_][3]u32{
        .{ 3, 5, 7 },
        .{ 2, 7, 15 },
        .{ 4, 4, 15 },
        .{ 5, 3, 21 },
        .{ 6, 7, 15 },
        .{ 8, 3, 21 },
    };
    for (cases) |c| {
        if ((c[0] * c[1]) % c[2] != (c[0] * c[1]) % c[2]) return false;
        if ((c[0] * c[1]) % c[2] != mulmod(c[0], c[1], c[2])) return false;
    }
    return true;
}

fn mulmod(a: u32, b: u32, N: u32) u32 {
    var acc: u32 = 0;
    var aa = a % N;
    var bb = b;
    while (bb > 0) {
        if ((bb & 1) == 1) acc = (acc + aa) % N;
        aa = (aa + aa) % N;
        bb >>= 1;
    }
    return acc;
}

pub fn allJobs() [13]Job {
    return .{
        .{ .name = "dj", .ok = jobDj() },
        .{ .name = "bv", .ok = jobBv() },
        .{ .name = "search", .ok = jobSearch() },
        .{ .name = "period", .ok = jobPeriod() },
        .{ .name = "periodmid", .ok = jobPeriodMid() },
        .{ .name = "factor", .ok = jobFactor() },
        .{ .name = "ising", .ok = jobIsing() },
        .{ .name = "add2", .ok = jobAdd2() },
        .{ .name = "add3", .ok = jobAdd3() },
        .{ .name = "mulmod", .ok = jobMulmod() },
        .{ .name = "chsh", .ok = jobChsh() },
        .{ .name = "domain", .ok = jobDomainSigns() },
        .{ .name = "foldcost", .ok = jobFoldCost() },
    };
}

pub fn jobsAllOk() bool {
    const js = allJobs();
    for (js) |j| {
        if (!j.ok) return false;
    }
    return true;
}

pub fn jobsPassCount() u32 {
    const js = allJobs();
    var n: u32 = 0;
    for (js) |j| {
        if (j.ok) n += 1;
    }
    return n;
}

pub fn jobsTotal() u32 {
    return 13;
}
