#!/usr/bin/env python3
"""
Task 1: Handle Database Connections with a Decorator

This module defines a decorator `with_db_connection` that automatically opens
and closes a SQLite database connection for functions that interact with the DB.
"""

import sqlite3
import functools


def with_db_connection(func):
    """
    Decorator that manages opening and closing of a SQLite database connection.

    The decorated function should accept the connection as its first argument.

    Args:
        func (function): The target function to decorate.

    Returns:
        function: A wrapped function with automatic connection handling.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # Call the original function, passing the connection as the first argument
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Retrieve a user from the database by ID.

    Args:
        conn (sqlite3.Connection): The database connection.
        user_id (int): The ID of the user to fetch.

    Returns:
        tuple or None: The user record if found, otherwise None.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# Fetch user by ID with automatic connection handling
if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)
