#!/usr/bin/env bash
set -e

# 1) Start Ollama server in the background
ollama serve &

# 2) Wait for Ollama to be ready
echo "Waiting for Ollama server..."
until curl -s http://localhost:11434/api/tags >/dev/null 2>&1; do
  sleep 2
done
echo "Ollama server is up."

# 3) Ensure the model is available (pull if missing)
#    You can change model name here if you switch models later
ollama list | grep "llama3.2:3b" >/dev/null 2>&1 || ollama pull llama3.2:3b

# 4) Start the Streamlit app
echo "Starting Streamlit..."
streamlit run chat_app.py --server.port=8501 --server.address=0.0.0.0