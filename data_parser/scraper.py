from pathlib import Path

import aiohttp
import asyncio

PARENT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PARENT_DIR / "data"


async def download_and_save(session, url, filename, extension = "xlsx"):
    async with session.get(url) as response:
        response.raise_for_status()
        with open(f"{str(DATA_DIR)}/{filename}.{extension}", "wb") as f:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                f.write(chunk)
        print(f"Saved {filename}")


async def get_files(urls: list[str], names: list[str]):
    conn = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = [
            download_and_save(session=session, url=url, filename=filename)
            for url, filename
            in zip(urls, names)
        ]
        await asyncio.gather(*tasks)
