import pandas as pd

# This is a small ETL pipeline.
#
# ETL means:
# Extract data from a source
# Transform it into a useful structure
# Load it into an output file or warehouse
#
# In this starter project, the source is a CSV file.
# In a real cloud project, the source could be S3, Azure Data Lake,
# an API, a database or a streaming service.

RAW_FILE = "data/sample_applications.csv"
OUTPUT_FILE = "data/capacity_summary.csv"

# Extract
df = pd.read_csv(RAW_FILE)

# Transform
# We group applications by district, school, grade and status.
# This helps a dashboard answer questions like:
# How many learners are eligible
# How many are waiting
# Which schools are receiving the most applications
summary = (
    df.groupby(["district", "school_name", "grade", "status"])
    .size()
    .reset_index(name="application_count")
)

# Load
summary.to_csv(OUTPUT_FILE, index=False)

print("ETL complete.")
print("Output file:", OUTPUT_FILE)
print(summary)
