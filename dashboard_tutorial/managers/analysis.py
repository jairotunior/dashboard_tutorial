from abc import ABC
from dashboard_tutorial.managers.manager import BaseManager

class ManagerAnalysis(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(name="Analysis", **kwargs)
