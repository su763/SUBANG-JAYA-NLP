import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the webpage layout
st.set_page_config(page_title="Cafe NLP Dashboard", layout="wide")
st.title("☕ Cafe Review Intelligence Dashboard")
st.markdown("An NLP pipeline analyzing customer sentiment across core business aspects.")

# 1. Load the data
@st.cache_data # This caches the data so the app runs super fast
def load_data():
    df = pd.read_csv('data/yelp_analyzed.csv')
    return df

df = load_data()

# 2. Sidebar Filters
st.sidebar.header("Filter Results")
# Create a dropdown to filter by Sentiment
sentiment_filter = st.sidebar.multiselect(
    "Select Sentiment:",
    options=df["Sentiment"].unique(),
    default=df["Sentiment"].unique()
)

# Apply the filter to the dataset
filtered_df = df[df["Sentiment"].isin(sentiment_filter)]

# 3. Top Level Metrics (The quick summary)
col1, col2, col3 = st.columns(3)
col1.metric("Total Reviews Analyzed", len(filtered_df))
col2.metric("Positive Reviews", len(filtered_df[filtered_df['Sentiment'] == 'POSITIVE']))
col3.metric("Negative Reviews", len(filtered_df[filtered_df['Sentiment'] == 'NEGATIVE']))

st.divider()

# 4. Charts and Visuals
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Sentiment Distribution")
    # A simple pie chart showing Positive vs Negative
    fig_pie = px.pie(filtered_df, names='Sentiment', hole=0.4, color='Sentiment',
                     color_discrete_map={'POSITIVE':'#00cc96', 'NEGATIVE':'#ef553b'})
    st.plotly_chart(fig_pie, use_container_width=True)

with col_chart2:
    st.subheader("What are people talking about?")
    # Count how many times each aspect was mentioned
    aspect_counts = filtered_df['Aspects_Mentioned'].str.split(', ').explode().value_counts().reset_index()
    aspect_counts.columns = ['Aspect', 'Count']
    
    fig_bar = px.bar(aspect_counts, x='Aspect', y='Count', color='Aspect')
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# 5. The Raw Data Explorer
st.subheader("Raw Review Explorer")
st.dataframe(filtered_df, use_container_width=True)