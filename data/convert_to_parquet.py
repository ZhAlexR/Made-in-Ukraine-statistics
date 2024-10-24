import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

sellers_excel_path = DATA_DIR / "sellers.xlsx"
sellers_parquet_path = DATA_DIR / "sellers.parquet"

sellers_df = pd.read_excel(sellers_excel_path)
sellers_df.to_parquet(sellers_parquet_path)
print(f"Converted {sellers_excel_path} to {sellers_parquet_path}")

products_excel_path = DATA_DIR / "products.xlsx"
products_parquet_path = DATA_DIR / "products.parquet"

products_df = pd.read_excel(products_excel_path)
products_df.to_parquet(products_parquet_path)
print(f"Converted {products_excel_path} to {products_parquet_path}")
