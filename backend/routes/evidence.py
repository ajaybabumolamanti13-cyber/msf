from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models
import hashlib, os, uuid

router = APIRouter(prefix="/evidence", tags=["evidence"])

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'imported'))
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/')
def list_evidence(db: Session = Depends(get_db)):
    rows = db.query(models.Evidence).all()
    return [{'id': r.id, 'evidence_id': r.evidence_id, 'case_id': r.case_id, 'filename': r.filename, 'evidence_type': r.evidence_type, 'source': r.source, 'sha256': r.sha256, 'status': r.status} for r in rows]


@router.post('/import')
def import_evidence(case_id: int = Form(...), evidence_type: str = Form(...), source: str = Form('upload'), file: UploadFile = File(...)):
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)
    try:
        content = file.file.read()
        with open(path, 'wb') as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to save file: {e}")

    sha256 = hashlib.sha256(content).hexdigest()
    db = next(get_db())
    evidence_id = f"EV-{uuid.uuid4().hex[:8]}"
    ev = models.Evidence(
        evidence_id=evidence_id,
        case_id=case_id,
        filename=filename,
        evidence_type=evidence_type,
        source=source,
        sha256=sha256
    )
    db.add(ev)
    db.commit()
    db.refresh(ev)

    log = models.AuditLog(user='system', action='evidence_imported', case_id=case_id, evidence_id=ev.id)
    db.add(log)
    db.commit()

    return {
        'evidence_id': ev.evidence_id,
        'filename': ev.filename,
        'sha256': ev.sha256,
        'imported_at': ev.imported_at.isoformat()
    }
