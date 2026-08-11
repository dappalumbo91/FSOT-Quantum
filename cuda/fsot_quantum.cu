// FSOT-Quantum — bare-metal GPU kernels (NVIDIA CUDA)
// Authority: FSOT-2.1-Lean pin D1D38A + phase1 Trinary.lean
//
// Spins (signed):  -1 = SpinDown, 0 = Superposed, +1 = SpinUp
// Pack codes:       0 = SpinDown, 1 = Superposed, 2 = SpinUp  (2 bits each)
// Collapse Θ:       C_eff * P_var  (seed-derived; no free parameters)
//
// Build (Windows MSVC host):
//   nvcc -O3 -shared -Xcompiler "/LD" -o fsot_quantum_cuda.dll fsot_quantum.cu
// Smoke binary:
//   nvcc -O3 -DFSOT_QUANTUM_MAIN -o fsot_quantum_smoke.exe fsot_quantum.cu

#include <cuda_runtime.h>
#include <stdint.h>
#include <stdio.h>
#include <math.h>

// Seed-derived collapse threshold (matches fsot_lib / vendor triangulation)
// C_eff ≈ 0.9577022026205613
// P_var ≈ 0.9579871226722757
// Θ = C_eff * P_var ≈ 0.9174663774653723
#ifndef FSOT_COLLAPSE_THRESHOLD
#define FSOT_COLLAPSE_THRESHOLD 0.9174663774653723
#endif

// --- pack / unpack (32 codes per uint64) ---------------------------------

__device__ __forceinline__ uint64_t pack32(const uint8_t* codes) {
    uint64_t w = 0;
    #pragma unroll
    for (int i = 0; i < 32; ++i) {
        w |= (uint64_t)(codes[i] & 0x3u) << (2 * i);
    }
    return w;
}

__device__ __forceinline__ void unpack32(uint64_t w, uint8_t* codes) {
    #pragma unroll
    for (int i = 0; i < 32; ++i) {
        codes[i] = (uint8_t)((w >> (2 * i)) & 0x3u);
    }
}

__device__ __forceinline__ int8_t code_to_signed(uint8_t c) {
    // 0→-1, 1→0, 2→+1
    if (c == 0) return -1;
    if (c == 2) return 1;
    return 0;
}

__device__ __forceinline__ uint8_t signed_to_code(int8_t s) {
    if (s < 0) return 0;
    if (s > 0) return 2;
    return 1;
}

__device__ __forceinline__ int8_t collapse_one(float v, float thr) {
    if (v > thr) return 1;
    if (v < -thr) return -1;
    return 0;
}

__device__ __forceinline__ int8_t neg_spin(int8_t t) { return (int8_t)(-t); }

__device__ __forceinline__ int8_t pair_spin(int8_t a, int8_t b) {
    return (int8_t)(a * b);
}

__device__ __forceinline__ int8_t consensus_spin(int8_t a, int8_t b) {
    return (a == b) ? a : (int8_t)0;
}

__device__ __forceinline__ int8_t sum_sat(int8_t a, int8_t b) {
    int s = (int)a + (int)b;
    if (s > 1) return 1;
    if (s < -1) return -1;
    return (int8_t)s;
}

// CX-analog: control +1 flip; 0 super; -1 hold
__device__ __forceinline__ int8_t cx_target(int8_t c, int8_t t) {
    if (c == 0) return 0;
    if (c > 0) return neg_spin(t);
    return t;
}

// --- kernels -------------------------------------------------------------

extern "C" __global__ void fsot_pack_kernel(
    const uint8_t* __restrict__ in_codes,
    uint64_t* __restrict__ out_words,
    size_t n_groups
) {
    size_t g = blockIdx.x * blockDim.x + threadIdx.x;
    if (g >= n_groups) return;
    out_words[g] = pack32(in_codes + g * 32);
}

