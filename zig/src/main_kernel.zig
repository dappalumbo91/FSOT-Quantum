//! FSOT-Quantum freestanding Multiboot kernel — QEMU serial gate.
//! Pattern: PFLT / fsot-neuron-zig bare metal.
//! Integer-only quantum core (soft-FPU safe).

const serial = @import("serial.zig");
const qc = @import("quantum_core.zig");
const jobs = @import("jobs.zig");

const MULTIBOOT_MAGIC: u32 = 0x1BADB002;
const MULTIBOOT_FLAGS: u32 = 0x00000003;
const MULTIBOOT_CHECKSUM: u32 = 0 -% (MULTIBOOT_MAGIC +% MULTIBOOT_FLAGS);

export const multiboot_header align(4) linksection(".multiboot") = [_]u32{
    MULTIBOOT_MAGIC,
    MULTIBOOT_FLAGS,
    MULTIBOOT_CHECKSUM,
};

var stack_bytes: [256 * 1024]u8 align(16) = undefined;

export fn _start() callconv(.c) noreturn {
    const stack_top = @intFromPtr(&stack_bytes) + stack_bytes.len;
    asm volatile (
        \\mov %[sp], %%esp
        \\mov %[sp], %%ebp
        :
        : [sp] "r" (stack_top),
        : .{ .memory = true }
    );
    kmain();
}

fn enableFpu() void {
    asm volatile (
        \\mov %%cr0, %%eax
        \\and $0xFFFFFFF3, %%eax
        \\or  $0x2, %%eax
        \\mov %%eax, %%cr0
        \\mov %%cr4, %%eax
        \\or  $0x600, %%eax
        \\mov %%eax, %%cr4
        \\fninit
        ::: .{ .eax = true, .memory = true }
    );
}

fn kmain() noreturn {
    serial.init();
    serial.write("FSOT_QUANTUM_KERNEL boot\n");
    serial.write("pin D1D38A trinary pathway\n");

    enableFpu();
    serial.write("FPU ok\n");

    serial.write("test:pack...\n");
    if (qc.packRoundtripOk()) serial.write("FSOT pack PASS\n") else serial.write("FSOT pack FAIL\n");

    serial.write("test:collapse...\n");
    if (qc.collapseRoundtripOk()) serial.write("FSOT collapse PASS\n") else serial.write("FSOT collapse FAIL\n");

    serial.write("test:gates...\n");
    const gates_ok = qc.neg(1) == -1 and qc.cxTarget(1, 1) == -1;
    if (gates_ok) serial.write("FSOT gates PASS\n") else serial.write("FSOT gates FAIL\n");

    serial.write("test:bell...\n");
    const b = qc.bellAnalog();
    const bell_ok = b[0] == -1 and b[1] == -1;
    if (bell_ok) serial.write("FSOT bell PASS\n") else serial.write("FSOT bell FAIL\n");

    serial.write("test:bv...\n");
    if (qc.bvRecover101()) serial.write("FSOT bv PASS\n") else serial.write("FSOT bv FAIL\n");

    serial.write("test:ising4...\n");
    if (qc.isingCycle4ExactOk()) serial.write("FSOT ising4 PASS\n") else serial.write("FSOT ising4 FAIL\n");

    serial.write("test:fold...\n");
    if (qc.foldLtHilbertOk()) serial.write("FSOT fold PASS\n") else serial.write("FSOT fold FAIL\n");

    serial.write("test:cnotfold...\n");
    if (qc.cnotFoldOk()) serial.write("FSOT cnotfold PASS\n") else serial.write("FSOT cnotfold FAIL\n");

    serial.write("test:selftest...\n");
    const core_ok = qc.selftest();
    if (core_ok) serial.write("FSOT selftest PASS\n") else serial.write("FSOT selftest FAIL\n");

    serial.write("jobs:qc_qm...\n");
    const js = jobs.allJobs();
    for (js) |j| {
        serial.write("JOB ");
        serial.write(j.name);
        if (j.ok) serial.write(" PASS\n") else serial.write(" FAIL\n");
    }
    serial.write("JOBS ");
    serial.writeU32(jobs.jobsPassCount());
    serial.write("/");
    serial.writeU32(jobs.jobsTotal());
    serial.write("\n");

    const ok = core_ok and jobs.jobsAllOk();
    if (ok) {
        serial.write("FSOT_QUANTUM_JOBS PASS\n");
        serial.write("FSOT_QUANTUM_KERNEL PASS\n");
    } else {
        serial.write("FSOT_QUANTUM_JOBS FAIL\n");
        serial.write("FSOT_QUANTUM_KERNEL FAIL\n");
    }

    while (true) {
        asm volatile ("hlt");
    }
}
