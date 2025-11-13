"""Test basic import and version."""

import liru


def test_import() -> None:
    """Test liru can be imported."""
    assert liru is not None


def test_version() -> None:
    """Test version is defined."""
    assert hasattr(liru, "__version__")
    assert isinstance(liru.__version__, str)
    # Version should be a valid semver-like string (e.g., "0.1.0")
    assert len(liru.__version__.split(".")) >= 2


def test_public_api() -> None:
    """Test public API exports."""
    assert hasattr(liru, "Sender")
    assert hasattr(liru, "Receiver")
    assert "Sender" in liru.__all__
    assert "Receiver" in liru.__all__
