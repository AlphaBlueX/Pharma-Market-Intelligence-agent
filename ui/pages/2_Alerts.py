import streamlit as st
import requests
from ui.components.cards import render_alert_card

st.set_page_config(page_title="Alerts | Pharma Intel", page_icon="🚨", layout="wide")

st.title("Market Alerts 🚨")
st.markdown("Real-time monitoring of pharmaceutical market events.")

backend_url = st.session_state.get("backend_url", "http://localhost:8000")

try:
    resp = requests.get(f"{backend_url}/query/alerts")
    if resp.status_code == 200:
        alerts = resp.json()
    else:
        st.error("Failed to fetch alerts from backend.")
        alerts = []
except Exception as e:
    # st.error(f"Error connecting to backend: {e}")
    alerts = []

if not alerts:
    st.info("No active alerts. Ingest fresh data to see real-time updates.")
    # Fallback to a few helpful tips if no alerts
    alerts = [
        {"title": "System Active", "severity": "Low", "text": "The Pharma Intel Agent is monitoring for new market signals."},
    ]

col1, col2 = st.columns(2)
for i, alert in enumerate(alerts):
    with (col1 if i % 2 == 0 else col2):
        render_alert_card(alert)

if st.button("Back to Dashboard"):
    st.switch_page("app.py")
