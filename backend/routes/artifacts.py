from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models

router = APIRouter(prefix="/artifacts", tags=["artifacts"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/sms')
def list_sms(db: Session = Depends(get_db)):
    rows = db.query(models.SMSMessage).all()
    return [{'id': r.id, 'sender': r.sender, 'receiver': r.receiver, 'message': r.message, 'timestamp': r.timestamp.isoformat() if r.timestamp else None, 'device_id': r.device_id, 'source': r.source} for r in rows]


@router.get('/calls')
def list_calls(db: Session = Depends(get_db)):
    rows = db.query(models.CallLog).all()
    return [{'id': r.id, 'phone_number': r.phone_number, 'contact': r.contact, 'direction': r.direction, 'timestamp': r.timestamp.isoformat() if r.timestamp else None, 'duration': r.duration, 'device_id': r.device_id} for r in rows]


@router.get('/locations')
def list_locations(db: Session = Depends(get_db)):
    rows = db.query(models.Location).all()
    return [{'id': r.id, 'latitude': r.latitude, 'longitude': r.longitude, 'timestamp': r.timestamp.isoformat() if r.timestamp else None, 'accuracy': r.accuracy, 'device_id': r.device_id, 'source': r.source} for r in rows]


@router.get('/applications')
def list_applications(db: Session = Depends(get_db)):
    rows = db.query(models.ApplicationActivity).all()
    return [{'id': r.id, 'application': r.application, 'event': r.event, 'timestamp': r.timestamp.isoformat() if r.timestamp else None, 'device_id': r.device_id, 'source': r.source} for r in rows]


@router.get('/social')
def list_social(db: Session = Depends(get_db)):
    rows = db.query(models.SocialMediaArtifact).all()
    return [{'id': r.id, 'platform': r.platform, 'account': r.account, 'event': r.event, 'timestamp': r.timestamp.isoformat() if r.timestamp else None, 'content': r.content, 'source': r.source} for r in rows]


@router.get('/summary')
def summary(db: Session = Depends(get_db)):
    return {
        'sms': db.query(models.SMSMessage).count(),
        'calls': db.query(models.CallLog).count(),
        'locations': db.query(models.Location).count(),
        'applications': db.query(models.ApplicationActivity).count(),
        'social': db.query(models.SocialMediaArtifact).count(),
    }
