# Smart School Placement Hub

AI Powered Data Platform for School Capacity Planning, Admissions Analytics and Learner Placement

Founder and Lead Architect: Adelaide Montana

## Project overview

Smart School Placement Hub is a starter data engineering and cloud engineering project.

The project is based on a real problem. Every year parents apply for Grade 1 and Grade 8 school placement. Some schools become full, some learners wait too long, and education officials need better data to plan capacity.

This project shows how school applications can become useful data.

The system allows a parent to apply for a school seat. If the learner is within the 5 km rule and the school has available space, the system creates a five day offer. The offer moves the seat from available to under offer. When the parent accepts the offer, the seat becomes taken.

The project also includes analytics and ETL code so it is not only a web application. It shows how data can be collected, cleaned, transformed and used for dashboards.

## Why this is a data engineering project

This project is not only about submitting an application form.

It shows the full data journey.

```text
Parent application
        |
        v
FastAPI backend
        |
        v
Operational database
        |
        v
ETL pipeline
        |
        v
Analytics dataset
        |
        v
Capacity dashboard and future forecasting
```

A data engineer cares about how data moves, how it is cleaned, how it is stored, and how it becomes useful for decision making.

This project demonstrates those skills in a simple but clear way.

## What the demo should show

The demo should be shown in this order.

1. Show the API running in the browser using FastAPI docs.
2. Show the list of schools and their current capacity.
3. Submit a Grade 1 application.
4. Show that the system creates an offer when the learner is eligible.
5. Show that available seats reduce and under offer seats increase.
6. Accept the offer.
7. Show that under offer seats reduce and taken seats increase.
8. Run the ETL script.
9. Show the generated analytics CSV file.
10. Explain how this can move to AWS, Azure and Power BI.

## Project structure

```text
smart-school-placement-hub
|
|-- backend
|   |-- main.py
|
|-- database
|   |-- init_db.py
|   |-- schema.sql
|
|-- data
|   |-- sample_applications.csv
|
|-- etl
|   |-- capacity_etl.py
|
|-- sql
|   |-- analytics_queries.sql
|
|-- docs
|   |-- uml_class_diagram_mermaid.md
|   |-- sequence_diagram_mermaid.md
|   |-- data_engineering_architecture.md
|   |-- demo_script.md
|
|-- requirements.txt
|-- .gitignore
|-- README.md
```

## Technology used

```text
Python
FastAPI
SQLite
SQL
Pandas
Mermaid UML
```

## Future cloud version

This starter project runs locally so it can be demoed quickly.

The future cloud version can use:

```text
AWS S3 as the data lake
AWS Glue or PySpark for ETL
Amazon Redshift as the data warehouse
Azure Data Factory for pipelines
Power BI for dashboards
Azure AI or Amazon SageMaker for forecasting
```

## How to run the project

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it on Windows.

```bash
.venv\Scripts\activate
```

Install requirements.

```bash
pip install -r requirements.txt
```

Create the database.

```bash
python database/init_db.py
```

Start the API.

```bash
uvicorn backend.main:app --reload
```

Open this in your browser.

```text
http://127.0.0.1:8000/docs
```

## Useful API endpoints

```text
GET /health
GET /schools
POST /applications
POST /offers/{offer_id}/accept
GET /analytics/capacity-summary
```

## Example application data for the demo

Use this in the FastAPI docs when calling POST /applications.

```json
{
  "parent_name": "Nomsa Mokoena",
  "learner_name": "Lerato Mokoena",
  "grade": "Grade 1",
  "school_id": 1,
  "home_distance_km": 3.2
}
```

If the learner is within 5 km and the school has available seats, the system creates an offer.

## How to run the ETL

```bash
python etl/capacity_etl.py
```

This creates:

```text
data/capacity_summary.csv
```

The ETL script reads raw application data and creates an analytics summary by district, school, grade and status.

## What makes this project stand out

A simple weather app usually shows data from one API.

This project shows a bigger data engineering idea.

It has:

```text
Real world problem
Operational database
Business rules
Offer state changes
Data pipeline
Analytics output
Future cloud architecture
UML diagrams
```

## Status

This is the first starter version.

The next version should add:

```text
Frontend interface
School desk seat map
Power BI style dashboard
Forecasting model
Cloud deployment
Authentication
More realistic data
```
