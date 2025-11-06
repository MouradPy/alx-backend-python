import time
import sqlite3 
import functools

# Global cache dictionary to store query results
query_cache = {}

def with_db_connection(func):
    """
    Decorator that automatically handles database connection:
    - Opens a connection before calling the function
    - Passes the connection as the first argument
    - Closes the connection after the function completes
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open database connection
        conn = sqlite3.connect('users.db')
        try:
            # Call the original function with connection as first argument
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Always close the connection, even if an error occurs
            conn.close()
    return wrapper

def cache_query(func):
    """
    Decorator that caches database query results based on the SQL query string.
    - Caches results in a global dictionary
    - Uses the query string as the cache key
    - Returns cached result if available, otherwise executes and caches the result
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract query from arguments (either positional or keyword)
        query = kwargs.get('query') or (args[0] if args else None)
        
        # If query is in cache, return cached result
        if query in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[query]
        
        # If not in cache, execute the query and cache the result
        print(f"Cache miss for query: {query}")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
print("First call (will cache):")
users = fetch_users_with_cache(query="SELECT * FROM users")
print(f"Retrieved {len(users)} users")

print("\n" + "="*50 + "\n")

# Second call will use the cached result
print("Second call (will use cache):")
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(f"Retrieved {len(users_again)} users from cache")

print("\n" + "="*50 + "\n")

# Different query will not use cache
print("Different query (will not use cache):")
users_count = fetch_users_with_cache(query="SELECT COUNT(*) FROM users")
print(f"Retrieved count: {users_count[0][0]}")