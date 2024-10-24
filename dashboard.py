import streamlit as st
import pandas as pd
from data_handler import DataHandler
from metrics_calculator import MetricsCalculator
from plotter import Plotter
from pathlib import Path


parent_dir = Path(__file__).resolve().parent
sellers = parent_dir / "data/sellers.parquet"
products = parent_dir / "data/products.parquet"

@st.cache_data
def load_data(sellers_file, products_file):
    data_handler = DataHandler(sellers_file, products_file)
    sellers_data, products_data = data_handler.get_data()
    return sellers_data, products_data

sellers_data, products_data = load_data(str(sellers), str(products))

start_date = st.date_input(
    "Початкова дата",
    value=sellers_data.index.min().date(),
    min_value=sellers_data.index.min().date(),
    max_value=sellers_data.index.max().date()
)

end_date = st.date_input(
    "Кінцева дата",
    value=sellers_data.index.max().date(),
    min_value=sellers_data.index.min().date(),
    max_value=sellers_data.index.max().date()
)

if start_date > end_date:
    st.error("Початкова дата не може бути пізніше за кінцеву дату.")
    st.stop()

@st.cache_data
def get_metrics(products_data, sellers_data, start_date, end_date):
    metrics_calculator = MetricsCalculator(products_data, sellers_data)
    return metrics_calculator.calculate_metrics(start_date, end_date)

metrics = get_metrics(products_data, sellers_data, start_date, end_date)

st.subheader("Основні метрики за обраний період:")
metrics_df = pd.DataFrame(metrics.items(), columns=['Метрика', 'Значення'])
st.table(metrics_df)

plotter = Plotter()

st.subheader("Візуалізація даних")

col1, col2 = st.columns(2)

with col1:
    plotter.plot_manufacturers_combined(products_data, start_date, end_date)

with col2:
    plotter.plot_brands_combined(products_data, start_date, end_date)

col3, col4 = st.columns(2)

with col3:
    plotter.plot_products_combined(products_data, start_date, end_date)

with col4:
    plotter.plot_sellers_combined(sellers_data, start_date, end_date)

plotter.plot_pie_chart(products_data)
plotter.plot_interactive_heatmap(products_data, start_date, end_date)
