import pandas as pd
import os, asyncio, aiohttp, aiofiles
import time
import requests
from bs4 import BeautifulSoup

MAX_CONCURRENT = 50

os.makedirs("images", exist_ok=True)

semaphore = asyncio.Semaphore(MAX_CONCURRENT)

df = pd.read_csv("data.csv")

async def download_image(session, i):
    async with semaphore:
        id_str = f"{i:06d}"
        image_url = f"https//cdli.earth/dl/photo/P{id_str}.jpg"
        image_path = os.path.join("images", f"P{id_str}.jpg")

        if os.path.exists(image_path):
            return
        async with session.get(image_url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(image_path, mode='wb')
                await f.write(await resp.read())
                print(f"Downlodaded: {id_str}")
            else:
                print(f"Error: {id_str} {resp.status}")

async def extract():
    async with aiohttp.ClientSession() as session:
        tasks = [download_image(session, int(i)) for i in df['artifact_id']]
        await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(extract())
loop.close()
