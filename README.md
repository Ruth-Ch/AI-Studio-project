# AI-Studio-project
# 🧠 LLM ROI & Sustainability Dashboard  
###  

## 📋 Overview  
This project is part of the **Break Through Tech AI x KPMG Trusted AI Fellowship**.  
The dashboard helps users **compare Large Language Models (LLMs)** based on cost, energy use, carbon emissions, and estimated ROI metrics to explore trade-offs between **performance, sustainability, and cost efficiency**.  

Built in **Streamlit**, this tool provides a visual and interactive way to evaluate AI models’ sustainability and ROI profiles.  

---

## 🎯 Objective  
To create a transparent, data-driven dashboard that allows users to:  
- Evaluate how different LLMs perform on financial and environmental metrics  
- Understand cost-to-efficiency and cost-to-emission trade-offs  
- Estimate ROI and sustainability performance through visual comparisons  

---

## 🧩 Key Features  
### 🎛️ Interactive Metric Selector  
Users can choose which metric to visualize from a dropdown menu.  

**Available metrics:**  
- `cost_usd` — Total cost of running the model  
- `co2_g` — CO₂ emissions (in grams)  
- `energy_Wh` — Energy consumed in watt-hours  
- `energy_Wh_per_token` — Energy usage per generated token  
- `roi_tokens_per_dollar` — ROI measured as tokens per dollar spent  
- `roi_sustainability_score` — Combined metric estimating overall sustainability and ROI performance  

---

## 📊 Visualizations  
- **Bar Chart:** Compares selected metrics (like cost or ROI) across LLM models  
- **Scatter Plot:** Displays trade-offs between **cost** and **CO₂ emissions** for visual insight into sustainability vs. expense  

---

## 🧠 Models Compared  
- `gemma:2b`  
- `gemma:7b`  
- `llama3`  
- `llama3:70b`  
- `codellama:7b`  
- `codellama:70b`  

---

## 📈 ROI & Sustainability Metrics  
The dashboard integrates multiple ROI-related metrics such as **tokens per dollar** and **ROI sustainability score**.  
These provide a simplified view of how efficiently each model performs relative to its **environmental footprint** and **cost**.  
*(Exact calculation formulas can be adjusted or expanded in future updates.)*  

---

## 🧰 Tech Stack  
- **Python 3.10+**  
- **Streamlit** – Web framework for interactive dashboards  
- **Pandas / NumPy** – Data processing and calculations  
- **Matplotlib / Plotly** – Chart visualizations  

---

## 🚀 Future Improvements  
- Refine ROI formula with adjustable weights (productivity, efficiency, sustainability)  
- Add performance and accuracy metrics for a more holistic comparison  
- Improve UI with **KPMG-branded color scheme** and design elements  
- Introduce a scoring system combining cost, performance, and sustainability  
