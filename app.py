import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
# Load data & pre-compute metrics
# ================================
df = pd.read_csv("summary_data.csv")
df["roi_sustainability_score"] = df["roi_tokens_per_dollar"] / df["co2_g"]

TOKENS = 1_000_000
df["usd_per_million_tokens"] = TOKENS / df["roi_tokens_per_dollar"]
df["co2_g_per_million_tokens"] = df["co2_g"] / df["roi_tokens_per_dollar"] * TOKENS

# performance "power" proxy
power_map = {
    "gemma:2b": 1,
    "gemma:7b": 2,
    "codellama:7b": 2,
    "llama3": 2,
    "codellama:70b": 3,
    "llama3:70b": 3,
}
df["power_score"] = df["model_name"].map(power_map).fillna(1)

# convenience subsets
small_models = df[df["power_score"] <= 2]
large_models = df[df["power_score"] == 3]

# choose a default small + large model (you can change these names if needed)
default_small = "gemma:2b"
default_large = "codellama:70b"

# ================================
# Dashboard Tabs (decision focus)
# ================================
tab1, tab2, tab3 = st.tabs(
    ["Tiered Model Routing Planner", "OPEX & CO₂ Forecasting", "Model Selector"]
)

# -------------- TAB 1 --------------
with tab1:
    st.subheader("Tiered Model Routing Planner")

    st.write(
        "Use this planner to estimate the impact of **tiered routing**: "
        "sending most workloads to a small model and reserving large models "
        "for high-complexity queries. This directly connects to Business "
        "Insight #1: smaller models can handle ~70–85% of enterprise workloads."
    )

    col_a, col_b = st.columns(2)

    with col_a:
        small_choice = st.selectbox(
            "Smaller / efficient model (default for everyday tasks)",
            options=small_models["model_name"].tolist(),
            index=list(small_models["model_name"]).index(default_small)
            if default_small in list(small_models["model_name"]) else 0,
        )

    with col_b:
        large_choice = st.selectbox(
            "Large / high-power model (for complex queries)",
            options=large_models["model_name"].tolist(),
            index=list(large_models["model_name"]).index(default_large)
            if default_large in list(large_models["model_name"]) else 0,
        )

    # % of workloads routed to small model
    st.markdown("### Workload split")
    routing_mode = st.radio(
        "Choose a routing strategy (you can still fine-tune the slider):",
        [
            "Conservative: 60% small / 40% large",
            "Balanced: 75% small / 25% large",
            "Aggressive: 85% small / 15% large",
            "Custom split",
        ],
    )

    if routing_mode.startswith("Conservative"):
        initial_share = 0.60
    elif routing_mode.startswith("Balanced"):
        initial_share = 0.75
    elif routing_mode.startswith("Aggressive"):
        initial_share = 0.85
    else:
        initial_share = 0.75

    small_share = st.slider(
        "Percentage of workloads handled by the small model",
        0.0,
        1.0,
        initial_share,
        step=0.05,
        format="%.0f",
    )

    st.caption(
        "Example: 0.75 means ~75% of enterprise workloads (summarization, support, "
        "basic analytics) go to the small model; the remaining 25% use the large model."
    )

    monthly_tokens = st.number_input(
        "Estimated monthly token volume",
        min_value=1_000_000,
        value=10_000_000,
        step=1_000_000,
    )

    # look up model rows
    small_row = df[df["model_name"] == small_choice].iloc[0]
    large_row = df[df["model_name"] == large_choice].iloc[0]

    # workload split
    small_tokens = monthly_tokens * small_share
    large_tokens = monthly_tokens * (1 - small_share)

    # costs & CO2 for tiered routing
    small_factor = small_tokens / TOKENS
    large_factor = large_tokens / TOKENS

    tiered_cost = (
        small_factor * small_row["usd_per_million_tokens"]
        + large_factor * large_row["usd_per_million_tokens"]
    )
    tiered_co2_g = (
        small_factor * small_row["co2_g_per_million_tokens"]
        + large_factor * large_row["co2_g_per_million_tokens"]
    )
    tiered_co2_kg = tiered_co2_g / 1000.0

    # baseline: always use large model for 100% workloads
    baseline_factor = monthly_tokens / TOKENS
    baseline_cost = baseline_factor * large_row["usd_per_million_tokens"]
    baseline_co2_g = baseline_factor * large_row["co2_g_per_million_tokens"]
    baseline_co2_kg = baseline_co2_g / 1000.0

    cost_savings = baseline_cost - tiered_cost
    co2_savings_kg = baseline_co2_kg - tiered_co2_kg

    st.markdown("### Impact of Tiered Routing (vs. all-large-model baseline)")

    c1, c2, c3 = st.columns(3)
    c1.metric(
        "Tiered routing monthly cost (USD)",
        f"{tiered_cost:,.2f}",
    )
    c2.metric(
        "All-large-model monthly cost (USD)",
        f"{baseline_cost:,.2f}",
    )
    c3.metric(
        "Monthly cost savings",
        f"{cost_savings:,.2f}",
        delta=f"{(cost_savings / baseline_cost):.0%}" if baseline_cost > 0 else None,
    )

    d1, d2, d3 = st.columns(3)
    d1.metric(
        "Tiered routing monthly CO₂ (kg)",
        f"{tiered_co2_kg:,.1f}",
    )
    d2.metric(
        "All-large-model monthly CO₂ (kg)",
        f"{baseline_co2_kg:,.1f}",
    )
    d3.metric(
        "Monthly CO₂ savings (kg)",
        f"{co2_savings_kg:,.1f}",
    )

    st.info(
        "This directly supports Business Insight #1: by routing ~70–85% of workloads to the "
        f"{small_choice} model and reserving {large_choice} for complex queries, "
        "organizations can significantly reduce both OPEX and emissions."
    )

