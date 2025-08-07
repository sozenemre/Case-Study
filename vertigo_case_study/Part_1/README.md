


# Clan API - Vertigo Case Study

This project includes a lightweight REST API for clan management, containerized with Docker and deployed to Google Cloud Run. It also features a simple ETL job that loads sample clan data into a PostgreSQL database hosted on Google Cloud SQL.

## 1. Database Setup (Google Cloud SQL)

- I created a Cloud SQL instance running PostgreSQL.
- I enabled public IP access and allowed connections from all IP addresses by setting the authorized networks to 0.0.0.0/0.
- I created a database named `vg` and ran the following schema:

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE clans (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) UNIQUE NOT NULL,
  region VARCHAR(10),
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 2. API Overview

The API is deployed on Google Cloud Run using Docker.  
(*You can test it with `curl`, but for a smoother experience, I highly recommend using the Postman Collection shared at the end of this README — it includes full API documentation and ready-to-use requests.*)

### Base URL:
```
https://clan-api-oma6ecvz5a-ew.a.run.app
```

### Endpoints:

#### Create Clan
```
POST /clans
```
**Payload:**
```json
{
  "name": "Shadow Warriors",
  "region": "TR"
}
```

#### Get Clans
```
GET /clans
```
**Query Parameters (optional):**
- `region`: filter by region
- `sort`: set to `created_at` for sorting by creation date (default: descending)

#### Get Clan by ID
```
GET /clans/<clan_id>
```

#### Delete Clan by ID
```
DELETE /clans/<clan_id>
```

## 3. ETL Job

The ETL job reads `clan_sample_data.csv`, transforms and cleans the data, and inserts it into the `clans` table.

### Transform Logic:

- If `created_at` is missing, it's set to `1970-01-01 00:00:00`.
- If `created_at` is a Unix timestamp like `1719227554`, it is converted to datetime.
- If `region` is not a valid two-letter country code, it's set to `"ZZ"`.

## 4. Docker

The API is containerized using the following Dockerfile:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "main:app", "-b", "0.0.0.0:8080"]
```

Then deployed using:
```bash
gcloud builds submit --tag gcr.io/<vertigo_games_case_study>/clan-api
gcloud run deploy clan-api \
  --image gcr.io/<vertigo_games_case_study>/clan-api \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated \
  --set-env-vars DB_HOST=...,DB_USER=...,DB_PASSWORD=...,DB_NAME=vg
```

## 5. Testing with `curl`

```bash
curl -X POST https://clan-api-oma6ecvz5a-ew.a.run.app/clans \
  -H "Content-Type: application/json" \
  -d '{"name": "CrimsonOrder", "region": "TR"}'

curl https://clan-api-oma6ecvz5a-ew.a.run.app/clans
```
## 6. Testing with `Postman Collection`
👉 [View the Postman Collection](https://sozen-emre98-9928497.postman.co/workspace/dev~aca37e47-4415-4e18-86e4-8b20ca86ca7d/collection/47365831-9ec09769-883a-43c3-a4a5-d74b70f13c7e?action=share&source=copy-link&creator=47365831)