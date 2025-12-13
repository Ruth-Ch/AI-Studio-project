# 🧠 LLM ROI & Sustainability Dashboard  
### Optimizing AI Model Selection: Cost & Environmental Impact Analysis  

---

## 📋 Project Overview  

### **Objective**  
The primary objective of this project is to develop a **decision-support dashboard** that helps organizations evaluate and compare **Large Language Models (LLMs)** based on **financial and environmental performance**.  
Specifically, the system aims to:  

- Quantify **cost, energy usage, and CO₂ emissions** for different LLMs  
- Measure **efficiency (tokens per dollar)** and **sustainability (energy per token)**  
- Estimate **ROI (Return on Investment)** combining cost and environmental impact  
- Visualize trade-offs between **performance, cost, and sustainability**  
- Support **responsible AI adoption** through transparent data insights  

---

### **Scope**  
This project focuses on developing an interactive **Streamlit dashboard** that integrates cost, energy, and emission metrics from multiple sources to compare different AI model configurations.  
The tool currently includes six representative models (2B–70B parameters) from **Gemma**, **Llama**, and **CodeLlama**, and can be extended to additional LLM families in future releases.  

---

### **Goals**  
- Build an **interactive dashboard** for evaluating model trade-offs  
- Integrate cost, energy, and emission data from trusted sources  
- Implement a **custom ROI formula** balancing productivity and sustainability  
- Create **business insights** linking model selection to financial and ESG outcomes  
- Deliver a **KPMG-branded prototype** supporting AI governance and advisory use cases  

---

### **Business Relevance**  
For KPMG’s Trusted AI team and enterprise clients, this dashboard provides a foundation for:  
- Understanding how **AI model selection impacts cost and environmental footprint**  
- Incorporating **sustainability and ESG metrics** into AI adoption decisions  
- Reducing **AI operational costs** through smarter workload routing  
- Enabling **transparent, responsible AI governance**  
- Supporting **data-driven ROI forecasting** for AI investment strategies  

By connecting cost-efficiency with sustainability, the tool empowers organizations to make AI deployment decisions that are **profitable, responsible, and future-proof.**  

---

## 📊 Data Exploration  

### **Datasets Used**  
1. **Hugging Face Energy Dataset** – Tracks energy use, emissions, and compute data for AI models  
2. **Harvard/BCG Productivity Study** – Provides insights on how AI affects productivity and cost savings  
3. **Anthropic Economic Index** – Measures public and economic sentiment around AI adoption  

Together, these datasets help quantify both the **business benefits** and **environmental trade-offs** of AI systems.  

---

### **Data Preprocessing and Integration**  
- Standardized units (Wh, gCO₂, USD) across all datasets  
- Filtered to include comparable model configurations  
- Normalized values per million tokens for fair comparison  
- Combined financial and environmental metrics into unified DataFrames  
- Derived new metrics: `energy_Wh_per_token`, `roi_tokens_per_dollar`, `roi_sustainability_score`  

---

### **Exploratory Data Analysis (EDA)**  
Key visual insights include:  
- **Cost vs. CO₂ scatter plot:** shows efficiency–sustainability trade-offs  
- **Bar chart comparisons:** highlights model-level differences in ROI and emissions  
- **Energy breakdowns:** demonstrates how larger models drive higher power and cooling demands  
- **Sustainability pie chart:** visualizes how ~92% of data center energy goes to electricity and cooling (Lawrence Berkeley National Lab, 2024)  

---

## 🧠 Model Development  

### **Technical Approach**  

1. **ROI & Sustainability Framework**  
   - Combines three core metrics:  
     - *Cost efficiency* (tokens per dollar)  
     - *Energy intensity* (Wh per token)  
     - *Carbon output* (gCO₂ per token)  
   - Generates a unified `roi_sustainability_score` using weighted averages  

2. **Dashboard Architecture**  
   - **Frontend:** Streamlit app (`app.py`) for visual interaction  
   - **Backend:** Pandas-based processing of cost and energy data  
   - **Visualization:** Plotly charts for interactivity and dynamic filtering  
   - **Computation:** Real-time ROI and sustainability calculations per model  

