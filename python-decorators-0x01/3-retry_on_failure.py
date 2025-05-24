#!/usr/bin/env python3
"""
Task 3: Retry on Failure Decorator

This script adds retry logic to database operations.
Retries a failing function up to N times with a delay between attempts.
"""

import time
import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator to automatically open and close a DB connection.
    Passes the connection as the first argument to the wrapped function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


def retry_on_failure(retries=3, delay=2):
    """
    Decorator to retry a function if it raises an exception.
    Retries the function `retries` times, waiting `delay` seconds between attempts.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    print(f"[Attempt {attempt}/{retries}] Error: {e}")
                    if attempt < retries:
                        time.sleep(delay)
                    else:
                        print("Max retry attempts reached. Raising exception.")
                        raise
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetches all users from the database.
    Will retry up to 3 times if a transient failure occurs.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


# Attempt to fetch users with automatic retry on failure
if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)
