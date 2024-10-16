import sqlite3, threading

class Database:
    def __init__(self, db_file):
        self.conn = None
        self.cursor = None
        self.db_file = db_file
        self.lock = threading.Lock()

    def create_table(self):
        with self.lock:
            try:
                self.conn = sqlite3.connect(self.db_file)
                self.cursor = self.conn.cursor()
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS music_library (
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        artist TEXT NOT NULL
                    )
                ''')
            except sqlite3.Error as e:
                print(f"Error creating table: {e}")

    def add_music(self, data):
        with self.lock:
            try:
                self.cursor.execute('''
                    INSERT INTO music_library (title, artist)
                    VALUES (?, ?)
                ''', (data['title'], data['artist']))
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Error adding music: {e}")

    def get_all_music(self):
        with self.lock:
            try:
                self.cursor.execute('SELECT * FROM music_library')
                rows = self.cursor.fetchall()
                return rows
            except sqlite3.Error as e:
                print(f"Error getting all music: {e}")
                return []

    def update_music(self, data):
        with self.lock:
            try:
                self.cursor.execute('''
                    UPDATE music_library
                    SET title = ?, artist = ?
                    WHERE id = ?
                ''', (data['title'], data['artist'], data['id']))
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Error updating music: {e}")

    def delete_music(self, id):
        with self.lock:
            try:
                self.cursor.execute('''
                    DELETE FROM music_library
                    WHERE id = ?
                ''', (id,))
                self.conn.commit()
                return True
            except sqlite3.Error as e:
                print(f"Error deleting music: {e}")
                return False
