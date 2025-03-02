.. _examples_adapters_redis:

Redis Adapters
============

Working with Redis for caching and messaging.

Configuration
------------

First, configure your Redis settings:

.. code-block:: python

    from archipy.configs.base_config import BaseConfig

    class AppConfig(BaseConfig):
        REDIS = {
            "MASTER_HOST": "localhost",
            "PORT": 6379,
            "PASSWORD": "password",
            "DB": 0,
            "DECODE_RESPONSES": True
        }

    # Set global configuration
    config = AppConfig()
    BaseConfig.set_global(config)

Synchronous Operations
-------------------

Examples of synchronous Redis operations:

.. code-block:: python

    import json
    from archipy.adapters.redis.redis_adapters import RedisAdapter

    # Create Redis adapter
    redis = RedisAdapter()

    # Basic operations
    def cache_user(user_id, user_data):
        # Cache user data with 1 hour expiry
        redis.set(f"user:{user_id}", json.dumps(user_data), ex=3600)

    def get_cached_user(user_id):
        data = redis.get(f"user:{user_id}")
        if data:
            return json.loads(data)
        return None

    def delete_cached_user(user_id):
        redis.delete(f"user:{user_id}")

    # List operations
    def add_to_recent_users(user_id):
        # Add to list and trim to 10 most recent
        redis.lpush("recent_users", user_id)
        redis.ltrim("recent_users", 0, 9)

    def get_recent_users():
        return redis.lrange("recent_users", 0, -1)

    # Set operations
    def add_user_role(user_id, role):
        redis.sadd(f"user:{user_id}:roles", role)

    def has_user_role(user_id, role):
        return redis.sismember(f"user:{user_id}:roles", role)

    def get_user_roles(user_id):
        return redis.smembers(f"user:{user_id}:roles")

Asynchronous Operations
--------------------

Examples of asynchronous Redis operations:

.. code-block:: python

    import asyncio
    import json
    from archipy.adapters.redis.redis_adapters import AsyncRedisAdapter

    # Create async Redis adapter
    async_redis = AsyncRedisAdapter()

    # Basic async operations
    async def cache_user_async(user_id, user_data):
        # Cache user data with 1 hour expiry
        await async_redis.set(f"user:{user_id}", json.dumps(user_data), ex=3600)

    async def get_cached_user_async(user_id):
        data = await async_redis.get(f"user:{user_id}")
        if data:
            return json.loads(data)
        return None

    # Hash operations
    async def update_user_profile(user_id, **fields):
        # Update multiple fields in a hash
        await async_redis.hset(f"profile:{user_id}", mapping=fields)

    async def get_user_profile(user_id):
        # Get all fields from a hash
        return await async_redis.hgetall(f"profile:{user_id}")

    # Usage with asyncio
    async def main():
        # Cache a user
        await cache_user_async("123", {"name": "John", "email": "john@example.com"})

        # Update profile
        await update_user_profile("123",
                                 first_name="John",
                                 last_name="Doe",
                                 age=30)

        # Get cached data
        user = await get_cached_user_async("123")
        profile = await get_user_profile("123")

        print(f"User: {user}")
        print(f"Profile: {profile}")

    # Run the async function
    asyncio.run(main())

Pub/Sub Messaging
---------------

Using Redis for publish/subscribe messaging:

.. code-block:: python

    import asyncio
    import json
    from archipy.adapters.redis.redis_adapters import AsyncRedisAdapter

    async_redis = AsyncRedisAdapter()

    # Publisher
    async def publish_event(event_type, data):
        message = json.dumps({
            "type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        })
        await async_redis.publish(f"events:{event_type}", message)

    # Subscriber
    async def subscribe_to_events():
        # Create a new connection for the subscription
        pubsub = async_redis.pubsub()

        # Subscribe to channels
        await pubsub.subscribe("events:user_created", "events:user_updated")

        # Process messages
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                print(f"Received event: {data['type']}")
                # Process event based on type
                if data["type"] == "user_created":
                    await process_user_created(data["data"])
                elif data["type"] == "user_updated":
                    await process_user_updated(data["data"])

    # Usage
    async def main():
        # Start subscriber in the background
        asyncio.create_task(subscribe_to_events())

        # Publish events
        await publish_event("user_created", {"id": "123", "name": "Alice"})
        await publish_event("user_updated", {"id": "123", "name": "Alice Smith"})

        # Keep running to receive messages
        await asyncio.sleep(10)

    # Run the async function
    asyncio.run(main())
