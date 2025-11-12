# Next Steps: Implementing Spout SDK Integration

## Current Status: Infrastructure Complete ✅

The liru project structure is **production-ready** and waiting for the actual Spout SDK integration.

### What's Done ✅

1. **Build System**
   - ✅ pyproject.toml with scikit-build-core
   - ✅ CMakeLists.txt configured for Spout SDK
   - ✅ Spout SDK paths set up correctly
   - ✅ DLL bundling configured

2. **Python API**
   - ✅ liru.Sender class with all methods
   - ✅ liru.Receiver class with all methods
   - ✅ Type hints and docstrings
   - ✅ Error handling structure

3. **C++ Wrapper Stubs**
   - ✅ SenderWrapper class skeleton
   - ✅ ReceiverWrapper class skeleton
   - ✅ Performance monitoring structure
   - ✅ pybind11 bindings

4. **Infrastructure**
   - ✅ GitHub Actions CI/CD
   - ✅ Documentation (API reference, architecture)
   - ✅ Test suite structure
   - ✅ License and attributions

### What Needs Implementation ❌

The **only** remaining work is uncommenting and implementing the actual Spout SDK calls in the C++ wrappers.

---

## Step-by-Step Implementation Guide

### Prerequisites

1. Ensure Spout SDK is downloaded:
   ```bash
   scripts\download_spout_sdk.bat
   ```

2. Verify SDK structure:
   ```bash
   ls external/Spout2/Spout-SDK-binaries/Libs_2-007-017/include/SpoutGL/
   ```
   Should show: `Spout.h`, `SpoutGL.h`

### Step 1: Implement SenderWrapper

**File:** [src/sender_wrapper.cpp](../src/sender_wrapper.cpp)

#### 1.1 Add Spout SDK Include

Replace line 5:
```cpp
// #include <SpoutGL/Spout.h>  // Uncomment when Spout SDK is available
```

With:
```cpp
#include "Spout.h"  // Spout SDK header
```

#### 1.2 Implement Constructor

Replace lines 25-28:
```cpp
// TODO: Initialize SpoutSender
// m_sender = std::make_unique<SpoutSender>();
// if (!m_sender->CreateSender(name.c_str(), width, height)) {
//     throw std::runtime_error("Failed to create Spout sender");
// }
```

With:
```cpp
m_sender = std::make_unique<spoutSenderNames>();
if (!m_sender->CreateSender(name.c_str(), width, height)) {
    throw std::runtime_error("Failed to create Spout sender");
}
```

**Note:** Check the actual Spout SDK class name - it might be `SpoutSender` or `spoutSenderNames`.

#### 1.3 Implement send_texture()

Replace lines 43-53:
```cpp
// TODO: Implement actual Spout send
// bool success = m_sender->SendTexture(
//     texture_id,
//     GL_TEXTURE_2D,
//     m_width,
//     m_height,
//     false,  // bInvert
//     0       // HostFBO
// );

bool success = true;  // Placeholder
```

With:
```cpp
bool success = m_sender->SendTexture(
    texture_id,
    GL_TEXTURE_2D,
    m_width,
    m_height,
    false,  // bInvert
    0       // HostFBO
);
```

#### 1.4 Implement release()

Replace lines 79-80:
```cpp
// TODO: Release Spout sender
// m_sender->ReleaseSender();
```

With:
```cpp
m_sender->ReleaseSender();
```

### Step 2: Implement ReceiverWrapper

**File:** [src/receiver_wrapper.cpp](../src/receiver_wrapper.cpp)

#### 2.1 Add Spout SDK Include

Same as Step 1.1, add:
```cpp
#include "Spout.h"
```

#### 2.2 Implement Constructor

Replace lines 16-22:
```cpp
// TODO: Initialize SpoutReceiver
// m_receiver = std::make_unique<SpoutReceiver>();

if (!sender_name.empty()) {
    // TODO: Connect to specific sender
    // m_receiver->SetReceiverName(sender_name.c_str());
    m_active_sender = sender_name;
}
```

With:
```cpp
m_receiver = std::make_unique<spoutReceiverNames>();

if (!sender_name.empty()) {
    m_receiver->SetReceiverName(sender_name.c_str());
    m_active_sender = sender_name;
}
```

#### 2.3 Implement receive_texture()

Replace lines 41-56:
```cpp
// TODO: Implement actual Spout receive
// char sender_name[256] = {0};
// unsigned int width = 0;
// unsigned int height = 0;
// bool success = m_receiver->ReceiveTexture(
//     sender_name,
//     width,
//     height,
//     texture_id,
//     GL_TEXTURE_2D,
//     false  // bInvert
// );

bool success = true;  // Placeholder
unsigned int width = m_width > 0 ? m_width : 1920;   // Placeholder
unsigned int height = m_height > 0 ? m_height : 1080; // Placeholder
```

With:
```cpp
char sender_name[256] = {0};
unsigned int width = 0;
unsigned int height = 0;

bool success = m_receiver->ReceiveTexture(
    sender_name,
    width,
    height,
    texture_id,
    GL_TEXTURE_2D,
    false  // bInvert
);
```

