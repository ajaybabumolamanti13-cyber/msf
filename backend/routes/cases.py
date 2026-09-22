from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import SessionLocal

router = APIRouter(prefix="/cases", tags=["cases"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/', response_model=schemas.CaseOut)
def create_case(case: schemas.CaseCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Case).filter(models.Case.case_id == case.case_id).first()
    if existing:
        raise HTTPException(status_code=400, detail='Case ID already exists')
    db_case = models.Case(
        case_id=case.case_id,
        name=case.name,
        investigator=case.investigator,
        description=case.description,
        status=case.status
    )
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case

@router.get('/', response_model=list[schemas.CaseOut])
def list_cases(db: Session = Depends(get_db)):
    cases = db.query(models.Case).order_by(models.Case.created_at.desc()).all()
    return cases

@router.get('/{case_id}', response_model=schemas.CaseOut)
def get_case(case_id: int, db: Session = Depends(get_db)):
    c = db.query(models.Case).filter(models.Case.id == case_id).first()
    if not c:
        raise HTTPException(status_code=404, detail='Case not found')
    return c

@router.delete('/{case_id}')
def delete_case(case_id: int, db: Session = Depends(get_db)):
    c = db.query(models.Case).filter(models.Case.id == case_id).first()
    if not c:
        raise HTTPException(status_code=404, detail='Case not found')
    db.delete(c)
    db.commit()
    return {'detail': 'deleted'}
