//! FSOT-QC-OS — tiny standalone quantum-job operating system.
//! Not a hijack of Reality OS. Own Multiboot image. Same pin D1D38A.
//! Later Reality OS can *host* this; this image already runs alone in QEMU.

const serial = @import("serial.zig");
const qc = @import("quantum_core.zig");
const jobs = @import("jobs.zig");

pub const VERSION: []const u8 = "0.1.0";

pub fn banner() void {
    serial.write("FSOT-QC-OS v");
    serial.write(VERSION);
    serial.write("\n");
    serial.write("standalone quantum job OS - no host OS, no fridge\n");
    serial.write("pin D1D38A Apache-2.0 trinary -1/0/+1\n");
}

pub fn runCore() bool {
    serial.write("svc:core...\n");
    const ok = qc.selftest();
    if (ok) serial.write("FSOT selftest PASS\n") else serial.write("FSOT selftest FAIL\n");
    return ok;
}

pub fn runJobs() bool {
    serial.write("svc:jobs...\n");
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
    const ok = jobs.jobsAllOk();
    if (ok) serial.write("FSOT_QUANTUM_JOBS PASS\n") else serial.write("FSOT_QUANTUM_JOBS FAIL\n");
    return ok;
}

pub fn halt() noreturn {
    while (true) {
        asm volatile ("hlt");
    }
}

/// One-shot boot: banner → core → jobs → halt. (Interactive shell later.)
pub fn boot() noreturn {
    serial.init();
    banner();
    const core_ok = runCore();
    const jobs_ok = runJobs();
    if (core_ok and jobs_ok) {
        serial.write("FSOT-QC-OS READY\n");
        serial.write("FSOT_QUANTUM_KERNEL PASS\n");
    } else {
        serial.write("FSOT-QC-OS FAIL\n");
        serial.write("FSOT_QUANTUM_KERNEL FAIL\n");
    }
    halt();
}