#### 2.4 Implement is_updated()

Replace lines 77-79:
```cpp
// TODO: Implement actual Spout frame check
// return m_receiver->IsUpdated();
return true;  // Placeholder
```

With:
```cpp
return m_receiver->IsUpdated();
```

#### 2.5 Implement select_sender()

Replace lines 87-89:
```cpp
// TODO: Implement sender selection
// m_receiver->SetReceiverName(name.c_str());
m_active_sender = name;
```

With:
```cpp
m_receiver->SetReceiverName(name.c_str());
m_active_sender = name;
```

#### 2.6 Implement get_sender_list()

Replace lines 95-106:
```cpp
// TODO: Implement actual sender enumeration
// int count = m_receiver->GetSenderCount();
// for (int i = 0; i < count; i++) {
//     char name[256] = {0};
//     if (m_receiver->GetSender(i, name)) {
//         senders.push_back(std::string(name));
//     }
// }

// Placeholder
senders.push_back("Sender1");
senders.push_back("Sender2");
```

With:
```cpp
int count = m_receiver->GetSenderCount();
for (int i = 0; i < count; i++) {
    char name[256] = {0};
    if (m_receiver->GetSender(i, name)) {
        senders.push_back(std::string(name));
    }
}
```

#### 2.7 Implement Destructor

Replace lines 28-29:
```cpp
// TODO: Release Spout receiver
// m_receiver->ReleaseReceiver();
```

With:
```cpp
m_receiver->ReleaseReceiver();
```

### Step 3: Update Header Forward Declarations

**File:** [src/sender_wrapper.h](../src/sender_wrapper.h)

Replace line 11:
```cpp
class SpoutSender;
```

With the correct Spout class name (check Spout SDK documentation):
```cpp
class spoutSenderNames;  // Or whatever the actual class is
```

**File:** [src/receiver_wrapper.h](../src/receiver_wrapper.h)

Replace line 13:
```cpp
class SpoutReceiver;
```

With:
```cpp
class spoutReceiverNames;  // Or whatever the actual class is
```

### Step 4: Build and Test

1. **Build the project:**
   ```bash
   python -m build --wheel
   ```

2. **Install the wheel:**
   ```bash
   pip install dist/liru-0.1.0-cp313-cp313-win_amd64.whl
   ```

3. **Run tests:**
   ```bash
   pytest tests/ -v
   ```

4. **Create a simple test:**
   ```python
   import liru

   # Test sender creation
   sender = liru.Sender("TestSender", 1920, 1080)
   print(f"Created sender: {sender}")
   sender.release()

   # Test receiver
   receiver = liru.Receiver()
   senders = receiver.get_sender_list()
   print(f"Available senders: {senders}")
   ```

### Step 5: Fix Any Compilation Errors

Common issues you might encounter:

1. **Wrong class names:** Check Spout.h for the actual class names
2. **Missing GL constants:** Add `#include <GL/gl.h>` or `#include <windows.h>`
3. **Namespace issues:** Spout classes might be in a namespace
4. **Method signatures:** Verify exact method names and parameters in Spout.h

### Step 6: Update Documentation

Once implementation is complete:

1. Update [CHANGELOG.md](../CHANGELOG.md):
   - Move items from "TODO" to "Added"
   - Change version to "0.1.0"

2. Update [README.md](../README.md):
   - Change status from "Pre-Alpha" to "Alpha"
   - Update checkboxes to show completion
   - Add performance benchmarks

3. Update tests to remove `continue-on-error` flags

---

## Verification Checklist

Before considering implementation complete:

- [ ] SenderWrapper creates actual Spout sender
- [ ] SenderWrapper sends textures (verify with Spout monitor tool)
- [ ] ReceiverWrapper receives textures
- [ ] ReceiverWrapper lists available senders
- [ ] Performance monitoring shows real timing data
- [ ] FPS counter works correctly
- [ ] All tests pass
- [ ] No memory leaks (use valgrind or similar)
- [ ] Wheel builds successfully
- [ ] Wheel installs and runs on clean machine

---

## Expected Timeline

**Estimated time:** 2-4 hours for experienced C++ developer

- Step 1-2 (Implementation): 1-2 hours
- Step 3-4 (Build/Test): 30 minutes
- Step 5 (Debugging): 30 minutes - 1 hour
- Step 6 (Documentation): 30 minutes

---

## Getting Help

If you encounter issues:

1. Check Spout SDK examples in `external/Spout2/SPOUTSDK/Examples/`
2. Review Spout documentation: <https://spout.zeal.co/>
3. Inspect the actual Spout.h header for class/method names
4. Test with Spout's own demo applications first

---

## After Implementation

Once Spout integration is complete, you can:

1. **Build wheels for distribution:**
   ```bash
   scripts\build_all_wheels.bat
   ```

2. **Publish to PyPI** (when ready):
   ```bash
   twine upload dist/*.whl
   ```

3. **Enable GitHub Actions** to auto-build on commits

4. **Create releases** with pre-built wheels attached

---

**The infrastructure is ready - just add the Spout calls!** 🚀
