#!/usr/bin/env python3
"""
Custom class-based context manager for database connections
"""

import sqlite3


class DatabaseConnection:
    """
    A custom context manager for SQLite database connections
    """
    
    def __init__(self, db_path):
        """
        Initialize the database connection manager
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """
        Enter the runtime context and establish database connection
        
        Returns:
            sqlite3.Cursor: Database cursor for executing queries
        """
        try:
            # Establish database connection
            self.connection = sqlite3.connect(self.db_path)
            # Create cursor for executing queries
            self.cursor = self.connection.cursor()
            return self.cursor
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context and clean up resources
        
        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred  
            exc_tb: Exception traceback if an exception occurred
        """
        try:
            if self.cursor:
                self.cursor.close()
            
            if self.connection:
                if exc_type is not None:
                    # Rollback if there was an exception
                    self.connection.rollback()
                else:
                    # Commit if everything went well
                    self.connection.commit()
                
                self.connection.close()
                
        except sqlite3.Error as e:
            print(f"Error during cleanup: {e}")
            if exc_type is None:
                raise


def main():
    """
    Demonstrate the usage of DatabaseConnection context manager
    """
    db_path = "users.db"
    
    # First, let's create a sample database with some data
    create_sample_database(db_path)
    
    # Use the context manager to query the database
    print("--- Using DatabaseConnection context manager ---")
    with DatabaseConnection(db_path) as cursor:
        # Execute the SELECT query
        cursor.execute("SELECT * FROM users")
        
        # Fetch and print all results
        results = cursor.fetchall()
        
        print("Query results:")
        print("ID | Name     | Email")
        print("-" * 20)
        for row in results:
            print(f"{row[0]:2} | {row[1]:8} | {row[2]}")


def create_sample_database(db_path):
    """
    Create a sample database with a users table and some sample data
    """
    try:
        # Connect to database (or create it if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create users table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            )
        ''')
        
        # Clear existing data and insert fresh sample data
        cursor.execute("DELETE FROM users")
        
        sample_users = [
            ('Alice Johnson', 'alice@example.com'),
            ('Bob Smith', 'bob@example.com'),
            ('Charlie Brown', 'charlie@example.com'),
            ('Diana Prince', 'diana@example.com')
        ]
        
        cursor.executemany(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            sample_users
        )
        
        conn.commit()
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Error creating sample database: {e}")


if __name__ == "__main__":
    main()