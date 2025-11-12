# liru API Reference

Complete API documentation for liru Python package.

## Module: `liru`

### `__version__`

- **Type**: `str`
- **Description**: Current version of liru

### Class: `Sender`

GPU texture sender for sharing via Spout.

#### Constructor

```python
Sender(name: str, width: int, height: int)
```

Create a Spout sender.

**Parameters:**

- `name` (str): Unique sender name (visible to receivers)
- `width` (int): Texture width in pixels
- `height` (int): Texture height in pixels

**Raises:**

- `ValueError`: If name is empty or dimensions are invalid
- `RuntimeError`: If sender creation fails

**Example:**

```python
sender = liru.Sender("MySource", 1920, 1080)
```

#### Methods

##### `send_texture(texture_id: int) -> None`

Send OpenGL texture via Spout.

**Parameters:**

- `texture_id` (int): OpenGL texture ID (e.g., `texture.glo` in ModernGL)

**Raises:**

- `ValueError`: If texture_id is invalid
- `RuntimeError`: If send operation fails

**Example:**

```python
texture = ctx.texture((1920, 1080), 4)
sender.send_texture(texture.glo)
```

##### `release() -> None`

Release Spout sender resources. Should be called when done sending.

**Example:**

```python
sender.release()
```

##### `get_fps() -> float`

Get current frames per second (rolling average).

**Returns:**

- `float`: Current FPS

**Example:**

```python
fps = sender.get_fps()
print(f"Sending at {fps:.1f} FPS")
```

#### Properties

##### `last_send_time_ms: float`

Get last send latency in milliseconds.

**Returns:**

- `float`: Latency in milliseconds

**Example:**

```python
latency = sender.last_send_time_ms
print(f"Send time: {latency:.3f}ms")
```

##### `name: str`

Get sender name.

**Returns:**

- `str`: Sender name

##### `width: int`

Get texture width.

**Returns:**

- `int`: Width in pixels

##### `height: int`

Get texture height.

**Returns:**

- `int`: Height in pixels

---

### Class: `Receiver`

GPU texture receiver for receiving via Spout.

#### Constructor

```python
Receiver(sender_name: Optional[str] = None)
```

Create a Spout receiver.

**Parameters:**

- `sender_name` (Optional[str]): Name of sender to connect to (optional)

**Raises:**

- `RuntimeError`: If receiver creation fails

**Example:**

```python
receiver = liru.Receiver("MySource")
# or
receiver = liru.Receiver()  # Connect later
```

#### Methods

##### `receive_texture(texture_id: int) -> tuple[int, int]`

Receive texture from Spout sender.

**Parameters:**

- `texture_id` (int): OpenGL texture ID to receive into

**Returns:**

- `tuple[int, int]`: (width, height) of received texture

**Raises:**

- `ValueError`: If texture_id is invalid
- `RuntimeError`: If receive operation fails

**Example:**

```python
texture = ctx.texture((1920, 1080), 4)
width, height = receiver.receive_texture(texture.glo)
```

##### `is_updated() -> bool`

Check if new frame is available from sender.

**Returns:**

- `bool`: True if sender has new frame

**Example:**

```python
if receiver.is_updated():
    receiver.receive_texture(texture.glo)
```

##### `select_sender(name: str) -> None`

Connect to a different sender.

**Parameters:**

- `name` (str): Name of sender to connect to

**Raises:**

- `ValueError`: If name is empty
- `RuntimeError`: If connection fails

**Example:**

```python
receiver.select_sender("AnotherSource")
```

##### `get_sender_list() -> list[str]`

Get list of available Spout senders.

**Returns:**

- `list[str]`: List of sender names currently broadcasting

**Example:**

```python
senders = receiver.get_sender_list()
print(f"Available senders: {senders}")
```

#### Properties

##### `active_sender: str`

Get name of currently connected sender.

**Returns:**

- `str`: Active sender name (empty string if not connected)

##### `width: int`

Get current texture width.

**Returns:**

- `int`: Width in pixels (0 if not connected)

##### `height: int`

Get current texture height.

**Returns:**

- `int`: Height in pixels (0 if not connected)

##### `last_receive_time_ms: float`

Get last receive latency in milliseconds.

**Returns:**

- `float`: Latency in milliseconds

**Example:**

```python
latency = receiver.last_receive_time_ms
print(f"Receive time: {latency:.3f}ms")
```

---

## Complete Example

```python
import moderngl
import liru
import time

# Sender example
def sender_example():
    ctx = moderngl.create_context()
    texture = ctx.texture((1920, 1080), 4)
    sender = liru.Sender("DemoSource", 1920, 1080)

    try:
        for frame in range(60):
            # Render to texture
            # ... your rendering code ...

            # Send
            sender.send_texture(texture.glo)

            # Monitor performance
            if frame % 30 == 0:
                print(f"FPS: {sender.get_fps():.1f}")
                print(f"Latency: {sender.last_send_time_ms:.3f}ms")

            time.sleep(1/60)
    finally:
        sender.release()
        texture.release()
        ctx.release()

# Receiver example
def receiver_example():
    ctx = moderngl.create_context()
    receiver = liru.Receiver("DemoSource")
    texture = ctx.texture((1, 1), 4)

    try:
        for frame in range(60):
            if receiver.is_updated():
                width, height = receiver.receive_texture(texture.glo)
                print(f"Received {width}x{height} texture")

                # Use texture for compositing
                # ... your compositing code ...

            time.sleep(1/60)
    finally:
        texture.release()
        ctx.release()
```

---

## Type Stubs

liru includes type stubs (`py.typed` marker) for full type checking support with mypy and other type checkers.

## Error Handling

All liru functions raise appropriate exceptions:

- `ValueError`: Invalid parameters (empty names, invalid dimensions, etc.)
- `RuntimeError`: Operation failures (sender creation, texture send/receive, etc.)

Always wrap liru calls in try-except blocks for production code:

```python
try:
    sender = liru.Sender("MySource", 1920, 1080)
    sender.send_texture(texture.glo)
except ValueError as e:
    print(f"Invalid parameters: {e}")
except RuntimeError as e:
    print(f"Operation failed: {e}")
finally:
    sender.release()
```

---

**See also:**

- [Architecture Documentation](plan/02_architecture.md)
- [Integration Guide](plan/06_integration_guide.md)
