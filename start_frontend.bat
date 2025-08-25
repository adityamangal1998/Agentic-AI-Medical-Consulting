@echo off
echo 🏥 Starting AI Medical Consulting Frontend...
echo.

cd frontend
echo Starting Streamlit app on http://localhost:8501
echo Press Ctrl+C to stop
echo.

python -m streamlit run app.py
