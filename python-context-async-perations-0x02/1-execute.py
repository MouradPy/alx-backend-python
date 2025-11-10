#!/usr/bin/env python3
"""
Reusable Query Context Manager
"""

import sqlite3


class ExecuteQuery:
    """
    A reusable context manager for executing database queries
    """
    
    def __init__(self, db_path, query, params=None):
        """
        Initialize the query executor
        
        Args:
            db_path (str): Path to the SQLite database file
            query (str): SQL query to execute
            params (tuple, optional): Parameters for the query
        """
        self.db_path = db_path
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        """
        Enter the runtime context and execute the query
        
        Returns:
            list: Query results
        """
        try:
            # Establish database connection
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            
            # Execute the query with parameters
            self.cursor.execute(self.query, self.params)
            
            # Fetch results if it's a SELECT query
            if self.query.strip().upper().startswith('SELECT'):
                self.results = self.cursor.fetchall()
            else:
                self.results = self.cursor.rowcount
            
            return self.results
            
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            if self.connection:
                self.connection.rollback()
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context and clean up resources
        """
        try:
            if self.cursor:
                self.cursor.close()
            
            if self.connection:
                if exc_type is not None:
                    self.connection.rollback()
                else:
                    self.connection.commit()
                self.connection.close()
                
        except sqlite3.Error as e:
            print(f"Error during cleanup: {e}")
            if exc_type is None:
                raise


def main():
    """
    Demonstrate the usage of ExecuteQuery context manager
    """
    db_path = "users.db"
    
    # First, create a sample database with age data
    create_sample_database(db_path)
    
    # Use the ExecuteQuery context manager with the specified query
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    
    print("--- Using ExecuteQuery context manager ---")
    with ExecuteQuery(db_path, query, params) as results:
        print(f"Users older than 25:")
        print("ID | Name          | Email              | Age")
        print("-" * 50)
        for row in results:
            print(f"{row[0]:2} | {row[1]:13} | {row[2]:18} | {row[3]:2}")
    
    # Demonstrate reusability with different queries
    print("\n--- Reusing with different query (age < 30) ---")
    with ExecuteQuery(db_path, "SELECT name, age FROM users WHERE age < ?", (30,)) as results:
        print("Users younger than 30:")
        for name, age in results:
            print(f"  - {name}: {age} years old")
    
    print("\n--- Reusing with COUNT query ---")
    with ExecuteQuery(db_path, "SELECT COUNT(*) FROM users WHERE age BETWEEN 20 AND 40") as results:
        count = results[0][0]
        print(f"Total users aged 20-40: {count}")


def create_sample_database(db_path):
    """
    Create a sample database with a users table including age data
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create users table with age column
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                age INTEGER
            )
        ''')
        
        # Clear existing data and insert fresh sample data with ages
        cursor.execute("DELETE FROM users")
        
        sample_users = [
            ('Alice Johnson', 'alice@example.com', 22),
            ('Bob Smith', 'bob@example.com', 28),
            ('Charlie Brown', 'charlie@example.com', 35),
            ('Diana Prince', 'diana@example.com', 26),
            ('Eve Wilson', 'eve@example.com', 32),
            ('Frank Ocean', 'frank@example.com', 19),
            ('Grace Hopper', 'grace@example.com', 45),
            ('Henry Ford', 'henry@example.com', 24)
        ]
        
        cursor.executemany(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            sample_users
        )
        
        conn.commit()
        conn.close()
        print("Sample database created with age data")
        
    except sqlite3.Error as e:
        print(f"Error creating sample database: {e}")


if __name__ == "__main__":
    main()