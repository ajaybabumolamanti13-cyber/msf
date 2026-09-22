from sqlalchemy.orm import Session
from .. import models


def calculate_evidence_priority(db: Session, evidence_id: int):
    evidence = db.query(models.Evidence).filter(models.Evidence.id == evidence_id).first()
    if not evidence:
        return {'priority': 'LOW', 'reason': 'No evidence found'}
    score = 0
    if evidence.evidence_type in {'SMS', 'Call Log', 'Location', 'Application Activity'}:
        score += 2
    score += 1
    if score >= 3:
        priority = 'HIGH'
        reason = 'Strong relevance and artifact relationship'
    elif score == 2:
        priority = 'MEDIUM'
        reason = 'Moderate relevance; investigate further'
    else:
        priority = 'LOW'
        reason = 'Limited evidence significance'
    return {'priority': priority, 'reason': 'Evidence priority is an analytical aid and does not establish criminal activity.' + ' ' + reason, 'evidence_id': evidence_id}
