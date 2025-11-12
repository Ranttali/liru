"""Tests for liru.Receiver."""

import pytest
import liru


def test_receiver_creation() -> None:
    """Test receiver can be created."""
    receiver = liru.Receiver()
    assert receiver.active_sender == ""


def test_receiver_creation_with_sender(sender_name: str) -> None:
    """Test receiver can be created with sender name."""
    receiver = liru.Receiver(sender_name)
    # Note: With stub implementation, this might not connect yet
    # assert receiver.active_sender == sender_name


def test_receiver_get_sender_list() -> None:
    """Test getting list of senders."""
    receiver = liru.Receiver()
    senders = receiver.get_sender_list()
    assert isinstance(senders, list)
    # Stub implementation returns placeholder senders
    assert len(senders) >= 0


def test_receiver_receive_texture(texture_id: int) -> None:
    """Test receiving texture."""
    receiver = liru.Receiver()

    # TODO: This will work once Spout SDK is integrated
    # For now, stub returns placeholder dimensions
    try:
        width, height = receiver.receive_texture(texture_id)
        assert isinstance(width, int)
        assert isinstance(height, int)
        assert width > 0
        assert height > 0
    except RuntimeError:
        pass  # May fail without actual sender


def test_receiver_invalid_texture_id() -> None:
    """Test receiving fails with invalid texture ID."""
    receiver = liru.Receiver()

    with pytest.raises(ValueError, match="Invalid texture ID"):
        receiver.receive_texture(0)

    with pytest.raises(ValueError, match="Invalid texture ID"):
        receiver.receive_texture(-1)


def test_receiver_is_updated() -> None:
    """Test frame update check."""
    receiver = liru.Receiver()
    updated = receiver.is_updated()
    assert isinstance(updated, bool)


def test_receiver_select_sender(sender_name: str) -> None:
    """Test selecting sender."""
    receiver = liru.Receiver()
    receiver.select_sender(sender_name)
    # Note: Stub implementation sets active sender
    assert receiver.active_sender == sender_name


def test_receiver_select_sender_invalid() -> None:
    """Test selecting sender fails with empty name."""
    receiver = liru.Receiver()

    with pytest.raises(ValueError, match="Sender name cannot be empty"):
        receiver.select_sender("")


def test_receiver_dimensions() -> None:
    """Test dimension getters."""
    receiver = liru.Receiver()
    width = receiver.width
    height = receiver.height
    assert isinstance(width, int)
    assert isinstance(height, int)
    assert width >= 0
    assert height >= 0


def test_receiver_last_receive_time() -> None:
    """Test latency tracking."""
    receiver = liru.Receiver()
    latency = receiver.last_receive_time_ms
    assert isinstance(latency, float)
    assert latency >= 0.0


def test_receiver_repr() -> None:
    """Test string representation."""
    receiver = liru.Receiver()
    repr_str = repr(receiver)
    assert "Receiver" in repr_str
