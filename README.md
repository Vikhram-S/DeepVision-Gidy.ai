# **DeepVenture Hub**  

**DeepVenture Hub** is an AI-powered idea marketplace and business simulator that empowers entrepreneurs and graduates by providing an interactive platform for idea evaluation, business simulation, personalized microlearning, mentorship matching, and real-time industry analytics.  

![DeepVenture Hub Banner](https://via.placeholder.com/1200x400?text=DeepVenture+Hub)  

---

## **Features**  

### **🚀 AI-Powered Idea Evaluation**  
🔍 Submit your business idea and receive an **AI-generated evaluation score**.  
![Idea Evaluation](https://via.placeholder.com/600x300?text=AI+Idea+Evaluation)  

### **📊 Business Simulation**  
🎮 Run simulations based on your idea to assess potential **success and market viability**.  
![Business Simulation](https://via.placeholder.com/600x300?text=Business+Simulation)  

### **🤝 Mentor Matching**  
🎯 Get matched with industry experts based on the **keywords in your idea description**.  
![Mentor Matching](https://via.placeholder.com/600x300?text=Mentor+Matching)  

### **📚 Personalized Microlearning Modules**  
📖 Explore curated **microlearning content** across topics such as **business fundamentals, digital marketing, and financial management**.  
![Microlearning](https://via.placeholder.com/600x300?text=Microlearning+Modules)  

### **📈 Real-Time Analytics Dashboard**  
📊 View **up-to-date market trends, funding rounds, and sector-specific insights** via a dedicated dashboard.  
![Analytics Dashboard](https://via.placeholder.com/600x300?text=Real-Time+Analytics)  

---

## **Technologies Used**  

- **Python 3.x**  
- **Gradio** - For interactive **idea evaluation UI**.  
- **Streamlit** - For building the **real-time analytics dashboard**.  
- **Standard Python Libraries** (e.g., `random`) for mock implementations.  

---
**2️⃣ Install Dependencies** 
```
pip install -r requirements.txt
```
**3️⃣ Dataset** 
📂 Dataset Used: Yelp Review Full Dataset
🔗 Dataset Download: ![Click here](https://huggingface.co/datasets/Yelp/yelp_review_full)

**📑 Dataset Columns:**

idea_description – Text of the idea description.
score – A numeric target score for training the evaluation model.
Project Structure
plaintext

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
**Usage**
**1️⃣ Training and Evaluation**
- 💡 **Idea Evaluation**
- 📌 The function evaluate_idea(description) in deepventure_backend.py:

- Loads (or trains) a scikit-learn model using the stackoverflow_survey_2024.csv dataset.
- Transforms the idea description using a TF-IDF vectorizer.
- Predicts a score between 0 and 100.

**📈 Business Simulation**
- 📌 The function run_simulation(title, description, score):

- Loads (or trains) a TensorFlow model that takes a normalized idea score as input.
- Outputs a predicted success rate for the idea.  
**2️⃣ Launch Gradio Interface**
- 📌 To start the interactive idea evaluation interface, run:

```
python gradio_app.py
```
**🚀 A local web interface will open where you can:**
- ✅ Enter your idea title and description.
- ✅ Receive an AI evaluation score.
- ✅ Run a business simulation.
- ✅ Get matched with a mentor.
- ✅ Explore microlearning modules.


**3️⃣ Launch Streamlit Dashboard**
- 📌 To view the real-time analytics dashboard, run:
```
streamlit run streamlit_app.py
```
**📊 This dashboard displays:**
- ✔️ Market trends
- ✔️ Funding rounds
- ✔️ Sector insights


# License
📜 This project is licensed under the MIT License.

# Contact
📧 For questions or further information and inquiries, please contact:
``
vikhrams@saveetha.ac.in
``
