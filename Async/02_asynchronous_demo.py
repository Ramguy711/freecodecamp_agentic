"""
02_asynchronous_demo.py
========================
Asynchronous programming demo.

Same two "fetch" functions as 01_synchronous_demo.py, same simulated
delays (4s + 2s) — but this time using async/await and asyncio.gather(),
so both waits overlap instead of stacking.

Key things to notice when you run this:
- Both "Fetching..." lines print BEFORE either "...fetched." line.
  That's the "cashier takes both orders before either comes back from
  the kitchen" moment.
- "News data fetched." prints before "Weather data fetched." — the
  shorter wait (2s) finishes first, even though fetch_weather() was
  started first.
- Total time is ~4 seconds (the longer of the two waits), not 6
  (the sum of both) — proof the waits overlapped instead of stacking.

Compare this directly against 01_synchronous_demo.py's ~6 second total.
"""

import asyncio
import time


async def fetch_weather():
    print("Fetching weather data...")
    await asyncio.sleep(4)  # Simulate a network delay (non-blocking)
    print("Weather data fetched.")


async def fetch_news():
    print("Fetching news data...")
    await asyncio.sleep(2)  # Simulate a network delay (non-blocking)
    print("News data fetched.")


async def main():
    start_time = time.time()

    # Both coroutines are started together here. Each one runs until it
    # hits its own `await`, then control returns to the event loop, which
    # moves on to the other one instead of sitting idle.
    await asyncio.gather(fetch_weather(), fetch_news())

    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
