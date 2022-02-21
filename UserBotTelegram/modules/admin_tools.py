import asyncio
import logging
from datetime import timedelta

from telethon import errors
from telethon.tl.functions.channels import EditBannedRequest, InviteToChannelRequest
from telethon.tl.types import ChatBannedRights

logging.basicConfig(
    format="%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.INFO,
)


async def PromoteOrDemoteToAdminChatHandler(event, promote=True):
    args = event.raw_text.split(' ', maxsplit=1)
    chat = await event.get_input_chat()
    title = 'Admin'
    reply = await event.get_reply_message()
    entity = await event.client.get_entity(reply.from_id)
    if len(args) > 1:
        try:
            if "@" in args[1]:
                entity = await event.client.get_entity(args[1])
            else:
                title = args[1]
        except Exception as e:
            logging.warning(e)
            await event.edit('Entity corrupted')
            await asyncio.sleep(1)
            await event.delete()
            return
    try:
        await event.client.edit_admin(chat, entity, is_admin=promote, add_admins=False, title=title)
        if promote:
            await event.edit(f'Promoted [{entity.first_name}](tg://user?id={entity.id}) on rank {title}',
                             parse_mode='markdown')
        else:
            await event.edit(f'Demoted [{entity.first_name}](tg://user?id={entity.id}) he just human.',
                             parse_mode='markdown')
        return
    except Exception as e:
        logging.warning(e)
        await event.edit('Im not have rights on this chat')
        await asyncio.sleep(1)
        await event.delete()


async def BanOrUnbanHandler(event, _type):
    args = event.raw_text.split(" ", maxsplit=2)
    chat = await event.get_input_chat()
    user = None
    try:
        time = timedelta(minutes=int(args[-1]))
    except Exception as e:
        logging.debug(e)
        time = None
    if event.is_reply:
        reply = await event.get_reply_message()
        user = await event.client.get_entity(reply.from_id)
    else:
        try:
            if "@" in args[1]:
                user = await event.client.get_entity(args.pop(1))
        except Exception as e:
            logging.warning(e)
            await event.edit("You need reply message.")
            await asyncio.sleep(1)
            await event.delete()
            return
    try:
        await event.client(
            EditBannedRequest(
                chat, user, ChatBannedRights(until_date=time, view_messages=_type)
            )
        )
        if _type:
            await event.edit(f"`Banned` [{user.first_name}](tg://user?id={user.id})")
        else:
            await event.edit(f"`Unban` [{user.first_name}](tg://user?id={user.id})")
            await event.client(InviteToChannelRequest(chat, [user]))
    except errors.BadRequestError:
        await event.edit("Im not admin here.")
        await asyncio.sleep(1)
        await event.delete()
    except Exception as e:
        await event.edit(f"Error:\n{e}")


async def MuteOrUnmuteHandler(event, _type):
    args = event.raw_text.split(" ", maxsplit=2)
    chat = await event.get_input_chat()
    user = None
    try:
        time = timedelta(minutes=int(args[-1]))
    except Exception as e:
        logging.debug(e)
        time = None
    if event.is_reply:
        reply = await event.get_reply_message()
        user = await event.client.get_entity(reply.from_id)
    else:
        try:
            if "@" in args[1]:
                user = await event.client.get_entity(args.pop(1))
        except Exception as e:
            logging.warning(e)
            await event.edit("You need reply message.")
            await asyncio.sleep(1)
            await event.delete()
            return
    try:
        await event.client.edit_permissions(chat, user, time, send_messages=_type)
        if _type:
            await event.edit(f"`Un muted` [{user.first_name}](tg://user?id={user.id})")
        else:
            await event.edit(
                f"`Muted for a {time}` [{user.first_name}](tg://user?id={user.id})"
            )
    except errors.BadRequestError:
        await event.edit("Im not admin here.")
        await asyncio.sleep(1)
        await event.delete()
        return
    except Exception as e:
        await event.edit(f"Error:\n{e}")
