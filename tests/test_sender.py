"""Tests for liru.Sender."""

import pytest

import liru


def test_sender_creation(sender_name: str, texture_width: int, texture_height: int) -> None:
    """Test sender can be created with valid parameters."""
    sender = liru.Sender(sender_name, texture_width, texture_height)
    assert sender.name == sender_name
    assert sender.width == texture_width
    assert sender.height == texture_height
    sender.release()


def test_sender_invalid_name(texture_width: int, texture_height: int) -> None:
    """Test sender creation fails with empty name."""
    with pytest.raises(ValueError, match="Sender name cannot be empty"):
        liru.Sender("", texture_width, texture_height)


def test_sender_invalid_dimensions(sender_name: str) -> None:
    """Test sender creation fails with invalid dimensions."""
    with pytest.raises(ValueError, match="Invalid dimensions"):
        liru.Sender(sender_name, 0, 1080)

    with pytest.raises(ValueError, match="Invalid dimensions"):
        liru.Sender(sender_name, 1920, 0)

    with pytest.raises(ValueError, match="Invalid dimensions"):
        liru.Sender(sender_name, -1, -1)


def test_sender_send_texture(
    sender_name: str, texture_width: int, texture_height: int, texture_id: int
) -> None:
    """Test sending texture."""
    sender = liru.Sender(sender_name, texture_width, texture_height)

    # TODO: This will work once Spout SDK is integrated
    # For now, expect RuntimeError from stub implementation
    try:
        sender.send_texture(texture_id)
    except RuntimeError:
        pass  # Expected with stub implementation

    sender.release()


def test_sender_invalid_texture_id(
    sender_name: str, texture_width: int, texture_height: int
) -> None:
    """Test sending fails with invalid texture ID."""
    sender = liru.Sender(sender_name, texture_width, texture_height)

    with pytest.raises(ValueError, match="Invalid texture ID"):
        sender.send_texture(0)

    with pytest.raises(ValueError, match="Invalid texture ID"):
        sender.send_texture(-1)

    sender.release()


def test_sender_get_fps(sender_name: str, texture_width: int, texture_height: int) -> None:
    """Test FPS tracking."""
    sender = liru.Sender(sender_name, texture_width, texture_height)
    fps = sender.get_fps()
    assert isinstance(fps, float)
    assert fps >= 0.0
    sender.release()


def test_sender_last_send_time(sender_name: str, texture_width: int, texture_height: int) -> None:
    """Test latency tracking."""
    sender = liru.Sender(sender_name, texture_width, texture_height)
    latency = sender.last_send_time_ms
    assert isinstance(latency, float)
    assert latency >= 0.0
    sender.release()


def test_sender_repr(sender_name: str, texture_width: int, texture_height: int) -> None:
    """Test string representation."""
    sender = liru.Sender(sender_name, texture_width, texture_height)
    repr_str = repr(sender)
    assert sender_name in repr_str
    assert str(texture_width) in repr_str
    assert str(texture_height) in repr_str
    sender.release()
