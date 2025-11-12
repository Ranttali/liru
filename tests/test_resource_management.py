"""Tests for resource management and warnings."""

import pytest
import warnings
import liru


def test_sender_explicit_release(
    sender_name: str, texture_width: int, texture_height: int
) -> None:
    """Test explicit release works correctly."""
    sender = liru.Sender(sender_name, texture_width, texture_height)
    sender.release()
    # Double release should be safe (idempotent)
    sender.release()


def test_sender_use_after_release(
    sender_name: str, texture_width: int, texture_height: int, texture_id: int
) -> None:
    """Test using sender after release raises error."""
    sender = liru.Sender(sender_name, texture_width, texture_height)
    sender.release()

    with pytest.raises(RuntimeError, match="Sender has been released"):
        sender.send_texture(texture_id)


def test_sender_resource_warning_on_del(
    sender_name: str, texture_width: int, texture_height: int
) -> None:
    """Test ResourceWarning is raised if sender not explicitly released."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always", ResourceWarning)

        # Create sender without releasing
        sender = liru.Sender(sender_name, texture_width, texture_height)
        sender_ref = sender
        del sender  # Trigger __del__

        # Check if ResourceWarning was raised
        assert len(w) >= 1
        assert issubclass(w[-1].category, ResourceWarning)
        assert "not explicitly released" in str(w[-1].message)
        assert sender_name in str(w[-1].message)


def test_sender_no_warning_with_explicit_release(
    sender_name: str, texture_width: int, texture_height: int
) -> None:
    """Test no ResourceWarning if sender explicitly released."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always", ResourceWarning)

        sender = liru.Sender(sender_name, texture_width, texture_height)
        sender.release()
        del sender

        # Should not have ResourceWarning
        resource_warnings = [warning for warning in w if issubclass(warning.category, ResourceWarning)]
        assert len(resource_warnings) == 0


def test_sender_no_warning_with_context_manager(
    sender_name: str, texture_width: int, texture_height: int
) -> None:
    """Test no ResourceWarning when using context manager."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always", ResourceWarning)

        with liru.Sender(sender_name, texture_width, texture_height) as sender:
            pass  # Just enter and exit

        # Should not have ResourceWarning
        resource_warnings = [warning for warning in w if issubclass(warning.category, ResourceWarning)]
        assert len(resource_warnings) == 0


def test_receiver_multiple_operations() -> None:
    """Test receiver can be used multiple times."""
    receiver = liru.Receiver()

    # Multiple calls should work
    for _ in range(3):
        senders = receiver.get_sender_list()
        assert isinstance(senders, list)
        updated = receiver.is_updated()
        assert isinstance(updated, bool)


def test_sender_properties_after_release(
    sender_name: str, texture_width: int, texture_height: int
) -> None:
    """Test read-only properties still work after release."""
    sender = liru.Sender(sender_name, texture_width, texture_height)
    sender.release()

    # Properties should still be accessible
    assert sender.name == sender_name
    assert sender.width == texture_width
    assert sender.height == texture_height
