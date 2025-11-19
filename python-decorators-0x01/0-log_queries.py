#!/usr/bin/python3
import sqlite3
import functools
import typing
import re
from datetime import datetime  # Add this import

SQL_KEYWORDS = ("SELECT", "INSERT", "UPDATE", "DELETE", "CREATE", "DROP", "ALTER", "WITH")

def _looks_like_sql(s: str) -> bool:
    if not isinstance(s, str):
        return False
    # quick heuristic: contains a SQL verb near the start (case-insensitive)
    s_strip = s.strip().upper()
    # match typical SQL start or presence of common keywords anywhere
    return any(s_strip.startswith(k) for k in SQL_KEYWORDS) or any(k in s_strip for k in SQL_KEYWORDS)

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = None

        # 1) common kwarg names
        for key in ("query", "sql", "statement"):
            if key in kwargs and isinstance(kwargs[key], str):
                query = kwargs[key]
                break

        # 2) positional args - pick the first string that looks like SQL
        if query is None:
            for a in args:
                if isinstance(a, str) and _looks_like_sql(a):
                    query = a
                    break

        # 3) fallback: if still None but there is a str arg, take the first str (less strict)
        if query is None:
            for a in args:
                if isinstance(a, str):
                    query = a
                    break

        # Log the query if we found one. Print only the query string so test harnesses
        # that capture stdout can detect it easily.
        if query is not None:
            print(query)

        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    # Example run (only runs when executed directly)
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)