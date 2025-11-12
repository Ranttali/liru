# Spout SDK Structure for liru

## Overview

liru uses the **Spout SDK Binaries** package (version 2.007.017), which includes pre-compiled libraries and headers needed to build the Python extension.

## Download

**Automatic download:**
```bash
scripts\download_spout_sdk.bat
```

**Manual download:**
- URL: <https://github.com/leadedge/Spout2/releases/download/2.007.017/Spout-SDK-binaries_2-007-017_1.zip>
- Extract to: `external/Spout2/`

## Directory Structure

After extraction, you should have:

```text
external/Spout2/Spout-SDK-binaries/Libs_2-007-017/
├── include/
│   ├── SpoutGL/               # OpenGL headers (what we use)
│   │   ├── Spout.h           # Main Spout API
│   │   └── SpoutGL.h         # OpenGL-specific functions
│   ├── SpoutDX/              # DirectX 11 headers
│   ├── SpoutDX12/            # DirectX 12 headers
│   └── SpoutDX9/             # DirectX 9 headers
├── MD/                        # Multi-threaded DLL runtime (/MD) - WE USE THIS
│   ├── bin/
│   │   └── Spout.dll         # Runtime library (bundled with wheels)
│   └── lib/
│       └── Spout.lib         # Import library (for linking)
└── MT/                        # Multi-threaded static runtime (/MT)
    ├── bin/
    │   └── Spout.dll
    └── lib/
        └── Spout.lib
```

## What liru Uses

### Build Time (Compilation)

1. **Headers** from `include/SpoutGL/`:
   - `Spout.h` - Main Spout API declarations
   - `SpoutGL.h` - OpenGL-specific functions

2. **Import Library** from `MD/lib/`:
   - `Spout.lib` - For linking against Spout.dll

### Runtime (When liru is used)

1. **DLL** from `MD/bin/`:
   - `Spout.dll` - Bundled inside the wheel package
   - Located in `liru/` directory alongside `_liru_core.pyd`

## MD vs MT

**MD (Multi-threaded DLL):**
- Uses shared C runtime (MSVCRT)
- Smaller binary size
- **Recommended for Python extensions** (Python itself uses /MD)

**MT (Multi-threaded Static):**
- Statically links C runtime
- Larger binary size
- Not needed for our use case

## CMakeLists.txt Configuration

The build system is configured to:

1. **Find SDK:**
   ```cmake
   set(SPOUT_SDK_DIR "${CMAKE_CURRENT_SOURCE_DIR}/external/Spout2/Spout-SDK-binaries/Libs_2-007-017")
   set(SPOUT_INCLUDE_DIR "${SPOUT_SDK_DIR}/include")
   set(SPOUT_LIB_DIR "${SPOUT_SDK_DIR}/MD/lib")
   set(SPOUT_BIN_DIR "${SPOUT_SDK_DIR}/MD/bin")
   ```

2. **Include headers:**
   ```cmake
   target_include_directories(_liru_core PRIVATE
       ${SPOUT_INCLUDE_DIR}
       ${SPOUT_INCLUDE_DIR}/SpoutGL
       ${SPOUT_INCLUDE_DIR}/SpoutDX
   )
   ```

3. **Link import library:**
   ```cmake
   target_link_libraries(_liru_core PRIVATE
       "${SPOUT_LIB_DIR}/Spout.lib"
       opengl32
       gdi32
       user32
   )
   ```

4. **Bundle DLL in wheel:**
   ```cmake
   install(FILES "${SPOUT_BIN_DIR}/Spout.dll" DESTINATION liru)
   ```

## Wheel Contents

The final wheel includes:

```text
liru-0.1.0-cp313-cp313-win_amd64.whl
├── liru/
│   ├── __init__.py
│   ├── sender.py
│   ├── receiver.py
│   ├── _liru_core.pyd      # C++ extension
│   └── Spout.dll           # Spout runtime (bundled)
└── liru-0.1.0.dist-info/
```

**Important:** `Spout.dll` is automatically found because it's in the same directory as `_liru_core.pyd`.

## Verification

Check if SDK is properly installed:

```bash
# Should exist:
external/Spout2/Spout-SDK-binaries/Libs_2-007-017/include/SpoutGL/Spout.h
external/Spout2/Spout-SDK-binaries/Libs_2-007-017/MD/lib/Spout.lib
external/Spout2/Spout-SDK-binaries/Libs_2-007-017/MD/bin/Spout.dll
```

PowerShell check:

```powershell
Test-Path "external\Spout2\Spout-SDK-binaries\Libs_2-007-017\include\SpoutGL\Spout.h"
Test-Path "external\Spout2\Spout-SDK-binaries\Libs_2-007-017\MD\lib\Spout.lib"
Test-Path "external\Spout2\Spout-SDK-binaries\Libs_2-007-017\MD\bin\Spout.dll"
```

All three should return `True`.

## Troubleshooting

### DLL Not Found at Runtime

**Symptom:** ImportError: DLL load failed

**Solution:** Ensure `Spout.dll` is bundled in the wheel:
```bash
unzip -l dist/liru-*.whl | grep Spout.dll
```
Should show: `liru/Spout.dll`

### Link Error During Build

**Symptom:** Cannot open file 'Spout.lib'

**Solution:**
1. Check SDK path in CMakeLists.txt
2. Verify `Spout.lib` exists at `external/Spout2/Spout-SDK-binaries/Libs_2-007-017/MD/lib/Spout.lib`
3. Re-run `scripts\download_spout_sdk.bat`

### Header Not Found

**Symptom:** fatal error C1083: Cannot open include file: 'Spout.h'

**Solution:**
1. Check `external/Spout2/Spout-SDK-binaries/Libs_2-007-017/include/SpoutGL/Spout.h` exists
2. Verify include paths in CMakeLists.txt
3. Clean build: `rmdir /s /q build _skbuild`

## License

The Spout SDK is licensed separately from liru. See Spout's license at:
<https://github.com/leadedge/Spout2>

---

**Reference:**
- Spout Releases: <https://github.com/leadedge/Spout2/releases>
- Spout Documentation: <https://spout.zeal.co/>
