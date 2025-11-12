# liru

## Python wrapper for Spout 2 GPU texture sharing

[![License: BSD-2-Clause](https://img.shields.io/badge/License-BSD%202--Clause-blue.svg)](https://opensource.org/licenses/BSD-2-Clause)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

**liru** provides zero-copy GPU texture sharing between Python processes using Spout 2 DirectX shared texture mechanism. Designed for real-time video mixing, compositing, and live graphics applications.

## Features

Python wrapper for Spout.

## Quick Start

### Installation

```bash
pip install liru
```

### Basic Usage

```python
import moderngl
import liru

# Create OpenGL context and texture
ctx = moderngl.create_context()
texture = ctx.texture((1920, 1080), 4)  # RGBA

# Initialize Spout sender
sender = liru.Sender("MySource", 1920, 1080)

# Render loop
while running:
    # Render to texture
    # ... your rendering code ...

    # Send via Spout (GPU-only, no CPU copy)
    sender.send_texture(texture.glo)

    # Optional: check performance
    print(f"FPS: {sender.get_fps():.1f}, Latency: {sender.last_send_time_ms:.3f}ms")

# Cleanup
sender.release()
```

### Receiving Textures

```python
import moderngl
import liru

ctx = moderngl.create_context()
receiver = liru.Receiver("MySource")

# Create texture (receiver will update its size)
texture = ctx.texture((1, 1), 4)

while running:
    if receiver.is_updated():
        width, height = receiver.receive_texture(texture.glo)
        # Use texture in compositor
        # ... your compositing code ...
```

- **OS**: Windows 10/11 (Spout is Windows-only)
- **Python**: 3.13
- **GPU**: DirectX 11 compatible GPU
- **Runtime**: Visual C++ Redistributable 2022

## Documentation

- [API Reference](docs/api_reference.md) - Complete API documentation
- [Architecture](docs/plan/02_architecture.md) - System design and internals
- [Build Guide](docs/plan/05_build_and_distribution.md) - Building from source

## Why liru?

You want to use Python and Spout. It seems alternatives were somewhat stale or lacking at the time I needed this.

## API Overview

### Sender

```python
sender = liru.Sender("MySource", 1920, 1080)
sender.send_texture(texture_id: int) -> None
sender.get_fps() -> float
sender.last_send_time_ms -> float
sender.release() -> None
```

### Receiver

```python
receiver = liru.Receiver("SenderName")
receiver.receive_texture(texture_id: int) -> tuple[int, int]
receiver.is_updated() -> bool
receiver.select_sender(name: str) -> None
receiver.get_sender_list() -> list[str]
```

## Building from Source

```bash
# Clone repository
git clone https://github.com/veitsi/liru.git
cd liru

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install build dependencies
pip install build scikit-build-core pybind11

# Download Spout SDK 2.007
# Place in external/Spout2/SPOUTSDK/

# Build wheel
python -m build

# Install locally
pip install dist/liru-0.1.0-cp313-cp313-win_amd64.whl
```

See [Build Guide](docs/plan/05_build_and_distribution.md) for detailed instructions.

## Project Structure

```text
liru/
├── liru/                   # Python package
│   ├── __init__.py         # Public API
│   ├── sender.py           # Sender wrapper
│   ├── receiver.py         # Receiver wrapper
│   └── py.typed            # Type checking marker
├── src/                    # C++ sources
│   ├── bindings.cpp        # pybind11 bindings
│   ├── sender_wrapper.cpp  # Sender implementation
│   └── receiver_wrapper.cpp # Receiver implementation
├── tests/                  # Test suite
├── docs/                   # Documentation
├── CMakeLists.txt          # CMake configuration
├── pyproject.toml          # Python packaging (scikit-build-core)
└── README.md               # This file
```

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## License

**liru** is licensed under the BSD-2-Clause License - see [LICENSE](LICENSE) for details.
Q: Why not MIT? A: Because Spout is BSD-2 too so 1 type is less than 2.

### Third-Party Components

liru includes and redistributes the following third-party components:

- **Spout.dll** (BSD-2-Clause License) - GPU texture sharing framework by Lynn Jarvis
  - Bundled in wheel packages
  - See [THIRD_PARTY_LICENSES.txt](THIRD_PARTY_LICENSES.txt) for full license text
  - <https://github.com/leadedge/Spout2>

All third-party licenses are included in the distribution and must be retained when redistributing liru.

## Acknowledgments

- **Spout**: GPU texture sharing framework by Lynn Jarvis
  - <https://spout.zeal.co/>
  - <https://github.com/leadedge/Spout2>

- **pybind11**: Seamless C++/Python interoperability
  - <https://pybind11.readthedocs.io/>

## Support

- **Issues**: <https://github.com/veitsi/liru/issues>

## Project Status

liru is under active development. See [ROADMAP.md](ROADMAP.md) for detailed development status and plans.

---

**Maintained by**: Ranttali (Lauri Mäki)

**Created**: 2025-11-12

## AI Assistance Disclosure

This project was developed with the assistance of AI tools. AI was used for code generation, documentation, and project structure setup. All code has been reviewed and tested by human developers.
