from __future__ import annotations
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import csv
import json
from sqlalchemy.orm import Session
from .. import models

REPORT_DIR = Path(__file__).resolve().parent.parent.parent / 'reports'
REPORT_DIR.mkdir(exist_ok=True)


def generate_forensic_report(db: Session, case_id: int):
    case = db.query(models.Case).filter(models.Case.id == case_id).first() or db.query(models.Case).first()
    if not case:
        return {'error': 'No case found'}
    pdf_path = REPORT_DIR / f'report_{case.case_id}.pdf'
    csv_path = REPORT_DIR / f'report_{case.case_id}.csv'
    json_path = REPORT_DIR / f'report_{case.case_id}.json'

    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.setTitle(f'MFIS Report - {case.case_id}')
    c.drawString(50, 750, f'MFIS REPORT - {case.case_id}')
    c.drawString(50, 730, f'Case: {case.name}')
    c.drawString(50, 710, f'Investigator: {case.investigator or "N/A"}')
    c.drawString(50, 690, 'Disclaimer: Evidence priority is an analytical aid and does not establish criminal activity.')
    c.save()

    rows = db.query(models.SMSMessage).all()
    with csv_path.open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['source', 'sender', 'receiver', 'message'])
        for row in rows:
            writer.writerow(['SMS', row.sender, row.receiver, row.message])

    payload = {'case_id': case.case_id, 'case_name': case.name, 'sms_count': len(rows), 'status': case.status}
    with json_path.open('w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)

    return {'pdf_path': str(pdf_path), 'csv_path': str(csv_path), 'json_path': str(json_path), 'case_id': case.case_id}
