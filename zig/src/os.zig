//! FSOT-QC-OS — standalone quantum-job OS (not a Reality OS hijack).

const serial = @import("serial.zig");
const qc = @import("quantum_core.zig");
const jobs = @import("jobs.zig");

pub const VERSION: []const u8 = "0.3.0";

pub fn banner() void {
    serial.write("FSOT-QC-OS v");
    serial.write(VERSION);
    serial.write("\n");
    serial.write("standalone quantum job OS - no host OS, no fridge\n");
    serial.write("pin D1D38A Apache-2.0 trinary -1/0/+1\n");
}

pub fn help() void {
    serial.write("SHELL a=all c=core j=jobs h=help\n");
    serial.write("no input -> a (default)\n");
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

fn pollCmd() u8 {
    // Seed-ish spin: ~1/POOF * 20000 loops — file-serial QEMU usually sends nothing.
    var i: u32 = 0;
    while (i < 20000) : (i += 1) {
        if (serial.getc()) |c| {
            if (c >= 'A' and c <= 'Z') return c + 32;
            return c;
        }
    }
    return 'a';
}

pub fn halt() noreturn {
    while (true) {
        asm volatile ("hlt");
    }
}

pub fn boot() noreturn {
    serial.init();
    banner();
    help();
    const cmd = pollCmd();
    serial.write("CMD ");
    serial.putc(cmd);
    serial.write("\n");

    var core_ok = true;
    var jobs_ok = true;
    if (cmd == 'c') {
        core_ok = runCore();
        jobs_ok = true;
    } else if (cmd == 'j') {
        jobs_ok = runJobs();
        core_ok = true;
    } else if (cmd == 'h') {
        help();
    } else {
        core_ok = runCore();
        jobs_ok = runJobs();
    }

    if (core_ok and jobs_ok) {
        serial.write("FSOT-QC-OS READY\n");
        serial.write("FSOT_QUANTUM_KERNEL PASS\n");
    } else {
        serial.write("FSOT-QC-OS FAIL\n");
        serial.write("FSOT_QUANTUM_KERNEL FAIL\n");
    }
    halt();
}
