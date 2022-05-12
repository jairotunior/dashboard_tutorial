from abc import ABC

class BaseManager(ABC):
    def __init__(self, **kwargs):
        self.name = ""
        self.elements = {}

    def register(self, element):
        assert element.name not in self.elements, f"Ya existe un {self.name} registrado con ese nombre"

        self.elements[element.name] = element

    def get_by_name(self, name):
        return self.elements[name]

    def get_names(self):
        return self.elements.keys()

    def all(self):
        return [self.elements[k] for k in self.elements.keys()]
