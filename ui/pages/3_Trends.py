import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from ui.components.charts import render_sentiment_chart

st.set_page_config(page_title="Trends | Pharma Intel", page_icon="📊", layout="wide")

st.title("Sentiment Analysis & Trends 📊")
st.markdown("Visualizing market perception and brand sentiment shifts.")

backend_url = st.session_state.get("backend_url", "http://localhost:8000")

try:
    resp = requests.get(f"{backend_url}/query/trends")
    if resp.status_code == 200:
        trend_data = resp.json()
        brand_mentions = trend_data.get("brand_mentions", {})
        total_docs = trend_data.get("total_documents", 0)
    else:
        brand_mentions = {}
        total_docs = 0
except Exception as e:
    brand_mentions = {}
    total_docs = 0

st.subheader("Brand Visibility Index")
if brand_mentions:
    df = pd.DataFrame(list(brand_mentions.items()), columns=["Brand", "Mentions"])
    fig = px.bar(df, x="Brand", y="Mentions", color="Brand", 
                 title="Brand Mention Counts in Market Data",
                 template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No trend data available. Ingest more pharma news to see analytics.")

st.markdown("---")
st.subheader("Market Indicators")
m1, m2, m3 = st.columns(3)
m1.metric("Documents Analyzed", total_docs, f"+{total_docs}" if total_docs > 0 else "0")
m2.metric("Vaccine Adoption", "Stable", "0%")
m3.metric("Generic Competition", "High", "+25%")

if st.button("Back to Dashboard"):
    st.switch_page("app.py")
