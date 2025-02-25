import streamlit as st
from deepventure_backend import DeepVentureBackend
import time
import random
import pandas as pd
import plotly.express as px
from typing import List, Dict
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image as PILImage, ImageDraw, ImageFont
import io

# Hardcoded credentials for demonstration
VALID_CREDENTIALS = {
    "user1": "password1",
    "user2": "password2",
}

# Initialize backend with Hugging Face API token
HF_API_TOKEN = "hugging_face"  # Replace with your actual token securel
backend = DeepVentureBackend(HF_API_TOKEN)

# Set page configuration for a modern, engaging dashboard
st.set_page_config(
    page_title="DeepVenture Hub - Advanced Microlearning Module",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📚"
)

# Cache microlearning data
@st.cache_data
def fetch_microlearning(category: str) -> List[str]:
    return backend.get_microlearning(category.lower())

# Initialize session state for LMS tracking and login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "progress": {},
        "quiz_history": [],
        "badges": [],
        "leaderboard": {},
        "last_activity": time.time(),
        "certificate_name": ""  # Will be prefilled with username after login
    }

# Define quiz question pool for predefined categories
QUIZ_QUESTIONS = {
    "business": [
        {
            "question": "What is a business plan?",
            "options": ["A document outlining goals and strategies", "A financial statement", "A marketing campaign"],
            "correct_answer": "A document outlining goals and strategies"
        },
        {
            "question": "What does ROI stand for?",
            "options": ["Return on Investment", "Revenue of Income", "Rate of Interest"],
            "correct_answer": "Return on Investment"
        },
    ],
    "marketing": [
        {
            "question": "What is market segmentation?",
            "options": ["Dividing a market into distinct groups", "Increasing market share", "Reducing competition"],
            "correct_answer": "Dividing a market into distinct groups"
        },
        {
            "question": "What is a target audience?",
            "options": ["The primary group of potential customers", "All possible customers", "Competitors' customers"],
            "correct_answer": "The primary group of potential customers"
        },
    ],
    "finance": [
        {
            "question": "What is equity?",
            "options": ["Ownership interest in a company", "Debt owed by a company", "Annual revenue"],
            "correct_answer": "Ownership interest in a company"
        },
        {
            "question": "What is a balance sheet?",
            "options": ["A statement of assets and liabilities", "A profit report", "A sales forecast"],
            "correct_answer": "A statement of assets and liabilities"
        },
    ],
}

