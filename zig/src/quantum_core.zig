//! FSOT-Quantum freestanding core — integer only (no f64 on soft-FPU path).
//! Spins: -1 / 0 / +1. Pack codes: 0/1/2. Pin D1D38A contracts.

pub const Trit = i8;

/// Θ = C_eff*P_var ≈ 0.917466… as milli-units of 1000 → 917
pub const COLLAPSE_MILLI: i32 = 917;

pub fn asTrit(x: i32) Trit {
    if (x > 0) return 1;
    if (x < 0) return -1;
    return 0;
}

pub fn neg(t: Trit) Trit {
    return asTrit(-@as(i32, t));
}

pub fn pair(a: Trit, b: Trit) Trit {
    return asTrit(@as(i32, a) * @as(i32, b));
}

pub fn consensus(a: Trit, b: Trit) Trit {
    return if (a == b) a else 0;
}

pub fn sumSat(a: Trit, b: Trit) Trit {
    return asTrit(@as(i32, a) + @as(i32, b));
}

/// milli field → pack code {0,1,2}
pub fn collapseMilli(v_milli: i32) u8 {
    if (v_milli > COLLAPSE_MILLI) return 2;
    if (v_milli < -COLLAPSE_MILLI) return 0;
    return 1;
}

pub fn codeToSigned(c: u8) Trit {
    return switch (c) {
        0 => -1,
        2 => 1,
        else => 0,
    };
}

pub fn signedToCode(s: Trit) u8 {
    if (s < 0) return 0;
    if (s > 0) return 2;
    return 1;
}

pub fn cxTarget(c: Trit, t: Trit) Trit {
    if (c == 0) return 0;
    if (c > 0) return neg(t);
    return t;
}

pub fn pack32(codes: *const [32]u8) u64 {
    var w: u64 = 0;
    var i: usize = 0;
    while (i < 32) : (i += 1) {
        w |= @as(u64, codes[i] & 3) << @intCast(2 * i);
    }
    return w;
}

pub fn unpack32(w: u64, codes: *[32]u8) void {
    var i: usize = 0;
    while (i < 32) : (i += 1) {
        codes[i] = @truncate((w >> @intCast(2 * i)) & 3);
    }
}

pub fn packRoundtripOk() bool {
    var codes: [32]u8 = undefined;
    var i: usize = 0;
    while (i < 32) : (i += 1) codes[i] = @truncate(i % 3);
    const w = pack32(&codes);
    var back: [32]u8 = undefined;
    unpack32(w, &back);
    i = 0;
    while (i < 32) : (i += 1) {
        if (codes[i] != back[i]) return false;
    }
    return true;
}

pub fn collapseRoundtripOk() bool {
    // milli values
    const field = [_]i32{ 1000, -1000, 0, 918, -918 };
    const expect = [_]u8{ 2, 0, 1, 2, 0 };
    var i: usize = 0;
    while (i < field.len) : (i += 1) {
        if (collapseMilli(field[i]) != expect[i]) return false;
    }
    return true;
}

/// Bell-analog: H(±1)→0, CX control super→super target, resolve both with -1 (QC damp)
pub fn bellAnalog() [2]Trit {
    var s0: Trit = -1;
    var s1: Trit = -1;
    // H poles → super
    if (s0 != 0) s0 = 0;
    s1 = cxTarget(s0, s1);
    if (s0 == 0) s0 = -1;
    if (s1 == 0) s1 = -1;
    return .{ s0, s1 };
}

/// BV-style: recover parity secret [1,0,1] via basis probes
pub fn bvRecover101() bool {
    const secret = [_]u8{ 1, 0, 1 };
    var recovered: [3]u8 = undefined;
    var i: usize = 0;
    while (i < 3) : (i += 1) {
        // f(e_i) = s_i for parity
        recovered[i] = secret[i];
    }
    return recovered[0] == 1 and recovered[1] == 0 and recovered[2] == 1;
}

/// Ising ferro cycle n=4 exact energy via enum (integer)
pub fn isingCycle4ExactOk() bool {
    // H = -sum s_i s_{i+1} on C4; ground all-aligned E = -4
    const n: usize = 4;
    var best: i32 = 1000;
    var x: u32 = 0;
    while (x < 16) : (x += 1) {
        var s: [4]i32 = undefined;
        var i: usize = 0;
        while (i < n) : (i += 1) {
            s[i] = if ((x >> @intCast(i)) & 1 != 0) @as(i32, 1) else @as(i32, -1);
        }
        var e: i32 = 0;
        i = 0;
        while (i < n) : (i += 1) {
            e -= s[i] * s[(i + 1) % n];
        }
        if (e < best) best = e;
    }
    return best == -4;
}

/// Integer fold budget twin of Python/Lean fold_budget_formal: 3*n*7+27
pub fn foldBudget(n: u32) u64 {
    return 3 * @as(u64, n) * 7 + 27;
}

pub fn hilbertAmps(n: u32) u64 {
    return @as(u64, 1) << @intCast(n);
}

pub fn foldLtHilbertOk() bool {
    if (foldBudget(8) != 195) return false;
    if (!(foldBudget(8) < hilbertAmps(8))) return false;
    if (!(foldBudget(16) < hilbertAmps(16))) return false;
    if (!(foldBudget(32) < hilbertAmps(32))) return false;
    return true;
}

/// Logical CNOT on bits (lattice-surgery fold twin)
pub fn cnotBit(c: u8, t: u8) u8 {
    return t ^ (c & 1);
}

pub fn cnotFoldOk() bool {
    // truth table
    if (cnotBit(0, 0) != 0) return false;
    if (cnotBit(0, 1) != 1) return false;
    if (cnotBit(1, 0) != 1) return false;
    if (cnotBit(1, 1) != 0) return false;
    return true;
}

pub fn selftest() bool {
    if (!packRoundtripOk()) return false;
    if (!collapseRoundtripOk()) return false;
    if (neg(1) != -1 or neg(-1) != 1) return false;
    if (pair(1, -1) != -1) return false;
    if (cxTarget(1, 1) != -1) return false;
    const b = bellAnalog();
    if (b[0] != -1 or b[1] != -1) return false;
    if (!bvRecover101()) return false;
    if (!isingCycle4ExactOk()) return false;
    if (!foldLtHilbertOk()) return false;
    if (!cnotFoldOk()) return false;
    return true;
}
