from pathlib import Path
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

FRONTEND_DIR = Path(__file__).resolve().parent.parent / 'frontend'
if (FRONTEND_DIR / 'css').exists():
    app.mount('/css', StaticFiles(directory=str(FRONTEND_DIR / 'css')), name='css')
if (FRONTEND_DIR / 'js').exists():
    app.mount('/js', StaticFiles(directory=str(FRONTEND_DIR / 'js')), name='js')
if (FRONTEND_DIR / 'pages').exists():
    app.mount('/pages', StaticFiles(directory=str(FRONTEND_DIR / 'pages')), name='pages')

@app.get('/')
def root():
    index_file = FRONTEND_DIR / 'index.html'
    if index_file.is_file():
        return FileResponse(index_file)
    return {'status': 'MFIS backend running'}

@app.get('/frontend/{path:path}')
def frontend_file(path: str):
    file_path = FRONTEND_DIR / path
    if file_path.is_file():
        return FileResponse(file_path)
    return FileResponse(FRONTEND_DIR / 'index.html')