# Add custom CSS for dark theme and larger, bolder fonts globally
st.markdown("""
<style>
body {
    background-color: #1e1e1e;
    color: #ffffff;
}
.stTitle {
    color: #ffffff !important;
    font-size: 36px !important;
}
.stTextInput > div > div > input {
    font-size: 18px !important;
    font-weight: bold !important;
    color: #ffffff !important;
    background-color: #2d2d2d !important;
}
.stButton > button {
    font-size: 18px !important;
    font-weight: bold !important;
    background-color: #9333ea !important;
    color: #ffffff !important;
    border-radius: 8px !important;
}
.stError {
    font-size: 16px !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# Login page
def login():
    with st.container():
        st.title("Welcome to DeepVenture Hub")
        st.markdown("<p style='font-size: 16px; color: #a0aec0;'>Unleash Your Business Ideas with AI-Powered Insights!</p>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login", key="login_button"):
                if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_data["certificate_name"] = username  # Prefill certificate name
                    st.rerun()
                else:
                    st.error("Invalid username or password")

# Main application
if not st.session_state.logged_in:
    login()
else:
    # Sidebar for navigation, settings, and user input
    with st.sidebar:
        st.write(f"Welcome, {st.session_state.username}!")
        if st.button("Logout"):
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
            st.rerun()
        
        st.header("Learning Settings")
        # Certificate name input (prefilled with username)
        certificate_name = st.text_input(
            "Name for Certificates",
            value=st.session_state.user_data["certificate_name"],
            placeholder="Enter your name for certificates...",
            key="certificate_name_input"
        )
        if certificate_name.strip():
            st.session_state.user_data["certificate_name"] = certificate_name.strip()
        
        category_options = ["business", "marketing", "finance", "custom"]
        selected_category = st.selectbox(
            "Select Learning Path",
            options=category_options,
            index=0,
            key="category_select"
        )
        custom_input = st.text_input(
            "Custom Idea Description",
            placeholder="Describe your idea for custom modules...",
            key="custom_input",
            disabled=selected_category != "custom"
        )
        refresh_btn = st.button("Refresh Modules", key="refresh_btn")

    # Dashboard header
    st.title("DeepVenture Hub Microlearning")
    st.markdown("### Boost Your Skills with Advanced, Personalized Learning!")

    # Main content (rest of your code remains unchanged)
    col1, col2 = st.columns([2, 1])
    with col1:
        # Microlearning modules
        category = custom_input if selected_category == "custom" and custom_input.strip() else selected_category
        if category.strip():
            if refresh_btn or "last_category" not in st.session_state or st.session_state.last_category != category:
                with st.spinner("Fetching microlearning modules..."):
                    time.sleep(1)  # Simulate API delay
                    modules = fetch_microlearning(category)
                    if not modules:
                        modules = ["No microlearning modules available for this category. Try 'business', 'marketing', or 'finance'."]
                    # Initialize progress for this category
                    if category not in st.session_state.user_data["progress"]:
                        st.session_state.user_data["progress"][category] = {
                            "modules": modules,
                            "completed": {},
                            "total_modules": len(modules),
                            "last_accessed": time.time()
                        }
                    else:
                        st.session_state.user_data["progress"][category]["modules"] = modules
                        st.session_state.user_data["progress"][category]["total_modules"] = len(modules)
                        st.session_state.user_data["progress"][category]["last_accessed"] = time.time()
                    st.session_state.last_category = category
            
            st.subheader("Learning Modules")
            for i, module in enumerate(st.session_state.user_data["progress"][category]["modules"], 1):
                module_id = f"module_{i}"
                with st.expander(f"Module {i}: {module.split('.')[0]}..."):
                    st.markdown(module)
                    if st.button(f"Complete Module {i}", key=f"complete_{i}_{category}"):
                        timestamp = time.time()
                        st.session_state.user_data["progress"][category]["completed"][module_id] = timestamp
                        st.session_state.user_data["progress"][category]["last_accessed"] = timestamp
                        # Check for Category Master badge
                        if len(st.session_state.user_data["progress"][category]["completed"]) == st.session_state.user_data["progress"][category]["total_modules"]:
                            badge = f"Category Master: {category.capitalize()} {datetime.now().strftime('%Y-%m-%d')}"
                            if badge not in st.session_state.user_data["badges"]:
                                st.session_state.user_data["badges"].append(badge)
                        st.rerun()

            # Progress tracking
            st.subheader("Learning Progress")
            progress = st.session_state.user_data["progress"][category]
            st.write(f"Completed: {len(progress['completed'])}/{progress['total_modules']} modules")
            st.write(f"Last Accessed: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(progress['last_accessed']))}")

            # Visualize completion timeline
            if progress["completed"]:
                completion_data = pd.DataFrame([
                    {"Module": mod.replace("module_", "Module "), "Completion Time": pd.to_datetime(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts)))}
                    for mod, ts in progress["completed"].items()
                ])
                fig_timeline = px.scatter(
                    completion_data,
                    x="Completion Time",
                    y="Module",
                    title="Module Completion Timeline",
                    height=400,
                    hover_data={"Completion Time": "|%Y-%m-%d %H:%M:%S"}
                )
                st.plotly_chart(fig_timeline, use_column_width=True)

            # Simulate multimedia content (e.g., videos)
            try:
                rows = backend._fetch_hf_data(category, limit=3)
                multimedia = [f"Video: {row['row']['text'][:50]}..." for row in rows[:2]] if rows else []
                if multimedia:
                    st.subheader("Additional Multimedia")
                    for video in multimedia:
                        st.markdown(f"- {video}")
                        st.image("https://via.placeholder.com/300x200?text=Sample+Video", caption=video, use_column_width=True)
            except Exception as e:
                st.error(f"Error fetching multimedia: {e}")

        # Interactive quiz with enhanced visibility
        with st.expander("Interactive Quiz", expanded=False):
            if category in st.session_state.user_data["progress"]:
                if category in QUIZ_QUESTIONS:
                    quiz = random.choice(QUIZ_QUESTIONS[category])
                    quiz["id"] = f"quiz_{len(st.session_state.user_data['quiz_history']) + 1}"
                    st.markdown(f"**Quiz Question:** {quiz['question']}", unsafe_allow_html=True)
                    answer = st.radio("Select Your Answer", quiz["options"], key=f"quiz_{category}_{quiz['id']}")
                    if st.button("Submit Quiz", key=f"submit_quiz_{category}_{quiz['id']}"):
                        is_correct = answer == quiz["correct_answer"]
                        feedback = f"{'Correct! 🎉' if is_correct else 'Incorrect. Try again!'} The correct answer is {quiz['correct_answer']}."
                        timestamp = time.time()
                        
                        st.session_state.user_data["quiz_history"].append({
                            "category": category,
                            "question": quiz["question"],
                            "answer": answer,
                            "correct": is_correct,
                            "timestamp": timestamp,
                            "quiz_id": quiz["id"]
                        })
                        
                        if is_correct:
                            st.session_state.user_data["progress"][category]["completed"][quiz["id"]] = timestamp
                            badge = f"Quiz Master: {category.capitalize()} {datetime.now().strftime('%Y-%m-%d')}"
                            if badge not in st.session_state.user_data["badges"]:
                                st.session_state.user_data["badges"].append(badge)
                            st.session_state.user_data["leaderboard"][st.session_state.username] = (
                                st.session_state.user_data["leaderboard"].get(st.session_state.username, 0) + 100
                            )
                        
                        st.success(feedback)
                        st.session_state.user_data["progress"][category]["last_accessed"] = timestamp
                        st.rerun()
                else:
                    st.info("Quizzes are not available for custom categories.")

    with col2:
        # Progress visualization
        if category in st.session_state.user_data["progress"]:
            progress_data = pd.DataFrame({
                "Module": [f"Module {i+1}" for i in range(st.session_state.user_data["progress"][category]["total_modules"])],
                "Status": ["Completed" if f"module_{i+1}" in st.session_state.user_data["progress"][category]["completed"] else "Pending" 
                          for i in range(st.session_state.user_data["progress"][category]["total_modules"])]
            })
            fig_bar = px.bar(
                progress_data,
                x="Module",
                y=["Status"] * len(progress_data),
                color="Status",
                title=f"Learning Progress for {category.capitalize()}",
                color_discrete_map={"Completed": "green", "Pending": "gray"},
                height=400
            )
            st.plotly_chart(fig_bar, use_column_width=True)

        # Quiz history and leaderboard
        st.subheader("Quiz Performance")
        if st.session_state.user_data["quiz_history"]:
            quiz_df = pd.DataFrame(st.session_state.user_data["quiz_history"])
            fig_pie = px.pie(
                quiz_df.groupby("correct").size().reset_index(name="count"),
                names="correct",
                values="count",
                title="Quiz Performance",
                color_discrete_map={True: "green", False: "red"},
                height=400
            )
            st.plotly_chart(fig_pie, use_column_width=True)

        # Leaderboard
        st.subheader("Leaderboard")
        LEADERBOARD_USERS = ["User1", "User2", "User3", "User4", "User5"]
        leaderboard_scores = {user: random.randint(0, 1000) for user in LEADERBOARD_USERS}
        current_user_score = st.session_state.user_data["leaderboard"].get(st.session_state.username, 0)
        leaderboard_scores[st.session_state.username] = current_user_score
        leaderboard_df = pd.DataFrame(
            list(leaderboard_scores.items()),
            columns=["User", "Score"]
        ).sort_values("Score", ascending=False).head(5)
        fig_leaderboard = px.bar(
            leaderboard_df,
            x="User",
            y="Score",
            title="Top 5 Quiz Performers",
            text="Score",
            color="Score",
            color_continuous_scale="Purples",
            height=400
        )
        fig_leaderboard.update_traces(textposition="auto")
        st.plotly_chart(fig_leaderboard, use_column_width=True)

        # Badges and certificates
        st.subheader("Achievements")
        badges = st.session_state.user_data["badges"]
        st.write("**Earned Badges:**")
        if badges:
            cols = st.columns(3)
            for idx, badge in enumerate(badges):
                with cols[idx % 3]:
                    st.success(f"🏅 {badge}")
        else:
            st.info("No badges earned yet. Complete modules and quizzes to earn badges!")

        if category in st.session_state.user_data["progress"]:
            progress = st.session_state.user_data["progress"][category]
            if len(progress["completed"]) >= progress["total_modules"]:
                certificate_text = f"""
                **DeepVenture Hub Microlearning Certificate**
                Awarded to: {st.session_state.user_data["certificate_name"]}
                For: Completing all modules in {category.capitalize()}
                Date: {datetime.now().strftime('%Y-%m-%d')}
                """
                st.success(certificate_text)

                pdf_buffer = io.BytesIO()
                doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
                styles = getSampleStyleSheet()
                story = []
                story.append(Paragraph("DeepVenture Hub Microlearning Certificate", styles['Heading1']))
                story.append(Spacer(1, 12))
                story.append(Paragraph(certificate_text, styles['BodyText']))
                doc.build(story)
                pdf_data = pdf_buffer.getvalue()
                pdf_buffer.close()

                png_width, png_height = 800, 600
                png_image = PILImage.new('RGB', (png_width, png_height), color='white')
                draw = ImageDraw.Draw(png_image)
                try:
                    font = ImageFont.truetype("arial.ttf", 40)
                except:
                    font = ImageFont.load_default()
                draw.text((50, 50), "DeepVenture Hub", fill='black', font=font)
                draw.text((50, 150), certificate_text, fill='black', font=ImageFont.truetype("arial.ttf", 20) if os.path.exists("arial.ttf") else font)
                png_buffer = io.BytesIO()
                png_image.save(png_buffer, format="PNG")
                png_data = png_buffer.getvalue()
                png_buffer.close()

                st.download_button(
                    label="Download Certificate (PDF)",
                    data=pdf_data,
                    file_name=f"certificate_{st.session_state.user_data['certificate_name']}_{category}_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
                st.download_button(
                    label="Download Certificate (PNG)",
                    data=png_data,
                    file_name=f"certificate_{st.session_state.user_data['certificate_name']}_{category}_{datetime.now().strftime('%Y%m%d')}.png",
                    mime="image/png"
                )

                st.session_state.user_data["last_activity"] = time.time()
                st.rerun()

        if st.button("Reset Learning Progress", key="clear_progress"):
            st.session_state.user_data = {
                "progress": {},
                "quiz_history": [],
                "badges": [],
                "leaderboard": {},
                "last_activity": time.time(),
                "certificate_name": st.session_state.user_data["certificate_name"]
            }
            st.session_state.last_category = None
            st.rerun()

    st.markdown("---")
    st.caption("""
        <div style='text-align: center; font-size: 24px; color: #666;'>
            Powered by DeepVenture Hub | Data sourced from Yelp Reviews via Hugging Face API<br>
            Made with ❤️ By Vikhram S © | All Rights Reserved | Team DeepVision
        </div>
    """, unsafe_allow_html=True)
