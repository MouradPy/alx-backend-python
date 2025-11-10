#!/usr/bin/python3
"""
Test MySQL Connection
"""

import mysql.connector
from mysql.connector import Error

def test_connection():
    try:
        # Try common MySQL configurations
        configs = [
            {'host': 'localhost', 'user': 'root', 'password': ''},
            {'host': 'localhost', 'user': 'root', 'password': 'root'},
            {'host': 'localhost', 'user': 'root', 'password': 'password'},
        ]
        
        for config in configs:
            try:
                print(f"Trying: user={config['user']}, password={'*' * len(config['password']) if config['password'] else 'empty'}")
                connection = mysql.connector.connect(**config)
                print("✅ SUCCESS! Connected to MySQL")
                
                # Show MySQL version
                cursor = connection.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"MySQL Version: {version[0]}")
                
                cursor.close()
                connection.close()
                return config
                
            except Error as e:
                print(f"❌ Failed: {e}")
                continue
                
        print("\n💡 If all failed, you might need to:")
        print("1. Check your MySQL root password")
        print("2. Run: mysql -u root -p")
        print("3. Or reset MySQL password if needed")
        return None
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    print("=== Testing MySQL Connection ===")
    test_connection()