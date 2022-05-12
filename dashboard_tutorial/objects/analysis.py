import os
import re
import random
import logging
import pandas as pd
from bokeh.models import ColumnDataSource, DataRange1d
from dashboard_tutorial.objects import Serie


class Analysis:
    def __init__(self, **kwargs):
        self.name = kwargs.pop('analysis_name', "Default{}".format(str(random.randint(0, 1000))))
        self.series = kwargs.pop('series', []) # A list with Serie Object
        self.series_data = kwargs.pop('series_data', []) # A list dictionary with the serie info
        self.df = kwargs.pop('df', None)
        self.manager = kwargs.pop('manager', None)

        self.start_date = self.end_date = self.x_data_range = self.data_source = None

        if self.df is not None:
            self.start_date = self.df.date.min()
            self.end_date = self.df.date.max()
            self.x_data_range = DataRange1d(start=self.start_date, end=self.end_date)
            self.data_source = ColumnDataSource(self.df)

        if len(self.series_data) > 0:
            self._load_initial_data()
            self.update_data_source()

    def save(self):
        logging.info("[+] Guardando analisis: {}".format(self.name))

        df = None

        for i, s in enumerate(self.series):
            data = s.get_data_representation()

            if i == 0:
                df = pd.DataFrame(data={k: [] for k in data.keys()})

            df = df.append(data, ignore_index=True)

        df.to_pickle(os.path.join(self.manager.path, "{}.pkl".format(self.name)))
        logging.debug("[+] Se ha guardado exitosamente")

    def _set_df(self, df):
        self.df = df
        self.start_date = self.df.date.min()
        self.end_date = self.df.date.max()
        self.x_data_range = DataRange1d(start=self.start_date, end=self.end_date)
        self.data_source = ColumnDataSource(self.df)

    def add_serie(self, **kwargs):
        new_serie = Serie(analysis=self, **kwargs)
        self.series.append(new_serie)
        return new_serie

    def _load_initial_data(self):
        list_df_analisis = []

        for s in self.series_data:
            serie_id = s['serie_id']
            source = s['source']

            current_source = self.manager.sources.get_by_name(name=source)
            df = current_source.get_data_serie(serie_id, rename_column=serie_id)
            list_df_analisis.append(df)

        df_aux = pd.concat(list_df_analisis, axis=1)

        columns = [c for c in df_aux.columns if not re.search("_base$", c)]
        df_aux.loc[:, columns] = df_aux[columns].fillna(method='ffill')

        df_aux = df_aux.reset_index()

        # Set self.df and update related properties
        self._set_df(df_aux)

        for s in self.series_data:
            new_serie = Serie(analysis=self, **s)
            self.series.append(new_serie)


    def _get_data(self, **kwargs):
        serie_id = kwargs.get('serie_id')
        source = kwargs.get('source')

        if self.df is None:
            current_source = self.manager.sources.get_by_name(name=source)
            df_serie = current_source.get_data_serie(serie_id, rename_column=serie_id)

            df = df_serie.reset_index()

            # Set self.df and update related properties
            self._set_df(df)
        else:
            df = self.df
            if not serie_id in df.columns:
                current_source = self.manager.sources.get_by_name(name=source)
                df_serie = current_source.get_data_serie(serie_id, rename_column=serie_id)

                if 'date' in df.columns:
                    df = df.set_index('date')
                    df = pd.concat([df, df_serie], axis=1)

                    columns = [c for c in df.columns if not re.search("_base$", c)]
                    df.loc[:, columns] = df[columns].fillna(method='ffill')
                    df = df.reset_index()

                    # Set self.df and update related properties
                    self._set_df(df)
                else:
                    raise NotImplementedError("No existe la columns fecha.")

    def update_data_source(self):
        # print("**** Analysis Update Data Source *****")
        modification = False
        df = self.df

        for c in self.series:
            column_name = c.column
            serie_id = c.serie_id

            # Download required data
            self._get_data(serie_id=c.serie_id, source=c.source)

            for ot in self.manager.transformers.all():
                if "{}{}".format(serie_id, ot.suffix) == column_name:
                    if not column_name in df.columns:
                        mask = df['{}_base'.format(serie_id)] == 1

                        df.loc[mask, column_name] = ot.transform(series=df.loc[mask][serie_id])

                        columns = [c for c in df.columns if not re.search("_base$", c)]
                        df.loc[:, columns] = df[columns].fillna(method='ffill')

                        modification = True

        if modification:
            self.df = df
            if self.data_source is None:
                self.data_source = ColumnDataSource(self.df)
            else:
                self.data_source.data = self.df
