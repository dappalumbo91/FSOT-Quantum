//! FSOT-Quantum Zig twin — fixed trinary register.
//! Authority: pin D1D38A · pack codes match FSOT-GPU / Lean (0=down, 1=super, 2=up).
//! Signed: -1 / 0 / +1. Zero free parameters.

const std = @import("std");

pub const Trit = i8; // -1 | 0 | +1

// Seed-derived collapse threshold C_eff * P_var (FSOT-GPU triangulation)
pub const COLLAPSE_THRESHOLD: f64 = 0.9174663774653723;
pub const C_EFF: f64 = 0.9577022026205613;
pub const POOF: f64 = 0.1534822148944508;

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

/// Continuous → pack code {0,1,2}
pub fn collapseCode(v: f64) u8 {
    if (v > COLLAPSE_THRESHOLD) return 2;
    if (v < -COLLAPSE_THRESHOLD) return 0;
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

/// H-analog: ±1 → 0; 0 → resolve_sign (pass +1 for QM emergence, -1 for QC damp)
pub fn hAnalog(t: Trit, resolve: Trit) Trit {
    if (t != 0) return 0;
    return resolve;
}

/// CX-analog: control +1 flip; 0 super; -1 hold
pub fn cxTarget(c: Trit, t: Trit) Trit {
    if (c == 0) return 0;
    if (c > 0) return neg(t);
    return t;
}

/// Pack 32 codes {0,1,2} into u64 (FSOT-GPU wire format)
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
    while (i < 32) : (i += 1) {
        codes[i] = @truncate(i % 3);
    }
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
    const thr = COLLAPSE_THRESHOLD;
    const field = [_]f64{ 1.0, -1.0, 0.0, thr + 0.02, -(thr + 0.02) };
    const expect = [_]u8{ 2, 0, 1, 2, 0 };
    var i: usize = 0;
    while (i < field.len) : (i += 1) {
        if (collapseCode(field[i]) != expect[i]) return false;
    }
    return true;
}

/// Bell-analog structure: H on 0, CX 0→1, measure resolve both with resolve sign
pub fn bellAnalog(resolve: Trit) [2]Trit {
    var s0: Trit = -1;
    var s1: Trit = -1;
    s0 = hAnalog(s0, resolve); // → 0 if was ±1
    s1 = cxTarget(s0, s1); // control super → target super
    // measure: superposed → resolve
    if (s0 == 0) s0 = resolve;
    if (s1 == 0) s1 = resolve;
    return .{ s0, s1 };
}

pub fn selftest() bool {
    if (!packRoundtripOk()) return false;
    if (!collapseRoundtripOk()) return false;
    if (neg(1) != -1 or neg(-1) != 1 or neg(0) != 0) return false;
    if (pair(1, -1) != -1) return false;
    if (consensus(1, 1) != 1 or consensus(1, -1) != 0) return false;
    if (cxTarget(1, 1) != -1) return false;
    if (cxTarget(-1, 1) != 1) return false;
    if (cxTarget(0, 1) != 0) return false;
    // QC damp resolve = -1
    const b = bellAnalog(-1);
    if (b[0] != -1 or b[1] != -1) return false;
    return true;
}

pub fn main() void {
    const ok = selftest();
    std.debug.print("FSOT-Quantum Zig twin selftest: {s}\n", .{if (ok) "PASS" else "FAIL"});
    std.debug.print("COLLAPSE_THRESHOLD={d}\n", .{COLLAPSE_THRESHOLD});
    std.debug.print("pack_roundtrip={s} collapse={s}\n", .{
        if (packRoundtripOk()) "ok" else "fail",
        if (collapseRoundtripOk()) "ok" else "fail",
    });
    if (!ok) std.process.exit(1);
}
