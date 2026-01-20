# import os
# import requests
# import streamlit as st
# import pandas as pd

# # ---------------------------------------------------------------------
# # Config
# # ---------------------------------------------------------------------

# # Base URL for the local LLM API (inside Docker network we call it "llm")
# LLM_API_BASE = os.getenv("LLM_API_BASE", "http://llm:11434")
# DATA_DIR = "data"

# st.set_page_config(page_title="KPMG Local AI Assistant", page_icon="🤖")

# st.title("KPMG Local AI Assistant")
# st.markdown(
#     """
# This assistant runs on a **local AI model** (via Docker) and uses your project files
# from the `data/` folder, including:

# - Background notes (`.txt`)
# - Final presentation (`.txt`)
# - Notebook code/logic (`.py` from Colab export)
# - All CSV datasets (even in nested folders like `dataset1/`, `dataset2/release2025_*`)
# """
# )

# # ---------------------------------------------------------------------
# # Helper functions for loading project data
# # ---------------------------------------------------------------------


# def truncate(text: str, max_chars: int = 4000) -> str:
#     """Trim long documents so we don't blow up the context window."""
#     if len(text) <= max_chars:
#         return text
#     return text[:max_chars] + "\n\n[TRUNCATED]"


# def load_text_data_recursive():
#     """
#     Recursively load all .txt and .py files from data/ and its subfolders.
#     Returns dict: { "relative/path/file": "content" }
#     """
#     texts = {}

#     if not os.path.isdir(DATA_DIR):
#         return texts

#     for root, _, files in os.walk(DATA_DIR):
#         for fname in files:
#             if fname.endswith((".txt", ".py")):
#                 path = os.path.join(root, fname)
#                 rel = os.path.relpath(path, DATA_DIR)
#                 try:
#                     with open(path, "r", encoding="utf-8") as f:
#                         texts[rel] = f.read()
#                 except Exception as e:
#                     texts[rel] = f"[ERROR READING FILE {rel}: {e}]"

#     return texts


# # def load_csv_summaries_recursive(max_rows: int = 3):
# #     """
# #     Recursively load .csv files and return summary strings.
# #     Each summary includes:
# #       - relative path
# #       - shape
# #       - columns
# #       - first few rows
# #     """
# #     summaries = {}

# #     if not os.path.isdir(DATA_DIR):
# #         return summaries

# #     for root, _, files in os.walk(DATA_DIR):
# #         for fname in files:
# #             if fname.endswith(".csv"):
# #                 path = os.path.join(root, fname)
# #                 rel = os.path.relpath(path, DATA_DIR)
# #                 try:
# #                     df = pd.read_csv(path)
# #                     summary_lines = [
# #                         f"File: {rel}",
# #                         f"Shape: {df.shape[0]} rows × {df.shape[1]} columns",
# #                         f"Columns: {list(df.columns)}",
# #                         "",
# #                         f"First {min(max_rows, len(df))} rows:",
# #                         df.head(max_rows).to_markdown(index=False),
# #                     ]
# #                     summaries[rel] = "\n".join(summary_lines)
# #                 except Exception as e:
# #                     summaries[rel] = f"[ERROR READING CSV {rel}: {e}]"

# #     return summaries
# def load_csv_summaries_recursive(max_rows: int = 3):
#     summaries = {}

#     if not os.path.isdir(DATA_DIR):
#         return summaries

#     for root, _, files in os.walk(DATA_DIR):
#         for fname in files:
#             if fname.endswith(".csv"):
#                 path = os.path.join(root, fname)
#                 rel = os.path.relpath(path, DATA_DIR)
#                 try:
#                     df = pd.read_csv(path)

#                     try:
#                         preview = df.head(max_rows).to_markdown(index=False)
#                     except Exception:
#                         # If tabulate is missing, fall back to plain text
#                         preview = df.head(max_rows).to_string(index=False)

#                     summary_lines = [
#                         f"File: {rel}",
#                         f"Shape: {df.shape[0]} rows × {df.shape[1]} columns",
#                         f"Columns: {list(df.columns)}",
#                         "",
#                         f"First {min(max_rows, len(df))} rows:",
#                         preview,
#                     ]
#                     summaries[rel] = "\n".join(summary_lines)
#                 except Exception as e:
#                     summaries[rel] = f"[ERROR READING CSV {rel}: {e}]"

