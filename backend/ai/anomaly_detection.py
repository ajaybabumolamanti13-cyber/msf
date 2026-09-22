import pandas as pd
from sklearn.ensemble import IsolationForest
from ..database import SessionLocal
from .. import models
import uuid

def run_isolation_forest(n_estimators=100):
    db = SessionLocal()
    try:
        # Example features: message count per device, call count per device
        sms = pd.read_sql(db.query(models.SMSMessage).statement, db.bind)
        calls = pd.read_sql(db.query(models.CallLog).statement, db.bind)

        sms_counts = sms.groupby('device_id').size().rename('sms_count')
        call_counts = calls.groupby('device_id').size().rename('call_count')

        df = pd.concat([sms_counts, call_counts], axis=1).fillna(0)
        if df.empty:
            return {'detail': 'no data to analyze'}

        clf = IsolationForest(n_estimators=n_estimators, random_state=42)
        features = df.copy()
        # Fit and score on the same feature set
        labels = clf.fit_predict(features)
        scores = clf.score_samples(features)
        df['label'] = labels
        df['anomaly_score'] = scores

        # Persist findings
        for idx, row in df.iterrows():
            finding = models.AIFinding(
                finding_id=f'AF-{uuid.uuid4().hex[:8]}',
                artifact_type='device_summary',
                timestamp=None,
                reason=f'IsolationForest on device {idx}',
                anomaly_score=float(row['anomaly_score']),
                related_evidence=str(idx)
            )
            db.add(finding)
        db.commit()
        return {'detail': 'analysis complete', 'rows': len(df)}
    finally:
        db.close()
