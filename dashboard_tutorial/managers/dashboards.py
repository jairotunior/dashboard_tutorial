import os
import logging
import pandas as pd
from dashboard_tutorial.managers.analysis import ManagerAnalysis
from dashboard_tutorial.managers.sources import ManagerSources
from dashboard_tutorial.managers.transformers import ManagerTransformer
from dashboard_tutorial.objects import Analysis

class ManagerDashboard:
    def __init__(self, path, **kwargs):
        self.path = path
        self.transformers = ManagerTransformer()
        self.sources = ManagerSources()
        self.analysis = ManagerAnalysis()

    def load(self):
        self._load_analysis()

    def add_analysis(self, **kwargs):
        new_analysis = Analysis(manager=self, **kwargs)
        self.analysis.register(new_analysis)
        return new_analysis

    def _load_analysis(self):
        logging.info("[+] Cargando datos...")
        analysis = {}

        # Iterate Analysis Files
        for file in os.listdir(self.path):
            if file.endswith(".pkl"):
                df_analysis = pd.read_pickle(os.path.join(self.path, file))

                name_analysis = file.split('.')[0]

                # 1. Get data of series in Analysis
                list_df_analisis = []
                list_series = []

                # Iterate each one time serie
                for i, s in df_analysis.iterrows():
                    serie_id = s['serie_id']
                    source = s['source']
                    units = s['units']
                    units_show = s['units_show']
                    freq = s['freq']
                    serie_name = s['serie_name']
                    column = s['column']

                    serie_info = {"serie_id": serie_id, "source": source, 'units': units, 'units_show': units_show, 'freq': freq,
                         'serie_name': serie_name, 'column': column}

                    # Add Info Series in List
                    list_series.append(serie_info)

                # 2. Create Analysis Object
                new_analysis = Analysis(analysis_name=name_analysis, manager=self, series_data=list_series)

                # 3. Register Analysis
                self.analysis.register(new_analysis)
