import aiohttp
import asyncio
import logging
from pathlib import Path
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

PARENT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PARENT_DIR / "data"

async def fetch_last_modified(session, url):
    logger.info(f"Fetching last modified time for {url}")
    try:
        async with session.head(url) as response:
            response.raise_for_status()
            last_modified = response.headers.get('Last-Modified')
            if last_modified:
                remote_last_modified = parsedate_to_datetime(last_modified)
                return remote_last_modified
    except Exception as e:
        logger.error(f"Error fetching last modified time for {url}: {e}")
    return None

async def download_file(session, url, file_path, filename):
    logger.info(f"Downloading {filename}.csv from {url}")
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.read()
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(content)
            logger.info(f"Downloaded {filename}.csv successfully")
    except Exception as e:
        logger.error(f"Error downloading {filename}.csv from {url}: {e}")

async def download_if_needed(session, url, filename):
    csv_path = DATA_DIR / f"{filename}.csv"
    logger.info(f"Checking if {filename}.csv needs to be updated")

    try:
        remote_last_modified = await fetch_last_modified(session, url)
        if remote_last_modified is not None:
            if csv_path.exists():
                local_last_modified_timestamp = csv_path.stat().st_mtime
                local_last_modified = datetime.fromtimestamp(local_last_modified_timestamp, tz=timezone.utc)

                if remote_last_modified.tzinfo is None:
                    remote_last_modified = remote_last_modified.replace(tzinfo=timezone.utc)
                else:
                    remote_last_modified = remote_last_modified.astimezone(timezone.utc)

                if local_last_modified >= remote_last_modified:
                    logger.info(f"{filename}.csv is up to date. No download needed.")
                    return
            else:
                logger.info(f"{filename}.csv does not exist. Downloading...")
        else:
            logger.warning(f"Could not fetch last modified time for {filename}. Downloading file.")

        await download_file(session, url, csv_path, filename)
    except Exception as e:
        logger.error(f"Error processing {filename}.csv: {e}")

async def get_files(urls: list[str], names: list[str]):
    logger.info("Starting to download files")
    conn = aiohttp.TCPConnector(ssl=False)
    try:
        async with aiohttp.ClientSession(connector=conn) as session:
            tasks = [
                download_if_needed(session=session, url=url, filename=filename)
                for url, filename in zip(urls, names)
            ]
            await asyncio.gather(*tasks)
    except Exception as e:
        logger.error(f"Error during file download: {e}")

if __name__ == "__main__":
    urls = [
        "https://madeinukraine.gov.ua/files/perelik-tovariv/products.csv",
        "https://madeinukraine.gov.ua/files/perelik-prodavtsiv/perelik-prodavtsiv.csv"
    ]
    names = ["products", "sellers"]

    logger.info("Starting scraper script")
    asyncio.run(get_files(urls, names))
    logger.info("Scraper script finished")
