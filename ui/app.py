import streamlit as st
import requests

st.set_page_config(
    page_title="Pharma Market Intelligence Suite",
    page_icon="💊",
    layout="wide"
)

# Custom CSS for Hero Section
st.markdown("""
<style>
    .hero-container {
        padding: 60px 0;
        text-align: center;
        background: linear-gradient(135deg, #131314 0%, #1e1f20 100%);
        border-radius: 20px;
        margin-bottom: 40px;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4285f4, #34a853, #fbbc05, #ea4335);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
    }
    .hero-subtitle {
        font-size: 1.5rem;
        color: #e3e3e3;
        margin-bottom: 40px;
    }
    .about-us {
        background-color: #1e1f20;
        padding: 40px;
        border-radius: 20px;
        margin-top: 60px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.title("Pharma Agent 💊")
    st.markdown("---")
    # Backend URL is now hardcoded for seamless experience
    backend_url = "http://localhost:8000"
    st.session_state["backend_url"] = backend_url
    
    st.info("Directly connected to local backend at :8000")

# Hero Section
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">Pharma Market Intelligence Agent</h1>
    <p class="hero-subtitle">Your Strategic AI Partner for Real-Time Pharmaceutical Insights</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🤖 AI Reasoning")
    st.write("Powered by Qwen2.5-1.5B-Instruct, our agent provides deep-dive analysis grounded in pharmaceutical data.")
    if st.button("Open Chatbot UI", type="primary", use_container_width=True):
        st.switch_page("pages/1_Chatbot.py")

with col2:
    st.subheader("🚨 Real-Time Alerts")
    st.write("Monitor FDA priority reviews, clinical trial updates, and competitive market shifts as they happen.")
    if st.button("View Market Alerts", use_container_width=True):
        st.switch_page("pages/2_Alerts.py")

with col3:
    st.subheader("📊 Sentiment Analysis")
    st.write("Track brand perception and market sentiment across major pharma players with interactive charts.")
    if st.button("Explore Trends", use_container_width=True):
        st.switch_page("pages/3_Trends.py")

st.markdown("---")

# About Us Section
st.markdown("""
<div class="about-us">
    <h2>About Pharma Intel Agent</h2>
    <p>The Pharma Market Intelligence Agent is a production-grade RAG (Retrieval-Augmented Generation) system designed specifically for the pharmaceutical industry. 
    It combines web-scraped market intelligence with local LLM reasoning to provide actionable strategic advice.</p>
    <p><b>Key Features:</b></p>
    <ul>
        <li><b>Domain Discipline:</b> Hard-coded restriction to pharmaceutical topics.</li>
        <li><b>Long-Term Memory:</b> FAISS vector store with smart data retention/summarization.</li>
        <li><b>Always-On Monitoring:</b> Automated ingestion pipeline via n8n.</li>
    </ul>
    <p style="color: #888;">Built for the Future of Pharma Intelligence.</p>
</div>
""", unsafe_allow_html=True)
