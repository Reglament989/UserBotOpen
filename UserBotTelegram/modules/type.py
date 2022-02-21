import asyncio
import logging

from telethon.errors.rpcerrorlist import MessageNotModifiedError

logging.basicConfig(
    format=u"%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.INFO,
)


async def TypeCmdHandler(message):
    """.type <message>"""
    a = message.raw_text.split(" ", maxsplit=1)[-1]
    if not a or a == "$type":
        await message.edit("Nothing type")
        await asyncio.sleep(1)
        await message.delete()
        return
    m = ""
    for c in a:
        m += "▒"
        message = await _update_message(message, m)
        await asyncio.sleep(0.04)
        m = m[:-1] + c
        message = await _update_message(message, m)
        await asyncio.sleep(0.02)


async def _update_message(message, m):
    try:
        return await message.edit(m)
    except MessageNotModifiedError:
        return message  # space doesnt count
