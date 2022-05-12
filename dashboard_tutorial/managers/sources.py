from dashboard_tutorial.managers.manager import BaseManager

class ManagerSources(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(name="Sources", **kwargs)
