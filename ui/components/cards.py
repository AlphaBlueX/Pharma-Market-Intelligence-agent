import streamlit as st

def render_insight_card(insight_text: str):
    """
    Renders a beautified insight card using a container with custom CSS.
    """
    with st.container(border=True):
        st.markdown(f"""
        <style>
            .st-emotion-cache-12w0qpk {{
                border-left: 5px solid #4285f4 !important;
                background-color: #1e1f20 !important;
            }}
        </style>
        """, unsafe_allow_html=True)
        st.markdown(insight_text)

def render_alert_card(alert: dict):
    """
    Renders a brief alert card.
    """
    severity_colors = {
        "High": "#ff4b4b",
        "Medium": "#ffa500",
        "Low": "#00cc96"
    }
    color = severity_colors.get(alert["severity"], "#ffffff")
    
    with st.container():
        st.markdown(f"""
        <div style="border: 1px solid #444; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
            <span style="background-color: {color}; padding: 2px 6px; border-radius: 3px; font-size: 0.8em; font-weight: bold; color: white;">
                {alert['severity']}
            </span>
            <div style="font-weight: bold; margin-top: 5px;">{alert['title']}</div>
            <div style="font-size: 0.9em; color: #aaa;">{alert['text']}</div>
        </div>
        """, unsafe_allow_html=True)
