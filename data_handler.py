import pandas as pd

class DataHandler:
    def __init__(self, sellers_file, products_file):
        self.sellers_data = pd.read_excel(sellers_file)
        self.products_data = pd.read_excel(products_file)

    def get_data(self):
        return self.sellers_data, self.products_data
