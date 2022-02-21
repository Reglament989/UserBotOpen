import asyncio
import logging

logging.basicConfig(
    format="%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.INFO,
)


async def TagAllHandler(event):
    if event.fwd_from:
        return await event.delete()
    await event.delete()
    mentions = ""
    me = await event.client.get_entity("me")
    chat = await event.get_input_chat()
    async for x in event.client.iter_participants(chat, 100):
        if x == me:
            continue
        else:
            mentions += f" \n [{x.first_name}](tg://user?id={x.id})"
    if mentions:
        await event.client.send_message(chat, mentions)
    else:
        msg = await event.client.send_message(chat, "`This chat don't have participants.`")
        await asyncio.sleep(2)
        await msg.delete()
