# Data Engineering Architecture

## Simple version for the demo

```text
Parent applications
        |
        v
FastAPI backend
        |
        v
SQLite operational database
        |
        v
Python ETL pipeline
        |
        v
Analytics CSV
        |
        v
Dashboard ready data
```

## Cloud version

```text
Parent Portal and School Portal
        |
        v
API Gateway and FastAPI
        |
        v
Operational Database
        |
        v
Event Data
        |
        v
AWS S3 or Azure Data Lake
        |
        v
AWS Glue, PySpark or Azure Data Factory
        |
        v
Amazon Redshift or Azure Synapse
        |
        v
Power BI dashboards
        |
        v
AI forecasting
```

## Data engineering message

The system turns daily school placement activity into data that can help officials understand demand, capacity and shortages.
