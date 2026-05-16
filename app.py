import streamlit as st
from dotenv import load_dotenv
import time

from core.analyzer import analyze_content
from ui.components import load_css, render_header, render_score_card, render_tactics, render_reasoning

# Load environment variables (like GEMINI_API_KEY)
load_dotenv()

# Configure page
st.set_page_config(
    page_title="LieLens | Forensic Engine",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load styling
load_css()

# Header
render_header()

# Layout: Split into input (left) and results (right)
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("<div style='margin-bottom: 20px;' class='score-label'>TARGET ACQUISITION</div>", unsafe_allow_html=True)
    
    # We use a form to prevent auto-reruns on every keystroke
    with st.form("analysis_form", clear_on_submit=False):
        content_input = st.text_area(
            label="Paste internet content here",
            value="I made $100k with this AI tool in 2 days! Click here to buy my course before the timer runs out!",
            height=300,
            label_visibility="collapsed"
        )
        
        submitted = st.form_submit_button("ANALYZE CONTENT")

with col2:
    if submitted:
        if not content_input.strip():
            st.error("NO CONTENT DETECTED.")
        else:
            with st.spinner("ANALYZING TARGET..."):
                try:
                    # Simulate processing time for "terminal" feel
                    time.sleep(0.5)
                    
                    result = analyze_content(content_input)
                    
                    # Dashboard Layout
                    st.markdown("<div style='margin-bottom: 20px;' class='score-label'>FORENSIC REPORT</div>", unsafe_allow_html=True)
                    
                    # Top Row: Scores
                    score_col1, score_col2 = st.columns(2)
                    with score_col1:
                        # Color logic based on credibility
                        color = "#00ffcc" if result.credibility_score > 70 else ("#ffcc00" if result.credibility_score > 40 else "#ff3300")
                        render_score_card("CREDIBILITY", result.credibility_score, color)
                    with score_col2:
                        color = "#ff3300" if result.manipulation_score > 60 else ("#ffcc00" if result.manipulation_score > 30 else "#00ffcc")
                        render_score_card("MANIPULATION", result.manipulation_score, color)
                    
                    # Tactics
                    st.markdown("<br>", unsafe_allow_html=True)
                    render_tactics(result.tactics_detected)
                    
                    # Reasoning
                    st.markdown("<br>", unsafe_allow_html=True)
                    render_reasoning(result.reasoning)
                    
                    # Metadata
                    meta_html = f"""
                    <div style='margin-top: 20px; color: #555; font-family: "Space Grotesk", monospace; font-size: 0.8rem;'>
                        RISK CLASSIFICATION: {result.risk_classification} | AI GENERATED PROBABILITY: {result.ai_generated_probability}%
                    </div>
                    """
                    st.markdown(meta_html, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"SYSTEM FAILURE: {e}")
    else:
        st.markdown("""
        <div class="brutalist-card" style="text-align: center; color: #555; border-color: #333333; box-shadow: none;">
            AWAITING TARGET INPUT...
        </div>
        """, unsafe_allow_html=True)
