from pydantic import BaseModel
from typing import Optional
import datetime

class CaseCreate(BaseModel):
    case_id: str
    name: str
    investigator: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = 'OPEN'

class CaseOut(BaseModel):
    id: int
    case_id: str
    name: str
    investigator: Optional[str]
    description: Optional[str]
    status: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class DeviceCreate(BaseModel):
    device_id: str
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    os: Optional[str] = None
    os_version: Optional[str] = None
    serial: Optional[str] = None
    case_id: Optional[int] = None
    connection_status: Optional[str] = 'CONNECTED'

class DeviceOut(BaseModel):
    id: int
    device_id: str
    manufacturer: Optional[str]
    model: Optional[str]
    os: Optional[str]
    os_version: Optional[str]
    serial: Optional[str]
    connection_status: Optional[str]
    case_id: Optional[int]

    class Config:
        orm_mode = True

class EvidenceImport(BaseModel):
    evidence_id: str
    case_id: int
    filename: str
    evidence_type: str
    source: Optional[str]
    sha256: str

class EvidenceOut(BaseModel):
    id: int
    evidence_id: str
    case_id: int
    device_id: Optional[int]
    filename: str
    evidence_type: str
    source: Optional[str]
    sha256: str
    imported_at: datetime.datetime
    status: str

    class Config:
        orm_mode = True
