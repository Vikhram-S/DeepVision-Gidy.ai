import streamlit as st
from deepventure_backend import DeepVentureBackend  # Assuming this is a custom backend
import time
import random
import pandas as pd
import plotly.express as px
from typing import List
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image as PILImage, ImageDraw, ImageFont
import io
import uuid

# Hardcoded credentials for demonstration
VALID_CREDENTIALS = {
    "admin":"adminpassword",
    "user1": "password1",
    "user2": "password2",
}

# Initialize backend with Hugging Face API token
HF_API_TOKEN = "hugging_face"  # Replace with your actual token securely
backend = DeepVentureBackend(HF_API_TOKEN)

# Set page configuration for a modern dashboard
st.set_page_config(
    page_title="DeepVenture Hub - Microlearning Mastery",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🚀"
)

# Cache microlearning data
@st.cache_data
def fetch_microlearning(category: str) -> List[str]:
    return backend.get_microlearning(category.lower())

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_data = {
        "progress": {},
        "quiz_history": [],
        "badges": [],
        "leaderboard": {},
        "last_activity": time.time(),
        "certificate_name": ""
    }

# Quiz question pool
QUIZ_QUESTIONS = {
    "business": [
        {"question": "What is a business plan?", "options": ["A document outlining goals and strategies", "A financial statement", "A marketing campaign"], "correct_answer": "A document outlining goals and strategies"},
        {"question": "What does ROI stand for?", "options": ["Return on Investment", "Revenue of Income", "Rate of Interest"], "correct_answer": "Return on Investment"},
    ],
    "marketing": [
        {"question": "What is market segmentation?", "options": ["Dividing a market into distinct groups", "Increasing market share", "Reducing competition"], "correct_answer": "Dividing a market into distinct groups"},
        {"question": "What is a target audience?", "options": ["The primary group of potential customers", "All possible customers", "Competitors' customers"], "correct_answer": "The primary group of potential customers"},
    ],
    "finance": [
        {"question": "What is equity?", "options": ["Ownership interest in a company", "Debt owed by a company", "Annual revenue"], "correct_answer": "Ownership interest in a company"},
        {"question": "What is a balance sheet?", "options": ["A statement of assets and liabilities", "A profit report", "A sales forecast"], "correct_answer": "A statement of assets and liabilities"},
    ],
}

# Advanced UI/UX with custom CSS
st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: #e2e8f0;
    font-family: 'Arial', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}
