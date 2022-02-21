import aiohttp
import asyncio
import logging
import os

from UserBotTelegram.utils import Shoooot

logging.basicConfig(
    format=u"%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.INFO,
)

URL = os.getenv('HOST')


async def SurlHandler(event):
    await event.edit("`Process...`")
    url = event.raw_text.split(" ", maxsplit=1).pop(-1)
    response = await Shoooot(url)
    if response:
        await event.edit(response, link_preview=False)
    elif response == "Your href is not available!":
        await event.edit("`Your href is not available!`")
        await asyncio.sleep(2)
        await event.delete()


async def clear():
    async with aiohttp.ClientSession() as session:
        async with session.post(URL + "clearurl") as response:
            try:
                json = await response.json()
                if json.pop("code") == 200:
                    return True
                else:
                    return False
            except Exception as e:
                logging.critical(e)
                return False


async def ClearUrlsHandler(event):
    result = await clear()
    if result:
        await event.edit("`Successful`")
        await asyncio.sleep(1)
        await event.delete()
    else:
        await event.edit("`Failed..`")
        await asyncio.sleep(1)
        await event.delete()
