import pandas as pd
import numpy as np
from dashboard_tutorial.transformers import Transformation

class Differentiation(Transformation):

    def __init__(self, **kwargs):
        self.periods = kwargs.pop('periods', 1)
        name = kwargs.get('name', "Differentiation")
        suffix = kwargs.get('suffix', "diff")
        super().__init__(name=name, suffix=suffix, **kwargs)

    def transform(self, series, **kwargs):
        return series.diff(periods=self.periods)