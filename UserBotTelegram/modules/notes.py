import asyncio
import logging
from pprint import pprint

import telethon

from UserBotTelegram.mongo import DB

logging.basicConfig(
    format="%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.INFO,
)


async def NotesHandler(event):
    text = ""
    data = await DB().GetNotes()
    for i in data:
        if i.type_note:
            text += f"• **{i.name}** - {i.data}\n"
        else:
            text += f"• **{i.name}** - `{i.data}`\n"
    if text != "":
        await event.edit(text)
    else:
        await event.edit("**You don't having notes**")
        await asyncio.sleep(1)
        await event.delete()


async def GetNoteHandler(event):
    try:
        name = event.raw_text.split(" ", maxsplit=1).pop(-1)
        note = await DB().GetNote(name)
        if not note:
            await event.edit('Note is not defined!')
            await asyncio.sleep(1)
            await event.delete()
            return
        if note.type_note == 'media':
            reply = await DB().GetAsset(note.data)
            if not reply:
                await event.edit('**Note data not defined...**')
                # await DB().RemoveNotes(name=name)
                await asyncio.sleep(2)
                await event.delete()
                return
            chat = event.chat
            await event.delete()
            await event.client.send_message(chat, reply.message, file=reply.media)
            return
        await event.edit(note.data)
    except Exception as e:
        await event.edit("**Something went wrong!**")
        logging.info(f"Getting note | FAILED")
        logging.critical(e)
        await asyncio.sleep(2)
        await event.delete()


async def SaveNoteHandler(event: telethon.types.Message):
    args = event.raw_text.split(" ", maxsplit=2)
    type_note = 'text'
    if len(args) < 3:
        try:
            reply = await event.get_reply_message()
            if reply.media:
                name = args.pop(-1)
                if name == ':save':
                    await event.edit('Give name for note. :save <NoteName>')
                    await asyncio.sleep(1)
                    await event.delete()
                    return
                type_note = 'media'
                await DB().SaveAsset(name, reply, type_note)
                await event.edit("**Note saved!**")
                logging.info(f'Create note - name: "{name}", data: "{reply.id}" | SUCCESS')
                await asyncio.sleep(2)
                await event.delete()
                return
            else:
                data = reply.raw_text
            name = args.pop(-1)
            if name == ':save':
                await event.edit('Give name for note. :save <NoteName>')
                await asyncio.sleep(1)
                await event.delete()
                return
        except Exception as e:
            logging.critical(e)
            await event.edit("Try :save <NameNote> <BodyNote>")
            await asyncio.sleep(1)
            await event.delete()
            return
    else:
        data = args.pop(-1)
        name = args.pop(-1)
    if await DB().CreateNote(name, data, type_note):
        await event.edit("**Note saved!**")
        logging.info(f'Create note - name: "{name}", data: "{data}" | SUCCESS')
    else:
        await event.edit("**This note already exists!**")
        logging.warning(f"Create note | FAILED")
    await asyncio.sleep(2)
    await event.delete()


async def ResetNotesHandler(event):
    result = await DB().RemoveNotes(hard=True)
    if result:
        await event.edit("**Successfully reset!**")
        logging.info(f"Hard reset notes | SUCCESS")
    else:
        await event.edit("**Something went wrong!**")
        logging.warning(f"Hard reset | FAILED")
    await asyncio.sleep(2)
    await event.delete()


async def DeleteNoteHandler(event):
    args = event.raw_text.split(" ", maxsplit=1)
    name = args.pop(-1)
    if await DB().RemoveNotes(name=name):
        await event.edit(f'**Successfully delete, note: "{name}"**')
    else:
        await event.edit("**Something went wrong!**")
        logging.warning(f'Deleting note: "{name}" | FAILED')
    await asyncio.sleep(2)
    await event.delete()
