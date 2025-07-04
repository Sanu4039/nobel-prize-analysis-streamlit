
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import io

# Configuration
st.set_page_config(layout="wide")
st.title("📊 Nobel Prize Data Explorer")
st.markdown("Analyze trends and insights from Nobel Prize history.")

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv('nobel_prize_data.csv')
    df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
    df[['num', 'den']] = df['prize_share'].str.split('/', expand=True)
    df['share_pct'] = pd.to_numeric(df['num']) / pd.to_numeric(df['den'])
    df['winning_age'] = df['year'] - df['birth_date'].dt.year
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filters")
year_range = st.sidebar.slider("Year Range", int(df.year.min()), int(df.year.max()), (1901, 2020))
category_filter = st.sidebar.multiselect("Select Categories", options=df['category'].unique(), default=df['category'].unique())
gender_filter = st.sidebar.multiselect("Select Gender", options=df['sex'].dropna().unique(), default=df['sex'].dropna().unique())

filtered_df = df[
    (df['year'].between(*year_range)) &
    (df['category'].isin(category_filter)) &
    (df['sex'].isin(gender_filter))
]

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📌 Overview", "👥 Gender", "🌍 Geography", "🏛 Institutions", "🎂 Age Analysis"])

# Overview
with tab1:
    st.subheader("Number of Prizes Awarded per Year")
    yearly_counts = filtered_df.groupby('year').count()['prize']
    moving_avg = yearly_counts.rolling(5).mean()

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.scatter(yearly_counts.index, yearly_counts.values, alpha=0.6, color='dodgerblue', label='Prizes')
    ax.plot(moving_avg.index, moving_avg.values, color='crimson', linewidth=2.5, label='5-Year Moving Avg')
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Prizes")
    ax.legend()
    st.pyplot(fig)

# Gender Analysis
with tab2:
    st.subheader("Distribution of Nobel Prizes by Gender")
    gender_counts = filtered_df['sex'].value_counts()
    fig = px.pie(
        names=gender_counts.index,
        values=gender_counts.values,
        title="Male vs Female Nobel Laureates",
        hole=0.4
    )
    st.plotly_chart(fig)

    st.subheader("Gender Distribution by Category")
    cat_split = filtered_df.groupby(['category', 'sex']).size().reset_index(name='count')
    fig = px.bar(cat_split, x="category", y="count", color="sex", barmode='group',
                 title="Number of Prizes per Category by Gender")
    st.plotly_chart(fig)

# Geography
with tab3:
    st.subheader("Top 20 Countries by Number of Nobel Prizes")
    countries = filtered_df.groupby('birth_country_current').size().reset_index(name='prize')
    top20 = countries.sort_values('prize', ascending=False).head(20)
    fig = px.bar(top20, x='prize', y='birth_country_current', orientation='h', color='prize',
                 title='Top 20 Countries')
    st.plotly_chart(fig)

    st.subheader("Animated Global Map of Nobel Prizes Over Time")
    animated_map = filtered_df.groupby(['birth_country_current', 'ISO', 'year']).size().reset_index(name='count')
    fig = px.choropleth(animated_map, locations='ISO', color='count',
                        hover_name='birth_country_current', animation_frame='year',
                        title="Nobel Prizes by Country Over Time", color_continuous_scale='plasma')
    st.plotly_chart(fig)

# Institutions
with tab4:
    st.subheader("Top 20 Institutions")
    org_counts = filtered_df['organization_name'].value_counts().head(20)
    fig = px.bar(x=org_counts.values, y=org_counts.index, orientation='h',
                 title="Top Research Institutions", color=org_counts.values)
    st.plotly_chart(fig)

    st.subheader("Top Cities for Research Institutions")
    city_counts = filtered_df['organization_city'].value_counts().head(20)
    fig = px.bar(x=city_counts.values, y=city_counts.index, orientation='h',
                 title="Top Cities by Organization", color=city_counts.values)
    st.plotly_chart(fig)

# Age Analysis
with tab5:
    st.subheader("Age at Time of Winning")
    desc = filtered_df['winning_age'].describe()
    st.write("Descriptive Stats:")
    st.dataframe(desc)

    st.subheader("Age Distribution Histogram")
    bins = st.slider("Bins", 10, 100, 30)
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(filtered_df['winning_age'].dropna(), bins=bins, ax=ax, color='green')
    ax.set_xlabel("Age")
    ax.set_title("Distribution of Age on Winning")
    st.pyplot(fig)

    st.subheader("Regression: Age vs Year")
    fig = px.scatter(filtered_df, x='year', y='winning_age', color='category',
                     trendline='lowess', opacity=0.5,
                     title="Age at Award Over Years by Category")
    st.plotly_chart(fig)

# Export Section
st.sidebar.header("📥 Download Cleaned Data")
csv = filtered_df.to_csv(index=False)
st.sidebar.download_button(
    label="Download as CSV",
    data=csv,
    file_name='filtered_nobel_data.csv',
    mime='text/csv'
)