extern "C" __global__ void fsot_unpack_kernel(
    const uint64_t* __restrict__ in_words,
    uint8_t* __restrict__ out_codes,
    size_t n_groups
) {
    size_t g = blockIdx.x * blockDim.x + threadIdx.x;
    if (g >= n_groups) return;
    unpack32(in_words[g], out_codes + g * 32);
}

extern "C" __global__ void fsot_collapse_kernel(
    const float* __restrict__ field,
    int8_t* __restrict__ spins_out,
    size_t n,
    float threshold
) {
    size_t i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;
    spins_out[i] = collapse_one(field[i], threshold);
}

// Apply X (neg) on every spin
extern "C" __global__ void fsot_x_all_kernel(
    int8_t* __restrict__ spins,
    size_t n
) {
    size_t i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;
    spins[i] = neg_spin(spins[i]);
}

// Pairwise CX along even/odd pairs: (0,1), (2,3), ...
extern "C" __global__ void fsot_cx_pairs_kernel(
    int8_t* __restrict__ spins,
    size_t n_pairs
) {
    size_t p = blockIdx.x * blockDim.x + threadIdx.x;
    if (p >= n_pairs) return;
    size_t c = p * 2;
    size_t t = c + 1;
    spins[t] = cx_target(spins[c], spins[t]);
}

// Consensus coupling: spins[i] = consensus(spins[i], neighbor)  (ring)
extern "C" __global__ void fsot_consensus_ring_kernel(
    const int8_t* __restrict__ in_spins,
    int8_t* __restrict__ out_spins,
    size_t n
) {
    size_t i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;
    size_t j = (i + 1) % n;
    out_spins[i] = consensus_spin(in_spins[i], in_spins[j]);
}

// Export threshold for host verification
extern "C" __declspec(dllexport) double fsot_collapse_threshold(void) {
    return FSOT_COLLAPSE_THRESHOLD;
}

// Host launchers (exported) ------------------------------------------------

static int grid(size_t n, int threads) {
    return (int)((n + (size_t)threads - 1) / (size_t)threads);
}

extern "C" __declspec(dllexport) int fsot_gpu_pack(
    const uint8_t* h_codes, uint64_t* h_words, size_t n_groups
) {
    uint8_t* d_in = nullptr;
    uint64_t* d_out = nullptr;
    size_t bytes_in = n_groups * 32;
    cudaMalloc(&d_in, bytes_in);
    cudaMalloc(&d_out, n_groups * sizeof(uint64_t));
    cudaMemcpy(d_in, h_codes, bytes_in, cudaMemcpyHostToDevice);
    int threads = 256;
    fsot_pack_kernel<<<grid(n_groups, threads), threads>>>(d_in, d_out, n_groups);
    cudaDeviceSynchronize();
    cudaMemcpy(h_words, d_out, n_groups * sizeof(uint64_t), cudaMemcpyDeviceToHost);
    cudaFree(d_in); cudaFree(d_out);
    return 0;
}

extern "C" __declspec(dllexport) int fsot_gpu_collapse(
    const float* h_field, int8_t* h_spins, size_t n, float thr
) {
    float* d_f = nullptr;
    int8_t* d_s = nullptr;
    cudaMalloc(&d_f, n * sizeof(float));
    cudaMalloc(&d_s, n * sizeof(int8_t));
    cudaMemcpy(d_f, h_field, n * sizeof(float), cudaMemcpyHostToDevice);
    int threads = 256;
    fsot_collapse_kernel<<<grid(n, threads), threads>>>(d_f, d_s, n, thr);
    cudaDeviceSynchronize();
    cudaMemcpy(h_spins, d_s, n * sizeof(int8_t), cudaMemcpyDeviceToHost);
    cudaFree(d_f); cudaFree(d_s);
    return 0;
}

#ifdef FSOT_QUANTUM_MAIN
static void check_cuda(cudaError_t err, const char* what) {
    if (err != cudaSuccess) {
        fprintf(stderr, "CUDA error at %s: %s\n", what, cudaGetErrorString(err));
    }
}