#     return summaries


# @st.cache_data(show_spinner=False)
# def build_project_context():
#     """
#     Build a single big context string from:
#     - all .txt / .py files (background, slides, notebook, etc.)
#     - summaries of all .csv files (even nested)
#     """
#     text_docs = load_text_data_recursive()
#     csv_summaries = load_csv_summaries_recursive()

#     parts = []

#     if text_docs:
#         parts.append("## TEXT DOCUMENTS (notes, presentations, notebook, code)\n")
#         for name, content in text_docs.items():
#             parts.append(f"### {name}\n")
#             parts.append(truncate(content, max_chars=4000))
#             parts.append("\n")

#     if csv_summaries:
#         parts.append("## DATASET SUMMARIES (CSV files)\n")
#         for name, summary in csv_summaries.items():
#             parts.append(f"### {name}\n")
#             parts.append(truncate(summary, max_chars=2000))
#             parts.append("\n")

#     if not parts:
#         return (
#             "No files found in the `data/` folder. "
#             "Add .txt, .py, and .csv files for the assistant to use."
#         )

#     return "\n".join(parts)


# project_context = build_project_context()

# # ---------------------------------------------------------------------
# # Sidebar: model + data status
# # ---------------------------------------------------------------------


# def check_model():
#     try:
#         r = requests.get(f"{LLM_API_BASE}/api/tags", timeout=3)
#         if r.status_code == 200:
#             return True, None
#         else:
#             return False, f"Status code {r.status_code}"
#     except Exception as e:
#         return False, str(e)


# st.sidebar.header("Status")
# ok, err = check_model()
# if ok:
#     st.sidebar.success("Local model service detected ✅")
# else:
#     st.sidebar.error("Local model not responding ⚠️")
#     st.sidebar.write(
#         "Make sure Docker is running and `docker-compose up` is active in this folder."
#     )
#     if err:
#         st.sidebar.caption(f"Details: {err}")

# st.sidebar.subheader("Loaded project context (preview)")
# preview = project_context[:1500]
# if len(project_context) > 1500:
#     preview += "\n\n...[truncated preview]..."
# st.sidebar.text_area("Preview", preview, height=260)

# # ---------------------------------------------------------------------
# # Chat history
# # ---------------------------------------------------------------------

# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {
#             "role": "assistant",
#             "content": (
#                 "Hi, I'm your **local KPMG AI assistant**.\n\n"
#                 "I'm running on a model on this machine (not in the cloud) and I have access "
#                 "to your project files from the `data/` folder (background notes, slides, "
#                 "notebook code, and all datasets). Ask me anything about the project, "
#                 "data, or analysis."
#             ),
#         }
#     ]

# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])

# # ---------------------------------------------------------------------
# # LLM call helper
# # ---------------------------------------------------------------------


# def query_local_model(messages):
#     """
#     messages: list of dicts with 'role' and 'content' (user/assistant/system)
#     """
#     url = f"{LLM_API_BASE}/api/chat"
#     payload = {
#         "model": "llama3.2:3b",  # make sure you've pulled this model in Ollama
#         "messages": messages,
#         "stream": False,
#     }

#     try:
#         resp = requests.post(url, json=payload, timeout=180)
#         resp.raise_for_status()
#         data = resp.json()
#         return data["message"]["content"]
#     except Exception as e:
#         return f"Error talking to local model: {e}"


# # ---------------------------------------------------------------------
# # Chat input + response
# # ---------------------------------------------------------------------

# user_input = st.chat_input(
#     "Ask the assistant about your project, datasets, or analysis..."
# )

# if user_input:
#     # Add user message
#     st.session_state.messages.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     # System prompt with full project context
#     system_prompt = f"""
# You are the **KPMG Local AI Analyst**.

# You run on a local model via Ollama.
# You must use the project context below to answer questions about the KPMG AI Studio
# project, its datasets, analysis, and findings.

# If something is not supported by the context, say you don't know rather than
# inventing details.

# PROJECT CONTEXT START
# ---------------------
# {project_context}
# ---------------------
# PROJECT CONTEXT END
# """

