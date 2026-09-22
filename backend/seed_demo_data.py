import random
import datetime
from .database import SessionLocal, init_db
from . import models

def seed():
    init_db()
    db = SessionLocal()
    try:
        # Create a case
        case = models.Case(case_id='MFIS-2026-001', name='Mobile Device Investigation', investigator='Dr. Research', description='Demo case', status='OPEN')
        db.add(case)
        db.commit()
        db.refresh(case)

        # Devices
        devices = []
        for i in range(2):
            d = models.Device(device_id=f'DEV{i+1}', manufacturer='DemoCorp', model=f'Model-{i+1}', os='Android', os_version='11', serial=f'SN{i+100}', connection_status='DISCONNECTED', case_id=case.id)
            db.add(d)
            devices.append(d)
        db.commit()

        # SMS records (20)
        for i in range(20):
            msg = models.SMSMessage(sender=f'+1000{i}', receiver=f'+2000{i}', message=f'Demo message {i} (DEMO/SYNTHETIC DATA)', timestamp=datetime.datetime.utcnow() - datetime.timedelta(minutes=random.randint(0,5000)), device_id=random.choice(devices).id, source='DEMO')
            db.add(msg)

        # Call logs (15)
        for i in range(15):
            c = models.CallLog(phone_number=f'+3000{i}', contact=f'Contact {i}', direction=random.choice(['INCOMING','OUTGOING','MISSED']), timestamp=datetime.datetime.utcnow() - datetime.timedelta(minutes=random.randint(0,5000)), duration=random.randint(10,300), device_id=random.choice(devices).id)
            db.add(c)

        # Locations (20)
        for i in range(20):
            loc = models.Location(latitude=37.0 + random.random(), longitude=-122.0 - random.random(), timestamp=datetime.datetime.utcnow() - datetime.timedelta(minutes=random.randint(0,5000)), accuracy=random.uniform(5,50), device_id=random.choice(devices).id, source='DEMO')
            db.add(loc)

        # Application events (15)
        for i in range(15):
            a = models.ApplicationActivity(application=f'app.{i}', event='foreground', timestamp=datetime.datetime.utcnow() - datetime.timedelta(minutes=random.randint(0,5000)), device_id=random.choice(devices).id, source='DEMO')
            db.add(a)

        # Social media artifacts (10)
        for i in range(10):
            s = models.SocialMediaArtifact(platform=random.choice(['Twitter','Facebook','Instagram']), account=f'user{i}', event='post', timestamp=datetime.datetime.utcnow() - datetime.timedelta(minutes=random.randint(0,5000)), content=f'Synthetic social post {i} (DEMO)', source='DEMO')
            db.add(s)

        db.commit()
        print('Seeded demo data')
    finally:
        db.close()

if __name__ == '__main__':
    seed()
