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

# ---------------------------
# GLOBAL CSS
# ---------------------------
st.markdown(
    f"""
    <style>
        /* Background */
        .stApp {{
            background: radial-gradient(circle at top left, #0b1b4a, #000000);
            font-family: "Arial", sans-serif;
            color: {KPMG_WHITE};
        }}

        /* Zoomed OUT: full width with padding */
        .block-container {{
            max-width: 100% !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            padding-top: 2rem !important;
        }}

        /* Make general paragraph text bright */
        .block-container p {{
            color: white !important;
        }}

        /* Metric numbers */
        .stMetric > div {{
            color: white !important;
        }}

        /* Slider labels + numeric values */
        .stSlider label, .stSlider span {{
            color: white !important;
        }}

        /* Selectbox labels (e.g. "Task type") */
        .stSelectbox label {{
            color: white !important;
        }}

        /* Tabs */
        .stTabs [role="tab"] {{
            background-color: #111827;
            color: white;
            font-weight: 600;
            border-radius: 6px;
            padding: 8px 20px;
        }}
        .stTabs [role="tab"][aria-selected="true"] {{
            background-color: {KPMG_BLUE};
            color: white;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# Load data
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
    "<h1 style='text-align:center; color:white;'>KPMG LLM Decision Support Tool</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center; color:white;'>This tool helps compare models by cost, carbon impact and task fit.</p>",
    unsafe_allow_html=True,
)
st.markdown("")

# ---------------------------
# Tabs
# ---------------------------
tab1, tab2, tab3 = st.tabs(
    ["Model Overview", "Cost, CO2 and Savings", "Task based Recommendation"]
)

# ========================== TAB 1 ==========================
with tab1:
    st.subheader("Model Overview")

    st.write("Use this tab to compare models. Pick a metric and see how they rank.")

    metric = st.selectbox(
        "Metric",
        ["usd_per_million_tokens", "co2_g_per_million_tokens", "roi_tokens_per_dollar"],
        format_func=lambda x: x.replace("_", " ").title(),
    )

    # Smaller, centered bar chart
    left, center, right = st.columns([1, 2, 1])
    with center:
        fig, ax = plt.subplots(figsize=(5, 3))  # smaller figure

        # White chart background so black labels show clearly
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        sns.barplot(
            data=df.sort_values(metric, ascending=False),
            x=metric,
            y="model_name",
            ax=ax,
            color=KPMG_LIGHT_BLUE,
        )

        ax.set_title(f"{metric.replace('_',' ').title()} by Model", color="black", fontsize=12)
        ax.set_xlabel(metric.replace("_", " ").title(), color="black", fontsize=10)
        ax.set_ylabel("Model", color="black", fontsize=10)
        ax.tick_params(colors="black", labelsize=9)
        for s in ax.spines.values():
            s.set_color("black")

        st.pyplot(fig)

    st.caption("Higher bars mean higher cost, emissions or tokens per dollar.")

# ========================== TAB 2 ==========================
with tab2:
    st.subheader("Cost, CO2 and Savings")

    st.write("Estimate cost and CO2 for one model and compare two models to see savings.")

    colA, colB = st.columns(2)
    with colA:
        period = st.selectbox("Time period", ["Monthly", "Quarterly", "Yearly"])
    with colB:
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
    multiplier = total_tokens / TOKENS

    st.markdown("### Cost and CO2 for one model")

    col_model, _ = st.columns(2)
    with col_model:
        model_choice = st.selectbox("Model", df["model_name"].tolist())

    row = df[df["model_name"] == model_choice].iloc[0]

    est_cost = row["usd_per_million_tokens"] * multiplier
    est_co2_kg = (row["co2_g_per_million_tokens"] * multiplier) / 1000.0

    c1, c2 = st.columns(2)
    c1.metric(f"{period} cost (USD)", f"{est_cost:,.2f}")
    c2.metric(f"{period} CO2 (kg)", f"{est_co2_kg:,.2f}")

    st.markdown("---")
    st.markdown("### Compare two models to see savings")

    colX, colY = st.columns(2)
    with colX:
        base_model = st.selectbox(
            "Current or larger model", df["model_name"].tolist(), key="base"
        )
    with colY:
        compare_model = st.selectbox(
            "Alternative or smaller model", df["model_name"].tolist(), key="compare"
        )

    base_row = df[df["model_name"] == base_model].iloc[0]
    comp_row = df[df["model_name"] == compare_model].iloc[0]

    base_cost = base_row["usd_per_million_tokens"] * multiplier
    comp_cost = comp_row["usd_per_million_tokens"] * multiplier
    money_saved = base_cost - comp_cost
    percent_saved = money_saved / base_cost if base_cost > 0 else 0

    base_co2 = (base_row["co2_g_per_million_tokens"] * multiplier) / 1000
    comp_co2 = (comp_row["co2_g_per_million_tokens"] * multiplier) / 1000
    co2_saved = base_co2 - comp_co2

    s1, s2, s3 = st.columns(3)
    s1.metric("Money saved (USD)", f"{money_saved:,.2f}")
    s2.metric("Percent saved", f"{percent_saved:.0%}")
    s3.metric("CO2 saved (kg)", f"{co2_saved:,.2f}")

# ========================== TAB 3 ==========================
with tab3:
    st.subheader("Task based Recommendation")

    st.write(
        "Pick a task and adjust the sliders for cost, carbon and model strength to get a recommendation."
    )

    task_type = st.selectbox(
        "Task type",
        [
            "Summarization and note taking",
            "Customer support chat",
            "Analytical reports and data explanation",
            "Code generation and complex reasoning",
        ],
    )

    st.markdown("**Set priorities** (0 means not important, 1 means very important)")

    c1, c2, c3 = st.columns(3)
    with c1:
        cost_pref = st.slider("Cost", 0.0, 1.0, 0.7)
    with c2:
        carbon_pref = st.slider("Carbon", 0.0, 1.0, 0.7)
    with c3:
        perf_pref = st.slider("Model strength", 0.0, 1.0, 0.5)

    cost_norm = df["usd_per_million_tokens"] / df["usd_per_million_tokens"].max()
    co2_norm = df["co2_g_per_million_tokens"] / df["co2_g_per_million_tokens"].max()
    strength_norm = df["power_score"] / df["power_score"].max()

    df["score"] = (
        cost_pref * (1 - cost_norm)
        + carbon_pref * (1 - co2_norm)
        + perf_pref * strength_norm
    )

    best = df.sort_values("score", ascending=False).iloc[0]

    st.markdown(
        f"<h3 style='color:white;'>Suggested model: {best['model_name']}</h3>",
        unsafe_allow_html=True,
    )

    st.write(
        f"- Cost: {best['usd_per_million_tokens']:.2e} USD per 1M tokens\n"
        f"- CO2: {best['co2_g_per_million_tokens']:.2e} g per 1M tokens\n"
        f"- Strength level: {int(best['power_score'])}"
    )

    st.caption("This model balances your cost, carbon and strength choices.")
