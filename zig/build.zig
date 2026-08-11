const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Host twin selftest
    const exe = b.addExecutable(.{
        .name = "fsot_quantum_zig",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/quantum.zig"),
            .target = target,
            .optimize = optimize,
        }),
    });
    b.installArtifact(exe);
    const run_step = b.step("run", "Run host Zig quantum selftest");
    const run_cmd = b.addRunArtifact(exe);
    run_step.dependOn(&run_cmd.step);

    // Freestanding Multiboot kernel for QEMU (32-bit, PFLT/neuron pattern)
    const kernel_target = b.resolveTargetQuery(.{
        .cpu_arch = .x86,
        .os_tag = .freestanding,
        .abi = .none,
    });
    const kernel = b.addExecutable(.{
        .name = "fsot_quantum_kernel",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/main_kernel.zig"),
            .target = kernel_target,
            .optimize = .ReleaseSafe,
            .code_model = .kernel,
            .red_zone = false,
        }),
    });
    kernel.entry = .{ .symbol_name = "_start" };
    kernel.setLinkerScript(b.path("linker.ld"));
    kernel.pie = false;
    kernel.link_eh_frame_hdr = false;
    b.installArtifact(kernel);

    const kernel_step = b.step("kernel", "Build freestanding FSOT-Quantum QEMU kernel");
    kernel_step.dependOn(&b.addInstallArtifact(kernel, .{}).step);
}
