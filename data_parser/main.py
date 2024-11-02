import asyncio
import logging
from pathlib import Path

from scraper import get_files

urls = [
    "https://api.madeinukraine.gov.ua/storage/exports/products.csv",
    "https://api.madeinukraine.gov.ua/storage/exports/perelik-prodavtsiv.csv"
]

files_name = ["products", "sellers"]
CURRENT_DIR = Path.cwd()

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting parse files ...")
    await get_files(urls=urls, names=files_name)
    logger.info("Stopping parse files ...")

if __name__ == "__main__":
    asyncio.run(main())
