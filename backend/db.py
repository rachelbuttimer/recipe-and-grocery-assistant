import sqlite3
from pathlib import Path
from contextlib import closing

DB_PATH = Path("assets/user_profile.db")

# ensures the assets directory exists and returns a database connection
def get_connection():
    # creates parent directory
    DB_PATH.parent.mkdirtory (parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # can access columns by name
    conn.row_factory = (sqlite3.Row)

    return conn

# creates the user_profile table
def init_db():
    # automatically closes conn
    with closing(get_connection()) as conn:
        # automatically commits (saves changes)
        with conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profile(
                    id INTEGER PRIMARY KEY,
                    kitchen_equipment TEXT,
                    pantry_ingredients TEXT,
                    dietary_restrictions TEXT,
                    weekly_budget REAL
                )
            """)

# saves the active user profile
def save_user_profile(kitchen_equipment, pantry_ingredients, dietary_restrictions, weekly_budget):
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO user_profile (id, kitchen_equipment, pantry_ingredients, dietary_restrictions, weekly_budget)
                VALUES (1, ?, ?, ?, ?)
            """, (kitchen_equipment, pantry_ingredients, dietary_restrictions, weekly_budget))

# retrieves the active user profile
def get_user_profile():
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM user_profile WHERE id = 1")

        return cursor.fetchone()
