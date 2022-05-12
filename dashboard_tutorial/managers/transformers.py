from dashboard_tutorial.managers.manager import BaseManager

class ManagerTransformer(BaseManager):
    def __init__(self, **kwargs):
        super().__init__(name="Transformers", **kwargs)
