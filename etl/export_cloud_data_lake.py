from pathlib import Path
import sqlite3
import json
import shutil
import os


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "school_placement.db"
DATA_LAKE_DIR = BASE_DIR / "cloud_data_lake"
POWERBI_DIR = BASE_DIR / "data" / "powerbi"


def get_connection():
    return sqlite3.connect(DB_PATH)


def fetch_table(table_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM " + table_name)
    rows = cursor.fetchall()

    columns = []
    for column in cursor.description:
        columns.append(column[0])

    conn.close()

    records = []

    for row in rows:
        record = {}
        index = 0

        for column in columns:
            record[column] = row[index]
            index = index + 1

        records.append(record)

    return records


def write_jsonl(folder_name, file_name, records):
    folder_path = DATA_LAKE_DIR / "raw" / folder_name
    folder_path.mkdir(parents=True, exist_ok=True)

    file_path = folder_path / file_name

    with open(file_path, "w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record) + "\n")

    return file_path


def copy_processed_powerbi_files():
    processed_dir = DATA_LAKE_DIR / "processed" / "powerbi"
    processed_dir.mkdir(parents=True, exist_ok=True)

    copied_files = []

    if POWERBI_DIR.exists():
        for file_path in POWERBI_DIR.glob("*.csv"):
            target_path = processed_dir / file_path.name
            shutil.copy(file_path, target_path)
            copied_files.append(target_path)

    return copied_files


def write_manifest(raw_files, processed_files):
    manifest_path = DATA_LAKE_DIR / "manifest.json"

    bucket_name = os.getenv("AWS_S3_BUCKET", "smart-school-placement-hub-adelaide-2026")

    manifest = {
        "project": "Smart School Placement Hub",
        "data_lake_status": "CREATED",
        "local_data_lake_path": str(DATA_LAKE_DIR),
        "aws_s3_bucket": bucket_name,
        "zones": {
            "raw": [
                "raw/schools",
                "raw/applications",
                "raw/offers"
            ],
            "processed": [
                "processed/powerbi"
            ]
        },
        "raw_files": [],
        "processed_files": [],
        "message": "Cloud ready data lake export created successfully."
    }

    for file_path in raw_files:
        manifest["raw_files"].append(str(file_path.relative_to(DATA_LAKE_DIR)))

    for file_path in processed_files:
        manifest["processed_files"].append(str(file_path.relative_to(DATA_LAKE_DIR)))

    with open(manifest_path, "w", encoding="utf-8") as file:
        json.dump(manifest, file, indent=4)

    return manifest_path


def main():
    if not DB_PATH.exists():
        print("Database not found.")
        print("Run this first: python database/init_db.py")
        return

    DATA_LAKE_DIR.mkdir(parents=True, exist_ok=True)

    schools = fetch_table("schools")
    applications = fetch_table("applications")
    offers = fetch_table("offers")

    raw_files = []
    raw_files.append(write_jsonl("schools", "schools.jsonl", schools))
    raw_files.append(write_jsonl("applications", "applications.jsonl", applications))
    raw_files.append(write_jsonl("offers", "offers.jsonl", offers))

    processed_files = copy_processed_powerbi_files()

    manifest_path = write_manifest(raw_files, processed_files)

    print("Cloud data lake export complete.")
    print("Manifest created:", manifest_path)
    print("Upload the cloud_data_lake folder to your S3 bucket.")


main()