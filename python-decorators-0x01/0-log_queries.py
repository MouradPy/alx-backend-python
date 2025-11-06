#!/usr/bin/python3
import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Try to extract the SQL query argument (for readability)
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        if query:
            print(f"[LOG] Executing SQL query: {query}")
        else:
            print("[LOG] Executing SQL query (no query string found).")
        # Execute the original function
        result = func(*args, **kwargs)
        return result
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Fetch users while logging the query
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
