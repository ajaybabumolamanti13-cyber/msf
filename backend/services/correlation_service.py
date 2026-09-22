from sqlalchemy.orm import Session
from .. import models


def correlate_events(db: Session, case_id: int = None):
    results = []
    sms_rows = db.query(models.SMSMessage).all()
    call_rows = db.query(models.CallLog).all()
    for sms in sms_rows:
        for call in call_rows:
            if sms.device_id == call.device_id and abs((sms.timestamp - call.timestamp).total_seconds()) < 3600:
                results.append({'type': 'SMS + Call', 'device_id': sms.device_id, 'detail': f'{sms.sender}->{sms.receiver} and {call.phone_number}'} )
    locations = db.query(models.Location).all()
    for loc in locations:
        if loc.device_id is not None:
            results.append({'type': 'GPS + Timestamp', 'device_id': loc.device_id, 'detail': f'Location {loc.latitude},{loc.longitude} at {loc.timestamp}'})
    return results
