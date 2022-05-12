import os
import pandas as pd
import numpy as np
import datetime
import re
from dashboard_tutorial.sources import Source

class FileSource(Source):
    def __init__(self, dir, **kwargs):
        assert dir, "Debe definir el parametro dir."
        assert os.path.exists(dir), "La ruta suministrada para los dataset no existe."

        self.dir = dir

        name = kwargs.get('name', 'file')
        logo = 'https://fred.stlouisfed.org/images/masthead-88h-2x.png'
        header_color = 'black'
        header_background = '#2f2f2f'

        super().__init__(name=name, logo=logo, header_color=header_color, header_background=header_background, **kwargs)

        self.all_series = [
            {"name": "1 YR Yield", "id": "US01Y", 'observation_start': "1/1/1929",
             'observation_end': '31/12/1989', 'frequency': "Monthly", 'units': "Percentage",
             'seasonal_adjustment': "", 'notes': '', 'file_name': 'one.csv', 'format': 'csv', 'column_file': '1 YR', 'sep': ';'},
            {"name": "10 YR Yield", "id": "US10Y", 'observation_start': "1/1/1929",
             'observation_end': '31/12/1989', 'frequency': "Monthly", 'units': "Percentage",
             'seasonal_adjustment': "", 'notes': '', 'file_name': 'ten_yr_long.csv', 'format': 'csv', 'column_file': '10 YR', 'sep': ';'},
            {"name": "5 YR Yield", "id": "US05Y", 'observation_start': "1/1/1929",
             'observation_end': '31/12/1989', 'frequency': "Monthly", 'units': "Percentage",
             'seasonal_adjustment': "", 'notes': '', 'file_name': 'five.csv', 'format': 'csv', 'column_file': '5 YR', 'sep': ';'},
            {"name": "3 YR Yield", "id": "US03Y", 'observation_start': "1/1/1929",
             'observation_end': '31/12/1989', 'frequency': "Monthly", 'units': "Percentage",
             'seasonal_adjustment': "", 'notes': '', 'file_name': 'three.csv', 'format': 'csv', 'column_file': '3 YR', 'sep': ';'},
            {"name": "20 YR Yield", "id": "US20Y", 'observation_start': "1/1/1929",
             'observation_end': '31/12/1989', 'frequency': "Monthly", 'units': "Percentage",
             'seasonal_adjustment': "", 'notes': '', 'file_name': 'twenty.csv', 'format': 'csv', 'column_file': '20 YR', 'sep': ';'},
        ]

        self.search_result = []

    def do_search(self, search_word):
        assert type(search_word) is str, "El parametro search_word debe ser type str"

        self.search_result = [s for s in self.all_series if len(re.findall(search_word, s['name'].lower())) > 0]

    def get_data_serie(self, serie_id, columns=None, rename_column=None):
        serie_selected = None

        for s in self.all_series:
            if s['id'] == serie_id:
                serie_selected = s
                break

        filename = serie_selected['file_name']

        df = None

        if serie_selected['format'] == 'xlsx':
            df = pd.read_excel(os.path.join(self.dir, filename))
        elif serie_selected['format'] == 'csv':
            df = pd.read_csv(os.path.join(self.dir, filename), sep=serie_selected['sep'])

        df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
        df.rename(columns={'Date': 'date'}, inplace=True)
        df = df.set_index('date')

        if columns:
            for c in columns:
                column_name = c['name']
                column_type = c['type']
                periods = c['periods']

                if column_type == 'pct':
                    df[column_name] = df['value'].pct_change(periods=periods) * 100

            df = df[[*[c['name'] for c in columns]]]
        else:
            df = df[[serie_selected['column_file']]]

        if rename_column:
            df = df.rename(columns={serie_selected['column_file']: rename_column})

        #return df

        if re.search('Daily*', serie_selected['frequency']):
            # min_date = df.index.min()
            # max_date = df.index.max()
            # print(pd.date_range(start=min_date, end=max_date, freq=pd.offsets.MonthBegin(1)))
            df = df.resample(pd.offsets.MonthBegin(1)).agg({serie_id: 'last'})
        elif re.search('Week*', serie_selected['frequency']):
            df = df.resample(pd.offsets.MonthBegin(1)).agg({serie_id: 'last'})

        df.loc[:, "{}_{}".format(serie_id, 'base')] = 1

        return df

    def get_search_results(self):
        return self.search_result