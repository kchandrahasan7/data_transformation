import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Ad Performance Dashboard", layout="wide")

df = pd.read_csv('unified_ads.csv')
df['date'] = pd.to_datetime(df['date'])

st.title("Cross-Platform Ad Performance")

with st.sidebar:
    st.header("Filters")
    date_range = st.date_input(
        "Date Range",
        value=(df['date'].min(), df['date'].max()),
        min_value=df['date'].min(),
        max_value=df['date'].max()
    )
    
    platforms = st.multiselect(
        "Platform",
        options=df['platform'].unique(),
        default=df['platform'].unique()
    )
    
    campaigns = st.multiselect(
        "Campaign",
        options=sorted(df['campaign_name'].unique()),
        default=df['campaign_name'].unique()
    )

filtered_df = df[
    (df['date'] >= pd.to_datetime(date_range[0])) &
    (df['date'] <= pd.to_datetime(date_range[1])) &
    (df['platform'].isin(platforms)) &
    (df['campaign_name'].isin(campaigns))
]

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Spend", f"${filtered_df['cost'].sum():,.2f}")

with col2:
    st.metric("Conversions", f"{filtered_df['conversions'].sum():,}")

with col3:
    avg_cpa = filtered_df['cost'].sum() / filtered_df['conversions'].sum()
    st.metric("Avg CPA", f"${avg_cpa:.2f}")

with col4:
    overall_ctr = filtered_df['clicks'].sum() / filtered_df['impressions'].sum() * 100
    st.metric("CTR", f"{overall_ctr:.2f}%")

with col5:
    roas = filtered_df['conversion_value'].sum() / filtered_df['cost'].sum()
    st.metric("ROAS", f"{roas:.2f}x" if not pd.isna(roas) else "N/A")

st.divider()

col1, col2 = st.columns(2)

with col1:
    platform_spend = filtered_df.groupby('platform')['cost'].sum().reset_index()
    fig = px.pie(platform_spend, values='cost', names='platform', title='Spend by Platform')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    daily_metrics = filtered_df.groupby(['date', 'platform']).agg({
        'cost': 'sum',
        'conversions': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    for platform in daily_metrics['platform'].unique():
        platform_data = daily_metrics[daily_metrics['platform'] == platform]
        fig.add_trace(go.Scatter(
            x=platform_data['date'],
            y=platform_data['cost'],
            name=platform,
            mode='lines'
        ))
    
    fig.update_layout(title='Daily Spend Trend', xaxis_title='Date', yaxis_title='Spend')
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Platform Performance")

platform_metrics = filtered_df.groupby('platform').agg({
    'cost': 'sum',
    'impressions': 'sum',
    'clicks': 'sum',
    'conversions': 'sum'
}).reset_index()

platform_metrics['CTR'] = (platform_metrics['clicks'] / platform_metrics['impressions'] * 100).round(2)
platform_metrics['CPC'] = (platform_metrics['cost'] / platform_metrics['clicks']).round(2)
platform_metrics['CPA'] = (platform_metrics['cost'] / platform_metrics['conversions']).round(2)

platform_metrics.columns = ['Platform', 'Spend', 'Impressions', 'Clicks', 'Conversions', 'CTR %', 'CPC', 'CPA']
st.dataframe(platform_metrics, use_container_width=True, hide_index=True)

st.subheader("Top Campaigns by Conversions")

campaign_performance = filtered_df.groupby('campaign_name').agg({
    'conversions': 'sum',
    'cost': 'sum',
    'platform': 'first'
}).reset_index().sort_values('conversions', ascending=False).head(10)

fig = px.bar(
    campaign_performance,
    x='conversions',
    y='campaign_name',
    color='platform',
    orientation='h',
    title='Top 10 Campaigns'
)
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig, use_container_width=True)
