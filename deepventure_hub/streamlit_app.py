import streamlit as st
from deepventure_backend import DeepVentureBackend
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Replace with your Hugging Face API token
HF_API_TOKEN = "huggingface_token"
backend = DeepVentureBackend(HF_API_TOKEN)

# Set page configuration
st.set_page_config(
    page_title="DeepVenture Hub Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="📊"
)

# Cache analytics data
@st.cache_data
def fetch_analytics():
    return backend.get_analytics()

analytics = fetch_analytics()

# Initialize session state
if "filtered_data" not in st.session_state:
    st.session_state.filtered_data = analytics
if "selected_sector" not in st.session_state:
    st.session_state.selected_sector = "All Sectors"

# Function to filter data
def filter_data(sector):
    if sector == "All Sectors":
        return analytics
    else:
        filtered_trends = {sector: analytics["market_trends"][sector]}
        return {
            "market_trends": filtered_trends,
            "funding_rounds": analytics["funding_rounds"],
            "sector_growth": analytics["sector_growth"]
        }

# Dashboard header
st.title("DeepVenture Hub Dashboard")
st.markdown("### Real-Time Business Intelligence Insights")

# Filters at the top
with st.container():
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        sector_options = ["All Sectors"] + list(analytics["market_trends"].keys())
        selected_sector = st.selectbox(
            "Select Sector",
            options=sector_options,
            index=sector_options.index(st.session_state.selected_sector),
            key="sector_select"
        )
    with col2:
        performance_threshold = st.slider(
            "Performance Threshold (%)",
            min_value=0,
            max_value=100,
            value=50,
            step=5,
            help="Filter sectors above this performance level"
        )
    with col3:
        st.button("Refresh Data", on_click=lambda: st.cache_data.clear())

# Update filtered data
st.session_state.selected_sector = selected_sector
filtered_data = filter_data(selected_sector)
trends_df = pd.DataFrame(filtered_data["market_trends"].items(), columns=['Sector', 'Performance'])
filtered_trends_df = trends_df[trends_df["Performance"] >= performance_threshold]

# Tabbed layout
tabs = st.tabs(["Overview", "Trends", "Details"])

# Tab 1: Overview (KPIs and Multiple Charts)
with tabs[0]:
    st.subheader("Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Activity Proxy (Text/1000)", 
                  filtered_data["funding_rounds"],
                  delta=f"{int(filtered_data['funding_rounds'] * 0.1)}")
    with col2:
        st.metric("Sector Growth", 
                  f"{filtered_data['sector_growth']}%",
                  delta=f"{filtered_data['sector_growth'] * 0.05:.1f}%")
    with col3:
        avg_performance = filtered_trends_df["Performance"].mean() if not filtered_trends_df.empty else 0
        st.metric("Avg Performance", 
                  f"{avg_performance:.1f}%",
                  delta=f"{avg_performance * 0.02:.1f}%")

    col1, col2, col3 = st.columns(3)
    with col1:
        # Pie chart (increased size)
        fig_pie = px.pie(
            filtered_trends_df,
            names="Sector",
            values="Performance",
            title="Performance Distribution",
            height=450  # Increased from 300
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        # Bar chart for overview
        fig_bar_overview = px.bar(
            filtered_trends_df,
            x="Sector",
            y="Performance",
            title="Sector Overview",
            text=filtered_trends_df["Performance"].apply(lambda x: f"{x:.1f}%"),
            height=450  # Increased size
        )
        fig_bar_overview.update_traces(textposition="auto")
        st.plotly_chart(fig_bar_overview, use_container_width=True)

    with col3:
        # Gauge chart for avg performance
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_performance,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Average Performance (%)"},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "darkblue"},
                   'steps': [
                       {'range': [0, 50], 'color': "lightgray"},
                       {'range': [50, 100], 'color': "gray"}]}
        ))
        fig_gauge.update_layout(height=450)  # Increased size
        st.plotly_chart(fig_gauge, use_container_width=True)

# Tab 2: Trends (Multiple Visuals)
with tabs[1]:
    col1, col2, col3 = st.columns(3)
    with col1:
        # Bar chart (increased size)
        fig_bar = px.bar(
            filtered_trends_df,
            x="Sector",
            y="Performance",
            title="Sector Performance",
            text=filtered_trends_df["Performance"].apply(lambda x: f"{x:.1f}%"),
            height=500  # Increased from 350
        )
        fig_bar.update_traces(textposition="auto")
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # Line chart (increased size)
        time_data = pd.DataFrame({
            "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "Performance": [avg_performance * (0.9 + i * 0.04) for i in range(6)]
        })
        fig_line = px.line(
            time_data,
            x="Month",
            y="Performance",
            title="Performance Trend (Mock)",
            markers=True,
            height=500  # Increased from 350
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with col3:
        # Scatter chart (new)
        scatter_data = pd.DataFrame({
            "Sector": filtered_trends_df["Sector"],
            "Performance": filtered_trends_df["Performance"],
            "Size": [filtered_data["funding_rounds"] * (i + 1) / 10 for i in range(len(filtered_trends_df))]
        })
        fig_scatter = px.scatter(
            scatter_data,
            x="Sector",
            y="Performance",
            size="Size",
            title="Performance vs Activity",
            height=500
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

# Tab 3: Details (Table, Insights, and Heatmap)
with tabs[2]:
    st.subheader("Detailed Analytics")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.dataframe(
            filtered_trends_df,
            use_container_width=True,
            column_config={
                "Sector": st.column_config.TextColumn("Sector", width="medium"),
                "Performance": st.column_config.NumberColumn("Performance (%)", format="%.1f")
            }
        )

    with col2:
        # Heatmap (new)
        heatmap_data = pd.pivot_table(filtered_trends_df, values="Performance", index="Sector")
        fig_heatmap = px.imshow(
            heatmap_data.T,
            labels=dict(x="Sector", y="Metric", color="Performance"),
            title="Performance Heatmap",
            height=400  # Suitable size for heatmap
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)

    # Insights
    with st.expander("Business Insights", expanded=True):
        if selected_sector == "All Sectors":
            top_sector = filtered_trends_df.loc[filtered_trends_df["Performance"].idxmax(), "Sector"] if not filtered_trends_df.empty else "N/A"
            st.markdown(f"**Top Performer:** {top_sector} at {filtered_trends_df['Performance'].max():.1f}%")
        else:
            overall_avg = sum(analytics["market_trends"].values()) / len(analytics["market_trends"])
            st.markdown(f"**{selected_sector} Insight:** {filtered_data['market_trends'][selected_sector]:.1f}% vs. overall avg {overall_avg:.1f}%")

# Custom footer
st.markdown("---")
st.caption("""
    <div style='text-align: center; font-size: 24px; color: #666;'>
        Powered by DeepVenture Hub | Data sourced from Yelp Reviews via Hugging Face API<br>
        Made with ❤️ By Vikhram S © | All Rights Reserved | Team DeepVision
    </div>
""", unsafe_allow_html=True)