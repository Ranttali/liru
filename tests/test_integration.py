"""Integration tests combining multiple features."""

import pytest

import liru


def test_sender_receiver_lifecycle(
    sender_name: str, texture_width: int, texture_height: int
) -> None:
    """Test complete lifecycle of sender and receiver."""
    # Create sender
    sender = liru.Sender(sender_name, texture_width, texture_height)
    assert sender.name == sender_name

    # Create receiver
    receiver = liru.Receiver(sender_name)

    # Get sender list (should include our sender eventually)
    senders = receiver.get_sender_list()
    assert isinstance(senders, list)

    # Check receiver can select sender
    receiver.select_sender(sender_name)
    assert receiver.active_sender == sender_name

    # Cleanup
    sender.release()


def test_multiple_senders_different_names(texture_width: int, texture_height: int) -> None:
    """Test multiple senders can coexist with different names."""
    sender1 = liru.Sender("Sender1", texture_width, texture_height)
    sender2 = liru.Sender("Sender2", texture_width, texture_height)
    sender3 = liru.Sender("Sender3", texture_width, texture_height)

    assert sender1.name == "Sender1"
    assert sender2.name == "Sender2"
    assert sender3.name == "Sender3"

    # All should have same dimensions
    assert sender1.width == sender2.width == sender3.width == texture_width
    assert sender1.height == sender2.height == sender3.height == texture_height

    # Cleanup
    sender1.release()
    sender2.release()
    sender3.release()


def test_sender_properties_are_immutable(
    sender_name: str, texture_width: int, texture_height: int
) -> None:
    """Test sender properties cannot be changed after creation."""
    sender = liru.Sender(sender_name, texture_width, texture_height)

    # Properties should be read-only
    with pytest.raises(AttributeError):
        sender.name = "NewName"  # type: ignore

    with pytest.raises(AttributeError):
        sender.width = 1280  # type: ignore

    with pytest.raises(AttributeError):
        sender.height = 720  # type: ignore

    sender.release()


def test_receiver_properties_are_read_only() -> None:
    """Test receiver properties are read-only."""
    receiver = liru.Receiver()

    with pytest.raises(AttributeError):
        receiver.active_sender = "NewSender"  # type: ignore

    with pytest.raises(AttributeError):
        receiver.width = 1920  # type: ignore

    with pytest.raises(AttributeError):
        receiver.height = 1080  # type: ignore


def test_context_manager_with_exception_handling(
    sender_name: str, texture_width: int, texture_height: int
) -> None:
    """Test context manager properly cleans up even with exceptions."""
    with pytest.raises(RuntimeError, match="User code error"):
        with liru.Sender(sender_name, texture_width, texture_height):
            # Simulate error in user code
            raise RuntimeError("User code error")
    # Sender should be cleaned up despite exception


def test_performance_metrics_initialization(
    sender_name: str, texture_width: int, texture_height: int
) -> None:
    """Test performance metrics are initialized correctly."""
    sender = liru.Sender(sender_name, texture_width, texture_height)

    # FPS should start at 0
    fps = sender.get_fps()
    assert fps >= 0.0

    # Latency should start at 0
    latency = sender.last_send_time_ms
    assert latency >= 0.0

    sender.release()


def test_receiver_initialization_states() -> None:
    """Test receiver initializes with correct default states."""
    # Receiver without sender name
    receiver1 = liru.Receiver()
    assert receiver1.active_sender == ""
    assert receiver1.width >= 0
    assert receiver1.height >= 0

    # Receiver with sender name
    receiver2 = liru.Receiver("TestSender")
    # Note: May not be connected yet, but should be set
    senders = receiver2.get_sender_list()
    assert isinstance(senders, list)


def test_deterministic_behavior(sender_name: str, texture_width: int, texture_height: int) -> None:
    """Test operations are deterministic (same input → same output)."""
    # Create same sender multiple times
    for _ in range(3):
        sender = liru.Sender(sender_name, texture_width, texture_height)
        assert sender.name == sender_name
        assert sender.width == texture_width
        assert sender.height == texture_height
        sender.release()


def test_string_representation_consistency(
    sender_name: str, texture_width: int, texture_height: int
) -> None:
    """Test __repr__ is consistent and informative."""
    sender = liru.Sender(sender_name, texture_width, texture_height)
    repr1 = repr(sender)
    repr2 = repr(sender)

    # Should be deterministic
    assert repr1 == repr2

    # Should contain key information
    assert "Sender" in repr1
    assert sender_name in repr1
    assert str(texture_width) in repr1
    assert str(texture_height) in repr1

    sender.release()
