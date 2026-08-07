---
type: skill
version: "1.0.0"
date: "2026-08-02"
intent_hash: 0xSKL008_ZIG_PYTHON_BRIDGE_20260802
status: active
---

# Skill: SKL008 - Zig<->Python Bridge (ADMG/TALEX)

## Purpose
Provides bidirectional communication between Zig (TRIX kernel, bare-metal) and Python (PRIMUS core, TALEX narrative layer). Enables high-performance ternary operations in Zig with Python orchestration.

## Context
TALEX architecture splits compute:
- **Zig (TRIX)**: Bare-metal matrix kernels, syscall dispatch, SSE4.2 intrinsics
- **Python (PRIMUS)**: Narrative logic, state machines, lore validation, generation
- **Bridge**: Zero-copy data exchange, async syscall handling, type translation

## Bridge Architecture

```
-----------------------------------------------------------------
|                    PYTHON (TALEX/PRIMUS)                    |
|  ------------------  ------------------  ------------------      |
|  | Causal Engine|  | Lore Valid.  |  | Gen Engine   |      |
|  `--------+---------+--  `--------+---------+--  `--------+---------+--      |
|         |                 |                 |               |
|         v                 v                 v               |
|  ---------------------------------------------------------   |
|  |              BRIDGE LAYER (Python)                   |   |
|  |  * Type translation (Trit<->i8, WaveArray<->bytes)      |   |
|  |  * Syscall wrapper (TRIX syscall 21: MATRIX_RUN)    |   |
|  |  * Async event loop (trio/asyncio)                  |   |
|  |  * IntentHash verification                          |   |
|  `-----------------------+---------------------------------+--   |
`--------------------------+------------------------------------+--
                         | FFI / Shared Memory / IPC
                         v
-----------------------------------------------------------------
|                      ZIG (TRIX KERNEL)                      |
|  ------------------  ------------------  ------------------      |
|  | ExaGEMM      |  | SparseRolling|  | Syscall 21   |      |
|  | (SSE4.2)     |  | (CSR)        |  | MATRIX_RUN   |      |
|  `----------------+--  `----------------+--  `----------------+--      |
`---------------------------------------------------------------+--
```

## Type Translation

### Zig -> Python
```zig
// Zig types (src/trix/matrix/types.zig)
pub const Trit = enum(i8) { NEG = -1, ZERO = 0, POS = 1 };
pub const Wave = struct {
    band: u8,      // FrequencyBand (0-4)
    trit: Trit,
    phase: f32,    // [0, 2pi)
    amplitude: f32 // [0, 1]
};
pub const WaveArray = [81]Wave;
pub const TernaryMatrix = struct {
    data: [1641]u8,  // 6561 trits x 2 bits = 1641 bytes
};
```

```python
# Python translation (src/primus/core/bridge.py)
from ctypes import Structure, c_int8, c_uint8, c_float, c_uint32, CDLL
from src.primus.core.types import Trit, FrequencyBand, Wave, WaveArray

class ZWave(Structure):
    _fields_ = [
        ("band", c_uint8),
        ("trit", c_int8),
        ("phase", c_float),
        ("amplitude", c_float),
    ]

class ZWaveArray(Structure):
    _fields_ = [("waves", ZWave * 81)]

class ZTernaryMatrix(Structure):
    _fields_ = [("data", c_uint8 * 1641)]

def zig_wave_to_python(zw: ZWave) -> Wave:
    return Wave(
        band=FrequencyBand(zw.band),
        trit=Trit(zw.trit),
        phase=zw.phase,
        amplitude=zw.amplitude
    )

def python_wave_to_zig(w: Wave) -> ZWave:
    return ZWave(
        band=w.band.value,
        trit=w.trit.value,
        phase=w.phase,
        amplitude=w.amplitude
    )

def zig_wavearray_to_python(zwa: ZWaveArray) -> WaveArray:
    return WaveArray([zig_wave_to_python(zwa.waves[i]) for i in range(81)])

def python_wavearray_to_zig(wa: WaveArray) -> ZWaveArray:
    zwa = ZWaveArray()
    for i, w in enumerate(wa.waves):
        zwa.waves[i] = python_wave_to_zig(w)
    return zwa
```

## Syscall Interface (TRIX Syscall 21)

### Zig Syscall Definition
```zig
// src/trix/syscall/matrix_run.zig
pub fn matrix_run(
    op: u8,                    // 0=GEMM, 1=SparseRolling, 2=Project118to81
    input: *const WaveArray,
    output: *WaveArray,
    matrix: *const TernaryMatrix,
    dims: MatrixDims
) i32 {
    // Validate pointers, alignment
    // Dispatch to kernel
    // Return 0 on success, error code on failure
}
```

### Python Syscall Wrapper
```python
import ctypes
from ctypes import c_int8, c_uint8, c_int32, c_void_p, POINTER

# Load TRIX shared library
trix_lib = CDLL("libtrix.so")  # or .dll on Windows

