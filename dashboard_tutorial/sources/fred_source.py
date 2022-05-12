import os
import pandas as pd
import numpy as np
import re
from dashboard_tutorial.sources import Source
from full_fred.fred import Fred

class FREDSource(Source):

    def __init__(self, fred_credentials, **kwargs):
        assert fred_credentials is not None, "Debe suministrar las credenciales correctas"
        assert os.path.exists(fred_credentials), "La ruta suministrada para las credenciales no existe"

        logo = 'https://fred.stlouisfed.org/images/masthead-88h-2x.png'
        header_color = 'black'
        header_background = '#2f2f2f'

        name = kwargs.get('name', 'fred')
        self.fred_credentials = fred_credentials
        self.fred = Fred(self.fred_credentials)

        super().__init__(name=name, logo=logo, header_color=header_color, header_background=header_background, **kwargs)

        self.search_result = []

    def do_search(self, search_word):
        assert type(search_word) is str, "El parametro search_word debe ser str"

        series = self.fred.search_for_series([search_word], limit=20)

        self.search_result = []

        for s in series['seriess']:
            t = {"name": s['title'], "id": s['id'], 'observation_start': s['observation_start'],
                 'observation_end': s['observation_end'], 'frequency': s['frequency'], 'units': s['units'],
                 'seasonal_adjustment': s['seasonal_adjustment'], 'notes': ''}
            self.search_result.append(t)

    def get_data_serie(self, serie_id, columns=None, rename_column=None):
        data = self.fred.get_series_df(serie_id)
        data['date'] = pd.to_datetime(data['date'], format="%Y/%m/%d")
        data['value'].replace(".", np.nan, inplace=True)
        data = data.set_index('date')
        data['value'] = data['value'].astype('float')

        if columns:
            for c in columns:
                column_name = c['name']
                column_type = c['type']
                periods = c['periods']

                if column_type == 'pct':
                    data[column_name] = data['value'].pct_change(periods=periods) * 100

            data = data[[*[c['name'] for c in columns]]]
        else:
            data = data[['value']]

        if rename_column:
            data = data.rename(columns={'value': rename_column})

        serie_data = self.fred.search_for_series([serie_id], limit=20)

        if re.search('Daily*', serie_data['seriess'][0]['frequency']):
            # min_date = df.index.min()
            # max_date = df.index.max()
            # print(pd.date_range(start=min_date, end=max_date, freq=pd.offsets.MonthBegin(1)))
            data = data.resample(pd.offsets.MonthBegin(1)).agg({serie_id: 'last'})
        elif re.search('Week*', serie_data['seriess'][0]['frequency']):
            data = data.resample(pd.offsets.MonthBegin(1)).agg({serie_id: 'last'})

        data.loc[:, "{}_{}".format(serie_id, 'base')] = 1

        return data


    def get_search_results(self):
        return self.search_result