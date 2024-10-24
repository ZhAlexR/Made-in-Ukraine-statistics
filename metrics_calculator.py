import pandas as pd

class MetricsCalculator:
    def __init__(self, products_data, sellers_data):
        self.products_data = products_data
        self.sellers_data = sellers_data

    def calculate_metrics(self, start_date, end_date):
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        filtered_products = self.products_data[
            (self.products_data.index >= start_date) & (self.products_data.index <= end_date)
            ]
        filtered_sellers = self.sellers_data[
            (self.sellers_data.index >= start_date) & (self.sellers_data.index <= end_date)
            ]

        unique_manufacturers = filtered_products['Юридична назва'].nunique()
        unique_brands = filtered_products['Бренд'].nunique()
        total_products = filtered_products.shape[0]
        unique_sellers = filtered_sellers['Бренд'].nunique()
        most_popular_brand = filtered_products['Бренд'].value_counts().idxmax()
        most_popular_brand_count = filtered_products['Бренд'].value_counts().max()

        return {
            'Кількість виробників': unique_manufacturers,
            'Кількість брендів': unique_brands,
            'Кількість товарів': total_products,
            'Кількість унікальних продавців': unique_sellers,
            'Найпопулярніший бренд': f"{most_popular_brand} ({most_popular_brand_count} товарів)"
        }
