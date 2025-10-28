# 🛰️ Project Samarth: Intelligent Climate–Agriculture Q&A System

### 🌍 Vision
Government portals like [data.gov.in](https://data.gov.in/) host thousands of valuable datasets across ministries — but their varied formats make cross-domain insights difficult to obtain.  
**Project Samarth** bridges this gap by building an **AI-powered Q&A system** that integrates **climate and agriculture data**, allowing users to query India’s agricultural economy and its relationship with climate patterns — interactively and with full traceability.

---

## 🚀 Features
  🔹 **Intelligent Query System**: Ask analytical questions about groundwater levels, rainfall, and agricultural data.  
  🔹 **Integrated Data Sources**: Combines datasets from:     
        - Ministry of Agriculture & Farmers Welfare (e.g., KCC)
        - India Meteorological Department (e.g., Cyclone, Rainfall)
        - Ground Water Board (e.g., Pre-Monsoon Levels)
  🔹 **Dynamic Frontend**: Built with **Streamlit** — interactive filters for year, state, district, and keyword.  
  🔹 **Traceable Outputs**: Each insight links back to its dataset.  
  🔹 **Secure & Deployable**: Uses local SQLite database and can run entirely offline or securely in private environments.

---

## 🧠 Example Questions It Can Answer
1. Compare groundwater levels in Telangana across years.
2. Identify which districts show the fastest decline in groundwater.
3. Explore agricultural KCC queries related to specific crops or issues.
4. Observe cyclone frequency and correlate with water table patterns.

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
       git clone https://github.com/<your-username>/Project_Samarth.git
       cd Project_Samarth

### 2️⃣ Install dependencies
       pip install -r requirements.txt

### 3️⃣ Prepare the database
       cd notebooks
       python data_cleaning.py

### 4️⃣ Run the app locally
       cd ../frontend
       streamlit run app.py

