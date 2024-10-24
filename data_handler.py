# data_handler.py

import pandas as pd

class DataHandler:
    def __init__(self, sellers_file, products_file):
        self.sellers_data = pd.read_parquet(sellers_file)
        self.products_data = pd.read_parquet(products_file)

        self.sellers_data['Оновлено'] = pd.to_datetime(self.sellers_data['Оновлено'])
        self.products_data['Оновлено'] = pd.to_datetime(self.products_data['Оновлено'])

        self.sellers_data.set_index('Оновлено', inplace=True)
        self.products_data.set_index('Оновлено', inplace=True)

        self.sellers_data.sort_index(inplace=True)
        self.products_data.sort_index(inplace=True)

    def get_data(self):
        return self.sellers_data, self.products_data
