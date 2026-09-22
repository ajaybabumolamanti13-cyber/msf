from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Case(Base):
    __tablename__ = 'cases'
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    investigator = Column(String)
    description = Column(Text)
    status = Column(String, default='OPEN')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    devices = relationship('Device', back_populates='case')

class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    manufacturer = Column(String)
    model = Column(String)
    os = Column(String)
    os_version = Column(String)
    serial = Column(String)
    connection_status = Column(String, default='DISCONNECTED')
    case_id = Column(Integer, ForeignKey('cases.id'))
    case = relationship('Case', back_populates='devices')
    evidence = relationship('Evidence', back_populates='device')

class Evidence(Base):
    __tablename__ = 'evidence'
    id = Column(Integer, primary_key=True, index=True)
    evidence_id = Column(String, unique=True, index=True)
    case_id = Column(Integer, ForeignKey('cases.id'))
    device_id = Column(Integer, ForeignKey('devices.id'), nullable=True)
    filename = Column(String)
    evidence_type = Column(String)
    source = Column(String)
    sha256 = Column(String)
    imported_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default='IMPORTED')
    device = relationship('Device', back_populates='evidence')

class SMSMessage(Base):
    __tablename__ = 'sms_messages'
    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String)
    receiver = Column(String)
    message = Column(Text)
    timestamp = Column(DateTime)
    device_id = Column(Integer, ForeignKey('devices.id'))
    source = Column(String)

class CallLog(Base):
    __tablename__ = 'call_logs'
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String)
    contact = Column(String)
    direction = Column(String)
    timestamp = Column(DateTime)
    duration = Column(Integer)
    device_id = Column(Integer, ForeignKey('devices.id'))

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime)
    accuracy = Column(Float)
    device_id = Column(Integer, ForeignKey('devices.id'))
    source = Column(String)

class DeviceMetadata(Base):
    __tablename__ = 'device_metadata'
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey('devices.id'))
    key = Column(String)
    value = Column(Text)
    timestamp = Column(DateTime)

class TimelineEvent(Base):
    __tablename__ = 'timeline_events'
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey('cases.id'))
    device_id = Column(Integer, ForeignKey('devices.id'))
    artifact_type = Column(String)
    event_type = Column(String)
    description = Column(Text)
    timestamp = Column(DateTime)

class ApplicationActivity(Base):
    __tablename__ = 'application_activity'
    id = Column(Integer, primary_key=True, index=True)
    application = Column(String)
    event = Column(String)
    timestamp = Column(DateTime)
    device_id = Column(Integer, ForeignKey('devices.id'))
    source = Column(String)

class SocialMediaArtifact(Base):
    __tablename__ = 'social_media_artifacts'
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    account = Column(String)
    event = Column(String)
    timestamp = Column(DateTime)
    content = Column(Text)
    source = Column(String)

class AIFinding(Base):
    __tablename__ = 'ai_findings'
    id = Column(Integer, primary_key=True, index=True)
    finding_id = Column(String, unique=True, index=True)
    artifact_type = Column(String)
    timestamp = Column(DateTime)
    reason = Column(Text)
    anomaly_score = Column(Float)
    related_evidence = Column(String)
    status = Column(String, default='Potentially Unusual')

class EvidencePriority(Base):
    __tablename__ = 'evidence_priority'
    id = Column(Integer, primary_key=True, index=True)
    evidence_id = Column(Integer)
    priority = Column(String)
    reason = Column(Text)

class InvestigatorNote(Base):
    __tablename__ = 'investigator_notes'
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    case_id = Column(Integer)
    note = Column(Text)
    timestamp = Column(DateTime)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    action = Column(String)
    case_id = Column(Integer, nullable=True)
    evidence_id = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
