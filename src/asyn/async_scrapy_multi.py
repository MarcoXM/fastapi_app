import asyncio
from aiohttp import ClientSession
import pathlib
import time 
from datetime import datetime 

async def fetch(url, session, year):
    async with session.get(url) as response:
        await asyncio.sleep(15)
        html_body = await response.read()
        return {"body": html_body, "year": year}


loads = [8588922064, 8588924118, 8588923815,8588922578]

async def main(loads = loads):
    html_body = ""
    tasks = []
    # semaphore
    async with ClientSession() as session:
        for load in loads:

            url = f'https://my.yrc.com/tools/track/shipments?referenceNumber={load}&referenceNumberType=PRO&time={int(time.mktime(datetime.now().timetuple()))}'
            print("load#", load, url)
            tasks.append(
                asyncio.create_task(
                    fetch(url, session, load)
                )
            )
        pages_content = await asyncio.gather(*tasks) # [{"body": "..", "load": Pro# }]
        return pages_content


results = asyncio.run(main())

output_dir = pathlib.Path().resolve() / "snapshots"
output_dir.mkdir(parents=True, exist_ok=True)

for result in results:
    current_year = result.get("year")
    html_data = result.get('body')
    output_file = output_dir / f"{current_year}.html"
    output_file.write_text(html_data.decode())
    # with open('path/to/output', 'w') as f:
    #     f.write(html_data.decode())