#!/usr/bin/env python3
"""
Task 2: Transaction Management with a Decorator

This script adds transaction control to database operations using decorators.
If an operation fails, changes are rolled back. Otherwise, they're committed.
"""

import sqlite3
import functools


def with_db_connection(func):
    """
    Opens and closes the database connection automatically.
    Passes the connection as the first argument to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper


def transactional(func):
    """
    Decorator that ensures a function runs inside a transaction.
    Commits the transaction if successful, otherwise rolls back.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction failed: {e}")
            raise
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """
    Updates a user's email in the database.
    Wrapped with transaction and connection management decorators.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


# Update user's email with automatic transaction handling
if __name__ == "__main__":
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
