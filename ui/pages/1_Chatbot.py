import streamlit as st
import requests
from ui.components.cards import render_insight_card

st.set_page_config(page_title="Chatbot | Pharma Intel", page_icon="🤖", layout="wide")

# Custom CSS for Gemini-like aesthetics
st.markdown("""
<style>
    .stApp {
        background-color: #131314;
        color: #e3e3e3;
    }
    .user-msg {
        background-color: #2b2c2f;
        padding: 15px;
        border-radius: 20px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Hardcoded backend connection
backend_url = "http://localhost:8000"
st.session_state["backend_url"] = backend_url

st.title("Pharma AI Chatbot 🤖")
st.markdown("Ask about drug launches, clinical trials, or competitor movements.")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
        else:
            render_insight_card(message["content"])

# Chat Input
if prompt := st.chat_input("Ask a pharma question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing market data..."):
            try:
                resp = requests.post(f"{backend_url}/query/", json={"query": prompt})
                if resp.status_code == 200:
                    insight = resp.json()["insight"]
                else:
                    insight = f"Error from backend: {resp.text}"
                
                render_insight_card(insight)
                st.session_state.messages.append({"role": "assistant", "content": insight})
            except Exception as e:
                st.error(f"Connection Failed: {e}")

if st.button("Back to Dashboard"):
    st.switch_page("app.py")
