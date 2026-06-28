CREATE TABLE IF NOT EXISTS schools (
    school_id INTEGER PRIMARY KEY AUTOINCREMENT,
    school_name TEXT NOT NULL,
    district TEXT NOT NULL,
    total_capacity INTEGER NOT NULL,
    grade_1_capacity INTEGER NOT NULL,
    available_seats INTEGER NOT NULL,
    under_offer_seats INTEGER NOT NULL,
    taken_seats INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS applications (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_name TEXT NOT NULL,
    learner_name TEXT NOT NULL,
    grade TEXT NOT NULL,
    school_id INTEGER NOT NULL,
    home_distance_km REAL NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (school_id) REFERENCES schools(school_id)
);

CREATE TABLE IF NOT EXISTS offers (
    offer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER NOT NULL,
    school_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (application_id) REFERENCES applications(application_id),
    FOREIGN KEY (school_id) REFERENCES schools(school_id)
);
