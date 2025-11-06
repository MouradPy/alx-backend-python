import sqlite3 
import functools

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

def transactional(func):
    """
    Decorator that manages database transactions:
    - Automatically commits if the function succeeds
    - Automatically rolls back if the function raises an exception
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Call the original function
            result = func(conn, *args, **kwargs)
            # If no exception was raised, commit the transaction
            conn.commit()
            return result
        except Exception:
            # If any exception occurred, rollback the transaction
            conn.rollback()
            # Re-raise the exception to notify the caller
            raise
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

# Update user's email with automatic transaction handling 
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
print("User email updated successfully!")