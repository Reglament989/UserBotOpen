import random
import uuid

from telethon import TelegramClient, events
import logging
from PIL import Image
# import numpy as np
import os
import io
from UserBotTelegram.utils import System

logging.basicConfig(
    format=u"%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.INFO,
)


bot = TelegramClient('bot', '', '')

# .start(
# )



@bot.on(events.NewMessage(pattern="/start"))
async def start_handler(event):
    await bot.send_message(
        event.chat_id, "Hi, This bot help you for a compress images;)\nSimple send photo to me and im compressed his for you :}"
    )


@bot.on(events.NewMessage(pattern="/help"))
async def help_handler(event):
    await bot.send_message(
        event.chat_id,
        """
Simple send photo to me and im compressed his for you :}
""",
        link_preview=False,
    )


# @bot.on(events.NewMessage(pattern="/level"))
# async def enabler(event):
#     text = event.raw_text.split(' ', maxsplit=1)[-1]
#     systems = System.__repr__()
#     if text in systems:
#         return await bot.send_message(
#             event.chat_id, "Im not having this service"
#         )
#     with Switch(text) as case:
#         if case(systems[0]):
#             pass


@bot.on(events.NewMessage(pattern="/contribution"))
async def Contribution(event):
    pass


@bot.on(events.NewMessage(func=lambda e: e.media))
async def Compress(event):
    chat = await event.get_input_chat()
    msg = await event.reply('`Process`')
    photo = None
    document = None
    try:
        photo = event.media.photo
    except AttributeError:
        document = event.media.document
    if photo or document:
        try:
            logging.info(event.media.stringify())
            try:
                file_name = f'{uuid.uuid4()}.{event.media.document.attributes[-1].file_name}'
            except AttributeError:
                file_name = f'{uuid.uuid4()}.jpg'
            file = await event.download_media(file=bytes)
            await msg.edit('`Creating new photo...`')
            # logging.info(event.media.stringify())
            img = Image.open(io.BytesIO(file))
            img.save(f'Compressed-{file_name}', optimize=True, quality=50)
            await msg.edit('`Uploading`')
            async with event.client.action(chat, 'document'):
                await event.reply(file=f'Compressed-{file_name}', force_document=True)
            await msg.delete()
            # r = event.media.document.thumbs[-1].size - compressed_image.
            # await event.reply(random.choice(['Excellent photo!', 'Nice to meet you!', 'Great photo', 'Im like this']))
            os.remove(file_name)
            os.remove(f'Compressed-{file_name}')
        except Exception as e:
            logging.warning(e)
            await msg.edit('`Bad image, cannot compress...`')
    else:
        msg.edit('`Im working only with images`')


# @bot.on(events.InlineQuery(pattern=r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"))
# async def callback(event):
#     try:
#         builder = event.builder
#         await event.answer(
#             [
#                 await builder.article(
#                     "Rebrandly — rebrand.ly",
#                     text=await Shoooot(event.text, System.Rebrandly),
#                     link_preview=False,
#                 ),
#                 await builder.article(
#                     "Shorte, give the developer love ❤️",
#                     text=await Shoooot(event.text, System.Shorte),
#                     link_preview=False,
#                 ),
#                 await builder.article(
#                     "Heroku, supported by the developer 🔥",
#                     text=await Shoooot(event.text, System.Heroku),
#                     link_preview=False,
#                 ),
#             ]
#         )
#     except errors.rpcerrorlist.SendMessageMediaInvalidError:
#         pass
#     except Exception as e:
#         logging.error(e)
#         pass


if __name__ == "__main__":
    bot.run_until_disconnected()
