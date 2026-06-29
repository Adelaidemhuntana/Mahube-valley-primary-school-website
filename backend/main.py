from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

app = FastAPI(
    title="Smart School Placement Hub",
    description="Starter API for school capacity planning, admissions analytics and learner placement.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "database/school_placement.db"
FRONTEND_PATH = Path("frontend")


class ApplicationRequest(BaseModel):
    # This is the data a parent sends when applying for a learner.
    parent_name: str
    learner_name: str
    grade: str
    school_id: int
    home_distance_km: float


def get_connection():
    # SQLite is used for the local demo.
    # A real cloud version can use Azure SQL, PostgreSQL or Amazon RDS.
    return sqlite3.connect(DB_PATH)


@app.get("/")
def home_page():
    # This opens the visual dashboard.
    # It lets the demo start on the product interface instead of Swagger.
    return FileResponse(FRONTEND_PATH / "index.html")


app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/health")
def health_check():
    return {"status": "running", "project": "Smart School Placement Hub"}


@app.get("/schools")
def get_schools():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT school_id, school_name, district, total_capacity, grade_1_capacity,
               available_seats, under_offer_seats, taken_seats
        FROM schools
    ''')

    rows = cursor.fetchall()
    conn.close()

    schools = []
    for row in rows:
        schools.append({
            "school_id": row[0],
            "school_name": row[1],
            "district": row[2],
            "total_capacity": row[3],
            "grade_1_capacity": row[4],
            "available_seats": row[5],
            "under_offer_seats": row[6],
            "taken_seats": row[7]
        })

    return schools


@app.post("/applications")
def create_application(application: ApplicationRequest):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT available_seats FROM schools WHERE school_id = ?",
        (application.school_id,)
    )

    school = cursor.fetchone()

    if not school:
        conn.close()
        raise HTTPException(status_code=404, detail="School not found")

    available_seats = school[0]

    # This is the simple 5 km rule for the demo.
    if application.home_distance_km > 5:
        status = "OUTSIDE_RADIUS"
    elif available_seats <= 0:
        status = "WAITLISTED"
    else:
        status = "ELIGIBLE"

    created_at = datetime.utcnow().isoformat()

    cursor.execute('''
        INSERT INTO applications(
            parent_name, learner_name, grade, school_id,
            home_distance_km, status, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        application.parent_name,
        application.learner_name,
        application.grade,
        application.school_id,
        application.home_distance_km,
        status,
        created_at
    ))

    application_id = cursor.lastrowid
    offer = None

    if status == "ELIGIBLE":
        expires_at = (datetime.utcnow() + timedelta(days=5)).isoformat()

        cursor.execute('''
            INSERT INTO offers(application_id, school_id, status, expires_at, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            application_id,
            application.school_id,
            "UNDER_OFFER",
            expires_at,
            created_at
        ))

        offer_id = cursor.lastrowid

        cursor.execute('''
            UPDATE schools
            SET available_seats = available_seats - 1,
                under_offer_seats = under_offer_seats + 1
            WHERE school_id = ?
        ''', (application.school_id,))

        offer = {"offer_id": offer_id, "status": "UNDER_OFFER", "expires_at": expires_at}

    conn.commit()
    conn.close()

    return {"application_id": application_id, "application_status": status, "offer": offer}


@app.post("/offers/{offer_id}/accept")
def accept_offer(offer_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT school_id, status FROM offers WHERE offer_id = ?", (offer_id,))
    offer = cursor.fetchone()

    if not offer:
        conn.close()
        raise HTTPException(status_code=404, detail="Offer not found")

    school_id, status = offer

    if status != "UNDER_OFFER":
        conn.close()
        raise HTTPException(status_code=400, detail="Offer is not available for acceptance")

    cursor.execute("UPDATE offers SET status = ? WHERE offer_id = ?", ("ACCEPTED", offer_id))

    cursor.execute('''
        UPDATE schools
        SET under_offer_seats = under_offer_seats - 1,
            taken_seats = taken_seats + 1
        WHERE school_id = ?
    ''', (school_id,))

    conn.commit()
    conn.close()

    return {"message": "Offer accepted. Seat secured.", "offer_id": offer_id}


@app.get("/analytics/capacity-summary")
def capacity_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            SUM(total_capacity),
            SUM(grade_1_capacity),
            SUM(available_seats),
            SUM(under_offer_seats),
            SUM(taken_seats),
            COUNT(*)
        FROM schools
    ''')

    row = cursor.fetchone()
    conn.close()

    return {
        "total_school_capacity": row[0],
        "grade_1_capacity": row[1],
        "available_seats": row[2],
        "under_offer_seats": row[3],
        "taken_seats": row[4],
        "total_schools": row[5],
        "unplaced_learners": 243,
        "total_applications": 45128
    }
