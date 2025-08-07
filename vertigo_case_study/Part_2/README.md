# Creating a DBT Model & Visualization

This part of the case study demonstrates how to build a lightweight data pipeline for mobile gaming metrics using BigQuery, dbt for modeling, and Looker Studio for dashboarding.

## 1. service_setup.sh : Configure Required GCP Services

A shell script named service_setup.sh was created to handle:

- Authentication with GCP (via service account or gcloud auth)
- Enabling required services such as BigQuery API
- Creating datasets, e.g., vertigo_user_analytics

## 2. stg_user_level_daily_metrics.sh : Load Source Data into BigQuery

A staging script (etl/data/stg_user_level_daily_metrics.sh) was written to load user-level data provided in the case study into BigQuery.

This step allowed for:
- Inspecting the raw data structure
- Understanding what transformations would be needed

## 3. Cleaned Data and Created cleaned_user_metrics Table

After reviewing the staging data, a cleaned version of the dataset was created with meaningful filters:
- install_date < event_date : Ensures that users don’t generate events before the app is installed — these rows were removed.
- (victory_count + defeat_count) <= match_start_count : A user shouldn’t win/lose more matches than they started — such rows were excluded as data errors.

After cleaning, a new table was created in BigQuery (vertigo_user_analytics.cleaned_user_metrics)

## 4. Built the dbt Project & daily_metrics Model

A new dbt project was initialized under the vertigo_case_study/ directory.
 
Key Components:
- models/daily_metrics.sql : Transforms cleaned data into daily KPIs
- schema.yml : Contains model descriptions and column-level documentation
- sources : The cleaned_user_metrics table was defined as a source
- dbt_project.yml : Project configuration (with incremental model setup)

Key Metrics Computed:
- DAU – Daily Active Users
- arpdau – Average Revenue Per Daily Active User
- win_ratio, defeat_ratio
- server_error_per_dau
- match_per_dau
- total_iap_revenue, total_ad_revenue

Incremental Logic :

```sql {% if is_incremental() %}
  WHERE event_date > (SELECT MAX(event_date) FROM {{ this }}) {% endif %}
```
This ensures only new daily records are appended on each run.

## 5. Built a Dashboard in Looker Studio

The final step was to connect Looker Studio to BigQuery and create the dashboard.

👉 [View the Looker Studio Dashboard](https://lookerstudio.google.com/reporting/57b45932-3621-4837-b515-1de0dc5ee29f/page/4ltTF/edit)