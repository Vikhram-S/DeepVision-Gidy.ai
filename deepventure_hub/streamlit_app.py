import streamlit as st
from deepventure_backend import DeepVentureBackend
import pandas as pd
import plotly.express as px
import time
from datetime import datetime

# Replace with your actual token (kept confidential)
HF_API_TOKEN = "huggingface_api_token"
backend = DeepVentureBackend(HF_API_TOKEN)

# Page configuration for a sleek, modern look
st.set_page_config(
    page_title="DeepVenture Hub",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for advanced UI/UX
st.markdown("""
<style>
body {
    font-family: 'Inter', 'Roboto', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #e2e8f0;
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
    transition: transform 0.2s, box-shadow 0.2s;
}
.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(147, 51, 234, 0.5);
}
.stTextInput > div > div > input {
    background-color: #1e293b;
    color: #e2e8f0;
    border: 1px solid #4b5563;
    border-radius: 8px;
    padding: 8px;
    font-size: 16px;
}
.stTextArea > div > div > textarea {
    background-color: #1e293b;
    color: #e2e8f0;
    border: 1px solid #4b5563;
    border-radius: 8px;
    font-size: 16px;
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
.container {
    animation: fadeIn 1s ease-in;
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Function to evaluate and simulate the idea
def evaluate_and_simulate(title, description):
    with st.spinner("🚀 Evaluating your idea..."):
        time.sleep(1)  # Simulate processing delay for UX
        score = backend.evaluate_idea(description)
        simulation = backend.run_simulation(title, description, score)
        mentor = backend.match_mentor(description)
        microlearning = backend.get_microlearning("business")
    
    result = {
        "title": title,
        "description": description,
        "score": score,
        "success_rate": simulation["success_rate"],
        "market_potential": simulation["market_potential"],
        "risk_factor": simulation["risk_factor"],
        "mentor": mentor,
        "microlearning": microlearning
    }
    st.session_state.history.append(result)
    return result

# Function to clear inputs and reset state
def clear_inputs():
    st.session_state.title_input = ""
    st.session_state.desc_input = ""
    st.session_state.history = []

# Main app
def main():
    # Sidebar for settings and history
    with st.sidebar:
        st.markdown("### ✨ DeepVenture Hub")
        st.markdown("Empower your ideas with AI insights!")
        st.markdown("---")
        st.subheader("Idea Vault")
        if st.session_state.history:
            for i, entry in enumerate(st.session_state.history, 1):
                with st.expander(f"Pitch {i}: {entry['title']}"):
                    st.markdown(
                        f"**Description:** {entry['description']}\n\n"
                        f"**Score:** {entry['score']}/100 📊\n"
                        f"**Success Rate:** {entry['success_rate']}% 🚀\n"
                        f"**Market Potential:** {entry['market_potential']}% 💰\n"
                        f"**Risk Factor:** {entry['risk_factor']}% ⚠️\n"
                        f"**Mentor:** {entry['mentor']} 👩‍🏫\n"
                        f"**Modules:** {', '.join(entry['microlearning'])} 📚"
                    )
        else:
            st.info("No pitches yet. Submit an idea to start!")
        if st.button("Clear All", key="clear_btn"):
            clear_inputs()
            st.rerun()

    # Main content
    st.title("DeepVenture Idea Lab ✨")
    st.markdown("### Pitch your business idea and get AI-powered insights instantly!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Input section
        with st.container():
            st.subheader("Submit Your Idea")
            title = st.text_input("Idea Title", placeholder="e.g., Eco-Friendly Packaging Solution", key="title_input")
            description = st.text_area("Idea Description", placeholder="Describe your idea in detail...", height=200, key="desc_input")
            submit = st.button("Evaluate Now", key="submit_btn")
            
            if submit and title and description:
                result = evaluate_and_simulate(title, description)
                st.success("✅ Evaluation Complete!")
                
                # Display results
                st.subheader("Your Insights")
                st.markdown(
                    f"### 🚀 Evaluation Score: {result['score']}/100\n\n"
                    f"#### Simulation Results:\n"
                    f"- **Success Rate:** {result['success_rate']}% 📈\n"
                    f"- **Market Potential:** {result['market_potential']}% 💰\n"
                    f"- **Risk Factor:** {result['risk_factor']}% ⚠️\n\n"
                    f"**Recommended Mentor:** {result['mentor']} 👩‍🏫\n\n"
                    f"**Suggested Learning Modules:** {', '.join(result['microlearning'])} 📚"
                )
                
                # Visualization
                metrics = pd.DataFrame({
                    "Metric": ["Success Rate", "Market Potential", "Risk Factor"],
                    "Value": [result["success_rate"], result["market_potential"], result["risk_factor"]]
                })
                fig = px.bar(metrics, x="Metric", y="Value", color="Metric", 
                            title="Simulation Overview", height=300, 
                            color_discrete_map={"Success Rate": "#34d399", "Market Potential": "#fbbf24", "Risk Factor": "#f87171"})
                st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Tips and stats
        st.subheader("Quick Tips")
        st.markdown("""
        - Be specific and detailed
        - Highlight your unique value
        - Include your target audience
        """)
        
        st.subheader("Your Stats")
        if st.session_state.history:
            avg_score = sum(entry["score"] for entry in st.session_state.history) / len(st.session_state.history)
            st.metric("Average Score", f"{avg_score:.1f}/100")
            st.metric("Total Pitches", len(st.session_state.history))
        else:
            st.info("Submit an idea to see your stats!")

    st.markdown("---")
    st.caption("Powered by DeepVision | © 2025 Team DeepVision")

if __name__ == "__main__":
    main()