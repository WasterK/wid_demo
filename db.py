import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime

# Load .env variables
load_dotenv()

class DatabaseAccess:
    def __init__(self):
        self.db_path = os.getenv("DATABASE_PATH", "work_instructions.db")

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _execute_query(self, query, params=None, fetchone=False, fetchall=False):
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            result = cursor.fetchone() if fetchone else cursor.fetchall() if fetchall else None
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"[DB ERROR] {e}")
            raise
        finally:
            conn.close()

    # ========== User Management ==========
    def is_user_already_exists(self, username: str) -> bool:
        query = 'SELECT 1 FROM "User" WHERE username = ?'
        return self._execute_query(query, (username,), fetchone=True) is not None

    def get_user_by_username(self, username: str):
        query = 'SELECT * FROM "User" WHERE username = ?'
        row = self._execute_query(query, (username,), fetchone=True)
        return dict(row) if row else None

    def get_user(self, user_id: int):
        query = 'SELECT username FROM "User" WHERE id = ?'
        row = self._execute_query(query, (user_id,), fetchone=True)
        return dict(row) if row else None

    def add_user(self, user_data):
        try:
            query = """
                INSERT INTO "User" (username, password_hash, created_by, updated_by)
                VALUES (?, ?, 1, 1)
            """
            self._execute_query(query, (user_data["username"], user_data["password"]))
            return True
        except:
            return -1

    def delete_user(self, user_id: int):
        query = 'DELETE FROM "User" WHERE id = ?'
        self._execute_query(query, (user_id,))

    # ========== Part Management ==========
    def get_all_parts(self):
        query = 'SELECT * FROM "Part" ORDER BY id'
        return [dict(row) for row in self._execute_query(query, fetchall=True)]

    def add_part(self, name: str):
        query = 'INSERT INTO "Part" (name, created_by, updated_by) VALUES (?, 1, 1)'
        self._execute_query(query, (name,))

    def delete_part(self, part_id: int):
        query = 'DELETE FROM "Part" WHERE id = ?'
        self._execute_query(query, (part_id,))

    # ========== Media Management ==========
    def get_media_by_part(self, part_id: int):
        query = 'SELECT * FROM "Media" WHERE part_id = ? ORDER BY display_order'
        return [dict(row) for row in self._execute_query(query, (part_id,), fetchall=True)]

    def add_media(self, part_id, media_name, media_data, media_type, duration=5, display_order=0):
        query = """
        INSERT INTO "Media" (
            part_id, media_name, media_data, media_type,
            duration, display_order, created_by, updated_by
        ) VALUES (?, ?, ?, ?, ?, ?, 1, 1)
        """
        self._execute_query(query, (
            part_id, media_name, media_data, media_type,
            duration, display_order
        ))

    def delete_media(self, media_id: int):
        query = 'DELETE FROM "Media" WHERE id = ?'
        self._execute_query(query, (media_id,))

    def update_media_order(self, media_id: int, display_order: int):
        query = """
        UPDATE "Media"
        SET display_order = ?, updated_on = CURRENT_TIMESTAMP, updated_by = 1
        WHERE id = ?
        """
        self._execute_query(query, (display_order, media_id))


# Singleton instance for app-wide use
db = DatabaseAccess()
