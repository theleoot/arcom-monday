import os
import sqlite3

class DatabaseSetup:
    def __init__(self, db_name="C:/Users/leonardo.tiago/OneDrive - Arcom SA/Área de Trabalho/PROJECTS/Monday Integration/CODE/database/database/monday.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Create a table for storing user data
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                monday_name TEXT NOT NULL,
                monday_id TEXT NOT NULL UNIQUE,
                role CHAR (1) CHECK (role IN ('A', 'U', 'V'))
            )
        ''')
        # Create a table for storing chat messages
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        self.connection.commit()