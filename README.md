# 🧠 LLM ROI & Sustainability Dashboard  
### 🔹 Optimizing AI Model Selection: Cost & Environmental Impact Analysis  

---

## 📋 Overview  
This project was developed as part of the **Break Through Tech AI x KPMG Trusted AI Fellowship**.  
Our goal was to build a **data-driven decision-support dashboard** that helps users compare **Large Language Models (LLMs)** on both **financial and environmental impact**.  

The dashboard allows organizations to explore trade-offs between **cost, CO₂ emissions, and energy efficiency** — helping them make smarter, more sustainable choices when deploying AI.  

Built with **Streamlit**, the tool turns complex datasets into interactive visual insights that show where AI is worth the investment — and where it’s not.  

---

## 🎯 Objective  
To design a transparent, user-friendly dashboard that enables users to:  

- ⚙️ **Compare LLMs** on key business metrics — cost, energy, and emissions.  
- 🌍 **Quantify sustainability impact** through carbon and energy analysis.  
- 💰 **Estimate ROI** by balancing financial performance and sustainability.  
- 🧾 **Support AI governance and ESG reporting** with measurable data.  

---

## 🧩 Key Features  

### 🎛️ Interactive Metric Selector  
Choose what metric you want to analyze — from cost to carbon footprint.  

**Available metrics:**  
- `cost_usd` → Total operational cost  
- `co2_g` → CO₂ emissions in grams  
- `energy_Wh` → Total energy consumed  
- `energy_Wh_per_token` → Energy used per generated token  
- `roi_tokens_per_dollar` → Efficiency (tokens per dollar spent)  
- `roi_sustainability_score` → Combined sustainability + ROI index  

---

### 📊 Visual Insights  

- **Bar Chart** → Compare cost, energy, or ROI across different models.  
- **Scatter Plot** → Visualize trade-offs between CO₂ emissions and cost.  
- **Dashboard Filters** → Adjust for workload size, token count, or model type.  

These visuals make it easy to see which models are efficient, affordable, and environmentally responsible.  

---

## 💡 Business Insights from the Analysis  

### **1️⃣ Tiered Model Routing**  
Smaller models (2B–7B) can handle 70–85% of enterprise workloads.  
Routing simple tasks to smaller models can reduce **costs by up to 90%** and **CO₂ emissions by over 90%**.  
➡️ Integrated into the dashboard as part of the model recommendation logic.  

---

### **2️⃣ AI Financial Forecasting**  
Model selection directly impacts yearly operating expenses (OPEX).  
For example, 1B tokens/year with a 70B model costs ~$1,600, while a 2B model costs just ~$29 — a **98% cost saving**.  
➡️ The dashboard estimates financial trade-offs instantly.  

---

### **3️⃣ Responsible AI & Sustainability**  
AI emissions are now part of emerging **regulatory frameworks (ESG/CSRD)**.  
Our tool visualizes **CO₂ impact per model**, allowing easy integration into sustainability and compliance reports.  

---

### **4️⃣ Governance & Controls**  
Defines new **AI governance KPIs**, such as:  
- CO₂ per 1M tokens  
- Tokens per dollar  
- Model-size justification  
- Compliance logging & auditing  

➡️ These metrics can be expanded in future versions for enterprise monitoring.  

---

## 🧠 Models Compared  

| Model | Type | Parameters |
|-------|------|-------------|
| `gemma:2b` | General-purpose | 2B |
| `gemma:7b` | General-purpose | 7B |
| `llama3` | Meta LLM | 8B |
| `llama3:70b` | Meta LLM | 70B |
| `codellama:7b` | Code-specific | 7B |
| `codellama:70b` | Code-specific | 70B |  

These represent a range of small-to-large foundation models to simulate how scale affects ROI and sustainability.  

---

## 📈 ROI & Sustainability Metrics  

Our custom **ROI framework** combines both financial and environmental performance:  

\[
ROI_{score} = f(\text{tokens per dollar}, \text{energy per token}, \text{CO₂ per token})
\]

This unified metric helps identify models that are not only cost-efficient but also environmentally responsible.  

---

## 🧰 Tech Stack  

| Category | Tools Used |
|-----------|-------------|
| **Language** | Python 3.10+ |
| **Framework** | Streamlit |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly, Matplotlib |
| **Design** | KPMG-themed layout, dark-mode dashboard |

---

## 🚀 Future Improvements  

- ✨ Add **real-time data** from Hugging Face API for model emissions and energy data.  
- 🔧 Allow users to **adjust ROI weightings** (cost vs. energy vs. carbon).  
- 📊 Integrate **performance and accuracy benchmarks**.  
- 🌱 Expand dashboard for **model selection recommendations** using optimization algorithms.  
- 🧾 Link results to **ESG compliance templates** for reporting.  

---

## 👩‍💻 Team  

**Ruth Chane**  
**Krish Garg**  
**Michelle Garcia-Zamudio**  
**Deven Mittal**  
**Harsharandeep Dhillon**  

---

## 🏢 Acknowledgments  
Special thanks to **Dr. Uohna**, **KPMG Trusted AI Team**, and **Break Through Tech AI** for their mentorship and guidance throughout this project.  
