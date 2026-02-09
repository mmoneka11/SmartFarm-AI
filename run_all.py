import subprocess
import sys

print("🚀 Starting SmartFarm AI Backend + Frontend...")

# Start FastAPI backend
backend = subprocess.Popen(
    ["uvicorn", "backend.app.main:app", "--reload"],
    cwd="backend", 
    shell=True
)

# Start Streamlit frontend
frontend = subprocess.Popen(
    ["streamlit", "run", "frontend/streamlit_app.py"],
    shell=True
)

backend.wait()
frontend.wait()

