#!/usr/bin/python3
"""
Airbnb Clone - Database Seeding Module
Python Generators Project - Task 0
"""

import mysql.connector
import csv
import uuid
import os
from mysql.connector import Error


def connect_db():
    """
    Connects to the MySQL database server
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123'
	            )
        print("✅ Connected to MySQL server successfully")
        return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("✅ Database ALX_prodev created or already exists")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123',
            database='ALX_prodev'
        )
        print("✅ Connected to ALX_prodev database successfully")
        return connection
    except Error as e:
        print(f"❌ Error connecting to ALX_prodev database: {e}")
        return None


def create_table(connection):
    """
    Creates a table user_data if it does not exist with required fields
    """
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age INT NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        cursor.execute(create_table_query)
        print("✅ Table user_data created successfully")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")


def create_sample_csv(csv_file):
    """
    Creates a sample CSV file if it doesn't exist
    """
    sample_data = [
        ['name', 'email', 'age'],
        ['John Doe', 'john.doe@example.com', '25'],
        ['Jane Smith', 'jane.smith@example.com', '30'],
        ['Mike Johnson', 'mike.johnson@example.com', '35'],
        ['Sarah Wilson', 'sarah.wilson@example.com', '28'],
        ['David Brown', 'david.brown@example.com', '42'],
        ['Emily Davis', 'emily.davis@example.com', '31'],
        ['Robert Miller', 'robert.miller@example.com', '29'],
        ['Lisa Garcia', 'lisa.garcia@example.com', '33'],
        ['Thomas Anderson', 'thomas.anderson@example.com', '45'],
        ['Maria Martinez', 'maria.martinez@example.com', '27']
    ]
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(sample_data)
    
    print(f"✅ Created sample CSV file: {csv_file}")


def insert_data(connection, csv_file):
    """
    Inserts data in the database from CSV file if it does not exist
    """
    try:
        cursor = connection.cursor()
        
        # Check if table already has data
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print("ℹ️  Data already exists in the table")
            cursor.close()
            return
        
        # Check if CSV file exists, create if not
        if not os.path.exists(csv_file):
            print(f"📝 CSV file {csv_file} not found, creating sample data...")
            create_sample_csv(csv_file)
        
        # Read and insert data from CSV
        inserted_count = 0
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            
            for row in csv_reader:
                if len(row) >= 3:
                    user_id = str(uuid.uuid4())
                    name = row[0]
                    email = row[1]
                    try:
                        age = int(row[2])
                    except ValueError:
                        age = 0
                    
                    insert_query = """
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (user_id, name, email, age))
                    inserted_count += 1
        
        connection.commit()
        print(f"✅ Successfully inserted {inserted_count} records from {csv_file}")
        cursor.close()
        
    except Error as e:
        print(f"Error inserting data: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


class UserGenerator:
    """
    Generator class that streams rows from SQL database one by one
    This avoids the cursor cleanup issue
    """
    def __init__(self, connection, batch_size=100):
        self.connection = connection
        self.batch_size = batch_size
        self.cursor = None
        
    def __iter__(self):
        self.cursor = self.connection.cursor()
        self.offset = 0
        return self
        
    def __next__(self):
        if self.cursor is None:
            self.cursor = self.connection.cursor()
            
        # Fetch next batch if needed
        if not hasattr(self, '_current_batch') or self._batch_index >= len(self._current_batch):
            query = f"SELECT * FROM user_data LIMIT {self.batch_size} OFFSET {self.offset}"
            self.cursor.execute(query)
            self._current_batch = self.cursor.fetchall()
            self._batch_index = 0
            self.offset += self.batch_size
            
            if not self._current_batch:
                self.cursor.close()
                raise StopIteration
        
        # Get next row from current batch
        row = self._current_batch[self._batch_index]
        self._batch_index += 1
        return row
        
    def close(self):
        if self.cursor:
            self.cursor.close()


def user_generator(connection, batch_size=100):
    """
    Generator function that streams rows from SQL database one by one
    Uses yield keyword for memory-efficient processing
    """
    cursor = connection.cursor()
    try:
        offset = 0
        
        while True:
            query = f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}"
            cursor.execute(query)
            rows = cursor.fetchall()
            
            if not rows:
                break
                
            for row in rows:
                yield row  # This is the key generator feature!
                
            offset += batch_size
    finally:
        cursor.close()


if __name__ == "__main__":
    print("=" * 50)
    print("🏠 Airbnb Clone - Python Generators Project")
    print("📚 Task 0: Database Setup with Generators")
    print("=" * 50)
    
    # Test the implementation
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()
        print("✅ Database setup successful")

        connection = connect_to_prodev()
        if connection:
            create_table(connection)
            insert_data(connection, 'user_data.csv')
            
            # Test the generator - This is the main requirement!
            print("\n" + "=" * 30)
            print("🔄 TESTING PYTHON GENERATOR")
            print("=" * 30)
            print("Streaming users using generator (batch size: 3)...")
            print("Demonstrating memory-efficient data processing with YIELD:")
            
            # Using the generator function with proper cleanup
            gen = user_generator(connection, batch_size=3)
            user_count = 0
            
            print("\n🎯 First 5 users from generator:")
            for user in gen:
                user_count += 1
                print(f"   User {user_count}: {user}")
                
                # Stop after 5 users for demo
                if user_count >= 5:
                    print("   ... (generator can continue streaming more data)")
                    break
            
            print(f"\n✅ Generator successfully processed {user_count} users")
            print("💡 Key Features Demonstrated:")
            print("   - Uses YIELD keyword for memory efficiency")
            print("   - Processes data in batches")
            print("   - Streams one row at a time")
            print("   - No need to load entire dataset into memory")
            
            connection.close()
            print("\n" + "=" * 50)
            print("🎉 PROJECT COMPLETED SUCCESSFULLY!")
            print("📁 All requirements met:")
            print("   ✅ MySQL database setup")
            print("   ✅ Python generators with yield")
            print("   ✅ Batch processing")
            print("   ✅ Memory-efficient data streaming")
            print("=" * 50)
        else:
            print("❌ Failed to connect to ALX_prodev database")
    else:
        print("❌ Failed to connect to MySQL server")