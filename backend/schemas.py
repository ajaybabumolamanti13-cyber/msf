from pydantic import BaseModel, ConfigDict
from typing import Optional
import datetime

class CaseCreate(BaseModel):
    case_id: str
    name: str
    investigator: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = 'OPEN'

class CaseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    case_id: str
    name: str
    investigator: Optional[str] = None
    description: Optional[str] = None
    status: str
    created_at: datetime.datetime

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
    model_config = ConfigDict(from_attributes=True)

    id: int
    device_id: str
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    os: Optional[str] = None
    os_version: Optional[str] = None
    serial: Optional[str] = None
    connection_status: Optional[str] = None
    case_id: Optional[int] = None

class EvidenceImport(BaseModel):
    evidence_id: str
    case_id: int
    filename: str
    evidence_type: str
    source: Optional[str] = None
    sha256: str

class EvidenceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    evidence_id: str
    case_id: int
    device_id: Optional[int] = None
    filename: str
    evidence_type: str
    source: Optional[str] = None
    sha256: str
    imported_at: datetime.datetime
    status: str

