from sqlalchemy.orm import Session
from .. import models


def get_artifact_summary(db: Session):
    return {
        'sms': db.query(models.SMSMessage).count(),
        'calls': db.query(models.CallLog).count(),
        'locations': db.query(models.Location).count(),
        'applications': db.query(models.ApplicationActivity).count(),
        'social_media': db.query(models.SocialMediaArtifact).count(),
    }
