# Mobile Forensic Intelligence System (MFIS)

MFIS is an academic prototype for mobile forensic investigation workflows. It supports case management, device intake, evidence import, artifact parsing, AI-assisted anomaly detection, correlation, timeline review, and report generation using a local SQLite database and a FastAPI backend.

## Features
- Case management with SQLite persistence
- Android device detection through ADB (demo-safe fallback)
- Evidence import via CSV/JSON/SQLite/demo dataset
- Artifact review for SMS, calls, GPS, applications, and social data
- AI anomaly detection based on Isolation Forest
- Cross-artifact correlation and evidence prioritization
- Timeline and reporting modules
- Audit logging and integrity tracking

## Tech Stack
- Backend: Python, FastAPI
- Database: SQLite
- AI/ML: Pandas, NumPy, scikit-learn
- Report generation: ReportLab
- Frontend: HTML, CSS, JavaScript, Bootstrap

## Folder Structure
- backend/
- frontend/
- data/
- reports/
- tests/
- requirements.txt

## Setup

### Windows / VS Code
```powershell
cd "C:\Users\mamatha manigala\OneDrive\Desktop\mahitha project"
python -m venv venv
venv\Scripts\activate
pip install -r MFIS\requirements.txt
```

## Run backend
```powershell
cd "C:\Users\mamatha manigala\OneDrive\Desktop\mahitha project"
venv\Scripts\python.exe -m uvicorn MFIS.backend.main:app --reload --port 8000
```

Open:
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/frontend/index.html

## Database initialization and demo data
```powershell
cd "C:\Users\mamatha manigala\OneDrive\Desktop\mahitha project"
venv\Scripts\python.exe -m MFIS.backend.seed_demo_data
```

## Notes
- ADB is optional and only used for Android device discovery.
- Demo data is clearly labeled as synthetic.
- AI findings are investigative aids only and not proof of criminality.
- The project is designed as an academic prototype using authorized forensic data only.
