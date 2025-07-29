# Library
import sqlite3
import time


def db_retry_lock(func):
    def wrapper(*args, **kwargs):
        MAX_RETRY = 5
        RETRY_DELAY = 0.1  # seconds
        for attempt in range(MAX_RETRY):
            try:
                return func(*args, **kwargs)
            except sqlite3.OperationalError as err:
                if "database is locked" in str(err) and attempt < MAX_RETRY:
                    time.sleep(RETRY_DELAY)
                    continue
                raise
        return None

    return wrapper
