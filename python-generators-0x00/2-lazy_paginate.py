#!/usr/bin/python3
"""
Python Generators - Task 3
Lazy loading paginated data with generators
"""

import mysql.connector
from mysql.connector import Error


def paginate_users(page_size, offset):
    """
    Fetches a page of users from the database
    
    Args:
        page_size (int): Number of users per page
        offset (int): Starting position for the page
    
    Returns:
        list: A list of user dictionaries for the requested page
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123',
            database='ALX_prodev'
        )
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        
        cursor.close()
        connection.close()
        return rows
        
    except Error as e:
        print(f"Database error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []


def lazy_paginate(page_size):
    """
    Generator that lazily loads paginated data from the database
    
    Args:
        page_size (int): Number of users per page
    
    Yields:
        list: A page of user dictionaries
    """
    offset = 0
    
    # Single loop as required
    while True:
        # Fetch the next page
        page = paginate_users(page_size, offset)
        
        # If no more data, stop the generator
        if not page:
            break
        
        # Yield the current page
        yield page
        
        # Move to the next page
        offset += page_size


# Alternative implementation using the existing seed module
"""
import seed

def paginate_users(page_size, offset):
    
    #Fetches a page of users using the existing seed module
    
    connection = seed.connect_to_prodev()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        connection.close()
        return rows
    return []


def lazy_paginate(page_size):
    
    #Generator that lazily loads paginated data
    
    offset = 0
    
    # Single loop as required
    while True:
        page = paginate_users(page_size, offset)
        
        if not page:
            break
            
        yield page
        offset += page_size
"""

if __name__ == "__main__":
    # Test the lazy pagination
    print("Testing lazy pagination with page_size=3:")
    print("=" * 50)
    
    page_number = 0
    total_users = 0
    
    # Test with small page size for demonstration
    for page in lazy_paginate(3):
        page_number += 1
        print(f"\nPage {page_number}:")
        
        for user in page:
            total_users += 1
            print(f"  {user}")
        
        # Stop after 3 pages for testing
        if page_number >= 3:
            print(f"\n... (more pages available)")
            break
    
    print(f"\nTotal pages processed: {page_number}")
    print(f"Total users shown: {total_users}")