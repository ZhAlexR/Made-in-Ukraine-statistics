import os
import streamlit as st
import pandas as pd
from data_handler import DataHandler
from metrics_calculator import MetricsCalculator
from plotter import Plotter
from pathlib import Path

st.set_page_config(layout="wide")

parent_dir = Path(__file__).resolve().parent
sellers = parent_dir / "data/sellers.csv"
products = parent_dir / "data/products.csv"

# Ensure that the CSV files exist
if not sellers.exists() or not products.exists():
    st.error("Data files are missing. Please run the scraper to download the data.")
    st.stop()

sellers_mtime = os.path.getmtime(sellers)
products_mtime = os.path.getmtime(products)

@st.cache_data
def load_data(sellers_file, products_file, sellers_mtime, products_mtime):
    data_handler = DataHandler(sellers_file, products_file)
    return data_handler.get_data()

sellers_data, products_data = load_data(
    str(sellers),
    str(products),
    sellers_mtime,
    products_mtime
)

# Date inputs
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

# Create DataFrame and ensure 'Значення' is of type str
metrics_df = pd.DataFrame(metrics.items(), columns=['Метрика', 'Значення'])
metrics_df['Значення'] = metrics_df['Значення'].astype(str)

st.table(metrics_df)

# Initialize plotter
plotter = Plotter()

# Visualization
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
