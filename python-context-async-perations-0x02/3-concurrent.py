#!/usr/bin/env python3
"""
Concurrent Asynchronous Database Queries
"""

import asyncio
import aiosqlite


async def create_sample_database(db_path):
    """
    Create a sample database with users table and data
    """
    try:
        async with aiosqlite.connect(db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    age INTEGER
                )
            ''')
            
            await db.execute("DELETE FROM users")
            
            sample_users = [
                ('Alice Johnson', 'alice@example.com', 22),
                ('Bob Smith', 'bob@example.com', 28),
                ('Charlie Brown', 'charlie@example.com', 35),
                ('Diana Prince', 'diana@example.com', 26),
                ('Eve Wilson', 'eve@example.com', 32),
                ('Frank Ocean', 'frank@example.com', 45),
                ('Grace Hopper', 'grace@example.com', 48),
                ('Henry Ford', 'henry@example.com', 24),
                ('Ivy Chen', 'ivy@example.com', 52),
                ('Jack Ryan', 'jack@example.com', 38)
            ]
            
            await db.executemany(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                sample_users
            )
            
            await db.commit()
            print("Sample database created successfully")
            
    except Exception as e:
        print(f"Error creating sample database: {e}")


async def asyncfetchusers(db_path):
    """
    Fetch all users from the database
    
    Args:
        db_path (str): Path to the SQLite database file
        
    Returns:
        list: All users from the database
    """
    try:
        async with aiosqlite.connect(db_path) as db:
            async with db.execute("SELECT * FROM users") as cursor:
                results = await cursor.fetchall()
                print(f"Fetched {len(results)} total users")
                return results
    except Exception as e:
        print(f"Error in asyncfetchusers: {e}")
        return []


async def asyncfetcholder_users(db_path):
    """
    Fetch users older than 40 from the database
    
    Args:
        db_path (str): Path to the SQLite database file
        
    Returns:
        list: Users older than 40
    """
    try:
        async with aiosqlite.connect(db_path) as db:
            async with db.execute(
                "SELECT * FROM users WHERE age > ?", (40,)
            ) as cursor:
                results = await cursor.fetchall()
                print(f"Fetched {len(results)} users older than 40")
                return results
    except Exception as e:
        print(f"Error in asyncfetcholder_users: {e}")
        return []


async def fetch_concurrently():
    """
    Execute both queries concurrently using asyncio.gather
    """
    db_path = "async_users.db"
    
    # Create sample database first
    await create_sample_database(db_path)
    
    print("=== Starting Concurrent Queries ===")
    
    # Execute both queries concurrently
    all_users, older_users = await asyncio.gather(
        asyncfetchusers(db_path),
        asyncfetcholder_users(db_path)
    )
    
    print("\n=== Query Results ===")
    
    # Display all users
    print("All Users:")
    print("ID | Name          | Email              | Age")
    print("-" * 50)
    for user in all_users:
        print(f"{user[0]:2} | {user[1]:13} | {user[2]:18} | {user[3]:2}")
    
    # Display older users
    print(f"\nUsers Older Than 40:")
    print("ID | Name          | Email              | Age")
    print("-" * 50)
    for user in older_users:
        print(f"{user[0]:2} | {user[1]:13} | {user[2]:18} | {user[3]:2}")
    
    return all_users, older_users


async def benchmark_concurrent_vs_sequential():
    """
    Benchmark concurrent vs sequential execution
    """
    db_path = "async_users.db"
    
    print("\n=== Benchmark: Concurrent vs Sequential Execution ===")
    
    # Sequential execution
    print("Starting sequential execution...")
    start_time = asyncio.get_event_loop().time()
    
    users_seq = await asyncfetchusers(db_path)
    older_seq = await asyncfetcholder_users(db_path)
    
    sequential_time = asyncio.get_event_loop().time() - start_time
    print(f"Sequential execution time: {sequential_time:.4f} seconds")
    
    # Concurrent execution
    print("\nStarting concurrent execution...")
    start_time = asyncio.get_event_loop().time()
    
    users_conc, older_conc = await asyncio.gather(
        asyncfetchusers(db_path),
        asyncfetcholder_users(db_path)
    )
    
    concurrent_time = asyncio.get_event_loop().time() - start_time
    print(f"Concurrent execution time: {concurrent_time:.4f} seconds")
    
    improvement = ((sequential_time - concurrent_time) / sequential_time) * 100
    print(f"Performance improvement: {improvement:.2f}%")
    
    # Verify both methods return same results
    assert len(users_seq) == len(users_conc), "Results mismatch in all users"
    assert len(older_seq) == len(older_conc), "Results mismatch in older users"
    print("✓ Results verification: All queries returned consistent data")


def main():
    """
    Main function to run the concurrent queries
    """
    print("Concurrent Asynchronous Database Queries")
    print("=" * 50)
    
    # Run the concurrent fetch using asyncio.run()
    all_users, older_users = asyncio.run(fetch_concurrently())
    
    # Run benchmark
    asyncio.run(benchmark_concurrent_vs_sequential())


if __name__ == "__main__":
    main()