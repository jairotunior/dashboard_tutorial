import re
import quandl
import pandas as pd
import numpy as np
from dashboard_tutorial.sources import Source
import datetime

class QuandlSource(Source):
    def __init__(self, api_key, **kwargs):
        assert api_key, "Favor suministrar una api_key"

        self.api_key = api_key

        name = kwargs.get('name', 'quandl')
        logo = 'https://mms.businesswire.com/media/20210629005397/en/839761/23/Quandl-Wordmark.jpg'
        header_color = 'black'
        header_background = '#2f2f2f'

        super().__init__(name=name, logo=logo, header_color=header_color, header_background=header_background, **kwargs)

        quandl.ApiConfig.api_key = self.api_key

        self.all_series = [
            {"name": "1 YR Yield", "id": "QUS01Y", 'observation_start': "1/1/1990",
             'observation_end': datetime.date.today(), 'frequency': "Daily", 'units': "Percentage",
             'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'USTREASURY/YIELD', 'quandl_column': '1 YR'},
            {"name": "10 YR Yield", "id": "QUS10Y", 'observation_start': "1/1/1990",
             'observation_end': datetime.date.today(), 'frequency': "Daily", 'units': "Percentage",
             'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'USTREASURY/YIELD', 'quandl_column': '10 YR'},
            {"name": "20 YR Yield", "id": "QUS10Y", 'observation_start': "1/1/1990",
             'observation_end': datetime.date.today(), 'frequency': "Daily", 'units': "Percentage",
             'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'USTREASURY/YIELD', 'quandl_column': '20 YR'},
            {"name": "30 YR Yield", "id": "QUS30Y", 'observation_start': "1/1/1990",
             'observation_end': datetime.date.today(), 'frequency': "Daily", 'units': "Percentage",
             'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'USTREASURY/YIELD', 'quandl_column': '30 YR'},
            {"name": "2 YR Yield", "id": "QUS02Y", 'observation_start': "1/1/1990",
             'observation_end': datetime.date.today(), 'frequency': "Daily", 'units': "Percentage",
             'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'USTREASURY/YIELD', 'quandl_column': '2 YR'},
            {"name": "3 YR Yield", "id": "QUS03Y", 'observation_start': "1/1/1990",
             'observation_end': datetime.date.today(), 'frequency': "Daily", 'units': "Percentage",
             'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'USTREASURY/YIELD', 'quandl_column': '3 YR'},
            {"name": "5 YR Yield", "id": "QUS05Y", 'observation_start': "1/1/1990",
             'observation_end': datetime.date.today(), 'frequency': "Daily", 'units': "Percentage",
             'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'USTREASURY/YIELD', 'quandl_column': '5 YR'},

            {"name": "ISM - Services PMI Prices Index", "id": "ISM_NONMAN_PRICES", 'observation_start': "1/7/1997",
             'observation_end': datetime.date.today(), 'frequency': "Monthly", 'units': "Index",
             'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/NONMAN_PRICES', 'quandl_column': 'Diffusion Index'},
            {"name": "ISM - Services PMI Backlog of Orders Index", "id": "ISM_NONMAN_BACKLOG", 'observation_start': "1/7/1997",
             'observation_end': datetime.date.today(), 'frequency': "Monthly", 'units': "Index",
             'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/NONMAN_BACKLOG', 'quandl_column': 'Diffusion Index'},
            {"name": "ISM - Services PMI Business Activity Index", "id": "ISM_NONMAN_BUSACT",
             'observation_start': "1/7/1997", 'observation_end': datetime.date.today(), 'frequency': "Monthly", 'units': "Index",
             'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/NONMAN_BUSACT', 'quandl_column': 'Diffusion Index'},
            {"name": "ISM - Services PMI New Export Orders Index", "id": "ISM_NONMAN_EXPORTS",
             'observation_start': "1/7/1997", 'observation_end': datetime.date.today(), 'frequency': "Monthly",
             'units': "Index", 'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/NONMAN_EXPORTS', 'quandl_column': 'Diffusion Index'},
            {"name": "ISM - Services PMI Imports Index", "id": "ISM_NONMAN_EXPORTS",
             'observation_start': "1/7/1997", 'observation_end': datetime.date.today(), 'frequency': "Monthly",
             'units': "Index", 'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/NONMAN_IMPORTS', 'quandl_column': 'Diffusion Index'},
            {"name": "ISM - Services PMI Inventories Index", "id": "ISM_NONMAN_INVENT",
             'observation_start': "1/7/1997", 'observation_end': datetime.date.today(), 'frequency': "Monthly",
             'units': "Index", 'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/NONMAN_INVENT', 'quandl_column': 'Diffusion Index'},
            {"name": "ISM - Services PMI Inventory Sentiment Index", "id": "ISM_NONMAN_INVSENT",
             'observation_start': "1/7/1997", 'observation_end': datetime.date.today(), 'frequency': "Monthly",
             'units': "Index", 'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/NONMAN_INVSENT', 'quandl_column': 'Diffusion Index'},
            {"name": "ISM - Services PMI Supplier Deliveries Index", "id": "ISM_NONMAN_DELIV",
             'observation_start': "1/1/2002", 'observation_end': datetime.date.today(), 'frequency': "Monthly",
             'units': "Index", 'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/NONMAN_DELIV', 'quandl_column': 'Diffusion Index'},
            {"name": "ISM - Services PMI Employment Index", "id": "ISM_NONMAN_EMPL",
             'observation_start': "1/7/1997", 'observation_end': datetime.date.today(), 'frequency': "Monthly",
             'units': "Index", 'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/NONMAN_EMPL', 'quandl_column': 'Diffusion Index'},
            {"name": "ISM - Services PMI New Orders Index", "id": "ISM_NONMAN_NEWORD",
             'observation_start': "1/7/1997", 'observation_end': datetime.date.today(), 'frequency': "Monthly",
             'units': "Index", 'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/NONMAN_NEWORD', 'quandl_column': 'Diffusion Index'},
            {"name": "ISM - Services PMI Index (Formerly Non-Manufacturing)", "id": "ISM_NONMAN_NMI",
             'observation_start': "1/1/2008",
             'observation_end': datetime.date.today(), 'frequency': "Monthly", 'units': "Index",
             'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/NONMAN_NMI', 'quandl_column': 'Diffusion Index'},

            {"name": "ISM - Manufacturer PMI Composite Prices Index", "id": "ISM_MAN_PMI", 'observation_start': "1/1/1948",
             'observation_end': datetime.date.today(), 'frequency': "Monthly", 'units': "PMI",
             'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/MAN_PMI', 'quandl_column': 'Diffusion Index'},
            {"name": "ISM - Manufacturing Backlog of Orders Index", "id": "ISM_MAN_BACKLOG", 'observation_start': "1/12/1992",
             'observation_end': datetime.date.today(), 'frequency': "Monthly", 'units': "Index",
             'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/MAN_BACKLOG', 'quandl_column': 'Index'},
            {"name": "ISM - Manufacturing New Orders Index", "id": "ISM_MAN_NEWORDERS",
             'observation_start': "1/1/1948", 'observation_end': datetime.date.today(), 'frequency': "Monthly", 'units': "Index",
             'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/MAN_NEWORDERS', 'quandl_column': 'Index'},
            {"name": "ISM - Manufacturing New Export Orders Index", "id": "ISM_MAN_EXPORTS",
             'observation_start': "1/1/1988", 'observation_end': datetime.date.today(), 'frequency': "Monthly",
             'units': "Index", 'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/MAN_EXPORTS', 'quandl_column': 'Index'},
            {"name": "ISM - Manufacturing Production Index", "id": "ISM_MAN_PROD",
             'observation_start': "1/1/1948", 'observation_end': datetime.date.today(), 'frequency': "Monthly",
             'units': "Index", 'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/MAN_PROD', 'quandl_column': 'Index'},
            {"name": "ISM - Manufacturing Employment Index", "id": "ISM_MAN_EMPL",
             'observation_start': "1/1/1948", 'observation_end': datetime.date.today(), 'frequency': "Monthly",
             'units': "Index", 'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/MAN_EMPL', 'quandl_column': 'Index'},
            {"name": "ISM - Manufacturing Supplier Deliveries Index", "id": "ISM_MAN_DELIV",
             'observation_start': "1/6/1976", 'observation_end': datetime.date.today(), 'frequency': "Monthly",
             'units': "Index", 'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/MAN_DELIV', 'quandl_column': 'Index'},
            {"name": "ISM - Manufacturing Inventories Index", "id": "ISM_MAN_INVENT",
             'observation_start': "1/1/1988", 'observation_end': datetime.date.today(), 'frequency': "Monthly",
             'units': "Index", 'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/MAN_INVENT', 'quandl_column': 'Index'},
            {"name": "ISM - Manufacturing Customers' Inventories Index", "id": "ISM_MAN_CUSTINV",
             'observation_start': "1/1/1997", 'observation_end': datetime.date.today(), 'frequency': "Monthly",
             'units': "Index", 'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/MAN_CUSTINV', 'quandl_column': 'Index'},
            {"name": "ISM - Manufacturing Imports Index", "id": "ISM_MAN_IMPORTS",
             'observation_start': "1/10/1989", 'observation_end': datetime.date.today(), 'frequency': "Monthly",
             'units': "Index", 'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'ISM/MAN_IMPORTS', 'quandl_column': 'Index'},

            {"name": "University of Michigan Consumer Survey,Index of Consumer Sentiment", "id": "UMICH_SOC1",
             'observation_start': "1/11/1952", 'observation_end': datetime.date.today(), 'frequency': "Monthly", 'units': "Index",
             'seasonal_adjustment': "", 'notes': '', 'quandl_id': 'UMICH/SOC1', 'quandl_column': 'Index'},
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

        quandl_id = serie_selected['quandl_id']

        df = quandl.get(quandl_id)
        df.index.name = 'date'

        print(df.columns)

        if columns:
            for c in columns:
                column_name = c['name']
                column_type = c['type']
                periods = c['periods']

                if column_type == 'pct':
                    df[column_name] = df['value'].pct_change(periods=periods) * 100

            df = df[[*[c['name'] for c in columns]]]
        else:
            df = df[[serie_selected['quandl_column']]]

        if rename_column:
            df = df.rename(columns={serie_selected['quandl_column']: rename_column})

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