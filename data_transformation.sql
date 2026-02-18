CREATE OR REPLACE TABLE `ad_data.unified_ads` AS

WITH facebook_normalized AS (
  SELECT
    date,
    campaign_id,
    campaign_name,
    ad_set_id AS subgroup_id,
    ad_set_name AS subgroup_name,
    'Facebook' AS platform,
    impressions,
    clicks,
    spend AS cost,
    conversions,
    reach,
    frequency,
    video_views,
    engagement_rate,
    NULL AS conversion_value,
    NULL AS quality_score,
    NULL AS likes,
    NULL AS shares,
    NULL AS comments,
    SAFE_DIVIDE(clicks, impressions) AS ctr,
    SAFE_DIVIDE(spend, clicks) AS cpc,
    SAFE_DIVIDE(spend, impressions) * 1000 AS cpm,
    SAFE_DIVIDE(spend, conversions) AS cpa,
    NULL AS roas
  FROM `ad_data.facebook_ads`
),

google_normalized AS (
  SELECT
    date,
    campaign_id,
    campaign_name,
    ad_group_id AS subgroup_id,
    ad_group_name AS subgroup_name,
    'Google Ads' AS platform,
    impressions,
    clicks,
    cost,
    conversions,
    NULL AS reach,
    NULL AS frequency,
    NULL AS video_views,
    NULL AS engagement_rate,
    conversion_value,
    quality_score,
    NULL AS likes,
    NULL AS shares,
    NULL AS comments,
    ctr,
    avg_cpc AS cpc,
    SAFE_DIVIDE(cost, impressions) * 1000 AS cpm,
    SAFE_DIVIDE(cost, conversions) AS cpa,
    SAFE_DIVIDE(conversion_value, cost) AS roas
  FROM `ad_data.google_ads`
),

tiktok_normalized AS (
  SELECT
    date,
    campaign_id,
    campaign_name,
    adgroup_id AS subgroup_id,
    adgroup_name AS subgroup_name,
    'TikTok' AS platform,
    impressions,
    clicks,
    cost,
    conversions,
    NULL AS reach,
    NULL AS frequency,
    video_views,
    NULL AS engagement_rate,
    NULL AS conversion_value,
    NULL AS quality_score,
    likes,
    shares,
    comments,
    SAFE_DIVIDE(clicks, impressions) AS ctr,
    SAFE_DIVIDE(cost, clicks) AS cpc,
    SAFE_DIVIDE(cost, impressions) * 1000 AS cpm,
    SAFE_DIVIDE(cost, conversions) AS cpa,
    NULL AS roas
  FROM `ad_data.tiktok_ads`
)

SELECT * FROM facebook_normalized
UNION ALL
SELECT * FROM google_normalized
UNION ALL
SELECT * FROM tiktok_normalized;
