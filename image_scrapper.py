import os, asyncio, aiohttp, aiofiles
import time
import requests
from bs4 import BeautifulSoup

MAX_CONCURRENT = 50

#IDs = [i+1 for i in range(682, 100737)] #the sequential id numbers of the the tablets from CDLI

os.makedirs("images", exist_ok=True)

semaphore = asyncio.Semaphore(MAX_CONCURRENT)

async def download_image(session, i):
    async with semaphore:
        id_str = f"{i:06d}"
        image_url = "https://cdli.earth/dl/photo/P{}.jpg".format(id_str)
        image_path = os.path.join("images", f"P{id_str}.jpg")
    
        if os.path.exists(image_path):
            print(f"Skipped {id_str}")
            return

        async with session.get(image_url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(image_path, mode='wb')
                await f.write(await resp.read())
                print(f"Downloaded {id_str}")
            else:
                print(f"Error: {id_str} ({resp.status})")

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [download_image(session, i) for i in range(1, 100738)]
        await asyncio.gather(*tasks)

#asyncio.run(main())
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

