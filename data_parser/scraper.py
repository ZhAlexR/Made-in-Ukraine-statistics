import aiohttp
import asyncio
import pandas as pd
from pathlib import Path
from io import BytesIO
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

PARENT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PARENT_DIR / "data"

async def fetch_last_modified(session, url):
    async with session.head(url) as response:
        response.raise_for_status()
        last_modified = response.headers.get('Last-Modified')
        if last_modified:
            remote_last_modified = parsedate_to_datetime(last_modified)
            return remote_last_modified
    return None

async def fetch_file_and_convert(session, url, parquet_path, filename):
    async with session.get(url) as response:
        response.raise_for_status()
        content = await response.read()
        excel_file = BytesIO(content)
        df = pd.read_excel(excel_file)
        parquet_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(parquet_path)
        print(f"Downloaded and converted {filename} to Parquet")

async def download_and_convert(session, url, filename):
    parquet_path = DATA_DIR / f"{filename}.parquet"

    remote_last_modified = await fetch_last_modified(session, url)

    if remote_last_modified is not None:
        if parquet_path.exists():
            local_last_modified_timestamp = parquet_path.stat().st_mtime
            local_last_modified = datetime.fromtimestamp(
                local_last_modified_timestamp, tz=timezone.utc
            )

            if remote_last_modified.tzinfo is None:
                remote_last_modified = remote_last_modified.replace(tzinfo=timezone.utc)
            else:
                remote_last_modified = remote_last_modified.astimezone(timezone.utc)

            if local_last_modified >= remote_last_modified:
                print(f"{filename} is up to date.")
                return

    await fetch_file_and_convert(session, url, parquet_path, filename)

async def get_files(urls: list[str], names: list[str]):
    conn = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = [
            download_and_convert(session=session, url=url, filename=filename)
            for url, filename in zip(urls, names)
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    urls = [
        "https://madeinukraine.gov.ua/files/perelik-tovariv/products.xlsx",
        "https://madeinukraine.gov.ua/files/perelik-prodavtsiv/perelik-prodavtsiv.xlsx"
    ]
    names = ["products", "sellers"]

    asyncio.run(get_files(urls, names))
