#!/usr/bin/python3
"""
Test MySQL Connection with known password
"""

import mysql.connector
from mysql.connector import Error

def test_connection():
    try:
        # Use the known password
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123'
        )
        print("✅ SUCCESS! Connected to MySQL with password '123'")
        
        # Show MySQL version
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"MySQL Version: {version[0]}")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Failed with password '123': {e}")
        return False

if __name__ == "__main__":
    print("=== Testing MySQL Connection ===")
    test_connection()