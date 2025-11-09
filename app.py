import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

sns.set_style("whitegrid")

# --- KPMG color palette ---
KPMG_BLUE = "#00338D"
KPMG_LIGHT_BLUE = "#007DBA"
KPMG_NAVY = "#002B5C"
KPMG_GRAY = "#E6E6E6"
KPMG_WHITE = "#FFFFFF"

sns.set_palette([KPMG_BLUE, KPMG_LIGHT_BLUE, KPMG_NAVY])

# --- Custom CSS for KPMG styling ---
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {KPMG_WHITE};
            color: {KPMG_NAVY};
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: {KPMG_BLUE} !important;
            font-family: "Arial", sans-serif;
        }}
        [data-testid="stSidebar"] {{
            background-color: {KPMG_GRAY};
        }}
        .stSlider > div > div > div {{
            background: linear-gradient(90deg, {KPMG_BLUE}, {KPMG_LIGHT_BLUE});
        }}
        .stTabs [role="tab"] {{
            background-color: {KPMG_GRAY};
            color: {KPMG_NAVY};
            font-weight: 600;
            border-radius: 6px;
            padding: 8px 20px;
        }}
        .stTabs [role="tab"][aria-selected="true"] {{
            background-color: {KPMG_BLUE};
            color: {KPMG_WHITE};
        }}
    </style>
    """,
    unsafe_allow_html=True
)


# ================================
# Load data
# ================================
df = pd.read_csv("summary_data.csv")
df["roi_sustainability_score"] = df["roi_tokens_per_dollar"] / df["co2_g"]

# ================================
# Business impact metrics per model
# ================================
TOKENS = 1_000_000
df["usd_per_million_tokens"] = TOKENS / df["roi_tokens_per_dollar"]
df["co2_g_per_million_tokens"] = df["co2_g"] / df["roi_tokens_per_dollar"] * TOKENS

# Power mapping (proxy for performance)
power_map = {
    "gemma:2b": 1,
    "gemma:7b": 2,
    "codellama:7b": 2,
    "llama3": 2,
    "codellama:70b": 3,
    "llama3:70b": 3,
}
df["power_score"] = df["model_name"].map(power_map).fillna(1)

# ================================
# Dashboard Tabs
# ================================
tab1, tab2, tab3 = st.tabs(["Model Metrics", "Business Impact", "Model Recommendation"])

# ---------------- TAB 1 ----------------
with tab1:
    st.subheader("Per-Model Metrics")

    metric = st.sidebar.selectbox(
        "Select a metric to visualize",
        [
            "cost_usd",
            "co2_g",
            "energy_Wh",
            "energy_Wh_per_token",
            "roi_tokens_per_dollar",
            "roi_sustainability_score",
        ],
        index=0,
    )

    # Bar chart
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=df.sort_values(metric, ascending=False),
        x=metric,
        y="model_name",
        ax=ax1,
        color=KPMG_BLUE
    )
    ax1.set_xlabel(metric)
    ax1.set_ylabel("Model")
    ax1.set_title(f"{metric.replace('_', ' ').title()} by Model", color=KPMG_NAVY)
    st.pyplot(fig1)

    # Scatter (cost vs CO2)
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=df, x="cost_usd", y="co2_g", hue="model_name", s=100, palette="Blues", ax=ax2)
    for i in range(df.shape[0]):
        ax2.text(df["cost_usd"][i], df["co2_g"][i], df["model_name"][i], fontsize=8)
    ax2.set_xlabel("Cost (USD)")
    ax2.set_ylabel("CO₂ Emissions (g)")
    ax2.set_title("Trade-off: Cost vs CO₂ Emissions", color=KPMG_NAVY)
    st.pyplot(fig2)

# ---------------- TAB 2 ----------------
with tab2:
    st.subheader("Business Impact: Cost & CO₂ per 1M Tokens")
    st.write(
        "Estimate each model’s **cost** and **CO₂ emissions** for generating 1 million tokens. "
        "Helps identify optimal trade-offs between performance, sustainability, and budget."
    )

    st.dataframe(
        df[[
            "model_name",
            "roi_tokens_per_dollar",
            "usd_per_million_tokens",
            "co2_g_per_million_tokens",
        ]].sort_values("usd_per_million_tokens"),
        use_container_width=True,
    )

    # Cost bar
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=df.sort_values("usd_per_million_tokens", ascending=False),
        x="usd_per_million_tokens",
        y="model_name",
        ax=ax3,
        color=KPMG_LIGHT_BLUE
    )
    ax3.set_title("Cost per 1M Tokens by Model", color=KPMG_NAVY)
    st.pyplot(fig3)

    # CO₂ bar
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=df.sort_values("co2_g_per_million_tokens", ascending=False),
        x="co2_g_per_million_tokens",
        y="model_name",
        ax=ax4,
        color=KPMG_BLUE
    )
    ax4.set_title("CO₂ per 1M Tokens by Model", color=KPMG_NAVY)
    st.pyplot(fig4)

    st.info(
        "*Interpretation:* models with higher cost and CO₂ per 1M tokens should be reserved "
        "for high-complexity tasks, while smaller, cleaner models can handle everyday workloads."
    )

# ---------------- TAB 3 ----------------
with tab3:
    st.subheader("Model Recommendation")

    task_type = st.selectbox(
        "Choose a task type",
        [
            "Summarization / Note-taking",
            "Customer Support Chat",
            "Analytical Report / Data Explanation",
            "Code Generation / Complex Reasoning",
        ],
    )

    st.markdown("**Set your priorities** (0 = don’t care, 1 = care a lot)")
    cost_pref = st.slider("Cost sensitivity", 0.0, 1.0, 0.7)
    carbon_pref = st.slider("Carbon sensitivity", 0.0, 1.0, 0.7)
    perf_pref = st.slider("Performance priority", 0.0, 1.0, 0.5)

    cost_norm = df["usd_per_million_tokens"] / df["usd_per_million_tokens"].max()
    co2_norm = df["co2_g_per_million_tokens"] / df["co2_g_per_million_tokens"].max()
    power_norm = df["power_score"] / df["power_score"].max()

    df["composite_score"] = (
        cost_pref * (1 - cost_norm)
        + carbon_pref * (1 - co2_norm)
        + perf_pref * power_norm
    )

    best_row = df.sort_values("composite_score", ascending=False).iloc[0]
    st.markdown(
        f"<h3 style='color:{KPMG_BLUE}'>Suggested model: {best_row['model_name']}</h3>",
        unsafe_allow_html=True,
    )

    st.write(
        f"- **Estimated cost:** {best_row['usd_per_million_tokens']:.2e} USD per 1M tokens  \n"
        f"- **CO₂ impact:** {best_row['co2_g_per_million_tokens']:.2e} g per 1M tokens"
    )
    st.write(
        f"- With your selected priorities, it leans toward a "
        f"{'larger' if best_row['power_score'] > 1 else 'smaller'} model for this task."
    )

    st.caption(
        "This weighted scoring system helps balance budget, sustainability, and performance goals."
    )
