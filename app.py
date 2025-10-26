import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load summary data from CSV
df = pd.read_csv("summary_data.csv")

# Calculate a combined ROI sustainability score 
df["roi_sustainability_score"] = df["roi_tokens_per_dollar"] / df["co2_g"]

st.title(" LLM ROI & Sustainability Dashboard")
st.write("Compare LLM models by Cost, CO₂ Emissions, Energy, and ROI")

# Sidebar for metric selection
metric = st.sidebar.selectbox(
    "Select a metric to visualize",
    ["cost_usd", "co2_g", "energy_Wh", "energy_Wh_per_token", "roi_tokens_per_dollar", "roi_sustainability_score"]
)

# Barplot for selected metric
st.subheader(f"{metric} by Model")
fig, ax = plt.subplots()
sns.barplot(data=df.sort_values(metric, ascending=False), x=metric, y="model_name", ax=ax)
st.pyplot(fig)

# Scatter plot for tradeoffs
st.subheader(" Tradeoff: Cost vs CO₂ Emissions")
fig2, ax2 = plt.subplots()
sns.scatterplot(data=df, x="cost_usd", y="co2_g", hue="model_name", s=100)
for i in range(df.shape[0]):
    ax2.text(df["cost_usd"][i], df["co2_g"][i], df["model_name"][i])
st.xlabel("Cost (USD)")
st.ylabel("CO₂ Emissions (g)")
st.pyplot(fig2)