#     model_messages = [{"role": "system", "content": system_prompt}]

#     # Append conversation so far
#     for m in st.session_state.messages:
#         role = m["role"]
#         if role not in ("user", "assistant", "system"):
#             role = "user"
#         model_messages.append({"role": role, "content": m["content"]})

#     # Query local model
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking locally using your project files..."):
#             reply = query_local_model(model_messages)
#             st.markdown(reply)

#     # Save reply
#     st.session_state.messages.append({"role": "assistant", "content": reply})

import os
import requests
import streamlit as st
import pandas as pd

# ---------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------

LLM_API_BASE = os.getenv("LLM_API_BASE", "http://localhost:11434")
DATA_DIR = "data"

st.set_page_config(page_title="KPMG Local AI Assistant", page_icon="🤖")

st.title("KPMG Local AI Assistant")
st.markdown(
    """
This assistant runs on a **local AI model** (via Docker) and uses your project files
from the `data/` folder, including:

- Background notes (`.txt`)
- Final presentation (`.txt`)
- Notebook code/logic (`.py` from Colab export)
- All CSV datasets (even in nested folders like `dataset1/`, `dataset2/release2025_*`)
"""
)

# ---------------------------------------------------------------------
# Helper functions for loading project data
# ---------------------------------------------------------------------


def truncate(text: str, max_chars: int = 4000) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[TRUNCATED]"


def load_text_data_recursive():
    """
    Recursively load all .txt and .py files from data/ and its subfolders.
    Returns dict: { "relative/path/file": "content" }
    """
    texts = {}

    if not os.path.isdir(DATA_DIR):
        return texts

    for root, _, files in os.walk(DATA_DIR):
        for fname in files:
            if fname.endswith((".txt", ".py")):
                path = os.path.join(root, fname)
                rel = os.path.relpath(path, DATA_DIR)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        texts[rel] = f.read()
                except Exception as e:
                    texts[rel] = f"[ERROR READING FILE {rel}: {e}]"

    return texts


def load_csv_summaries_recursive(max_rows: int = 3):
    """
    Recursively load .csv files and return summary strings.
    Each summary includes:
      - relative path
      - shape
      - columns
      - first few rows
    """
    summaries = {}

    if not os.path.isdir(DATA_DIR):
        return summaries

    for root, _, files in os.walk(DATA_DIR):
        for fname in files:
            if fname.endswith(".csv"):
                path = os.path.join(root, fname)
                rel = os.path.relpath(path, DATA_DIR)
                try:
                    df = pd.read_csv(path)

                    # Try markdown preview, fall back to plain text if tabulate isn't available
                    try:
                        preview = df.head(max_rows).to_markdown(index=False)
                    except Exception:
                        preview = df.head(max_rows).to_string(index=False)

                    summary_lines = [
                        f"File: {rel}",
                        f"Shape: {df.shape[0]} rows × {df.shape[1]} columns",
                        f"Columns: {list(df.columns)}",
                        "",
                        f"First {min(max_rows, len(df))} rows:",
                        preview,
                    ]
                    summaries[rel] = "\n".join(summary_lines)
                except Exception as e:
                    summaries[rel] = f"[ERROR READING CSV {rel}: {e}]"

    return summaries


@st.cache_data(show_spinner=False)
def build_project_contexts():
    """
    Returns:
      - full_project_context: string with all docs + csv summaries
      - final_presentation_context: string with only final presentation content
    """
    text_docs = load_text_data_recursive()
    csv_summaries = load_csv_summaries_recursive()

    parts = []
    final_presentation_chunks = []

    # TEXT DOCS
    if text_docs:
        parts.append("## TEXT DOCUMENTS (notes, presentations, notebook, code)\n")
        for name, content in text_docs.items():
            lower = name.lower()
            if "final presentation" in lower:
                final_presentation_chunks.append(f"### {name}\n{content}\n")

            parts.append(f"### {name}\n")
            parts.append(truncate(content, max_chars=4000))
            parts.append("\n")

    # CSV SUMMARIES
    if csv_summaries:
        parts.append("## DATASET SUMMARIES (CSV files)\n")
        for name, summary in csv_summaries.items():
            parts.append(f"### {name}\n")
            parts.append(truncate(summary, max_chars=2000))
            parts.append("\n")

    if not parts:
        full_context = (
            "No files found in the `data/` folder. "
            "Add .txt, .py, and .csv files for the assistant to use."
        )
    else:
        full_context = "\n".join(parts)

    if final_presentation_chunks:
        # Give final presentation a larger budget; it's your main solutions doc
        final_presentation_context = truncate(
            "\n".join(final_presentation_chunks), max_chars=8000
        )
    else:
        final_presentation_context = ""

    return full_context, final_presentation_context


