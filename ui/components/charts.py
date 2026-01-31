import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def render_sentiment_chart():
    """
    Renders a dummy sentiment trend chart using Plotly.
    """
    dates = pd.date_range(start="2026-01-01", periods=10)
    brands = ["Pfizer", "Roche", "Novartis", "Merck"]
    
    data = []
    for brand in brands:
        sentiment_scores = np.random.uniform(0.1, 0.9, size=10)
        for d, s in zip(dates, sentiment_scores):
            data.append({"Date": d, "Brand": brand, "Sentiment Score": s})
            
    df = pd.DataFrame(data)
    
    fig = px.line(df, x="Date", y="Sentiment Score", color="Brand", 
                  title="Brand Sentiment Over Time",
                  template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
