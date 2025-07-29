# Library
import time
import random
import threading
from fake_useragent import UserAgent
from requests import Session
import logging


# ? Utils
from utils.constant import (
    BRIGHTDATA_PASS,
    BRIGHTDATA_PORT,
    BRIGHTDATA_USER,
    BRIGHTDATA_ZONE,
    REQUEST_RETRY_ATTEMPT,
    REQUEST_MAX_PER_MINUTE,
    PROXY,
)


def ethical_delay(base_delay=1.0, max_jitter=2.0) -> None:
    """
    The delay after processing each URL and before the next iteration.
    Ethical web scraping to:
    1. Avoid overwhelming the target server
    2. Prevent IP blocking/rate limiting
    3. Maintain polite scraping etiquette
    delay = 2 + random.uniform(-0.5, 0.5)
    """

    """Add random delay with jitter for more human-like patterns"""
    delay = base_delay + random.random() * max_jitter
    time.sleep(delay)


# ? For rate limiting
# Global list tracking when requests occur
request_timestamps = []
# Ensures thread-safe access to request_timestamps
# Prevents race conditions in multi-threaded scraping
rate_lock = threading.Lock()


def check_request_rate() -> None:
    """Check if we are exceeding the rate limit and pause if necessary"""
    global request_timestamps
    with rate_lock:
        now = time.time()
        # Remove timestamps older than 1 minute
        request_timestamps = [ts for ts in request_timestamps if now - ts < 60]
        # If record length ≥60 requests in last 60s, pauses for 30 seconds
        if len(request_timestamps) >= REQUEST_MAX_PER_MINUTE:
            # We are over the rate limit, sleep for 30 seconds
            time.sleep(30)
        # Adds current request timestamp to tracking list
        request_timestamps.append(now)


def create_session() -> Session:
    """
    Create a requests session with rotating User-Agent and proxy support
    Returns:
        requests.Session: Configured session object
    """
    session = Session()

    # Rotate User-Agent
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        # "Accept-Language": "en-US,en;q=0.9",
    }
    session.headers.update(headers)

    # "BRIGHTDATA" proxy configuration
    if BRIGHTDATA_ZONE:
        zone = BRIGHTDATA_ZONE
        user = BRIGHTDATA_USER
        password = BRIGHTDATA_PASS
        port = BRIGHTDATA_PORT

        # Generate random session ID for IP rotation
        session_id = random.randint(1000000, 9999999)
        proxy_url = f"http://{zone}-session-{session_id}:{password}@{user}:{port}"
        session.proxies = {"http": proxy_url, "https": proxy_url}

    # Fallback to "PROXY" if BrightData not configured
    elif len(PROXY):
        proxy_url = random.choice(PROXY)
        session.proxies = {"http": proxy_url, "https": proxy_url}

    return session


import time
import logging


def request_retry(func):
    def wrapper(*args, **kwargs):
        for attempt in range(REQUEST_RETRY_ATTEMPT):
            try:
                return func(*args, **kwargs)
            except Exception as err:
                logging.error(err)
                if attempt < REQUEST_RETRY_ATTEMPT:
                    print(
                        f"🔁[{attempt + 1}/{REQUEST_RETRY_ATTEMPT}] RETRYING : {err} "
                    )
                    ethical_delay()
                    continue
                raise  # Re-raise after final attempt
        return None

    return wrapper