# Build contexts once (cached)
project_context, final_presentation_context = build_project_contexts()

# ---------------------------------------------------------------------
# Sidebar: model + data status
# ---------------------------------------------------------------------


def check_model():
    try:
        r = requests.get(f"{LLM_API_BASE}/api/tags", timeout=3)
        if r.status_code == 200:
            return True, None
        else:
            return False, f"Status code {r.status_code}"
    except Exception as e:
        return False, str(e)


st.sidebar.header("Status")
ok, err = check_model()
if ok:
    st.sidebar.success("Local model service detected ✅")
else:
    st.sidebar.error("Local model not responding ⚠️")
    st.sidebar.write(
        "Make sure Docker is running and `docker compose up` is active in this folder."
    )
    if err:
        st.sidebar.caption(f"Details: {err}")

st.sidebar.subheader("Loaded project context (preview)")
preview = project_context[:1500]
if len(project_context) > 1500:
    preview += "\n\n...[truncated preview]..."
st.sidebar.text_area("Preview", preview, height=260)

if final_presentation_context:
    st.sidebar.success("Final presentation file detected ✅")
else:
    st.sidebar.warning("No file with 'Final Presentation' in its name was found.")

# ---------------------------------------------------------------------
# Chat history
# ---------------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hi, I'm your **local KPMG AI assistant**.\n\n"
                "I'm running on a model on this machine (not in the cloud) and I have access "
                "to your project files from the `data/` folder (background notes, slides, "
                "notebook code, and all datasets). Ask me anything about the project, data, "
                "or analysis. When you ask about our *solutions* or *findings*, I will pay "
                "special attention to the final presentation."
            ),
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------
# LLM call helper
# ---------------------------------------------------------------------


def query_local_model(messages):
    url = f"{LLM_API_BASE}/api/chat"
    payload = {
        "model": "llama3.2:3b",  # or whichever smaller model you pulled
        "messages": messages,
        "stream": False,
    }

    try:
        resp = requests.post(url, json=payload, timeout=180)
        if resp.status_code >= 400:
            return f"Error from LLM API (status {resp.status_code}): {resp.text}"
        data = resp.json()
        return data["message"]["content"]
    except Exception as e:
        return f"Error talking to local model: {e}"


# ---------------------------------------------------------------------
# Chat input + response
# ---------------------------------------------------------------------

user_input = st.chat_input(
    "Ask the assistant about your project, datasets, or analysis..."
)

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # System prompt with FINAL PRESENTATION highlighted
    system_prompt = f"""
You are the **KPMG Local AI Analyst**.

You run on a local model via Ollama.
You must answer questions using the project context provided below.

When the user asks about:
- "solutions"
- "findings"
- "recommendations"
- "final presentation"

you should rely **primarily** on the FINAL PRESENTATION content, and only
supplement it with other documents or dataset summaries as needed.

If something is not supported by the context, say you don't know rather than
inventing details.

================= FINAL PRESENTATION (PRIMARY SOURCE) =================
{final_presentation_context or "No final presentation file was found."}
================= OTHER PROJECT CONTEXT (BACKGROUND + DATA) ===========
{project_context}
======================================================================
"""

    model_messages = [{"role": "system", "content": system_prompt}]

    # Append conversation so far
    for m in st.session_state.messages:
        role = m["role"]
        if role not in ("user", "assistant", "system"):
            role = "user"
        model_messages.append({"role": role, "content": m["content"]})

    # Query local model
    with st.chat_message("assistant"):
        with st.spinner("Thinking locally using your project files..."):
            reply = query_local_model(model_messages)
            st.markdown(reply)

    # Save reply
    st.session_state.messages.append({"role": "assistant", "content": reply})