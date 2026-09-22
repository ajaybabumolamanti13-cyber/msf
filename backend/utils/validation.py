from datetime import datetime


def require_fields(payload, required_fields):
    missing = [field for field in required_fields if payload.get(field) in (None, '')]
    if missing:
        raise ValueError(f'Missing required fields: {missing}')


def parse_timestamp(value):
    if value in (None, ''):
        raise ValueError('Timestamp is required')
    try:
        return datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError('Invalid timestamp format. Use ISO 8601.') from exc
