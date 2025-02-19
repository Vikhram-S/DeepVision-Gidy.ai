# DeepVenture Hub

**DeepVenture Hub** is an AI-powered idea marketplace and business simulator that empowers entrepreneurs and graduates by providing an interactive platform for idea evaluation, business simulation, personalized microlearning, mentorship matching, and real-time industry analytics.

## Features

- **AI-Powered Idea Evaluation**  
  Submit your business idea and receive an AI-generated evaluation score.

- **Business Simulation**  
  Run simulations based on your idea to assess potential success and market viability.

- **Mentor Matching**  
  Get matched with industry experts based on the keywords in your idea description.

- **Personalized Microlearning Modules**  
  Explore curated microlearning content across topics such as business fundamentals, digital marketing, and financial management.

- **Real-Time Analytics Dashboard**  
  View up-to-date market trends, funding rounds, and sector-specific insights via a dedicated dashboard.

## Technologies

- **Python 3.x**
- **Gradio** - For interactive idea evaluation UI.
- **Streamlit** - For building the real-time analytics dashboard.
- **Standard Python Libraries** (e.g., `random`) for mock implementations.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/deepventure-hub.git
   cd deepventure-hub
   ```
2.**Install Dependencies**:

```
pip install -r requirements.txt
```
3.**Dataset:**

- Stackoverflow Annual Developer Survey Dataset
- Dataset Download link - https://survey.stackoverflow.co/

-idea_description – Text of the idea description.
-score – A numeric target score for training the evaluation model.
## Project Structure
```
deepventure_hub/
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation (this file)
├── deepventure_backend.py        # Core module:
│    - scikit‑learn functions for idea evaluation
│    - TensorFlow functions for simulation
│    - Microlearning, mentorship, and analytics functions
├── gradio_app.py                 # Gradio interface for interactive idea evaluation
└── streamlit_app.py              # Streamlit dashboard for real-time analytics
```
## Usage
**Training and Evaluation**
**Idea Evaluation**:

- The function evaluate_idea(description) in deepventure_backend.py:
- Loads (or trains) a scikit‑learn model using the stackoverflow_survey_2024.csv dataset.
- Transforms the idea description using a TF-IDF vectorizer.
- Predicts a score between 0 and 100.
**Business Simulation**:

- The function run_simulation(title, description, score):
- Loads (or trains) a TensorFlow model that takes a normalized idea score as input.
- Outputs a predicted success rate for the idea.
- Launch Gradio Interface
- To start the interactive idea evaluation interface:

```
python gradio_app.py
```
**A local web interface will open where you can**:

- Enter your idea title and description.
- Receive an AI evaluation score.
- Run a business simulation.
- Get matched with a mentor.
- Explore microlearning modules.
- Launch Streamlit Dashboard
- To view the real-time analytics dashboard:

```
streamlit run streamlit_app.py
```
**This dashboard displays:**

- Market trends.
- Funding rounds.
- Sector insights.   

## **License**
This project is licensed under the MIT License.

## **Contact**
For questions or further information, please contact vikhrams@saveetha.ac.in.
