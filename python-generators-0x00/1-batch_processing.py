#!/usr/bin/python3
"""
Python Generators - Task 2
Batch processing large data with generators
"""

import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator that fetches users from database in batches
    
    Args:
        batch_size (int): Number of users to fetch per batch
    
    Yields:
        list: A batch of user dictionaries
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
            offset = 0
            
            # Loop 1: Batch fetching loop
            while True:
                # Fetch a batch of users
                query = f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}"
                cursor.execute(query)
                rows = cursor.fetchall()
                
                if not rows:
                    break
                
                # Convert batch to list of dictionaries
                batch = []
                for row in rows:  # Loop 2: Converting rows to dictionaries
                    user_dict = {
                        'user_id': row[0],
                        'name': row[1],
                        'email': row[2],
                        'age': row[3]
                    }
                    batch.append(user_dict)
                
                yield batch  # Yield the entire batch
                offset += batch_size
            
            # Clean up
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"Database error: {e}", file=sys.stderr)
        yield from []  # Return empty generator on error
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        yield from []  # Return empty generator on error


def batch_processing(batch_size):
    """
    Processes batches of users and filters those over age 25
    
    Args:
        batch_size (int): Number of users to process per batch
    """
    import sys
    
    # Get the batch stream generator
    batch_stream = stream_users_in_batches(batch_size)
    
    # Loop 3: Process each batch
    for batch in batch_stream:
        # Filter users over age 25 within the batch
        filtered_users = [user for user in batch if user['age'] > 25]
        
        # Print each filtered user
        for user in filtered_users:
            print(user)


# Alternative implementation with explicit loops (meets 3-loop requirement)
"""
def batch_processing(batch_size):
    import sys
    
    batch_stream = stream_users_in_batches(batch_size)
    
    # Loop 1: Process each batch
    for batch in batch_stream:
        # Loop 2: Filter users over age 25
        for user in batch:
            if user['age'] > 25:
                # Print the user
                print(user)
"""

if __name__ == "__main__":
    # Test the functions
    print("Testing batch processing with batch_size = 3:")
    print("Users over age 25:")
    
    # Test with small batch size for demonstration
    test_batch_size = 3
    batch_count = 0
    user_count = 0
    
    batch_stream = stream_users_in_batches(test_batch_size)
    for batch in batch_stream:
        batch_count += 1
        print(f"\nBatch {batch_count}:")
        for user in batch:
            if user['age'] > 25:
                user_count += 1
                print(f"  {user}")
    
    print(f"\nTotal batches processed: {batch_count}")
    print(f"Total users over age 25: {user_count}")