# Bundling Third-Party DLLs in liru

## Question: Is it OK to bundle Spout.dll?

**Short Answer:** Yes, it's legally OK because Spout uses the BSD-2-Clause license which permits redistribution of binaries, **provided you comply with the license terms**.

## What You Must Do (Already Done ✅)

### 1. Include License & Copyright Notice

- ✅ Created `THIRD_PARTY_LICENSES.txt` with Spout's full license text
- ✅ Configured `pyproject.toml` to include license file in wheels
- ✅ Updated README.md to clearly state bundled components

### 2. Include Disclaimer

- ✅ Spout's BSD license disclaimer is in `THIRD_PARTY_LICENSES.txt`

### 3. Give Attribution

- ✅ README.md acknowledges Spout
- ✅ Links to Spout project provided

## Your Current Setup (Compliant)

```text
Wheel contents:
liru-0.1.0-cp313-cp313-win_amd64.whl
├── liru/
│   ├── __init__.py
│   ├── sender.py
│   ├── receiver.py
│   ├── _liru_core.pyd
│   └── Spout.dll              # ← Bundled third-party DLL
└── liru-0.1.0.dist-info/
    ├── METADATA
    ├── LICENSE                # Your MIT license
    ├── THIRD_PARTY_LICENSES.txt  # ← Spout's BSD license
    └── RECORD
```

Users installing via `pip install liru` will have:
- Spout.dll in the liru package directory
- Both licenses in the dist-info directory

## Alternative Approaches (If You Prefer)

If you're uncomfortable bundling the DLL, here are alternatives:

### Option 1: User Installs Spout Separately (Not Recommended)

**Pros:**
- No redistribution concerns
- Users get latest Spout version

**Cons:**
- ❌ Poor user experience
- ❌ Installation complexity
- ❌ Version compatibility issues
- ❌ Users must manually download from Spout website

**Implementation:**
```python
# Remove from CMakeLists.txt:
# install(FILES "${SPOUT_BIN_DIR}/Spout.dll" DESTINATION liru)

# Add to README:
"Users must install Spout 2.007 separately"
```

### Option 2: Dynamic Download on First Import (Not Recommended)

**Pros:**
- No bundling in wheel
- Automatic installation

**Cons:**
- ❌ Requires internet connection at runtime
- ❌ Security concerns (downloading executables)
- ❌ Slower first-time import
- ❌ Complex error handling

### Option 3: Separate "liru-with-spout" Package (Overkill)

**Pros:**
- Clear separation of code ownership

**Cons:**
- ❌ Confusing for users
- ❌ Maintenance overhead
- ❌ Unnecessary complexity

## Recommendation: Keep Current Approach ✅

**Why bundling is the right choice:**

1. **Legal**: Spout's BSD-2-Clause license explicitly allows this
2. **User Experience**: `pip install liru` just works
3. **Common Practice**: Most Python packages bundle third-party DLLs (numpy, scipy, opencv-python all do this)
4. **Compliant**: You're including all required attributions

## Similar Examples in PyPI

These popular packages also bundle third-party DLLs:

- **opencv-python**: Bundles OpenCV DLLs (Apache 2.0/BSD)
- **numpy**: Bundles OpenBLAS DLLs (BSD)
- **pillow**: Bundles libjpeg, libpng, etc. (Various licenses)
- **pyqt5**: Bundles Qt DLLs (GPL/LGPL with exceptions)

All properly attribute their third-party components, just like you're doing.

## License Compliance Checklist

- [x] Spout license text included in `THIRD_PARTY_LICENSES.txt`
- [x] Copyright notice preserved
- [x] Disclaimer included
- [x] Attribution in README.md
- [x] License file included in wheel
- [x] Links to original Spout project provided
- [x] No misrepresentation of authorship

## If Publishing to PyPI

When you publish, PyPI will show:

- Your project's MIT license as the main license
- `THIRD_PARTY_LICENSES.txt` will be in the wheel
- Users can inspect with: `pip show -f liru`

## Legal Disclaimer

This is not legal advice. If you have specific concerns about licensing, consult with a lawyer. However, the BSD-2-Clause license is one of the most permissive open-source licenses and is widely used in commercial and open-source projects.

## Summary

**You're doing it right!** Bundling Spout.dll is:
- ✅ Legal (BSD license permits it)
- ✅ Compliant (you've included all required attributions)
- ✅ Best practice (matches industry standards)
- ✅ User-friendly (simple installation)

The only requirement is to keep the license files and attributions, which you've already done.

---

**References:**
- BSD-2-Clause License: <https://opensource.org/licenses/BSD-2-Clause>
- Spout License: <https://github.com/leadedge/Spout2/blob/master/LICENSE>
- Python Packaging Guide: <https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#license>
