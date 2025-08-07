#!/bin/bash

PROJECT_ID="vertigo-games-case-study"
BUCKET_NAME="vertigo-case-study-user-data"
BQ_DATASET="vertigo_user_analytics"
BQ_LOCATION="EU"
GCS_LOCATION="europe-west1"

echo "Setting active GCP project to $PROJECT_ID..."
gcloud config set project "$PROJECT_ID"

echo "Checking GCS bucket..."
if gsutil ls -b "gs://$BUCKET_NAME" &> /dev/null; then
  echo "GCS bucket already exists: $BUCKET_NAME"
else
  echo "Creating GCS bucket: $BUCKET_NAME"
  gsutil mb -l "$GCS_LOCATION" "gs://$BUCKET_NAME"
fi

echo "Checking BigQuery dataset..."
if bq --location=$BQ_LOCATION ls "$BQ_DATASET" &> /dev/null; then
  echo "BigQuery dataset already exists: $BQ_DATASET"
else
  echo "Creating BigQuery dataset: $BQ_DATASET"
  bq --location=$BQ_LOCATION mk --dataset "$BQ_DATASET"
fi

echo "Setup completed"