# -------------- TAB 2 --------------
with tab2:
    st.subheader("OPEX & CO₂ Forecasting")

    st.write(
        "This tab links to Business Insight #2. It allows KPMG or a client to forecast "
        "annual OPEX and emissions based on a chosen model and token volume."
    )

    col1, col2 = st.columns(2)
    with col1:
        forecast_model = st.selectbox(
            "Select a single model for this forecast",
            options=df["model_name"].tolist(),
        )
    with col2:
        horizon = st.selectbox(
            "Time horizon",
            options=["Monthly", "Yearly"],
            index=1,
        )

    forecast_tokens = st.number_input(
        f"Estimated {horizon.lower()} token volume",
        min_value=1_000_000,
        value=1_000_000_000 if horizon == "Yearly" else 10_000_000,
        step=1_000_000,
    )

    row = df[df["model_name"] == forecast_model].iloc[0]
    factor = forecast_tokens / TOKENS

    total_cost = factor * row["usd_per_million_tokens"]
    total_co2_g = factor * row["co2_g_per_million_tokens"]
    total_co2_kg = total_co2_g / 1000.0

    st.markdown("### Forecast results")
    f1, f2 = st.columns(2)
    f1.metric(f"{horizon} cost (USD)", f"{total_cost:,.2f}")
    f2.metric(f"{horizon} CO₂ (kg)", f"{total_co2_kg:,.1f}")

    # comparison vs a 2B / 70B pair like in your slide
    st.markdown("---")
    st.markdown(
        "#### Example: Comparing a small vs large model (mirrors the 1B tokens example in the slides)"
    )

    small_ex = df[df["model_name"] == default_small].iloc[0]
    large_ex = df[df["model_name"] == default_large].iloc[0]

    example_tokens = 1_000_000_000  # 1B tokens
    ex_factor = example_tokens / TOKENS

    ex_small_cost = ex_factor * small_ex["usd_per_million_tokens"]
    ex_large_cost = ex_factor * large_ex["usd_per_million_tokens"]
    ex_savings = ex_large_cost - ex_small_cost
    ex_savings_pct = ex_savings / ex_large_cost

    st.write(
        f"- **1B tokens/year with {default_large} →** "
        f"${ex_large_cost:,.0f} cost  \n"
        f"- **Same workload with {default_small} →** "
        f"${ex_small_cost:,.0f} cost  \n"
        f"- **Savings:** ~{ex_savings_pct:.0%}"
    )

    st.caption(
        "These numbers are calculated directly from the cost-per-million-tokens table, "
        "just scaled up to the selected volume."
    )

# -------------- TAB 3 --------------
with tab3:
    st.subheader("Model Selector")

    st.write(
        "This tab turns priorities into a recommendation. It supports conversations like: "
        "*Which model should we standardize on for a given task, given our cost, ESG, and "
        "performance goals?*"
    )

    task_type = st.selectbox(
        "Task type",
        [
            "Summarization / Note-taking",
            "Customer Support Chat",
            "Analytical Report / Data Explanation",
            "Code Generation / Complex Reasoning",
        ],
    )

    st.markdown("**Set your priorities** (0 = don’t care, 1 = care a lot)")
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        cost_pref = st.slider("Cost", 0.0, 1.0, 0.7)
    with col_p2:
        carbon_pref = st.slider("CO₂", 0.0, 1.0, 0.7)
    with col_p3:
        perf_pref = st.slider("Performance", 0.0, 1.0, 0.5)

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
        f"<h3 style='color:{KPMG_BLUE}'>Recommended model: {best_row['model_name']}</h3>",
        unsafe_allow_html=True,
    )

    st.write(
        f"- **Estimated cost:** {best_row['usd_per_million_tokens']:.2e} USD per 1M tokens  \n"
        f"- **CO₂ impact:** {best_row['co2_g_per_million_tokens']:.2e} g per 1M tokens"
    )
    st.write(
        f"- For **{task_type}**, this choice balances your sliders by "
        f"leaning toward a "
        f"{'larger / more powerful' if best_row['power_score'] > 1 else 'smaller / more efficient'} model."
    )

    st.caption(
        "This uses the same underlying metrics as the analysis slides; the only difference is that "
        "we let the stakeholder choose weights to generate a recommended model."
    )
