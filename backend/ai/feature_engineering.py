import pandas as pd


def build_feature_frame(sms_df, calls_df, locations_df, app_df):
    if sms_df is None:
        sms_df = pd.DataFrame(columns=['device_id', 'timestamp'])
    if calls_df is None:
        calls_df = pd.DataFrame(columns=['device_id', 'timestamp'])
    if locations_df is None:
        locations_df = pd.DataFrame(columns=['device_id', 'timestamp'])
    if app_df is None:
        app_df = pd.DataFrame(columns=['device_id', 'timestamp'])

    features = {
        'sms_count': len(sms_df),
        'call_count': len(calls_df),
        'location_count': len(locations_df),
        'app_count': len(app_df),
    }
    return pd.DataFrame([features])
