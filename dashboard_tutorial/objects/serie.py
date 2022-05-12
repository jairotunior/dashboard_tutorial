
class Serie:
    def __init__(self, **kwargs):
        self.serie_id = kwargs.pop('serie_id', None)
        self.serie_name = kwargs.pop('serie_name', None)
        self.column = kwargs.pop('column', None)
        self.freq = kwargs.pop('freq', None)
        self.units = kwargs.pop('units', None)
        self.source = kwargs.pop('source', None)
        self.units_show = kwargs.pop('units_show', self.units)

        self.analysis = kwargs.pop('analysis', None)
        self.manager = self.analysis.manager

    def update(self, transform_name, **kwargs):
        is_updated = False

        for t in self.manager.transformers.all():
            if t.name == transform_name:
                self.column = "{}{}".format(self.serie_id, t.suffix)
                print(t.name, self.column)
                self.units_show = t.units_show
                is_updated = True

        if not is_updated:
            self.column = self.serie_id
            self.units_show = self.units

    def get_data_representation(self):
        return {
            "parent": self.analysis.name,
            "serie_id": self.serie_id,
            "serie_name": self.serie_name,
            "column": self.column,
            "units": self.units,
            "units_show": self.units_show,
            "freq": self.freq,
            "source": self.source,
        }
