#!/bin/bash

# YOLO Streamlit 

echo "🚀 Starting YOLO Object Detection Streamlit App..."
echo ""

if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not installed, installing dependencies..."
    pip install -r requirements.txt
fi

streamlit run app.py --server.port 8501 --server.address 0.0.0.0
