import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------
# Styling
# ---------------------------
sns.set_style("whitegrid")

KPMG_BLUE = "#00338D"
KPMG_LIGHT_BLUE = "#007DBA"
KPMG_NAVY = "#002B5C"
KPMG_GRAY = "#E6E6E6"
KPMG_WHITE = "#FFFFFF"

sns.set_palette([KPMG_BLUE, KPMG_LIGHT_BLUE, KPMG_NAVY])

st.set_page_config(page_title="KPMG LLM Decision Support Tool", layout="wide")

st.markdown(
    f"""
    <style>
        .stApp {{
            background: radial-gradient(circle at top left, #0b1b4a, #000000);
            color: {KPMG_WHITE};
            font-family: "Arial", sans-serif;
        }}

        /* Make metric text white */
        .stMetric > div {{
            color: white !important;
        }}

        /* Make slider labels white */
        .css-10trblm, .css-1p3jz0k, .stSlider > label, .stSlider label {{
            color: white !important;
        }}

        /* Make slider numbers white */
        .stSlider .css-1cpxqw2, .stSlider .css-1k2i4p1 {{
            color: white !important;
        }}

        /* Tabs */
        .stTabs [role="tab"] {{
            background-color: #111827;
            color: {KPMG_WHITE};
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
    unsafe_allow_html=True,
)

# ---------------------------
# Load data and create metrics
# ---------------------------
df = pd.read_csv("summary_data.csv")

TOKENS = 1_000_000

df["usd_per_million_tokens"] = TOKENS / df["roi_tokens_per_dollar"]
df["co2_g_per_million_tokens"] = df["co2_g"] / df["roi_tokens_per_dollar"] * TOKENS

power_map = {
    "gemma:2b": 1,
    "gemma:7b": 2,
    "codellama:7b": 2,
    "llama3": 2,
    "codellama:70b": 3,
    "llama3:70b": 3,
}
df["power_score"] = df["model_name"].map(power_map).fillna(1)

# ---------------------------
# Header
# ---------------------------
st.markdown(
    "<h1 style='text-align:center;'>KPMG LLM Decision Support Tool</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;'>This tool helps compare language models by cost, carbon impact and task fit.</p>",
    unsafe_allow_html=True,
)

# ---------------------------
# Tabs
# ---------------------------
tab1, tab2, tab3 = st.tabs(
    ["Model Overview", "Cost, CO2 and Savings", "Task based Recommendation"]
)

# ---------------- TAB 1: Model Overview ----------------
with tab1:
    st.subheader("Model Overview")

    st.write(
        "Use this tab to compare models side by side. "
        "Pick a metric and the chart shows how each model ranks."
    )

    metric = st.selectbox(
        "Metric",
        ["usd_per_million_tokens", "co2_g_per_million_tokens", "roi_tokens_per_dollar"],
        format_func=lambda x: x.replace("_", " ").title(),
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=df.sort_values(metric, ascending=False),
        x=metric,
        y="model_name",
        ax=ax,
        color=KPMG_LIGHT_BLUE,
    )

    ax.set_title(f"{metric.replace('_', ' ').title()} by Model", color=KPMG_WHITE)
    ax.set_xlabel(metric.replace("_", " ").title())
    ax.set_ylabel("Model")

    # fix invisible labels
    ax.tick_params(colors="white")
    plt.setp(ax.get_yticklabels(), color="white")
    plt.setp(ax.get_xticklabels(), color="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")

    for spine in ax.spines.values():
        spine.set_color("white")

    st.pyplot(fig)

    st.caption(
        "Higher bars mean higher cost, higher emissions or higher tokens per dollar."
    )

# ---------------- TAB 2: Cost, CO2 and Savings ----------------
with tab2:
    st.subheader("Cost, CO2 and Savings")

    st.write(
        "This tab lets you estimate cost and carbon impact for a model and see how much you could save by choosing a different one."
    )

    col_top1, col_top2 = st.columns(2)
    with col_top1:
        period = st.selectbox(
            "Time period",
            ["Monthly", "Quarterly", "Yearly"],
        )
    with col_top2:
        monthly_tokens = st.number_input(
            "Estimated monthly tokens",
            min_value=1_000_000,
            value=10_000_000,
            step=1_000_000,
        )

    if period == "Monthly":
        token_factor = 1
    elif period == "Quarterly":
        token_factor = 3
    else:
        token_factor = 12

    total_tokens = monthly_tokens * token_factor

    st.markdown("### Cost and CO2 for one model")

    col_model, _ = st.columns(2)
    with col_model:
        model_choice = st.selectbox("Model", df["model_name"].tolist())

    row = df[df["model_name"] == model_choice].iloc[0]
    multiplier = total_tokens / TOKENS

    est_cost = row["usd_per_million_tokens"] * multiplier
    est_co2_kg = (row["co2_g_per_million_tokens"] * multiplier) / 1000.0

    c1, c2 = st.columns(2)
    c1.metric(f"{period} cost (USD)", f"{est_cost:,.2f}")
    c2.metric(f"{period} CO2 (kg)", f"{est_co2_kg:,.2f}")

    st.markdown("---")
    st.markdown("### Compare two models to see savings")

    colx1, colx2 = st.columns(2)
    with colx1:
        base_model = st.selectbox(
            "Current or larger model", df["model_name"].tolist(), key="base_model"
        )
    with colx2:
        compare_model = st.selectbox(
            "Alternative or smaller model", df["model_name"].tolist(), key="compare_model"
        )

    base_row = df[df["model_name"] == base_model].iloc[0]
    compare_row = df[df["model_name"] == compare_model].iloc[0]

    base_cost = base_row["usd_per_million_tokens"] * multiplier
    compare_cost = compare_row["usd_per_million_tokens"] * multiplier

    money_saved = base_cost - compare_cost
    percent_saved = money_saved / base_cost if base_cost > 0 else 0

    base_co2 = (base_row["co2_g_per_million_tokens"] * multiplier) / 1000.0
    compare_co2 = (compare_row["co2_g_per_million_tokens"] * mu*
