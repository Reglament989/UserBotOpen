import asyncio
import logging

from googletrans import Translator

from UserBotTelegram.mongo import DB

translator = Translator()


async def TranslateHandler(event):
    await event.edit('`Process...`')
    to_lang = await DB().GetLanguage()
    reply = await event.get_reply_message()
    translated = translator.translate(reply.raw_text, dest=to_lang)
    await event.edit(translated.text)


async def TranslateToHandler(event):
    await event.edit('`Process...`')
    args = event.raw_text.split(' ', maxsplit=2)
    if args[1] == ':tolang':
        await event.edit('Please set language.')
        await asyncio.sleep(1)
        await event.delete()
    try:
        translated = translator.translate(args[-1], dest=args[1])
    except Exception as e:
        logging.critical(e)
        await event.edit('Bad language, abort..')
        await asyncio.sleep(1)
        await event.delete()
        return
    await event.edit(translated.text)


async def SetLanguageHandler(event):
    args = event.raw_text.split(' ', maxsplit=1)
    if args[-1] != ':settolang' and len(args[-1]):
        await DB().SetLanguage(args[-1])
        await event.edit('Language sets successfully')
        await asyncio.sleep(1)
        await event.delete()
    else:
        await event.edit('Lang must be a google format, example: en, ru, de, pl')
        await asyncio.sleep(3)
        await event.delete()
