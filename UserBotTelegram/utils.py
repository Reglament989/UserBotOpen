import aiohttp
import json
import logging
import random

from UserBotTelegram.settings import Config

logging.basicConfig(
    format=u"%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.INFO,
)


async def Shoooot(url: str, system: str = None) -> str:
    async with aiohttp.ClientSession() as session:
        if system is None:
            system = random.choice(System.get())
        if system not in System.get():
            return "Invalid system"
        response = await create_post(url, session, system)
        if response:
            return response
        else:
            return "Your href is not available!"


async def create_post(url, session, system):
    working = True  # await work_url(url, session)
    if working:
        post = session.post
        put = session.put
        if system == System.Rebrandly:
            request = json.dumps(
                {"destination": url, "domain": {"fullName": "rebrand.ly"}}
            )
            headers = {
                "Content-type": "application/json",
                "apikey": Config.api_key_rebrandly,
            }
            method = post
        elif system == System.Shorte:
            request = json.dumps({"urlToShorten": url})
            headers = {"public-api-token": Config.api_key_shorte}
            method = put
        else:
            logging.info(f"Url: {url}\nStatus FAILED not found system (pre-method)")
            return False
        async with method(system, data=request, headers=headers) as response:
            try:
                link = await response.json()
            except Exception as e:
                logging.critical(e)
                return False
            if system == System.Rebrandly:
                return link.pop("shortUrl")
            elif system == System.Shorte:
                return link.pop("shortenedUrl")
            else:
                logging.info(f"Url: {url}\nStatus FAILED not found system")
                return False
    else:
        logging.info(f"Url: {url}\nDon't working")
        return False


async def work_url(url, session):
    logging.info(f"testing url: {url}")
    try:
        async with session.get(url) as response:
            code = response.status
            if code == 200:
                logging.info(f"Url: {url}\nStatus OK")
                return True
            else:
                logging.info(f"Url: {url}\nStatus FAILED\nCode: {code}")
                return False
    except Exception as e:
        logging.info(f"Url: {url}\nStatus FAILED ({e})")
        return False


class System:
    @staticmethod
    def get():
        return [
            System.Rebrandly,
            System.Shorte,
        ]  # Heroku must be last on list / Nope :-)

    Rebrandly = "https://api.rebrandly.com/v1/links"
    Shorte = "https://api.shorte.st/v1/data/url"
