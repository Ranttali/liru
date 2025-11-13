# liru Quick Start Guide

Get up and running with liru in 5 minutes.

## Prerequisites

- Windows 10/11
- Python 3.13+
- Visual Studio 2022 (for building from source)

## Option 1: Install from PyPI (Recommended)

```bash
pip install liru
```

**Test installation:**

```bash
python -c "import liru; print(liru.__version__)"
```

## Option 2: Build from Source

### Step 1: Clone Repository

```bash
git clone https://github.com/Ranttali/liru.git
cd liru
```

### Step 2: Set Up Environment

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Download Spout SDK

```bash
scripts\download_spout_sdk.bat
```

Or manually:

1. Download [Spout 2.007](https://github.com/leadedge/Spout2/releases/tag/2.007g)
2. Extract to `external/Spout2/`

### Step 4: Build

```bash
python -m build --wheel
pip install dist/liru-0.1.0-cp313-cp313-win_amd64.whl
```

### Step 5: Verify

```bash
python scripts\verify_install.py
```

## First Example: Simple Sender

```python
import moderngl
import liru

# Create OpenGL context
ctx = moderngl.create_context()

# Create texture
texture = ctx.texture((1920, 1080), 4)

# Create sender
sender = liru.Sender("MySource", 1920, 1080)

# Render and send
# ... render to texture ...
sender.send_texture(texture.glo)

# Check performance
print(f"FPS: {sender.get_fps():.1f}")
print(f"Latency: {sender.last_send_time_ms:.3f}ms")

# Cleanup
sender.release()
```

## Second Example: Simple Receiver

```python
import moderngl
import liru

# Create OpenGL context
ctx = moderngl.create_context()

# Create receiver
receiver = liru.Receiver("MySource")

# Create texture
texture = ctx.texture((1, 1), 4)

# Receive frames
if receiver.is_updated():
    width, height = receiver.receive_texture(texture.glo)
    print(f"Received {width}x{height} texture")
```

## Running Tests

```bash
pytest tests/ -v
```

## Building Wheels

```bash
# Current Python version
python -m build --wheel

# All supported versions
scripts\build_all_wheels.bat
```

## Development Mode

For active development:

```bash
pip install -e .
```

Changes to Python code take effect immediately. C++ changes require rebuild:

```bash
pip install -e . --force-reinstall --no-deps
```

## Common Issues

### DLL Load Failed

**Solution:** Install Visual C++ Redistributable 2022

- <https://aka.ms/vs/17/release/vc_redist.x64.exe>

### CMake Cannot Find pybind11

**Solution:**

```bash
pip install "pybind11[global]"
```

### Import Error

**Solution:** Ensure wheel is installed:

```bash
pip show liru
```

## Next Steps

- Read [API Reference](docs/api_reference.md)
- Check [Architecture](docs/plan/02_architecture.md)
- Review [Contributing Guide](CONTRIBUTING.md)
- Explore [Examples](examples/)

## Getting Help

- [Issues](https://github.com/Ranttali/liru/issues)
- [Discussions](https://github.com/Ranttali/liru/discussions)
- [Documentation](docs/)
