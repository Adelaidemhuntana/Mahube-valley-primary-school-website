from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from datetime import datetime, timedelta

# This API is the main entry point of the project.
# For the first demo, it runs locally and uses SQLite.
# Later, the same idea can move to AWS or Azure.
#
# The goal is to show how parent applications change school capacity
# and how those changes can later be used for analytics.

app = FastAPI(
    title="Smart School Placement Hub",
    description="Starter API for school capacity planning, admissions analytics and learner placement.",
    version="1.0.0"
)

DB_PATH = "database/school_placement.db"


class ApplicationRequest(BaseModel):
    """
    This model describes the information a parent sends when applying.

    We keep it small for the first demo.
    In the real system, this would also include documents,
    parent ID details, learner birth certificate details,
    sibling information and school choices.
    """
    parent_name: str
    learner_name: str
    grade: str
    school_id: int
    home_distance_km: float


def get_connection():
    """
    Opens a connection to the SQLite database.

    SQLite is used because it is easy to run for a student demo.
    In a cloud version, this can be replaced by PostgreSQL,
    Amazon RDS, Azure SQL or another production database.
    """
    return sqlite3.connect(DB_PATH)


@app.get("/health")
def health_check():
    """
    Simple endpoint to confirm that the API is running.
    This is useful during a demo because it proves the backend is alive.
    """
    return {
        "status": "running",
        "project": "Smart School Placement Hub"
    }


@app.get("/schools")
def get_schools():
    """
    Returns the schools and their current capacity.

    This endpoint is important because it shows the same idea as a ticket booking system.
    A school has available seats, under offer seats and taken seats.

    Available means a seat can still be offered.
    Under offer means the seat is reserved while the parent decides.
    Taken means the parent accepted and the seat is confirmed.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT school_id, school_name, district, total_capacity, grade_1_capacity,
               available_seats, under_offer_seats, taken_seats
        FROM schools
    """)

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "school_id": row[0],
            "school_name": row[1],
            "district": row[2],
            "total_capacity": row[3],
            "grade_1_capacity": row[4],
            "available_seats": row[5],
            "under_offer_seats": row[6],
            "taken_seats": row[7]
        }
        for row in rows
    ]


@app.post("/applications")
def create_application(application: ApplicationRequest):
    """
    Creates a new learner application.

    This is the most important demo endpoint.

    The logic is simple:
    1. Check if the school exists.
    2. Check if the learner is within 5 km.
    3. Check if the school still has seats.
    4. If eligible, create an offer that expires in five days.
    5. Move one seat from available to under offer.

    This shows how a business event becomes useful data.
    """

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

    # This is a simple version of the GDE style distance rule.
    # In a real system this would use coordinates and a mapping service.
    if application.home_distance_km > 5:
        status = "OUTSIDE_RADIUS"
    elif available_seats <= 0:
        status = "WAITLISTED"
    else:
        status = "ELIGIBLE"

    created_at = datetime.utcnow().isoformat()

    cursor.execute("""
        INSERT INTO applications(
            parent_name,
            learner_name,
            grade,
            school_id,
            home_distance_km,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
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

    # If the learner is eligible, the system creates a five day offer.
    # The seat is not fully taken yet. It is only reserved.
    if status == "ELIGIBLE":
        expires_at = (datetime.utcnow() + timedelta(days=5)).isoformat()

        cursor.execute("""
            INSERT INTO offers(
                application_id,
                school_id,
                status,
                expires_at,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            application_id,
            application.school_id,
            "UNDER_OFFER",
            expires_at,
            created_at
        ))

        offer_id = cursor.lastrowid

        # This is where the capacity changes.
        # One available seat becomes an under offer seat.
        cursor.execute("""
            UPDATE schools
            SET available_seats = available_seats - 1,
                under_offer_seats = under_offer_seats + 1
            WHERE school_id = ?
        """, (application.school_id,))

        offer = {
            "offer_id": offer_id,
            "status": "UNDER_OFFER",
            "expires_at": expires_at
        }

    conn.commit()
    conn.close()

    return {
        "application_id": application_id,
        "application_status": status,
        "offer": offer
    }


@app.post("/offers/{offer_id}/accept")
def accept_offer(offer_id: int):
    """
    Accepts an offer.

    This is the second important demo endpoint.

    When a parent accepts an offer:
    1. The offer status changes to accepted.
    2. The seat moves from under offer to taken.
    3. The analytics numbers change.

    This proves that the project is not only storing data.
    It is changing data based on a real placement process.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT school_id, status FROM offers WHERE offer_id = ?",
        (offer_id,)
    )

    offer = cursor.fetchone()

    if not offer:
        conn.close()
        raise HTTPException(status_code=404, detail="Offer not found")

    school_id, status = offer

    if status != "UNDER_OFFER":
        conn.close()
        raise HTTPException(status_code=400, detail="Offer is not available for acceptance")

    cursor.execute(
        "UPDATE offers SET status = ? WHERE offer_id = ?",
        ("ACCEPTED", offer_id)
    )

    cursor.execute("""
        UPDATE schools
        SET under_offer_seats = under_offer_seats - 1,
            taken_seats = taken_seats + 1
        WHERE school_id = ?
    """, (school_id,))

    conn.commit()
    conn.close()

    return {
        "message": "Offer accepted. Seat secured.",
        "offer_id": offer_id
    }


@app.get("/analytics/capacity-summary")
def capacity_summary():
    """
    Returns a simple analytics summary.

    This endpoint is useful for explaining the data engineering side.
    A dashboard can use this data to show total capacity,
    available seats, under offer seats and taken seats.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            SUM(total_capacity),
            SUM(grade_1_capacity),
            SUM(available_seats),
            SUM(under_offer_seats),
            SUM(taken_seats)
        FROM schools
    """)

    row = cursor.fetchone()
    conn.close()

    return {
        "total_school_capacity": row[0],
        "grade_1_capacity": row[1],
        "available_seats": row[2],
        "under_offer_seats": row[3],
        "taken_seats": row[4]
    }
