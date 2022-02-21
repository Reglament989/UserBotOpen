import logging, asyncio
from datetime import timedelta
from datetime import datetime
from telethon.tl.types import InputPeerChat
from telethon.tl.types import InputPeerUser
from telethon.tl.types import InputPeerChannel
from telethon.tl.types import InputPeerSelf
from UserBotTelegram.mongo import DB

logging.basicConfig(
    format="%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.INFO,
)


async def PurgeHandler(event):
    """ For .purge command, purge all messages starting from the reply. """
    chat = await event.get_input_chat()
    msgs = []
    iter_msg = event.client.iter_messages(chat, min_id=event.reply_to_msg_id)
    count = 0

    if event.reply_to_msg_id is not None:
        msgs.append(event.reply_to_msg_id)
        async for msg in iter_msg:
            msgs.append(msg)
            count = count + 1
            if len(msgs) == 100:
                await event.client.delete_messages(chat, msgs)
                msgs = []
    else:
        await event.edit("`I need a message to start purging from.`")
        return

    if msgs:
        await event.client.delete_messages(chat, msgs)
        done = await event.client.send_message(
            event.chat_id,
            f"`Fast purge complete!`\nPurged {str(count)} messages",
            silent=True
        )
        await asyncio.sleep(1)
        await done.delete()
    logging.info(f"Purge from chat: {chat}, deleted msg: {count} | SUCCESS! ")


async def delete_msgs(delay, chat, msgs, event):
    time = datetime.now() + timedelta(seconds=delay)
    if isinstance(chat, InputPeerSelf):
        _id = 'me'
    elif isinstance(chat, InputPeerChannel):
        _id = chat.channel_id
    elif isinstance(chat, InputPeerUser):
        _id = chat.user_id
    elif isinstance(chat, InputPeerChat):
        _id = chat.chat_id
    else:
        logging.critical("Not found types")
        raise Exception("Not found types")
    del_data = {"chat_id": _id, "time": time.strftime('%Y-%m-%d-%H-%M'), "msgs": msgs}
    await DB().Append_DelayPurge(del_data)
    await delay_delete(event.client, chat, delay, msgs, del_data)


async def delay_delete(client, chat, time, msgs, del_data):
    await asyncio.sleep(time)
    await client.delete_messages(chat, msgs)
    await DB().Remove_DelayPurge(del_data)


async def AdvancedTimePurgeHandler(event, ff=True):
    await event.edit('`Process`')
    data = await DB().Get_DelayPurge()
    for i in data:
        del_data = {"chat_id": i['chat_id'], "time": i['time'], "msgs": i['msgs']}
        if ff:
            await event.client.delete_messages(i['chat_id'], i['msgs'])
        for task in asyncio.Task.all_tasks():
            task_name = task.get_name()
            if task_name == 'purge':
                logging.info(f"task: {task_name} | CANCELED")
                task.cancel()
        await DB().Remove_DelayPurge(del_data)
    await event.edit("OK")
    await asyncio.sleep(1)
    await event.delete()


async def delete_time_purge_on_startup(client):
    data = await DB().Get_DelayPurge()
    # logging.error(data)
    for purge in data:
        # logging.info(purge)
        time = datetime.strptime(purge['time'], '%Y-%m-%d-%H-%M') - datetime.now()
        time = time.total_seconds()
        del_data = {"chat_id": purge['chat_id'], "time": purge['time'], "msgs": purge['msgs']}
        if time < 0:
            try:
                client.loop.create_task(delay_delete(client, purge['chat_id'], time, purge['msgs'], del_data)).set_name(
                    'purge')
            except Exception as e:
                logging.critical(e)
                pass
            continue

        client.loop.create_task(delay_delete(client, purge['chat_id'], time, purge['msgs'], del_data)).set_name('purge')


async def TimePurgeHandler(event):
    chat = await event.get_input_chat()
    try:
        time = int(event.raw_text.split(' ', maxsplit=1)[-1]) * 60
        if time > 43200:
            time = 43200
    except Exception as e:
        logging.critical(e)
        await event.edit('Maybe time it should be int?')
        await asyncio.sleep(1)
        await event.delete()
        return
    msgs = []
    iter_msg = event.client.iter_messages(chat, min_id=event.reply_to_msg_id)
    count = 0

    if event.reply_to_msg_id is not None:
        msgs.append(event.reply_to_msg_id)
        async for msg in iter_msg:
            msgs.append(msg.id)
            count = count + 1
            if len(msgs) == 100:
                event.client.loop.create_task(delete_msgs(time, chat, msgs, event)).set_name('purge')
                # await task()
                msgs = []
    else:
        await event.edit("`I need a message to start purging from.`")
        return

    if msgs:
        await event.delete()
        time_d = timedelta(minutes=time / 60)
        done = await event.client.send_message(
            event.chat_id,
            f"`Scheduled purge through {time_d}`\
            \nPurged {str(count)} messages",
            silent=True
        )
        await asyncio.sleep(1)
        await done.delete()
        event.client.loop.create_task(delete_msgs(time, chat, msgs, event)).set_name('purge')
        # await task()
    logging.info(f"TPurge from chat: {chat}, deleted msg: {count}, time: {time} | SUCCESS! ")


async def GetTPurgesHandler(event):
    await event.edit('`Process`')
    data = await DB().Get_DelayPurge()
    result = "All time purges **active**:\n"
    for purge in data:
        result += f"[Chat {purge['chat_id']}](tg://user?id={purge['chat_id']}) - deadline on __{purge['time']}__\n"
    if result == "All time purges **active**:\n":
        await event.edit("You don't have tpurges")
        await asyncio.sleep(1)
        await event.delete()
        return
    await event.edit(result)
