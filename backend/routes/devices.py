from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..services.adb_service import detect_devices, get_device_info
from .. import models, schemas

router = APIRouter(prefix="/devices", tags=["devices"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/scan')
def scan_devices():
    return detect_devices()


@router.get('/info/{device_id}')
def device_info(device_id: str):
    return get_device_info(device_id)


@router.get('/')
def list_devices(db: Session = Depends(get_db)):
    items = db.query(models.Device).all()
    return [{'id': it.id, 'device_id': it.device_id, 'manufacturer': it.manufacturer, 'model': it.model, 'os': it.os, 'os_version': it.os_version, 'serial': it.serial, 'connection_status': it.connection_status, 'case_id': it.case_id} for it in items]


@router.post('/')
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Device).filter(models.Device.device_id == device.device_id).first()
    if existing:
        raise HTTPException(status_code=400, detail='Device already exists')
    item = models.Device(**device.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
