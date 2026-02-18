# Cross-Platform Advertising Analytics

A data pipeline and dashboard for unified analysis of advertising performance across Facebook, Google Ads, and TikTok.

## Overview

This project demonstrates end-to-end data integration from multiple advertising platforms into a single analytical framework. Raw campaign data is transformed into a unified schema, enabling cross-platform performance comparison and analysis.

## Live Dashboard

Access the interactive dashboard here: [https://datatransformation-ahwfvvqy3fqjjgjt7qkwdm.streamlit.app/](https://datatransformation-ahwfvvqy3fqjjgjt7qkwdm.streamlit.app/)

## Architecture

**Data Layer**
- Google BigQuery for data warehousing
- Three source tables (Facebook Ads, Google Ads, TikTok Ads)
- One unified table with standardized schema

**Visualization Layer**
- Streamlit for interactive dashboard
- Plotly for charts and visualizations

## Data Transformation

The SQL transformation script handles:

- Schema normalization across platforms
- Standardization of metric names (spend vs cost)
- Calculation of derived metrics (CTR, CPC, CPM, CPA, ROAS)
- Platform identification and tagging
- Union of all data sources

Key transformations include:
- Facebook: `spend` → `cost`
- Google Ads: Preservation of `conversion_value` for ROAS calculation
- TikTok: Social engagement metrics (likes, shares, comments)

## Dashboard Features

**Key Metrics**
- Total spend across all platforms
- Total conversions
- Average CPA (Cost Per Acquisition)
- Overall CTR (Click-Through Rate)
- ROAS (Return on Ad Spend)

**Visualizations**
- Spend distribution by platform
- Daily spend trends with platform breakdown
- Platform performance comparison table
- Top 10 campaigns by conversions

**Filters**
- Date range selector
- Platform filter
- Campaign filter

## Technical Stack

- Python 3.x
- Streamlit
- Pandas
- Plotly
- Google BigQuery

## Files

- `dashboard.py` - Streamlit application code
- `data_transformation.sql` - BigQuery SQL script for data unification
- `unified_ads.csv` - Processed dataset
- `requirements.txt` - Python dependencies

## Installation

```bash
pip install -r requirements.txt
streamlit run dashboard.py
```

## Data Schema

The unified table includes:

**Common Fields**
- date, campaign_id, campaign_name, platform
- impressions, clicks, cost, conversions

**Calculated Metrics**
- ctr, cpc, cpm, cpa, roas

**Platform-Specific Fields**
- Facebook: reach, frequency, engagement_rate
- Google Ads: quality_score, conversion_value
- TikTok: likes, shares, comments, video_views

## Use Cases

- Cross-platform advertising budget allocation
- Campaign performance benchmarking
- Platform efficiency analysis
- Conversion trend identification
- ROI optimization
