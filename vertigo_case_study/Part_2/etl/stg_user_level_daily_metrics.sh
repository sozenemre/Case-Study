#!/bin/bash

PROJECT_ID="vertigo-games-case-study"
BUCKET_NAME="vertigo-case-study-user-data"
BQ_DATASET="vertigo_user_analytics"
BQ_TABLE="stg_user_level_daily_metrics"
BQ_LOCATION="EU"
GCS_FOLDER="staging_data"
LOCAL_DATA_DIR="data"

echo "Uploading .csv.gz files from $LOCAL_DATA_DIR to GCS bucket $BUCKET_NAME..."

for file in "$LOCAL_DATA_DIR"/*.csv.gz; do
  filename=$(basename "$file")
  echo "Uploading $filename to GCS..."
  gsutil cp "$file" "gs://$BUCKET_NAME/$GCS_FOLDER/$filename"

  echo "Loading $filename into BigQuery table $BQ_DATASET.$BQ_TABLE..."
  bq --location=$BQ_LOCATION load \
    --autodetect \
    --source_format=CSV \
    --field_delimiter="," \
    --skip_leading_rows=1 \
    "$BQ_DATASET.$BQ_TABLE" \
    "gs://$BUCKET_NAME/$GCS_FOLDER/$filename"
done

echo "All files have been uploaded to BigQuery successfully."