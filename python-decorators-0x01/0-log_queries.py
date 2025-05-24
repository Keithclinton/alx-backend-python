#!/usr/bin/env python3
"""
Task 0: Logging Database Queries with a Decorator

This module defines a decorator `log_queries` that logs SQL queries
executed by a function before executing them. It helps track and debug
database activity in Python applications.
"""

import sqlite3
import functools


def log_queries(func):
    """
    Decorator that logs the SQL query before executing it.

    Args:
        func (function): The target function to decorate.

    Returns:
        function: A wrapped function that logs SQL queries.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the SQL query from the arguments
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else 'UNKNOWN QUERY'

        print(f"[LOG] Executing SQL Query: {query}")
        return func(*args, **kwargs)

    return wrapper


@log_queries
def fetch_all_users(query):
    """
    Fetch all users from the database using the provided SQL query.

    Args:
        query (str): The SQL query to execute.

    Returns:
        list: A list of tuples containing user records.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Fetch users while logging the query
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    for user in users:
        print(user)
