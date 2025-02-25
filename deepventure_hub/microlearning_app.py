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

# Initialize backend with Hugging Face API token
HF_API_TOKEN = "hugging_face"  # hugging face api token is confidential so iam not updated in github. should Replace with my actual token
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

# Initialize session state for LMS tracking
if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "progress": {},
        "quiz_history": [],
        "badges": [],
        "leaderboard": {},
        "last_activity": time.time(),
        "user_name": "Anonymous"  # Default user name
    }

# Dashboard header
st.title("DeepVenture Hub Microlearning")
st.markdown("### Boost Your Skills with Advanced, Personalized Learning!")

# Sidebar for navigation, settings, and user input
with st.sidebar:
    st.header("Learning Settings")
    # User name input
    user_name = st.text_input(
        "Your Name",
        value=st.session_state.user_data["user_name"],
        placeholder="Enter your name for personalized certificates...",
        key="user_name_input"
    )
    if user_name.strip():
        st.session_state.user_data["user_name"] = user_name.strip()
    
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

# Main content
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
                st.session_state.user_data["progress"][category] = {
                    "modules": modules,
                    "completed": st.session_state.user_data["progress"].get(category, {}).get("completed", []),
                    "total_modules": len(modules),
                    "last_accessed": time.time()
                }
                st.session_state.last_category = category
        
        st.subheader("Learning Modules")
        for i, module in enumerate(st.session_state.user_data["progress"][category]["modules"], 1):
            st.markdown(f"**Module {i}:** {module}")
            if st.button(f"Complete Module {i}", key=f"complete_{i}_{category}"):
                st.session_state.user_data["progress"][category]["completed"].append(f"module_{i}")
                st.session_state.user_data["progress"][category]["last_accessed"] = time.time()
                st.rerun()

        # Progress tracking
        st.subheader("Learning Progress")
        progress = st.session_state.user_data["progress"][category]
        st.write(f"Completed: {len(progress['completed'])}/{progress['total_modules']} modules")
        st.write(f"Last Accessed: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(progress['last_accessed']))}")

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
            quiz = {
                "question": f"What is the key focus of {category.capitalize()} microlearning?",
                "options": ["Strategy", "Technology", "Finance", "Marketing"],
                "correct_answer": random.choice(["Strategy", "Technology", "Finance", "Marketing"]),
                "id": f"quiz_{len(st.session_state.user_data['quiz_history']) + 1}"
            }
            st.session_state.user_data["quiz"] = quiz

            st.markdown(f"**Quiz Question:** {quiz['question']}", unsafe_allow_html=True)
            answer = st.radio("Select Your Answer", quiz["options"], key=f"quiz_{category}")
            if st.button("Submit Quiz", key=f"submit_quiz_{category}"):
                is_correct = answer == quiz["correct_answer"]
                feedback = f"{'Correct! 🎉' if is_correct else 'Incorrect. Try again!'} The answer is {quiz['correct_answer']}."
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
                    st.session_state.user_data["progress"][category]["completed"].append(quiz["id"])
                    # Award badge for quiz completion
                    badge = f"Quiz Master {datetime.now().strftime('%Y-%m-%d')}"
                    if badge not in st.session_state.user_data["badges"]:
                        st.session_state.user_data["badges"].append(badge)
                    # Update leaderboard (simulated score: 100 for correct, 0 for incorrect)
                    st.session_state.user_data["leaderboard"][f"User_{random.randint(1, 100)}"] = (
                        st.session_state.user_data["leaderboard"].get(f"User_{random.randint(1, 100)}", 0) + (100 if is_correct else 0)
                    )
                
                st.success(feedback)
                st.session_state.user_data["progress"][category]["last_accessed"] = time.time()
                st.rerun()

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
    if st.session_state.user_data["leaderboard"]:
        leaderboard_df = pd.DataFrame(
            st.session_state.user_data["leaderboard"].items(),
            columns=["User", "Score"]
        ).sort_values("Score", ascending=False).head(5)
        fig_leaderboard = px.bar(
            leaderboard_df,
            x="User",
            y="Score",
            title="Top 5 Quiz Performers",
            text=leaderboard_df["Score"],
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
        for badge in badges:
            st.success(badge)
    else:
        st.info("No badges earned yet. Complete modules and quizzes to earn badges!")

    if category in st.session_state.user_data["progress"]:
        progress = st.session_state.user_data["progress"][category]
        if len(progress["completed"]) == progress["total_modules"]:
            certificate_text = f"""
            **DeepVenture Hub Microlearning Certificate**
            Awarded to: {st.session_state.user_data["user_name"]}
            For: Completing all modules in {category.capitalize()}
            Date: {datetime.now().strftime('%Y-%m-%d')}
            """
            st.success(certificate_text)

            # Generate PDF certificate
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

            # Generate PNG certificate
            png_width, png_height = 800, 600
            png_image = PILImage.new('RGB', (png_width, png_height), color='white')
            draw = ImageDraw.Draw(png_image)
            try:
                font = ImageFont.truetype("arial.ttf", 40)  # Use a system font; install if needed
            except:
                font = ImageFont.load_default()  # Fallback if font not found
            draw.text((50, 50), "DeepVenture Hub", fill='black', font=font)
            draw.text((50, 150), certificate_text, fill='black', font=ImageFont.truetype("arial.ttf", 20) if os.path.exists("arial.ttf") else font)
            png_buffer = io.BytesIO()
            png_image.save(png_buffer, format="PNG")
            png_data = png_buffer.getvalue()
            png_buffer.close()

            # Download buttons for PDF and PNG
            st.download_button(
                label="Download Certificate (PDF)",
                data=pdf_data,
                file_name=f"certificate_{st.session_state.user_data['user_name']}_{category}_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )
            st.download_button(
                label="Download Certificate (PNG)",
                data=png_data,
                file_name=f"certificate_{st.session_state.user_data['user_name']}_{category}_{datetime.now().strftime('%Y%m%d')}.png",
                mime="image/png"
            )

            st.session_state.user_data["last_activity"] = time.time()
            st.rerun()

    # Clear progress button
    if st.button("Reset Learning Progress", key="clear_progress"):
        st.session_state.user_data = {
            "progress": {},
            "quiz_history": [],
            "badges": [],
            "leaderboard": {},
            "last_activity": time.time(),
            "user_name": st.session_state.user_data["user_name"]  # Preserve user name
        }
        st.session_state.last_category = None
        st.rerun()

# Custom footer
st.markdown("---")
st.caption("""
    <div style='text-align: center; font-size: 24px; color: #666;'>
        Powered by DeepVenture Hub | Data sourced from Yelp Reviews via Hugging Face API<br>
        Made with ❤️ By Vikhram S © | All Rights Reserved | Team DeepVision
    </div>
""", unsafe_allow_html=True)
