"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture
def sender_name() -> str:
    """Fixture for test sender name."""
    return "TestSender"


@pytest.fixture
def texture_width() -> int:
    """Fixture for test texture width."""
    return 1920


@pytest.fixture
def texture_height() -> int:
    """Fixture for test texture height."""
    return 1080


@pytest.fixture
def texture_id() -> int:
    """Fixture for mock OpenGL texture ID."""
    return 42
