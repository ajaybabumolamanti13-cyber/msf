from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..services.report_service import generate_forensic_report

router = APIRouter(prefix="/reports", tags=["reports"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/generate')
def generate_report(case_id: int = 1, db: Session = Depends(get_db)):
    result = generate_forensic_report(db, case_id)
    return result
