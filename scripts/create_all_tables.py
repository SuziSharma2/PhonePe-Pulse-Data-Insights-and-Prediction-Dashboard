import sqlite3
import os

# Create or connect to SQLite database
conn = sqlite3.connect("db/phonepe_data.db")
cursor = conn.cursor()

# Table for aggregated_insurance
cursor.execute('''
    CREATE TABLE IF NOT EXISTS aggregated_insurance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        "table" TEXT,
        state TEXT,
        year INTEGER,
        quarter INTEGER,
        name TEXT,
        type TEXT,
        count INTEGER,
        amount REAL
    );
''')

# Table for aggregated_transactions
cursor.execute('''
    CREATE TABLE IF NOT EXISTS aggregated_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state TEXT,
        year INTEGER,
        quarter INTEGER,
        transaction_type TEXT,
        transaction_count INTEGER,
        transaction_amount REAL
    );
''')

# Table for aggregated_user
cursor.execute('''
    CREATE TABLE IF NOT EXISTS aggregated_user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state TEXT,
        year INTEGER,
        quarter INTEGER,
        brand TEXT,
        count INTEGER,
        percentage REAL
    );
''')

# Table for map_user
cursor.execute('''
    CREATE TABLE IF NOT EXISTS map_user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        state TEXT,
        year INTEGER,
        quarter INTEGER,
        district TEXT,
        registered_users INTEGER,
        app_opens INTEGER
    );
''')

conn.commit()
conn.close()

print("✅ Tables created successfully in db/phonepe_data.db")
