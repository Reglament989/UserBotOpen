import asyncio
import logging
import os
import aiohttp_jinja2
import jinja2
import base64
from telethon.utils import parse_phone

from aiohttp import web

from UserBotTelegram.main import client
from UserBotTelegram.modules.purge import delete_time_purge_on_startup
from UserBotTelegram.mongo import DB

logging.basicConfig(
    format="%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.INFO,
)

routes = web.RouteTableDef()
if os.getenv("HEROKU"):
    URL = "https://userbot989.herokuapp.com/"
else:
    URL = "http://localhost:8080/"

# routes.static('/static', './UserBotTelegram/templates')


# @routes.get('/setup')
@aiohttp_jinja2.template('setup.html')
async def initSetup(_):
    phone = os.getenv('TG_NUMBER_PHONE')
    await client.connect()
    await client.send_code_request(phone)


# @routes.post('/setup')
async def get_telegram_code(request):
    phone = os.getenv('TG_NUMBER_PHONE')
    data = await request.post()
    code = data['code']
    # try:
    await client.sign_in(parse_phone(phone), code=code)
    client.loop.create_task(DB().init(client))
    await asyncio.sleep(3)
    client.loop.create_task(delete_time_purge_on_startup(client))
    logging.critical('Successful login')
    await client.run_until_disconnected()
    # except telethon.errors.SessionPasswordNeededError:
    #     return web.Response(status=401)  # Requires 2FA login
    # except telethon.errors.PhoneCodeExpiredError:
    #     return web.Response(status=404)
    # except telethon.errors.PhoneCodeInvalidError:
    #     return web.Response(status=403)
    # except telethon.errors.FloodWaitError:
    #     return web.Response(status=421)


@routes.get('/finish')
@aiohttp_jinja2.template('finish.html')
async def finishRoute(_):
    return


# @routes.get("/{key}", name="index")
# async def index(request):
#     key = request.match_info["key"]
#     if key == 'uptime':
#         return web.json_response({"status": "OK", "code": 200})
#     document_url = await DB().CheckUrl(key)
#     if document_url:
#         raise web.HTTPFound(location=document_url["url"])
#     else:
#         return web.json_response({"status": "Not found", "code": 400})
#
#
# @routes.post("/create", name="create")
# async def create(request):
#     data = await request.post()
#     logging.info(data)
#     url = data["url"]
#     logging.info(url)
#     key = await get_key(url)
#     response = await Mongo.CreateUrl(url, key)
#     if response:
#         logging.info("New href created: {}".format(URL + key))
#         res = {"url": "{}".format(URL + key), "code": 201}
#         return web.json_response(res)
#     if not response:
#         check = await Mongo.CheckUrl(key)
#         if check:
#             logging.info("New href created: {}".format(URL + check["_id"]))
#             res = {"url": "{}".format(URL + check["_id"]), "code": 201}
#             return web.json_response(res)
#         else:
#             return web.json_response({"status": "Error", "code": 400})
#     else:
#         return web.json_response({"status": "Error", "code": 400})
#
#
# @routes.post("/clearurl", name="clearurl")
# async def clear_hrefs(request):
#     if await Mongo.ClearUrl():
#         return web.json_response({"status": "OK", "code": 200})
#     else:
#         return web.json_response({"status": "Error", "code": 400})


async def get_key(url):
    text = list(url)
    num = 0
    for i in text:
        num += ord(i)
    if num < 10000:
        href = hex(num * 1200).split("x")[-1]
    else:
        href = hex(num * 120).split("x")[-1]
    return href


app = web.Application()
app.add_routes(routes)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./UserBotTelegram/templates'))


def mmain():
    # client.loop.create_task(DB().init(client))
    # client.loop.create_task(delete_time_purge_on_startup(client))
    # logging.critical('Successful login')
    # client.run_until_disconnected()
    # asyncio.run(web.run_app(app, port=os.getenv("PORT")))
    with client:
        client.loop.create_task(DB().init(client)).__await__()
        client.loop.run_until_complete(
            web.run_app(app, port=os.getenv("PORT")))
        client.loop.create_task(delete_time_purge_on_startup(client))
        client.run_until_disconnected()


if __name__ == "__main__":
    if os.getenv("HEROKU"):
        print('Found heroku')
        import tarfile

        tar_name = 'ffmpeg.tar.xz'
        with tarfile.open(tar_name) as tar:
            print('Unarchived')
            tar.extractall()
        # os.remove(tar_name)
    mmain()
