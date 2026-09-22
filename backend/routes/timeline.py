from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models

router = APIRouter(prefix="/timeline", tags=["timeline"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/')
def get_timeline(db: Session = Depends(get_db)):
    events = []
    for row in db.query(models.SMSMessage).all():
        events.append({'timestamp': row.timestamp, 'artifact_type': 'SMS', 'description': f"SMS {row.sender}->{row.receiver}", 'device_id': row.device_id})
    for row in db.query(models.CallLog).all():
        events.append({'timestamp': row.timestamp, 'artifact_type': 'Call', 'description': f"Call {row.phone_number}", 'device_id': row.device_id})
    for row in db.query(models.Location).all():
        events.append({'timestamp': row.timestamp, 'artifact_type': 'Location', 'description': f"Location {row.latitude},{row.longitude}", 'device_id': row.device_id})
    for row in db.query(models.ApplicationActivity).all():
        events.append({'timestamp': row.timestamp, 'artifact_type': 'Application', 'description': f"App {row.application} {row.event}", 'device_id': row.device_id})
    for row in db.query(models.SocialMediaArtifact).all():
        events.append({'timestamp': row.timestamp, 'artifact_type': 'Social Media', 'description': f"{row.platform} {row.event}", 'device_id': None})
    events.sort(key=lambda e: (e['timestamp'] or '', str(e['artifact_type'])))
    return [{'timestamp': e['timestamp'].isoformat() if e['timestamp'] else None, 'artifact_type': e['artifact_type'], 'description': e['description'], 'device_id': e['device_id']} for e in events]
