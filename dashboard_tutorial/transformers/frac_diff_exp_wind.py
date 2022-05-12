import pandas as pd
import numpy as np
from dashboard_tutorial.transformers import Transformation


class FractionalDifferentiationEW(Transformation):

    def __init__(self, **kwargs):
        name = kwargs.get('name', "Fractional Differentiation EW")
        suffix = kwargs.get('suffix', "fdiff")
        self.d = kwargs.pop('d', 0.4)
        self.thres = kwargs.pop('thres', 0.01)
        super().__init__(name=name, suffix=suffix, **kwargs)

    def _get_weights(self, d, size):
        w = [1.]
        for k in range(1, size):
            w_ = -w[-1] / k * (d - k + 1)
            w.append(w_)

        w = np.array(w[::-1]).reshape(-1, 1)
        return w

    def transform(self, series, **kwargs):
        w = self._get_weights(self.d, series.shape[0])
        w_ = np.cumsum(abs(w))
        w_ /= w_[-1]
        skip = w_[w_ > self.thres].shape[0]

        # 2. Apply weights to values
        seriesF, df_ = series.fillna(method='ffill').dropna(), pd.Series(index=series.index, dtype=float)
        for iloc in range(skip, seriesF.shape[0]):
            loc = seriesF.index[iloc]
            if not np.isfinite(series.loc[loc]):
                continue
            df_[loc] = np.dot(w[-(iloc + 1):, :].T, seriesF.loc[:loc])[0]
        return df_