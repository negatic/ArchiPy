import asyncio
import time

import aiohttp

URL = "http://192.168.150.83:8585/events"
HEADERS = {
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
}

TOTAL_REQUESTS = 100000
CONCURRENT_REQUESTS = 100


async def fetch(session, idx):
    start = time.perf_counter()
    try:
        async with session.get(URL, headers=HEADERS) as resp:
            result = await resp.text()
            elapsed = time.perf_counter() - start
            print(f"Request {idx+1}: {elapsed:.3f}s")
            print(result)
            if result:
                raise Exception(result)
            return elapsed
    except Exception as e:
        print(f"Request {idx+1} failed: {e}")
        return None


async def main():
    tasks = []
    connector = aiohttp.TCPConnector(limit=CONCURRENT_REQUESTS)
    async with aiohttp.ClientSession(connector=connector) as session:
        for idx in range(TOTAL_REQUESTS):
            tasks.append(fetch(session, idx))
        results = await asyncio.gather(*tasks)
    # Summary stats
    successful = [r for r in results if r is not None]
    print(f"\nTotal requests: {TOTAL_REQUESTS}")
    print(f"Successful requests: {len(successful)}")
    if successful:
        print(f"Avg response time: {sum(successful)/len(successful):.3f}s")
        print(f"Fastest: {min(successful):.3f}s, Slowest: {max(successful):.3f}s")


if __name__ == "__main__":
    asyncio.run(main())
