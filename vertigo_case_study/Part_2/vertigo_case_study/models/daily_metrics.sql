{{ config(
    materialized='incremental'
) }}

SELECT
  event_date,
  country,
  platform,
  COUNT(DISTINCT user_id) AS DAU,
  SUM(iap_revenue) AS total_iap_revenue,
  SUM(ad_revenue) AS total_ad_revenue,
  SAFE_DIVIDE(SUM(iap_revenue) + SUM(ad_revenue), COUNT(DISTINCT user_id)) AS arpdau,
  SUM(match_start_count) AS matches_started,
  SAFE_DIVIDE(SUM(match_start_count), COUNT(DISTINCT user_id)) AS match_per_dau,
  SAFE_DIVIDE(SUM(victory_count), SUM(match_end_count)) AS win_ratio,
  SAFE_DIVIDE(SUM(defeat_count), SUM(match_end_count)) AS defeat_ratio,
  SAFE_DIVIDE(SUM(server_connection_error), COUNT(DISTINCT user_id)) AS server_error_per_dau

FROM
  {{ source('vertigo_user_analytics', 'cleaned_user_metrics') }}

{% if is_incremental() %}
  WHERE event_date > (SELECT MAX(event_date) FROM {{ this }})
{% endif %}

GROUP BY
  event_date,
  country,
  platform
ORDER BY
  event_date,
  country,
  platform