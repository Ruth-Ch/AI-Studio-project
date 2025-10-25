import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_summary = pd.read_csv("summary_data.csv")

st.title("LLM ROI and Sustainability Dashboard")

metric = st.sidebar.selectbox("Choose a metric", df_summary.columns[1:])
st.write(f"### {metric.title()} by Model")

fig, ax = plt.subplots()
sns.barplot(data=df_summary.sort_values(metric, ascending=False),
            x=metric, y='model_name', ax=ax)
st.pyplot(fig)


