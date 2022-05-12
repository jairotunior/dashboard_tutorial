import pandas as pd
import numpy as np
from dashboard_tutorial.transformers import Transformation


class PercentageChange(Transformation):

    def __init__(self, **kwargs):
        self.periods = kwargs.pop('periods', 1)
        name = kwargs.pop('name', "Percentage Change")
        suffix = kwargs.pop('suffix', "pct{}".format(self.periods))

        super().__init__(name=name, suffix=suffix, **kwargs)

    def transform(self, series, **kwargs):
        return series.pct_change(periods=self.periods) * 100