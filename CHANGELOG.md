<!-- markdownlint-disable MD024 -->
# Changelog

All notable changes to liru will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.6] - 2025-11-13

- Fixed project links

## [0.2.5] - 2025-11-13

### Changed

- README: Improved API Overview with proper type signature formatting
- README: Added `running` variable definition to Quick Start examples

### Fixed

- README: Fixed missing closing backticks in code block

## [0.2.4] - 2025-11-13

### Changed

- Documentation: Added clarification about is_updated() warmup behavior in README
- Code quality: Resolved all Black, Ruff, and mypy linting issues

### Fixed

- pyproject.toml: Removed py315 from Black target-version (not yet supported)

## [0.2.3] - 2025-11-13

### Fixed

- Critical fix: Receiver dimensions now correctly populated without OpenGL context
- Uses GetSenderInfo() to query Spout shared memory registry
- Receiver.width and Receiver.height return correct values

### Changed

- Lazy initialization: OpenGL connection established on first receive_texture() call
- Added query_sender_info() method to explicitly query sender dimensions
- Added is_initialized() diagnostic method

## [0.2.2] - 2025-11-13

### Fixed

- Receiver.width and Receiver.height now return correct values without requiring frame reception
- Receiver uses CreateReceiver() API to establish proper connection with OpenGL context
- Constructor and select_sender() methods now query sender dimensions immediately

## [0.2.0] - 2025-11-13

### Added

- Python 3.14 support

## [0.1.4] - 2025-11-13

- CMakeLists.txt - Fixed install destination to avoid double nesting (liru/liru/)
- Import statements - Changed to relative imports (from . import _liru_core)
- del method - Fixed to handle cases where __init__ fails
- Resource warning test - Added gc.collect() to force cleanup
- Version test - Made it flexible instead of hardcoded version

## [0.1.2] - 2025-11-13

### Added

- Initial project structure with modern Python + C++ extension layout
- pyproject.toml with scikit-build-core build system
- CMake build configuration with Spout SDK paths
- Python API with Sender and Receiver classes
- Full Spout SDK integration in C++ wrappers
- GPU texture sharing functionality (Sender)
- Zero-copy receiving functionality (Receiver)
- Performance monitoring (FPS, latency tracking)
- ModernGL API compatibility
- Context manager support (with statement) for Sender and Receiver
- Type stub file (\_\_init\_\_.pyi) for better IDE autocomplete and type checking
- Resource warnings for unclosed Sender instances
- Platform check with clear error message on non-Windows systems
- Single source of truth for version (`__version__.py` with dynamic reading)
- Comprehensive documentation structure (API reference, architecture, build guides)
- CI/CD workflow templates (GitHub Actions for build and release)
- Python 3.13+ support configured
- BSD-2-Clause license matching Spout
- Third-party license attributions
- Automated Spout SDK download script
- Comprehensive test suite with pytest
  - Context manager tests
  - Resource management and warning tests
  - Platform compatibility tests
  - Integration tests for complete workflows
  - Deterministic and reproducible test design

### Changed

- Implemented real Spout SDK calls replacing placeholder stubs
- Updated forward declarations to use `Spout` class
- Improved error handling in C++ wrappers
