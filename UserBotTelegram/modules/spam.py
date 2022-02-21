from telethon import errors
import logging
import asyncio

logging.basicConfig(
    format="%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.INFO,
)


async def SpamHandler(event):
    await event.delete()
    client = event.client
    chat = await event.get_input_chat()
    args = event.raw_text.split(" ", maxsplit=2)
    try:
        count = int(args.pop(1))
    except Exception as e:
        logging.critical(e)
        return await event.edit("Maybe you want send int counter?")
    text = args.pop(-1)
    del args
    if type(count) is int and count < 20:
        if count <= 10:
            time = 0.35
        else:
            time = 0.8
        for i in range(count):
            try:
                await client.send_message(chat, text)
            except errors.FloodWaitError as e:
                logging.error(f"Got a gag from flood for {e.seconds} seconds")
                await event.edit(f"Got a gag from flood for {e.seconds} seconds")
                return
            await asyncio.sleep(time)
    logging.info(
        f"Spam from chat: {chat}, count: {count}, text: {text} | SUCCESS! ")


async def SpellSpamHandler(event):
    await event.delete()
    chat = await event.get_input_chat()
    text = list(event.raw_text.split(" ", maxsplit=1).pop(-1))
    if len(text) <= 10:
        time = 0.2
    elif len(text) <= 15:
        time = 0.35
    else:
        time = 0.8
    for letter in text:
        await asyncio.sleep(time)
        try:
            await event.client.send_message(chat, letter)
        except Exception as e:
            logging.warning(e)
            pass
