import aiohttp
import asyncio
from pathlib import Path
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

async def download_file(session, url, file_path, filename):
    async with session.get(url) as response:
        response.raise_for_status()
        content = await response.read()
        # Save the content to a .csv file
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(content)
        print(f"Downloaded {filename}.csv")

async def download_if_needed(session, url, filename):
    csv_path = DATA_DIR / f"{filename}.csv"

    remote_last_modified = await fetch_last_modified(session, url)

    if remote_last_modified is not None:
        if csv_path.exists():
            local_last_modified_timestamp = csv_path.stat().st_mtime
            # Make local_last_modified timezone-aware in UTC
            local_last_modified = datetime.fromtimestamp(
                local_last_modified_timestamp, tz=timezone.utc
            )

            # Ensure remote_last_modified is timezone-aware in UTC
            if remote_last_modified.tzinfo is None:
                # Assume it's in UTC
                remote_last_modified = remote_last_modified.replace(tzinfo=timezone.utc)
            else:
                # Convert to UTC
                remote_last_modified = remote_last_modified.astimezone(timezone.utc)

            if local_last_modified >= remote_last_modified:
                print(f"{filename}.csv is up to date.")
                return

    # Download the CSV file and save it to disk
    await download_file(session, url, csv_path, filename)

async def get_files(urls: list[str], names: list[str]):
    conn = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = [
            download_if_needed(session=session, url=url, filename=filename)
            for url, filename in zip(urls, names)
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    urls = [
        "https://madeinukraine.gov.ua/files/perelik-tovariv/products.csv",
        "https://madeinukraine.gov.ua/files/perelik-prodavtsiv/perelik-prodavtsiv.csv"
    ]
    names = ["products", "sellers"]

    asyncio.run(get_files(urls, names))
