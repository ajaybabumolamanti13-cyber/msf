from pathlib import Path
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database import init_db
from .routes import cases, devices, evidence, artifacts, analysis, timeline, reports

app = FastAPI(title='MFIS - Mobile Forensic Intelligence System')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
def startup():
    init_db()

app.include_router(cases.router, prefix='/api')
app.include_router(devices.router, prefix='/api')
app.include_router(evidence.router, prefix='/api')
app.include_router(artifacts.router, prefix='/api')
app.include_router(analysis.router, prefix='/api')
app.include_router(timeline.router, prefix='/api')
app.include_router(reports.router, prefix='/api')

@app.get('/')
def root():
    return {'status': 'MFIS backend running'}

# Serve frontend static files only in local development
FRONTEND_DIR = Path(__file__).resolve().parent.parent / 'frontend'
if FRONTEND_DIR.exists():
    app.mount('/css', StaticFiles(directory=str(FRONTEND_DIR / 'css')), name='css')
    app.mount('/js', StaticFiles(directory=str(FRONTEND_DIR / 'js')), name='js')
    app.mount('/pages', StaticFiles(directory=str(FRONTEND_DIR / 'pages')), name='pages')

    @app.get('/frontend/{path:path}')
    def frontend_file(path: str):
        file_path = FRONTEND_DIR / path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIR / 'index.html')

