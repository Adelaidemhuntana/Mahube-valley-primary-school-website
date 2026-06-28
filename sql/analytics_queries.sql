-- Capacity summary by school
-- This query can support a school or district dashboard.

SELECT
    school_name,
    district,
    grade_1_capacity,
    available_seats,
    under_offer_seats,
    taken_seats,
    ROUND((taken_seats * 100.0) / grade_1_capacity, 2) AS grade_1_taken_percentage
FROM schools;


-- Applications by status
-- This helps the department understand how many learners are eligible,
-- waitlisted or outside the radius rule.

SELECT
    status,
    COUNT(*) AS total_applications
FROM applications
GROUP BY status;


-- Offers by status
-- This shows how many offers are still pending and how many were accepted.

SELECT
    status,
    COUNT(*) AS total_offers
FROM offers
GROUP BY status;
