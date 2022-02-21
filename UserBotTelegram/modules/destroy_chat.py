import asyncio
import logging

from telethon.tl.functions.channels import DeleteChannelRequest

logging.basicConfig(
    format="%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.INFO,
)


async def DeleteAllUsersHandler(event):
    client = event.client
    await event.edit("Destroy chat...")
    chat = await event.get_input_chat()
    try:
        await client(DeleteChannelRequest(chat))
    except Exception as e:
        logging.critical(e)
        await event.edit("Only supergroup.")
        await asyncio.sleep(1)
        await event.delete()
        return
    logging.info(f"Destroying chat: {chat} | SUCCESS! ")
