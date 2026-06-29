from pathlib import Path

try:
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import count, col
except ImportError:
    print("PySpark is not installed yet.")
    print("This file shows the production scale version of the ETL pipeline.")
    print("Install later with: pip install pyspark")
    raise SystemExit()


RAW_FILE = "data/sample_applications.csv"
OUTPUT_FOLDER = "data/spark_capacity_summary"


def main():
    spark = (
        SparkSession.builder
        .appName("SmartSchoolPlacementAdmissionsETL")
        .getOrCreate()
    )

    applications = (
        spark.read
        .option("header", True)
        .csv(RAW_FILE)
    )

    cleaned = applications.dropna(
        subset=["district", "school_name", "grade", "status"]
    )

    summary = (
        cleaned
        .groupBy("district", "school_name", "grade", "status")
        .agg(count("*").alias("application_count"))
        .orderBy(col("district"), col("school_name"), col("status"))
    )

    summary.show(truncate=False)

    (
        summary
        .coalesce(1)
        .write
        .mode("overwrite")
        .option("header", True)
        .csv(OUTPUT_FOLDER)
    )

    print("Spark ETL complete.")
    print("Output folder:", OUTPUT_FOLDER)

    spark.stop()


if __name__ == "__main__":
    main()