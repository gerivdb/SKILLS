---
type: skill
version: "1.0.0"
date: "2026-08-01"
intent_hash: 0xMATRIX_RUNNER_20260801
status: active
---

# Skill: matrix-runner

## Purpose
Execute MATRIX-RUNNERS kernel: ExaGEMM, SparseRolling, SSE4.2 intrinsics, 118u219281 dimension mapping. Integrated via TRIX syscall 21 and PLIX unner matrix command.

## Context
MATRIX-RUNNERS provides bare-metal linear algebra for the ecosystem. 1.78x baseline achieved, 13.29x deferred (Sprint 2.5).

## Kernel Components

### 1. ExaGEMM
- Dense matrix multiplication
- SSE4.2 intrinsics (Westmere compatible)
- Blocking: 64x64 tiles, 8x8 micro-kernels
- Current: 1.78x vs Zig native

### 2. SparseRolling
- Sparse matrix rolling window
- CSR format with 118u219281 mapping
- Optimized for LLUX attention patterns

### 3. Dimension Mapping
- Input: 118-dim embeddings
- Output: 81-dim latent (9x9 grid)
- Mapping: learned projection + quantization

## TRIX Integration
- Syscall 21: MATRIX_RUN (defined in TRIX dispatch table)
- Entry: src/trix/syscall/matrix_run.zig
- ABI: n matrix_run(op: u8, input: *const f32, output: *f32, dims: MatrixDims) i32

## PLIX Command
`ash
plix runner matrix compute_projection --input embeddings.bin --output latent.bin --mode exagemm
plix runner matrix rolling_attention --window 512 --sparse-csr sparse.bin
`

## Performance Targets
| Kernel | Baseline (Zig) | Current | Target (Sprint 2.5) |
|--------|----------------|---------|---------------------|
| ExaGEMM 64x64 | 1.0x | 1.78x | 13.29x |
| SparseRolling | 1.0x | 1.45x | 8.2x |
| 118u219281 map | 1.0x | 1.62x | 5.8x |

## Build Requirements
- Zig 0.14 (current) or 0.15+ (for 13.29x)
- -Dcpu=westmere for SSE4.2
- -O ReleaseFast
- TRIX dispatch table slot 21 reserved

## Validation
`powershell
zig test src/matrix/kernels.zig --summary all
plix runner matrix benchmark --iterations 100
`

## Anti-patterns
- Running without -Dcpu=westmere (AVX2 not available)
- Using Zig 0.14 for 13.29x target (needs 0.15+ intrinsics)
- Ignoring alignment requirements (16-byte for SSE)
- Not validating output against reference implementation

## References
- D-008: matrix-runners-architecture (design)
- ATOM-066: git-engineering
- TRIX syscall 21
- Sprint 2.5 deferred
