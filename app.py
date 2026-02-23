import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Global Cybersecurity Threats Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load data
@st.cache_data
def load_data():
    try:
        data_path = Path(__file__).parent / "data_sets" / "Global_Cybersecurity_Threats_2015-2024.csv"
        df = pd.read_csv(data_path)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")
st.sidebar.markdown("---")

years = sorted(df["Year"].unique())
selected_years = st.sidebar.multiselect("Year", years, default=years)

countries = sorted(df["Country"].unique())
selected_countries = st.sidebar.multiselect("Country", countries, default=countries)

attack_types = sorted(df["Attack Type"].unique())
selected_attack_types = st.sidebar.multiselect("Attack Type", attack_types, default=attack_types)

industries = sorted(df["Target Industry"].unique())
selected_industries = st.sidebar.multiselect("Target Industry", industries, default=industries)

attack_sources = sorted(df["Attack Source"].unique())
selected_sources = st.sidebar.multiselect("Attack Source", attack_sources, default=attack_sources)

# Apply filters
filtered_df = df[
    (df["Year"].isin(selected_years))
    & (df["Country"].isin(selected_countries))
    & (df["Attack Type"].isin(selected_attack_types))
    & (df["Target Industry"].isin(selected_industries))
    & (df["Attack Source"].isin(selected_sources))
]

# Header
st.title("🛡️ Global Cybersecurity Threats Dashboard")
st.markdown("Analysis of cybersecurity incidents (2015–2024)")
st.markdown("---")

# KPI cards
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Total Incidents",
        value=f"{len(filtered_df):,}",
    )

with col2:
    total_loss = filtered_df["Financial Loss (in Million $)"].sum()
    st.metric(
        label="Financial Loss (Million $)",
        value=f"{total_loss:,.0f}",
    )

with col3:
    total_users = filtered_df["Number of Affected Users"].sum()
    st.metric(
        label="Affected Users",
        value=f"{total_users/1e6:.1f}M",
    )

with col4:
    avg_resolution = filtered_df["Incident Resolution Time (in Hours)"].mean()
    st.metric(
        label="Avg Resolution (Hours)",
        value=f"{avg_resolution:.0f}",
    )

with col5:
    st.metric(
        label="Countries Affected",
        value=filtered_df["Country"].nunique(),
    )

st.markdown("---")

# Row 1: Attack types and target industries
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    attack_counts = filtered_df["Attack Type"].value_counts().reset_index()
    attack_counts.columns = ["Attack Type", "Count"]
    fig_attack = px.bar(
        attack_counts,
        x="Attack Type",
        y="Count",
        title="Attacks by Type",
        color="Count",
        color_continuous_scale="Reds",
    )
    fig_attack.update_layout(showlegend=False, margin=dict(t=40))
    st.plotly_chart(fig_attack, use_container_width=True)

with row1_col2:
    industry_counts = filtered_df["Target Industry"].value_counts().reset_index()
    industry_counts.columns = ["Target Industry", "Count"]
    fig_industry = px.bar(
        industry_counts,
        x="Target Industry",
        y="Count",
        title="Target Industries",
        color="Count",
        color_continuous_scale="Blues",
    )
    fig_industry.update_layout(showlegend=False, margin=dict(t=40))
    st.plotly_chart(fig_industry, use_container_width=True)

# Row 2: Trends over time and attack source
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    yearly = filtered_df.groupby("Year").agg(
        Incidents=("Country", "count"),
        Financial_Loss=("Financial Loss (in Million $)", "sum"),
        Affected_Users=("Number of Affected Users", "sum"),
    ).reset_index()
    fig_trend = px.line(
        yearly,
        x="Year",
        y="Incidents",
        title="Incidents Over Time",
        markers=True,
    )
    fig_trend.update_layout(margin=dict(t=40))
    st.plotly_chart(fig_trend, use_container_width=True)

with row2_col2:
    source_counts = filtered_df["Attack Source"].value_counts().reset_index()
    source_counts.columns = ["Attack Source", "Count"]
    fig_source = px.pie(
        source_counts,
        names="Attack Source",
        values="Count",
        title="Attack Source Distribution",
        hole=0.4,
    )
    fig_source.update_layout(margin=dict(t=40))
    st.plotly_chart(fig_source, use_container_width=True)

# Row 3: Financial loss by country and vulnerability types
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    country_loss = (
        filtered_df.groupby("Country")["Financial Loss (in Million $)"]
        .sum()
        .sort_values(ascending=True)
        .tail(15)
    )
    fig_country = px.bar(
        x=country_loss.values,
        y=country_loss.index,
        orientation="h",
        title="Top 15 Countries by Financial Loss (Million $)",
        labels={"x": "Financial Loss (Million $)", "y": "Country"},
    )
    fig_country.update_layout(margin=dict(t=40))
    st.plotly_chart(fig_country, use_container_width=True)

with row3_col2:
    vuln_counts = filtered_df["Security Vulnerability Type"].value_counts().reset_index()
    vuln_counts.columns = ["Vulnerability", "Count"]
    fig_vuln = px.bar(
        vuln_counts,
        x="Vulnerability",
        y="Count",
        title="Security Vulnerability Types",
        color="Count",
        color_continuous_scale="Oranges",
    )
    fig_vuln.update_layout(showlegend=False, margin=dict(t=40))
    st.plotly_chart(fig_vuln, use_container_width=True)

# Row 4: Defense mechanisms and resolution time distribution
row4_col1, row4_col2 = st.columns(2)

with row4_col1:
    defense_counts = filtered_df["Defense Mechanism Used"].value_counts().reset_index()
    defense_counts.columns = ["Defense Mechanism", "Count"]
    fig_defense = px.bar(
        defense_counts,
        x="Defense Mechanism",
        y="Count",
        title="Defense Mechanisms Used",
        color="Count",
        color_continuous_scale="Greens",
    )
    fig_defense.update_layout(showlegend=False, margin=dict(t=40))
    st.plotly_chart(fig_defense, use_container_width=True)

with row4_col2:
    fig_resolution = px.histogram(
        filtered_df,
        x="Incident Resolution Time (in Hours)",
        nbins=30,
        title="Incident Resolution Time Distribution (Hours)",
    )
    fig_resolution.update_layout(margin=dict(t=40))
    st.plotly_chart(fig_resolution, use_container_width=True)

# Data table
st.markdown("---")
st.subheader("📊 Data Explorer")
st.caption("Filtered dataset. Use sidebar to refine.")
st.dataframe(filtered_df, use_container_width=True, height=400)