3. **Pipeline Overview**  
   - Load datasets → Normalize metrics → Calculate derived features → Display via Streamlit  
   - Users can switch metrics, compare models, and see live trade-offs  

---

### **Model Comparison Logic**  
| Model | Parameters | Category | Key Insight |
|--------|-------------|-----------|--------------|
| Gemma 2B | 2B | General-purpose | Highly efficient, minimal emissions |
| Gemma 7B | 7B | General-purpose | Balanced trade-off between accuracy and energy |
| Llama 3 | 8B | Meta AI | Moderate cost, scalable performance |
| Llama 3 70B | 70B | Meta AI | High compute and energy, expensive to run |
| CodeLlama 7B | 7B | Code-focused | Strong for development use cases |
| CodeLlama 70B | 70B | Code-focused | High performance but carbon intensive |

---

## 💡 Business Insights  

### **1️⃣ Tiered Model Routing**  
Smaller models can handle 70–85% of enterprise tasks, while large models are only needed for complex workloads.  
Routing smaller tasks through lighter models cuts **costs by 70–90%** and **CO₂ by 90%+.**  
Built into dashboard logic for smart model recommendations.  

### **2️⃣ AI Financial Forecasting**  
Shows how model size impacts annual operating expenses.  
Example: 1B-token workload → **$1,600 (70B)** vs **$29 (2B)** → 98% savings.  
The dashboard visualizes cost-to-efficiency trade-offs instantly.  

### **3️⃣ Responsible AI & Sustainability**  
Visualizes **CO₂ impact per model** and helps integrate sustainability metrics into ESG reports.  
Supports KPMG’s advisory goals for **Responsible AI adoption and carbon accountability.**  

### **4️⃣ Governance & Controls**  
Proposes new **KPIs** (e.g., CO₂ per million tokens, tokens per dollar, model-size approvals).  
Future dashboard versions can include **compliance logging and reporting integration.**

---

## 🗂️ Code Highlights  

### **Key Files**  
| File | Description |
|------|--------------|
| `app.py` | Streamlit dashboard UI and logic |
| `data/` | Model energy, cost, and emission data |
| `src/` | ROI and sustainability computation scripts |
| `notebooks/` | Exploratory analysis and visualization tests |
| `requirements.txt` | Python dependencies |
| `README.md` | Project documentation |

---

## 📈 Results & Key Findings  

- Tiered Model Routing reduces emissions by **>90%** and cost by **70–90%**  
- ROI analysis reveals smaller models outperform large ones in **cost-to-output efficiency**  
- Emission metrics align with **Lawrence Berkeley Lab (2024)** findings on energy usage  
- Dashboard enables **instant model comparison** across cost, carbon, and performance  

---

## 💬 Discussion & Reflection  

### **What Worked Well**  
- Integrating real datasets (Hugging Face, Harvard/BCG, Anthropic) into one unified tool  
- Combining business and sustainability perspectives in ROI design  
- Streamlit’s flexibility for rapid prototyping and visualization  

### **Challenges**  
- Normalizing diverse datasets across units (Wh, gCO₂, USD)  
- Defining a fair sustainability-weighted ROI metric  
- Balancing simplicity and interpretability in visual outputs  

### **Lessons Learned**  
- Sustainability can be quantified directly in ROI frameworks  
- Small design choices (like tiered routing) can lead to huge environmental savings  
- Interactive dashboards greatly improve engagement with non-technical audiences  


## 👩‍💻 Team  

**Ruth Chane**  
**Krish Garg**  
**Michelle Garcia-Zamudio**  
**Deven Mittal**  
**Harsharandeep Dhillon**  

---

## 🏢 Acknowledgments  
Special thanks to **Dr. Uohna**, **KPMG Trusted AI Team**, and **Break Through Tech AI** for their mentorship and guidance throughout this project.  
