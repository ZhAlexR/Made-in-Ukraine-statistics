from pathlib import Path

import streamlit as st
import pandas as pd
from data_handler import DataHandler
from metrics_calculator import MetricsCalculator
from plotter import Plotter

st.markdown(
    """
    <style>
    .main {
        max-width: 100% !important;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

parent_dir = Path(__file__).resolve().parent.parent
sellers = parent_dir / "data_scraper/sellers.xlsx"
products = parent_dir / "data_scraper/products.xlsx"

# Завантаження даних
data_handler = DataHandler(sellers_file=str(sellers), products_file=str(products))
sellers_data, products_data = data_handler.get_data()

# Вибір дат через Streamlit
start_date = st.date_input("Початкова дата", value=sellers_data['Оновлено'].min().date(), min_value=sellers_data['Оновлено'].min().date(), max_value=sellers_data['Оновлено'].max().date())
end_date = st.date_input("Кінцева дата", value=sellers_data['Оновлено'].max().date(), min_value=sellers_data['Оновлено'].min().date(), max_value=sellers_data['Оновлено'].max().date())

# Підрахунок метрик
metrics_calculator = MetricsCalculator(products_data, sellers_data)
metrics = metrics_calculator.calculate_metrics(start_date, end_date)

# Відображення метрик
st.subheader("Основні метрики за обраний період:")
metrics_df = pd.DataFrame(metrics.items(), columns=['Метрика', 'Значення'])
st.table(metrics_df)

# Створення об'єкта Plotter для побудови графіків
plotter = Plotter()

# Відображення графіків у сітці 2x2
st.subheader("Візуалізація даних")

# Створюємо перший ряд колонок для двох графіків
col1, col2 = st.columns(2)

with col1:
    plotter.plot_manufacturers_combined(products_data, start_date, end_date)

with col2:
    plotter.plot_brands_combined(products_data, start_date, end_date)

# Створюємо другий ряд колонок для двох графіків
col3, col4 = st.columns(2)

with col3:
    plotter.plot_products_combined(products_data, start_date, end_date)

with col4:
    plotter.plot_sellers_combined(sellers_data, start_date, end_date)

# Окремо виводимо кругову діаграму і теплову карту
plotter.plot_pie_chart(products_data)
plotter.plot_interactive_heatmap(products_data, start_date, end_date)
