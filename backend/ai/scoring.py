def score_features(feature_values):
    total = sum(float(value) for value in feature_values.values())
    return round(min(total / 10.0, 1.0), 4)
