#!/usr/bin/python3
"""
Python Generators - Task 4
Memory-efficient aggregation with generators
"""

import mysql.connector
from mysql.connector import Error


def stream_user_ages():
    """
    Generator that yields user ages one by one from the database
    
    Yields:
        int: User age
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
            
            # Loop 1: Stream ages one by one
            cursor.execute("SELECT age FROM user_data")
            
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                
                yield row[0]  # Yield age only
            
            # Clean up
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"Database error: {e}")
        yield from []  # Return empty generator on error
    except Exception as e:
        print(f"Unexpected error: {e}")
        yield from []  # Return empty generator on error


def calculate_average_age():
    """
    Calculates the average age using the generator
    without loading all data into memory
    
    Returns:
        float: Average age of users
    """
    total_age = 0
    user_count = 0
    
    # Loop 2: Process each age from the generator
    for age in stream_user_ages():
        total_age += age
        user_count += 1
    
    # Calculate average (avoid division by zero)
    if user_count > 0:
        average_age = total_age / user_count
        return average_age
    else:
        return 0.0


# Alternative implementation with running average
"""
def calculate_average_age():
    
    #Calculates average age with running computation
    
    total_age = 0
    user_count = 0
    
    for age in stream_user_ages():
        total_age += age
        user_count += 1
    
    return total_age / user_count if user_count > 0 else 0.0
"""

if __name__ == "__main__":
    # Calculate and print the average age
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age:.2f}")
    
    # Optional: Show some statistics
    print("\nAdditional Statistics:")
    print("=" * 30)
    
    # Demonstrate the generator in action
    age_gen = stream_user_ages()
    sample_ages = []
    total_users = 0
    
    # Show first few ages and count total
    for i, age in enumerate(age_gen):
        total_users += 1
        if i < 5:  # Show first 5 ages as sample
            sample_ages.append(age)
    
    print(f"Sample ages: {sample_ages}")
    print(f"Total users processed: {total_users}")
    print(f"Average age calculated: {average_age:.2f}")