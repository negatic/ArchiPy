# Redis Adapter Examples

This guide demonstrates how to use the ArchiPy Redis adapter for common caching and key-value storage patterns.

## Basic Usage

### Installation

First, ensure you have the Redis dependencies installed:

```bash
pip install "archipy[redis]"
# or
poetry add "archipy[redis]"
```

### Synchronous Redis Adapter

```python
from archipy.adapters.redis import RedisAdapter

# Create a Redis adapter with connection details
redis = RedisAdapter(
    host="localhost",
    port=6379,
    db=0,
    password=None,  # Optional
    ssl=False,      # Optional
    socket_timeout=5.0  # Optional
)

# Set and get values
redis.set("user:123:name", "John Doe")
name = redis.get("user:123:name")
print(f"User name: {name}")  # Output: User name: John Doe

# Set with expiration (seconds)
redis.set("session:456", "active", ex=3600)  # Expires in 1 hour

# Delete a key
redis.delete("user:123:name")

# Check if key exists
if redis.exists("session:456"):
    print("Session exists")
```

### Asynchronous Redis Adapter

```python
import asyncio
from archipy.adapters.redis import AsyncRedisAdapter

async def main():
    # Create an async Redis adapter
    redis = AsyncRedisAdapter(
        host="localhost",
        port=6379,
        db=0
    )

    # Async operations
    await redis.set("counter", "1")
    await redis.incr("counter")  # Increment
    count = await redis.get("counter")
    print(f"Counter: {count}")  # Output: Counter: 2

    # Cleanup
    await redis.close()

# Run the async function
asyncio.run(main())
```

## Caching Patterns

### Function Result Caching

```python
import json
import time
from archipy.adapters.redis import RedisAdapter

redis = RedisAdapter(host="localhost", port=6379, db=0)

def cache_result(key, ttl=300):
    """Decorator to cache function results in Redis."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Create a cache key with function name and arguments
            cache_key = f"{key}:{func.__name__}:{hash(str(args) + str(kwargs))}"

            # Try to get from cache
            cached = redis.get(cache_key)
            if cached:
                return json.loads(cached)

            # Execute function and cache result
            result = func(*args, **kwargs)
            redis.set(cache_key, json.dumps(result), ex=ttl)
            return result
        return wrapper
    return decorator

# Example usage
@cache_result("api", ttl=60)
def expensive_api_call(item_id):
    print("Executing expensive operation...")
    time.sleep(1)  # Simulate expensive operation
    return {"id": item_id, "name": f"Item {item_id}", "data": "Some data"}

# First call will execute the function
result1 = expensive_api_call(123)
print("First call:", result1)

# Second call will retrieve from cache
result2 = expensive_api_call(123)
print("Second call:", result2)
```

## Mock Redis for Testing

ArchiPy provides a Redis mock for unit testing that doesn't require a real Redis server:

```python
import unittest
from archipy.adapters.redis import RedisMock, RedisAdapter

class UserService:
    def __init__(self, redis_adapter):
        self.redis = redis_adapter

    def get_user(self, user_id):
        cached = self.redis.get(f"user:{user_id}")
        if cached:
            return cached

        # In real code, we'd fetch from database if not in cache
        user_data = f"User {user_id} data"
        self.redis.set(f"user:{user_id}", user_data, ex=300)
        return user_data

class TestUserService(unittest.TestCase):
    def setUp(self):
        # Use the RedisMock instead of a real Redis connection
        self.redis_mock = RedisMock()
        self.user_service = UserService(self.redis_mock)

    def test_get_user(self):
        # Test first fetch (not cached)
        user_data = self.user_service.get_user(123)
        self.assertEqual(user_data, "User 123 data")

        # Test that it was cached
        self.assertEqual(self.redis_mock.get("user:123"), "User 123 data")

        # Change the cached value to test cache hit
        self.redis_mock.set("user:123", "Modified data")

        # Test cached fetch
        user_data = self.user_service.get_user(123)
        self.assertEqual(user_data, "Modified data")

# Run the test
if __name__ == "__main__":
    unittest.main()
```

## Advanced Redis Features

### Publish/Subscribe

```python
import threading
import time
from archipy.adapters.redis import RedisAdapter

redis = RedisAdapter(host="localhost", port=6379, db=0)

# Subscriber thread
def subscribe_thread():
    subscriber = RedisAdapter(host="localhost", port=6379, db=0)
    pubsub = subscriber.pubsub()

    def message_handler(message):
        if message["type"] == "message":
            print(f"Received message: {message['data']}")

    pubsub.subscribe(**{"channel:notifications": message_handler})
    pubsub.run_in_thread(sleep_time=0.5)

    # Keep thread running for demo
    time.sleep(10)
    pubsub.close()

# Start subscriber in background
thread = threading.Thread(target=subscribe_thread)
thread.start()

# Wait for subscriber to initialize
time.sleep(1)

# Publish messages
for i in range(5):
    message = f"Notification {i}"
    redis.publish("channel:notifications", message)
    time.sleep(1)

# Wait for thread to complete
thread.join()
```

### Pipeline for Multiple Operations

```python
from archipy.adapters.redis import RedisAdapter

redis = RedisAdapter(host="localhost", port=6379, db=0)

# Create a pipeline for atomic operations
pipe = redis.pipeline()
pipe.set("stats:visits", 0)
pipe.set("stats:unique_users", 0)
pipe.set("stats:conversion_rate", "0.0")
pipe.execute()  # Execute all commands at once

# Increment multiple counters atomically
pipe = redis.pipeline()
pipe.incr("stats:visits")
pipe.incr("stats:unique_users")
results = pipe.execute()
print(f"Visits: {results[0]}, Unique users: {results[1]}")
```