int main() {
    int dev = 0;
    cudaDeviceProp prop{};
    check_cuda(cudaGetDeviceProperties(&prop, dev), "cudaGetDeviceProperties");
    printf("GPU: %s  CC %d.%d\n", prop.name, prop.major, prop.minor);

    const size_t groups = 1024;
    uint8_t* h_in = new uint8_t[groups * 32];
    for (size_t i = 0; i < groups * 32; ++i) h_in[i] = (uint8_t)(i % 3);

    uint8_t *d_in = nullptr, *d_out = nullptr;
    uint64_t *d_packed = nullptr;
    check_cuda(cudaMalloc(&d_in, groups * 32), "malloc d_in");
    check_cuda(cudaMalloc(&d_packed, groups * sizeof(uint64_t)), "malloc d_packed");
    check_cuda(cudaMalloc(&d_out, groups * 32), "malloc d_out");
    check_cuda(cudaMemcpy(d_in, h_in, groups * 32, cudaMemcpyHostToDevice), "H2D codes");

    int threads = 256;
    int blocks = grid(groups, threads);
    fsot_pack_kernel<<<blocks, threads>>>(d_in, d_packed, groups);
    check_cuda(cudaGetLastError(), "pack launch");
    fsot_unpack_kernel<<<blocks, threads>>>(d_packed, d_out, groups);
    check_cuda(cudaGetLastError(), "unpack launch");
    check_cuda(cudaDeviceSynchronize(), "pack sync");

    uint8_t* h_out = new uint8_t[groups * 32];
    check_cuda(cudaMemcpy(h_out, d_out, groups * 32, cudaMemcpyDeviceToHost), "D2H codes");

    size_t mismatches = 0;
    for (size_t i = 0; i < groups * 32; ++i) {
        if (h_in[i] != h_out[i]) ++mismatches;
    }
    printf("FSOT-Quantum trinary pack roundtrip mismatches: %zu / %zu\n",
           mismatches, groups * 32);
    printf("Collapse threshold: %.16f\n", FSOT_COLLAPSE_THRESHOLD);

    // collapse smoke — poles clearly outside Θ
    const size_t n = 8;
    float field[8] = {1.0f, -1.0f, 0.0f, 0.5f, -0.5f, 0.95f, -0.95f, 0.1f};
    int8_t spins[8] = {99, 99, 99, 99, 99, 99, 99, 99};
    float* d_f = nullptr; int8_t* d_s = nullptr;
    check_cuda(cudaMalloc(&d_f, n * sizeof(float)), "malloc field");
    check_cuda(cudaMalloc(&d_s, n * sizeof(int8_t)), "malloc spins");
    check_cuda(cudaMemcpy(d_f, field, n * sizeof(float), cudaMemcpyHostToDevice), "H2D field");
    fsot_collapse_kernel<<<1, 32>>>(d_f, d_s, n, (float)FSOT_COLLAPSE_THRESHOLD);
    check_cuda(cudaGetLastError(), "collapse launch");
    check_cuda(cudaDeviceSynchronize(), "collapse sync");
    check_cuda(cudaMemcpy(spins, d_s, n * sizeof(int8_t), cudaMemcpyDeviceToHost), "D2H spins");
    printf("Collapse sample spins:");
    for (size_t i = 0; i < n; ++i) printf(" %d", (int)spins[i]);
    printf("\n");
    // expect: +1 -1 0 0 0 +1 -1 0
    int collapse_ok =
        spins[0] == 1 && spins[1] == -1 && spins[2] == 0 &&
        spins[5] == 1 && spins[6] == -1;

    cudaFree(d_in); cudaFree(d_packed); cudaFree(d_out);
    cudaFree(d_f); cudaFree(d_s);
    delete[] h_in; delete[] h_out;
    int ok = (mismatches == 0) && collapse_ok;
    printf("SMOKE: %s\n", ok ? "PASS" : "FAIL");
    return ok ? 0 : 1;
}
#endif
