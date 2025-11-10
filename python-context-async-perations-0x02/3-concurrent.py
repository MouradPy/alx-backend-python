#!/usr/bin/env python3
"""
Concurrent Asynchronous Database Queries
"""

import asyncio
import aiosqlite

DB_PATH = "async_users.db"


async def async_fetch_users():
    """
    Fetch all users from the database
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            return results


async def async_fetch_older_users():
    """
    Fetch users older than 40 from the database
    """
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            return results


async def fetch_concurrently():
    """
    Execute both queries concurrently using asyncio.gather
    """
    # Create sample database first
    await create_sample_database()
    
    # Use asyncio.gather to execute both queries concurrently
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    return results


async def create_sample_database():
    """
    Create a sample database with users table and data
    """
    async with aiosqlite.connect(DB_PATH) as db:
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
            ('Grace Hopper', 'grace@example.com', 48)
        ]
        
        await db.executemany(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            sample_users
        )
        
        await db.commit()


if __name__ == "__main__":
    # Use asyncio.run() to run the concurrent fetch
    asyncio.run(fetch_concurrently())