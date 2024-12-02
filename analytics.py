import sqlite3
from contextlib import closing

DATABASE_NAME = ":memory:"

def initialize_database():
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS proposals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    instance_id TEXT NOT NULL,
                    proposal_details TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

def add_proposal(instance_id, proposal_details):
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        with conn:
            conn.execute('''
                INSERT INTO proposals (instance_id, proposal_details)
                VALUES (?, ?)
            ''', (instance_id, proposal_details))

def get_proposal_count():
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        with conn:
            cursor = conn.execute('SELECT COUNT(*) FROM proposals')
            return cursor.fetchone()[0]

def get_all_proposals():
    with closing(sqlite3.connect(DATABASE_NAME)) as conn:
        with conn:
            cursor = conn.execute('SELECT * FROM proposals')
            return cursor.fetchall()

# Initialize the database when the module is imported
initialize_database()
