import pandas as pd
import numpy as np
from dashboard_tutorial.transformers import Transformation


class FractionalDifferentiationFFD(Transformation):

    def __init__(self, **kwargs):
        name = kwargs.get('name', "Fractional Differentiation FFD")
        suffix = kwargs.get('suffix', "ffddiff")
        self.d = kwargs.pop('d', 0.4)
        self.thres = kwargs.pop('thres', 1e-5)
        super().__init__(name=name, suffix=suffix, **kwargs)

    def _get_weights_ffd(self, d, thres):
        w, k = [1.], 1
        while True:
            w_ = -w[-1] / k * (d - k + 1)
            if abs(w_) < thres:
                break
            w.append(w_)
            k += 1
        return np.array(w[::-1]).reshape(-1, 1)

    def transform(self, series, **kwargs):
        # 1. Compute weights for the longest series
        w = self._get_weights_ffd(self.d, self.thres)
        width = len(w) - 1

        seriesF, df_ = series.fillna(method='ffill').dropna(), pd.Series(index=series.index, dtype=float)
        for iloc1 in range(width, seriesF.shape[0]):
            loc0, loc1 = seriesF.index[iloc1 - width], seriesF.index[iloc1]
            if not np.isfinite(series.loc[loc1]):
                continue
            # Exclude NAs
            df_[loc1] = np.dot(w.T, seriesF.loc[loc0:loc1])[0]
        return df_