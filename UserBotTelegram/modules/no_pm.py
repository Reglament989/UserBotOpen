import logging
import asyncio
from telethon import functions
from telethon.tl.types import InputPeerUser
from UserBotTelegram.mongo import DB

logging.basicConfig(
    format=u"%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.INFO,
)


async def NoPmHandler(event):
    if event.is_private:
        # bot = await event.client.get_entity(await event.get_input_chat())
        # logging.info(bot)
        if not event.chat_id in await DB().get_whitelist():
            chat = await event.get_input_chat()
            await event.reply("Sorry, i do not accept pm.")
            await event.client(functions.contacts.BlockRequest(chat.user_id))


async def ShowWhiteListHandler(event):
    await event.edit('Fetching...')
    array = await DB().get_whitelist()
    string = '\tWhite list\t\n'
    for i in array:
        user = await event.client.get_entity(i['id'])
        string += f'[{user.first_name}](tg://user?id={x.id})\n'
    await event.edit(string)


async def AddToWhiteListHandler(event):
    _id = event.raw_text.split(' ', maxsplit=1)
    if len(_id) > 1:
        result = _id[-1]
    else:
        chat = await event.get_input_chat()
        if isinstance(chat, InputPeerUser):
            result = chat.user_id
        else:
            await event.edit("Only on pm")
            await asyncio.sleep(1)
            return await event.delete()
    await DB().append_to_whitelist(result)
    await event.edit(f"ID[{result}] has be append to whitelist.")
    await asyncio.sleep(2)
    await event.delete()


async def DeleteWhiteListHandler(event):
    _id = event.raw_text.split(' ', maxsplit=1)
    if len(_id) > 1:
        if len(_id[-1]) >= 9:
            result = _id[-1]
        else:
            await event.edit("Maybe length id must be > 9?")
            return
    else:
        chat = await event.get_input_chat()
        if isinstance(chat, InputPeerUser):
            result = chat.user_id
        else:
            await event.edit("Only on pm")
            await asyncio.sleep(1)
            return await event.delete()
    await DB().remove_for_whitelist(result)
    await event.edit(f"ID[{result}] has be remove for whitelist.")
    await asyncio.sleep(2)
    await event.delete()
