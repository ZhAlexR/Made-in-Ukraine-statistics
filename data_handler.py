import logging

import pandas as pd

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class DataHandler:
    def __init__(self, sellers_file, products_file):
        logger.info(f"Initializing DataHandler with files: sellers={sellers_file}, products={products_file}")

        self.sellers_data = pd.read_csv(sellers_file, sep=';', encoding='utf-8', on_bad_lines='skip')
        self.products_data = pd.read_csv(products_file, sep=';', encoding='utf-8', on_bad_lines='skip')

        self.sellers_data['Оновлено'] = pd.to_datetime(self.sellers_data['Оновлено'], dayfirst=True)
        self.products_data['Оновлено'] = pd.to_datetime(self.products_data['Оновлено'], dayfirst=True)


        self.sellers_data.set_index('Оновлено', inplace=True)
        self.products_data.set_index('Оновлено', inplace=True)

        self.sellers_data.sort_index(inplace=True)
        self.products_data.sort_index(inplace=True)

    def get_data(self):
        return self.sellers_data, self.products_data
