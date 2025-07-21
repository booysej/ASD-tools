import sqlite3
import os
from pathlib import Path

DB_PATH = Path.home() / ".cogtools_family_support.db"

class FamilySupportDB:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            start_time DATETIME,
            end_time DATETIME,
            role TEXT,
            cognitive_load INTEGER,
            template_id INTEGER,
            completed BOOLEAN DEFAULT 0
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY,
            name TEXT,
            data TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME,
            type TEXT,
            people TEXT,
            context TEXT,
            tags TEXT,
            notes TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY,
            date DATE,
            mood INTEGER,
            triggers TEXT,
            notes TEXT
        )''')
        self.conn.commit()

    # Example: add_task, get_tasks, etc.
    def add_task(self, title, description, start_time, end_time, role, cognitive_load, template_id=None):
        c = self.conn.cursor()
        c.execute('''INSERT INTO tasks (title, description, start_time, end_time, role, cognitive_load, template_id) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (title, description, start_time, end_time, role, cognitive_load, template_id))
        self.conn.commit()
        return c.lastrowid

    def get_tasks(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM tasks')
        return c.fetchall()