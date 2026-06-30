from pathlib import Path
import sqlite3
import csv


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "school_placement.db"
OUTPUT_DIR = BASE_DIR / "data" / "powerbi"


def get_connection():
    return sqlite3.connect(DB_PATH)


def write_csv(file_name, rows, headers):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    file_path = OUTPUT_DIR / file_name

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for row in rows:
            writer.writerow(row)

    print("Created:", file_path)


def export_table(table_name, file_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM " + table_name)
    rows = cursor.fetchall()

    headers = []
    for column in cursor.description:
        headers.append(column[0])

    conn.close()

    write_csv(file_name, rows, headers)


def export_district_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            district,
            COUNT(*) AS total_schools,
            SUM(total_capacity) AS total_capacity,
            SUM(grade_1_capacity) AS grade_1_capacity,
            SUM(available_seats) AS available_seats,
            SUM(under_offer_seats) AS under_offer_seats,
            SUM(taken_seats) AS taken_seats
        FROM schools
        GROUP BY district
    """)

    rows = cursor.fetchall()
    conn.close()

    headers = [
        "district",
        "total_schools",
        "total_capacity",
        "grade_1_capacity",
        "available_seats",
        "under_offer_seats",
        "taken_seats"
    ]

    write_csv("district_summary.csv", rows, headers)


def export_seat_status_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            SUM(available_seats) AS total_seats
        FROM schools
    """)
    available = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            SUM(under_offer_seats) AS total_seats
        FROM schools
    """)
    under_offer = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            SUM(taken_seats) AS total_seats
        FROM schools
    """)
    taken = cursor.fetchone()[0]

    conn.close()

    rows = [
        ["Available", available],
        ["Under Offer", under_offer],
        ["Taken", taken]
    ]

    headers = ["seat_status", "total_seats"]

    write_csv("seat_status_summary.csv", rows, headers)


def main():
    if not DB_PATH.exists():
        print("Database not found.")
        print("Run this first: python database/init_db.py")
        return

    export_table("schools", "schools.csv")
    export_table("applications", "applications.csv")
    export_table("offers", "offers.csv")
    export_district_summary()
    export_seat_status_summary()

    print("Power BI export complete.")


main()