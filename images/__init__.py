import httpx

from PIL import Image
from io import BytesIO

# python -m asyncio

async def image_by_url(url):
    client = httpx.AsyncClient()
    r = await client.get(url)
    await client.aclose()

    return Image.open(BytesIO(r.content))
