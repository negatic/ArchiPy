.. _examples_helpers_interceptors:

Interceptors
===========

Examples of ArchiPy's interceptor utilities:

fastapi_rest_rate_limit_handler
-----------------------------

Control API request rates for FastAPI:

.. code-block:: python

    from archipy.helpers.interceptors.fastapi.rate_limit.fastapi_rest_rate_limit_handler import FastAPIRestRateLimitHandler
    from fastapi import FastAPI, Request, Response

    app = FastAPI()

    # Set up rate limiting
    rate_limiter = FastAPIRestRateLimitHandler(
        limit=100,              # 100 requests
        window_seconds=60,      # per minute
        key_func=lambda request: request.client.host  # by IP address
    )

    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        # Check rate limit
        limited, headers = await rate_limiter.check_rate_limit(request)

        if limited:
            # Rate limit exceeded
            response = Response(
                content="Rate limit exceeded. Try again later.",
                status_code=429,
                headers=headers
            )
            return response

        # Continue with request
        response = await call_next(request)

        # Add rate limit headers to response
        for key, value in headers.items():
            response.headers[key] = value

        return response
