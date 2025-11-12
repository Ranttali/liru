# Contributing to liru

Thank you for your interest in contributing to liru! This document provides guidelines for contributing to the project.

## Development Setup

### Prerequisites

**For all contributors:**

- Windows 10/11
- Python 3.13+ (3.13.9 recommended)
- Git

**For building from source (C++ development):**

- Visual Studio 2022 with "Desktop development with C++" workload
  - Required components: MSVC compiler, Windows SDK, CMake tools
  - **Not needed if only working on Python code, docs, or tests**
  - **Not needed for users installing from pre-built wheels**

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/veitsi/liru.git
cd liru

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Download Spout SDK
scripts\download_spout_sdk.bat

# Build in development mode
pip install -e .
```

## Development Workflow

### Before Making Changes

1. Create a new branch for your work:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Ensure all tests pass:

   ```bash
   pytest tests/ -v
   ```

### Making Changes

1. **Code Style**:
   - Python code must follow Black formatting
   - C++ code should follow the existing style
   - Run linters before committing:

     ```bash
     black liru/ tests/
     ruff check liru/ tests/
     mypy liru/
     ```

2. **Testing**:
   - Add tests for new functionality
   - Ensure all tests pass:

     ```bash
     pytest tests/ -v
     ```

3. **Documentation**:
   - Update docstrings for new functions/classes
   - Update README.md if adding user-facing features
   - Update CHANGELOG.md with your changes

### Submitting Changes

1. Commit your changes with a clear message:

   ```bash
   git add .
   git commit -m "Add feature: description of feature"
   ```

2. Push to your fork:

   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request on GitHub

## Code Review Process

1. All PRs must pass CI/CD checks
2. At least one maintainer review is required
3. Address any feedback from reviewers
4. Once approved, a maintainer will merge your PR

## Coding Standards

### Python

- Follow PEP 8 (enforced by Black and Ruff)
- Use type hints for all function signatures
- Write docstrings for public APIs (Google style)
- Maximum line length: 100 characters

Example:

```python
def send_texture(self, texture_id: int) -> None:
    """Send OpenGL texture via Spout.

    Args:
        texture_id: OpenGL texture ID

    Raises:
        ValueError: If texture_id is invalid
        RuntimeError: If send operation fails
    """
    # Implementation
```

### C++

- Follow C++17 standard
- Use RAII for resource management
- Prefer smart pointers over raw pointers
- Use meaningful variable names

Example:

```cpp
bool SenderWrapper::send_texture(unsigned int texture_id) {
    if (texture_id == 0) {
        throw std::invalid_argument("Invalid texture ID: 0");
    }

    // Implementation
    return true;
}
```

## Testing Guidelines

- Write unit tests for new functionality
- Ensure tests are deterministic (no random failures)
- Use pytest fixtures for common test setup
- Mock external dependencies when appropriate

## Building Wheels

To build wheels for distribution:

```bash
# Build for current Python version
python -m build --wheel

# Build for all supported versions
scripts\build_all_wheels.bat
```

## Reporting Issues

When reporting issues, please include:

1. **Environment**:
   - Python version
   - Windows version
   - GPU model

2. **Steps to Reproduce**:
   - Minimal code example
   - Expected behavior
   - Actual behavior

3. **Error Messages**:
   - Full stack trace
   - Any relevant log output

## Feature Requests

We welcome feature requests! Please:

1. Is this about the wrapper or Spout itself? If it is about Spout, this is wrong project.
2. Check if the feature is already requested
3. Describe the use case clearly
4. Explain why it would be valuable
5. Consider contributing the implementation

## Questions?

- Open a [Discussion](https://github.com/veitsi/liru/discussions)
- Check existing [Issues](https://github.com/veitsi/liru/issues)
- Review the [Documentation](docs/)

## License

By contributing to liru, you agree that your contributions will be licensed under the BSD-2-Clause License.

---

Thank you for contributing to liru!
