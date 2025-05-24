#!/usr/bin/env python3
"""
Task 4: Cache Query Decorator

Caches results of database queries based on the SQL query string
to avoid redundant calls and improve performance.
"""

import time
import sqlite3
import functools

# Global cache dictionary
query_cache = {}


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


def cache_query(func):
    """
    Decorator to cache the results of SQL queries using the query string as the key.
    """
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Returning cached result for query:", query)
            return query_cache[query]
        print("Executing and caching query:", query)
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetch users using a cached query to avoid redundant database calls.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


# First call will execute and cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

print(users)
print(users_again)
