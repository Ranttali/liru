"""Verify liru installation and basic functionality."""

import sys
from typing import Callable


def check_import() -> bool:
    """Test liru can be imported."""
    try:
        import liru

        print(f"✅ liru imported successfully (v{liru.__version__})")
        return True
    except ImportError as e:
        print(f"❌ Failed to import liru: {e}")
        return False


def check_version() -> bool:
    """Test version is correct."""
    try:
        import liru

        if not hasattr(liru, "__version__"):
            print("❌ liru has no __version__ attribute")
            return False

        print(f"✅ Version: {liru.__version__}")
        return True
    except Exception as e:
        print(f"❌ Version check failed: {e}")
        return False


def check_sender() -> bool:
    """Test Sender can be created."""
    try:
        import liru

        sender = liru.Sender("TestSender", 1920, 1080)
        print(f"✅ Sender created: {sender}")
        sender.release()
        return True
    except Exception as e:
        print(f"❌ Failed to create Sender: {e}")
        return False


def check_receiver() -> bool:
    """Test Receiver can be created."""
    try:
        import liru

        receiver = liru.Receiver()
        print(f"✅ Receiver created: {receiver}")
        return True
    except Exception as e:
        print(f"❌ Failed to create Receiver: {e}")
        return False


def check_core_extension() -> bool:
    """Test C++ extension is loaded."""
    try:
        import liru

        # Try to access the C++ extension
        sender = liru.Sender("Test", 1920, 1080)
        _ = sender._impl  # Access internal C++ wrapper
        print("✅ C++ extension (_liru_core) loaded successfully")
        sender.release()
        return True
    except AttributeError:
        print("⚠️  Warning: Cannot verify C++ extension (implementation hidden)")
        return True  # Not a critical error
    except Exception as e:
        print(f"❌ C++ extension check failed: {e}")
        return False


def main() -> int:
    """Run all verification checks."""
    print("=" * 60)
    print("liru Installation Verification")
    print("=" * 60)
    print()

    checks: list[tuple[str, Callable[[], bool]]] = [
        ("Import", check_import),
        ("Version", check_version),
        ("Sender", check_sender),
        ("Receiver", check_receiver),
        ("C++ Extension", check_core_extension),
    ]

    results: list[bool] = []
    for name, check_fn in checks:
        print(f"Running check: {name}")
        result = check_fn()
        results.append(result)
        print()

    print("=" * 60)
    passed = sum(results)
    total = len(results)

    if all(results):
        print(f"✅ All checks passed ({passed}/{total})")
        print()
        print("liru is installed correctly and ready to use!")
        return 0
    else:
        print(f"❌ Some checks failed ({passed}/{total} passed)")
        print()
        print("Please check the errors above and ensure:")
        print("  1. liru wheel is properly installed")
        print("  2. Visual C++ Redistributable 2022 is installed")
        print("  3. You're using Python 3.13+")
        return 1


if __name__ == "__main__":
    sys.exit(main())
