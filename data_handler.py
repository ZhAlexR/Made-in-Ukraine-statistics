import pandas as pd

class DataHandler:
    def __init__(self, sellers_file, products_file):
        self.sellers_data = pd.read_csv(sellers_file, sep=';', encoding='utf-8', on_bad_lines='skip')
        self.products_data = pd.read_csv(products_file, sep=';', encoding='utf-8', on_bad_lines='skip')

        # Parse the 'Оновлено' column as datetime with dayfirst=True
        self.sellers_data['Оновлено'] = pd.to_datetime(self.sellers_data['Оновлено'], dayfirst=True)
        self.products_data['Оновлено'] = pd.to_datetime(self.products_data['Оновлено'], dayfirst=True)

        # Set 'Оновлено' as the index
        self.sellers_data.set_index('Оновлено', inplace=True)
        self.products_data.set_index('Оновлено', inplace=True)

        # Sort the dataframes by index
        self.sellers_data.sort_index(inplace=True)
        self.products_data.sort_index(inplace=True)

    def get_data(self):
        return self.sellers_data, self.products_data
