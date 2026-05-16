import streamlit as st
import os

def load_css():
    """Loads the custom Cyber Brutalism CSS."""
    css_path = os.path.join(os.path.dirname(__file__), "styles.css")
    try:
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Failed to load CSS: {e}")

def render_header():
    st.markdown("<h1>LIELENS</h1>", unsafe_allow_html=True)
    st.markdown("<h2>DIGITAL FORENSIC ENGINE</h2>", unsafe_allow_html=True)

def render_score_card(label: str, score: int, color_hex: str = "#ff3300"):
    """Renders a brutalist score card."""
    html = f"""
    <div class="score-card" style="border-color: {color_hex}; box-shadow: 8px 8px 0px {color_hex};">
        <div class="score-value" style="color: {color_hex};">{score}%</div>
        <div class="score-label">{label}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_tactics(tactics: list[str]):
    """Renders detected manipulation tactics as chips."""
    chips_html = "".join([f'<span class="tactic-chip">{tactic}</span>' for tactic in tactics])
    
    html = f"""
    <div class="brutalist-card">
        <div class="score-label" style="margin-bottom: 15px; color: #00ffcc;">DETECTED TACTICS</div>
        <div>{chips_html if chips_html else '<span style="color:#555;">NONE DETECTED</span>'}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_reasoning(reasoning: str):
    """Renders the AI's reasoning block."""
    html = f"""
    <div class="brutalist-card" style="border-color: #00ffcc; box-shadow: 6px 6px 0px #00ffcc;">
        <div class="score-label" style="margin-bottom: 15px; color: #00ffcc;">REASONING ENGINE OUTPUT</div>
        <div class="reasoning-block">
            {reasoning}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
