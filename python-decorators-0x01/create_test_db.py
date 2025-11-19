import sqlite3

# Create and populate a test database
def create_test_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    
    # Clear existing data and insert fresh sample data
    cursor.execute("DELETE FROM users")
    cursor.execute("INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')")
    cursor.execute("INSERT INTO users (name, email) VALUES ('Bob', 'bob@example.com')")
    cursor.execute("INSERT INTO users (name, email) VALUES ('Charlie', 'charlie@example.com')")
    
    conn.commit()
    conn.close()
    print("Test database created successfully!")

if __name__ == "__main__":
    create_test_database()