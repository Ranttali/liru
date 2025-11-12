"""Tests for context manager support."""

import pytest
import liru


def test_sender_context_manager(
    sender_name: str, texture_width: int, texture_height: int
) -> None:
    """Test Sender works as context manager."""
    with liru.Sender(sender_name, texture_width, texture_height) as sender:
        assert sender.name == sender_name
        assert sender.width == texture_width
        assert sender.height == texture_height
    # After exiting context, sender should be released


def test_sender_context_manager_exception(
    sender_name: str, texture_width: int, texture_height: int
) -> None:
    """Test Sender context manager handles exceptions properly."""
    try:
        with liru.Sender(sender_name, texture_width, texture_height) as sender:
            # Simulate an error
            raise ValueError("Test error")
    except ValueError:
        pass  # Expected
    # Sender should still be cleaned up properly


def test_receiver_context_manager() -> None:
    """Test Receiver works as context manager."""
    with liru.Receiver() as receiver:
        assert receiver.width >= 0
        assert receiver.height >= 0
    # After exiting context, receiver should be cleaned up


def test_receiver_context_manager_with_sender(sender_name: str) -> None:
    """Test Receiver context manager with sender name."""
    with liru.Receiver(sender_name) as receiver:
        # Receiver should be functional
        senders = receiver.get_sender_list()
        assert isinstance(senders, list)
    # Cleanup should occur automatically
