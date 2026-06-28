import sqlite3
from pathlib import Path

# This file creates a fresh demo database.
# Run it before your demo so that your numbers start from a clean state.

DB_PATH = Path("database/school_placement.db")
SCHEMA_PATH = Path("database/schema.sql")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create the tables from the SQL schema file.
cursor.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

# Clear old demo data so the demo is repeatable.
cursor.execute("DELETE FROM offers")
cursor.execute("DELETE FROM applications")
cursor.execute("DELETE FROM schools")

# These are sample schools for the demo.
# The first school is the main school you can talk about in your presentation.
schools = [
    ("Mahlasedi Masana Primary School", "Tshwane East", 1200, 120, 18, 12, 90),
    ("Mamelodi Primary School", "Tshwane East", 950, 90, 6, 10, 74),
    ("Phomolong Primary School", "Tshwane East", 800, 60, 14, 5, 41)
]

cursor.executemany("""
    INSERT INTO schools(
        school_name,
        district,
        total_capacity,
        grade_1_capacity,
        available_seats,
        under_offer_seats,
        taken_seats
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", schools)

conn.commit()
conn.close()

print("Database created successfully.")
print("You can now run: uvicorn backend.main:app --reload")
