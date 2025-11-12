# Changelog

All notable changes to liru will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-11-13

### Added

- Initial project structure with modern Python + C++ extension layout
- pyproject.toml with scikit-build-core build system
- CMake build configuration with Spout SDK paths
- Python API with Sender and Receiver classes
- **Full Spout SDK integration in C++ wrappers**
- **GPU texture sharing functionality (Sender)**
- **Zero-copy receiving functionality (Receiver)**
- **Performance monitoring (FPS, latency tracking)**
- **ModernGL API compatibility**
- **Context manager support (with statement) for Sender and Receiver**
- **Type stub file (\_\_init\_\_.pyi) for better IDE autocomplete and type checking**
- **Resource warnings for unclosed Sender instances**
- **Platform check with clear error message on non-Windows systems**
- Single source of truth for version (`__version__.py` with dynamic reading)
- Comprehensive documentation structure (API reference, architecture, build guides)
- CI/CD workflow templates (GitHub Actions for build and release)
- Python 3.13+ support configured
- BSD-2-Clause license matching Spout
- Third-party license attributions
- Automated Spout SDK download script
- **Comprehensive test suite with pytest**
  - Context manager tests
  - Resource management and warning tests
  - Platform compatibility tests
  - Integration tests for complete workflows
  - Deterministic and reproducible test design

### Changed

- Implemented real Spout SDK calls replacing placeholder stubs
- Updated forward declarations to use `Spout` class
- Improved error handling in C++ wrappers

[Unreleased]: https://github.com/veitsi/liru/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/veitsi/liru/releases/tag/v0.1.1
