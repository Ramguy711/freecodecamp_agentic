"""
01_synchronous_demo.py
=======================
Synchronous programming demo.

Two "fetch" functions, each simulating a network delay with time.sleep().
Run back to back, one fully finishes before the next starts.

Compare the total time printed here against 02_asynchronous_demo.py —
same two waits (4s + 2s), but run sequentially instead of concurrently.
"""

import time


def fetch_weather():
    print("Fetching weather data...")
    time.sleep(4)  # Simulate a network delay
    print("Weather data fetched.")


def fetch_news():
    print("Fetching news data...")
    time.sleep(2)  # Simulate a network delay
    print("News data fetched.")


def main():
    start_time = time.time()

    fetch_weather()
    fetch_news()

    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