h1, h2, h3 {
    color: #a78bfa !important;
    font-weight: 700;
}
.stButton > button {
    background: linear-gradient(90deg, #9333ea, #c084fc);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 20px;
    font-size: 16px;
    font-weight: 600;
    transition: transform 0.2s;
}
.stButton > button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #c084fc, #9333ea);
}
.stTextInput > div > div > input {
    background-color: #1e293b;
    color: #e2e8f0;
    border: 1px solid #4b5563;
    border-radius: 8px;
    padding: 8px;
    font-size: 16px;
}
.stSelectbox > div > div {
    background-color: #1e293b;
    color: #e2e8f0;
    border-radius: 8px;
}
.sidebar .sidebar-content {
    background-color: #1e293b;
    border-right: 1px solid #4b5563;
}
.stExpander {
    background-color: #1e293b;
    border-radius: 8px;
    border: 1px solid #4b5563;
}
.stExpander summary {
    color: #a78bfa;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# Login page
def login():
    st.title("DeepVenture Hub 🚀")
    st.markdown("<p style='color: #94a3b8;'>Master Skills with AI-Driven Learning</p>", unsafe_allow_html=True)
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login", key="login_button"):
                if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_data["certificate_name"] = username
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")

# Certificate generation function
def generate_certificate(name: str, category: str) -> tuple:
    credential_id = str(uuid.uuid4())[:8].upper()
    date = datetime.now().strftime('%Y-%m-%d')
    
    # PDF Certificate
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    styles['Title'].textColor = colors.purple  # Changed from darkpurple to purple
    styles['BodyText'].fontSize = 14
    story = [
        Paragraph("Certificate of Completion", styles['Title']),
        Spacer(1, 36),
        Paragraph(f"Awarded to: {name}", styles['BodyText']),
        Paragraph(f"For successfully completing the {category.capitalize()} Microlearning Module", styles['BodyText']),
        Paragraph(f"Date: {date}", styles['BodyText']),
        Paragraph(f"Credential ID: {credential_id}", styles['BodyText']),
        Spacer(1, 24),
        Paragraph("Provided by DeepVision", styles['BodyText']),
    ]
    doc.build(story)
    pdf_data = pdf_buffer.getvalue()
    pdf_buffer.close()

    # PNG Certificate
    png_width, png_height = 800, 600
    png_image = PILImage.new('RGB', (png_width, png_height), color='#ffffff')
    draw = ImageDraw.Draw(png_image)
    try:
        title_font = ImageFont.truetype("arial.ttf", 40)
        text_font = ImageFont.truetype("arial.ttf", 20)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    draw.text((50, 50), "Certificate of Completion", fill='#800080', font=title_font)  # Using hex code for purple
    draw.text((50, 150), f"Awarded to: {name}", fill='black', font=text_font)
    draw.text((50, 200), f"For: {category.capitalize()} Module", fill='black', font=text_font)
    draw.text((50, 250), f"Date: {date}", fill='black', font=text_font)
    draw.text((50, 300), f"Credential ID: {credential_id}", fill='black', font=text_font)
    draw.text((50, 400), "Provided by DeepVision", fill='#800080', font=text_font)
    
    png_buffer = io.BytesIO()
    png_image.save(png_buffer, format="PNG")
    png_data = png_buffer.getvalue()
    png_buffer.close()
    
    return pdf_data, png_data, credential_id

# Main application
if not st.session_state.logged_in:
    login()
else:
    # Sidebar
    with st.sidebar:
        st.markdown(f"👋 Hello, **{st.session_state.username}**!")
        if st.button("Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_data = {"progress": {}, "quiz_history": [], "badges": [], "leaderboard": {}, "last_activity": time.time(), "certificate_name": ""}
            st.rerun()
        
        st.subheader("⚙️ Settings")
        certificate_name = st.text_input("Certificate Name", value=st.session_state.user_data["certificate_name"], key="cert_name")
        if certificate_name.strip():
            st.session_state.user_data["certificate_name"] = certificate_name.strip()
        
        category_options = ["business", "marketing", "finance", "custom"]
        selected_category = st.selectbox("Learning Path", options=category_options, key="category_select")
        custom_input = st.text_input("Custom Idea", disabled=selected_category != "custom", key="custom_input")
        st.button("Refresh Modules", key="refresh_btn")

    # Main content
    st.title("DeepVenture Microlearning Hub")
    st.markdown("### Elevate Your Skills with Smart, Interactive Modules")

    col1, col2 = st.columns([3, 2])
    with col1:
        category = custom_input if selected_category == "custom" and custom_input.strip() else selected_category
        if category.strip():
            if "last_category" not in st.session_state or st.session_state.last_category != category:
                with st.spinner("Loading modules..."):
                    modules = fetch_microlearning(category)
                    if not modules:
                        modules = ["No modules available. Try another category."]
                    st.session_state.user_data["progress"][category] = {
                        "modules": modules,
                        "completed": {},
                        "total_modules": len(modules),
                        "last_accessed": time.time()
                    }
                    st.session_state.last_category = category
            
            st.subheader("📚 Modules")
            for i, module in enumerate(st.session_state.user_data["progress"][category]["modules"], 1):
                with st.expander(f"Module {i}: {module[:30]}..."):
                    st.markdown(module)
                    if st.button(f"Mark Complete", key=f"complete_{i}_{category}"):
                        st.session_state.user_data["progress"][category]["completed"][f"module_{i}"] = time.time()
                        if len(st.session_state.user_data["progress"][category]["completed"]) == st.session_state.user_data["progress"][category]["total_modules"]:
                            badge = f"{category.capitalize()} Master - {datetime.now().strftime('%Y-%m-%d')}"
                            if badge not in st.session_state.user_data["badges"]:
                                st.session_state.user_data["badges"].append(badge)
                        st.rerun()

            # Progress
            progress = st.session_state.user_data["progress"][category]
            st.subheader("📊 Progress")
            st.metric("Completion", f"{len(progress['completed'])}/{progress['total_modules']}")
            if progress["completed"]:
                fig = px.bar(x=[f"Module {i+1}" for i in range(progress['total_modules'])], 
                            y=[1 if f"module_{i+1}" in progress['completed'] else 0 for i in range(progress['total_modules'])],
                            color=["Completed" if f"module_{i+1}" in progress['completed'] else "Pending" for i in range(progress['total_modules'])])
                st.plotly_chart(fig, use_container_width=True)

            # Quiz
            if category in QUIZ_QUESTIONS:
                with st.expander("🎯 Quiz"):
                    quiz = random.choice(QUIZ_QUESTIONS[category])
                    st.write(quiz["question"])
                    answer = st.radio("Options", quiz["options"], key=f"quiz_{category}")
                    if st.button("Submit", key=f"quiz_submit_{category}"):
                        is_correct = answer == quiz["correct_answer"]
                        st.session_state.user_data["quiz_history"].append({"category": category, "correct": is_correct})
                        if is_correct:
                            st.session_state.user_data["leaderboard"][st.session_state.username] = st.session_state.user_data["leaderboard"].get(st.session_state.username, 0) + 100
                        st.success(f"{'Correct!' if is_correct else 'Incorrect.'} Answer: {quiz['correct_answer']}")
                        st.rerun()

    with col2:
        st.subheader("🏆 Achievements")
        for badge in st.session_state.user_data["badges"]:
            st.markdown(f"🎖️ **{badge}**")
        
        if category in st.session_state.user_data["progress"] and len(st.session_state.user_data["progress"][category]["completed"]) >= st.session_state.user_data["progress"][category]["total_modules"]:
            pdf_data, png_data, credential_id = generate_certificate(st.session_state.user_data["certificate_name"], category)
            st.success(f"🎉 Course Completed! Credential ID: {credential_id}")
            st.download_button("Download PDF Certificate", pdf_data, f"certificate_{category}_{credential_id}.pdf", "application/pdf")
            st.download_button("Download PNG Certificate", png_data, f"certificate_{category}_{credential_id}.png", "image/png")

        st.subheader("🏅 Leaderboard")
        leaderboard_df = pd.DataFrame([(st.session_state.username, st.session_state.user_data["leaderboard"].get(st.session_state.username, 0))], columns=["User", "Score"])
        st.plotly_chart(px.bar(leaderboard_df, x="User", y="Score", color="Score", color_continuous_scale="Viridis"), use_container_width=True)

    st.markdown("---")
    st.caption("Powered by DeepVision | © 2025 Vikhram S Team DeepVision")
