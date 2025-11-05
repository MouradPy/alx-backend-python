#!/usr/bin/python3
"""
Python Generators - Task 1
Generator that streams rows from SQL database one by one
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Generator that streams rows from user_data table one by one
    Uses yield keyword for memory-efficient data streaming
    
    Yields:
        dict: A dictionary containing user data with keys:
            - user_id, name, email, age
    """
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123',
            database='ALX_prodev'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Use a single loop as required
            cursor.execute("SELECT * FROM user_data")
            
            # Fetch and yield rows one by one
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                
                # Convert row to dictionary format as shown in the example
                user_dict = {
                    'user_id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'age': row[3]
                }
                yield user_dict
            
            # Clean up
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"Database error: {e}")
        yield from []  # Return empty generator on error
    except Exception as e:
        print(f"Unexpected error: {e}")
        yield from []  # Return empty generator on error


# Alternative implementation with batch processing (commented out)
# Uncomment if you prefer batch processing approach

"""
def stream_users():
    
    #Generator that streams rows from user_data table using batch processing
    
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123',
            database='ALX_prodev'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            batch_size = 100
            offset = 0
            
            # Single loop as required
            while True:
                query = f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}"
                cursor.execute(query)
                rows = cursor.fetchall()
                
                if not rows:
                    break
                
                for row in rows:
                    user_dict = {
                        'user_id': row[0],
                        'name': row[1],
                        'email': row[2],
                        'age': row[3]
                    }
                    yield user_dict
                
                offset += batch_size
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"Database error: {e}")
        yield from []
"""

if __name__ == "__main__":
    # Test the generator
    print("Testing stream_users generator:")
    user_count = 0
    for user in stream_users():
        user_count += 1
        print(user)
        if user_count >= 3:  # Show only first 3 for testing
            print("... (generator can continue)")
            break
    print(f"Total users streamed: {user_count}")