# Define syscall signature
trix_lib.matrix_run.argtypes = [
    c_uint8,                    # op
    POINTER(ZWaveArray),        # input
    POINTER(ZWaveArray),        # output
    POINTER(ZTernaryMatrix),    # matrix
    c_void_p,                   # dims (opaque)
]
trix_lib.matrix_run.restype = c_int32

def trix_matrix_run(op: int, input_wa: WaveArray, matrix: TernaryMatrix) -> WaveArray:
    """Execute matrix operation via TRIX syscall 21."""
    input_zig = python_wavearray_to_zig(input_wa)
    output_zig = ZWaveArray()
    matrix_zig = python_matrix_to_zig(matrix)
    
    result = trix_lib.matrix_run(
        op,
        ctypes.byref(input_zig),
        ctypes.byref(output_zig),
        ctypes.byref(matrix_zig),
        None  # dims
    )
    
    if result != 0:
        raise RuntimeError(f"TRIX syscall 21 failed: {result}")
    
    return zig_wavearray_to_python(output_zig)

# Convenience functions
def trix_gemm(input_wa: WaveArray, matrix: TernaryMatrix) -> WaveArray:
    return trix_matrix_run(0, input_wa, matrix)

def trix_sparse_rolling(input_wa: WaveArray, matrix: TernaryMatrix) -> WaveArray:
    return trix_matrix_run(1, input_wa, matrix)

def trix_project_118_to_81(input_wa: WaveArray) -> WaveArray:
    # Special: no matrix needed, uses built-in projection
    return trix_matrix_run(2, input_wa, None)
```

## Async Bridge (High-Throughput)

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AsyncTrixBridge:
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.pending: dict[int, asyncio.Future] = {}
        self.request_id = 0
    
    async def gemm_async(self, input_wa: WaveArray, matrix: TernaryMatrix) -> WaveArray:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor, trix_gemm, input_wa, matrix
        )
    
    async def batch_gemm(self, requests: list[tuple[WaveArray, TernaryMatrix]]) -> list[WaveArray]:
        tasks = [self.gemm_async(inp, mat) for inp, mat in requests]
        return await asyncio.gather(*tasks)
    
    async def close(self):
        self.executor.shutdown(wait=True)
```

## IntentHash Verification Across Bridge

```python
def verify_bridge_integrity(
    python_state: TernaryState,
    zig_output: WaveArray
) -> bool:
    """Verify Zig output matches Python expected state."""
    # Compute expected hash from Python state
    expected_hash = python_state.hash_state()
    
    # Hash Zig output
    zig_bytes = wavearray_to_bytes(zig_output)
    actual_hash = ternary_hash(zig_bytes + expected_hash)
    
    return actual_hash == expected_hash
```

## Build Requirements

### Zig Side
- Zig 0.15+ (for comptime SIMD)
- `-Dcpu=westmere` for SSE4.2
- `-O ReleaseFast`
- Build as shared library: `zig build-lib -dynamic`

### Python Side
- Python 3.10+
- `ctypes` (stdlib)
- `trio` or `asyncio` for async
- PRIMUS core installed

### Build Commands
```bash
# Zig: Build TRIX shared library
cd trix/
zig build-lib src/trix.zig -dynamic -O ReleaseFast -Dcpu=westmere -fstrip
# Output: libtrix.so / trix.dll

# Python: Install bridge
pip install -e .  # Includes bridge module
```

## Validation

```python
# Test type translation round-trip
from src.primus.core import Wave, WaveArray, FrequencyBand, Trit
from bridge import zig_wave_to_python, python_wave_to_zig

original = Wave(band=FrequencyBand.BETA, trit=Trit.POS, phase=1.57, amplitude=0.8)
zig = python_wave_to_zig(original)
restored = zig_wave_to_python(zig)

assert restored.band == original.band
assert restored.trit == original.trit
assert abs(restored.phase - original.phase) < 1e-6
assert abs(restored.amplitude - original.amplitude) < 1e-6

# Test syscall (requires TRIX library)
try:
    result = trix_gemm(WaveArray.zeros(), TernaryMatrix.identity())
    assert len(result.waves) == 81
except OSError:
    print("TRIX library not loaded (expected in test env)")
```

## Anti-patterns
- Blocking calls in async context (use thread pool)
- Not verifying alignment (16-byte for SSE)
- Skipping IntentHash verification (silent corruption)
- Mixing Zig 0.14 and 0.15 ABIs
- Not handling syscall errors (check return codes)
- Zero-copy without lifetime management (use-after-free)

## References
- PRD-MOC-INVENTORY-SYNTHESIS.md (SKL008)
- PRIMUS core: types, matrix, hash, state
- TRIX syscall 21 (MATRIX_RUN)
- Zig 0.15 FFI guide
- SSE4.2 intrinsics (Westmere)
- TALEX architecture (Zig kernel + Python narrative)
- IntentHash specification