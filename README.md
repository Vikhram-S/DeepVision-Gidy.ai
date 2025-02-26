# **DeepVenture Hub**  

**DeepVenture Hub** is an AI-powered idea marketplace and business simulator that empowers entrepreneurs and graduates by providing an interactive platform for idea evaluation, business simulation, personalized microlearning, mentorship matching, and real-time industry analytics.   

---

## **Features**  

### **🚀 AI-Powered Idea Evaluation**  
🔍 Submit your business idea and receive an **AI-generated evaluation score**.  

![Screenshot 2025-02-26 225820](https://github.com/user-attachments/assets/1defd1b5-5511-466c-afac-83913d79fee3)



### **📊 Business Simulation**  
🎮 Run simulations based on your idea to assess potential **success and market viability**.

![Screenshot 2025-02-26 225840](https://github.com/user-attachments/assets/24efe60c-03c4-4846-85cf-cb42a88dfe7e)

 

### **🤝 Mentor Matching**  
🎯 Get matched with industry experts based on the **keywords in your idea description**.  

![Screenshot 2025-02-21 224455](https://github.com/user-attachments/assets/d82aa1bd-288b-41b2-a24a-da18d2dbab77)



### **📚 Personalized Microlearning Modules**  
📖 Explore curated **microlearning content** across topics such as **business fundamentals, digital marketing, and financial management**.  

![Screenshot 2025-02-26 231151](https://github.com/user-attachments/assets/19b3d01a-c851-44a5-b34c-51b37cad2d3c)

![Screenshot 2025-02-26 231839](https://github.com/user-attachments/assets/bc7bb635-6223-4d59-8a58-11da5f408ccd)




### **📈 Real-Time Analytics Dashboard**  
📊 View **up-to-date market trends, funding rounds, and sector-specific insights** via a dedicated dashboard.  

![Screenshot 2025-02-21 224731](https://github.com/user-attachments/assets/1bdbee35-acfa-46a5-b6e7-fa0f0b7420ab)


---

## **Technologies Used**  

- **Python 3.x**
- **Tensorflow**
- **Scikit-learn**
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
🔗 Dataset Download: (https://huggingface.co/datasets/Yelp/yelp_review_full)

**📑 Dataset Columns:**

- idea_description – Text of the idea description.
- score – A numeric target score for training the evaluation model.
**Project Structure**  

```
deepventure_hub/
├── requirements.txt             
├── README.md                    
├── deepventure_backend.py        
│    - scikit‑learn functions for idea evaluation
│    - TensorFlow functions for simulation
│    - Microlearning, mentorship, and analytics functions
├── gradio_app.py                
└── streamlit_app.py
└── streamlit_dashboard.py
└── microlearning_app.py
└── output/screenshots
       
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

4️⃣ Launch Streamlit Microlearning Module
📌 To explore the microlearning module and boost your skills, run:
```
streamlit run microlearning_streamlit.py
```
**📚 This module displays:**
- ✔️ **Secure Login Interface**

- ✔️ **Personalized Learning Modules**

- ✔️ **Interactive Quizzes**

- ✔️ **Progress Tracking**

- ✔️ **Certificates**


# License
📜 This project is licensed under the MIT License.

# Contact
📧 For questions or further information and inquiries, please contact:
``
vikhrams@saveetha.ac.in
``
