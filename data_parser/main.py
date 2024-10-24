import asyncio
from pathlib import Path

from scraper import get_files

urls = [
    "https://madeinukraine.gov.ua/files/perelik-tovariv/products.csv",
    "https://madeinukraine.gov.ua/files/perelik-prodavtsiv/perelik-prodavtsiv.csv"
]

files_name = ["products", "sellers"]
CURRENT_DIR = Path.cwd()


async def main():
    await get_files(urls=urls, names=files_name)

if __name__ == "__main__":
    asyncio.run(main())
