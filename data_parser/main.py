import asyncio
from pathlib import Path

from made_in_ukraine_statistic.data_parser.scraper import get_files

urls = [
    "https://madeinukraine.gov.ua/files/perelik-tovariv/products.xlsx",
    "https://madeinukraine.gov.ua/files/perelik-prodavtsiv/perelik-prodavtsiv.xlsx"
]

files_name = ["sellers", "products"]
CURRENT_DIR = Path.cwd()


async def main():
    await get_files(urls=urls, names=files_name)

if __name__ == "__main__":
    asyncio.run(main())
