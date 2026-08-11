import numpy as np
import pandas as pd

from features.session import build_session_features


def test_build_session_features_handles_range_index():
    df = pd.DataFrame(
        {"close": [1.0, 2.0, 3.0]},
        index=pd.RangeIndex(3),
    )

    feat = build_session_features(df)

    assert list(feat.columns) == ["hour", "weekday", "month", "asian", "london", "newyork", "overlap"]
    assert feat["hour"].tolist() == [0, 0, 0]
    assert feat["weekday"].tolist() == [0, 0, 0]
    assert feat["month"].tolist() == [0, 0, 0]
    assert feat["asian"].tolist() == [1, 1, 1]
    assert feat["london"].tolist() == [0, 0, 0]
    assert feat["newyork"].tolist() == [0, 0, 0]
    assert feat["overlap"].tolist() == [0, 0, 0]
