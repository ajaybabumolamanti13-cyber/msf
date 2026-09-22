from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..ai.anomaly_detection import run_isolation_forest
from .. import models

router = APIRouter(prefix="/analysis", tags=["analysis"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/run')
def run_analysis():
    result = run_isolation_forest()
    return result


@router.get('/findings')
def list_findings(db: Session = Depends(get_db)):
    rows = db.query(models.AIFinding).all()
    return [{'finding_id': r.finding_id, 'artifact_type': r.artifact_type, 'timestamp': r.timestamp.isoformat() if r.timestamp else None, 'reason': r.reason, 'anomaly_score': r.anomaly_score, 'related_evidence': r.related_evidence, 'status': r.status} for r in rows]
