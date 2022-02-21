import urllib.request
import math
import io
import asyncio
import logging
import random
from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto
from os import remove
from PIL import Image
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetID
from telethon.tl.types import DocumentAttributeSticker

logging.basicConfig(
    format="%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.INFO,
)

KANGING_STR = [
    "Using Witchery to kang this sticker...",
    "Plagiarising hehe...",
    "Inviting this sticker over to my pack...",
    "Kanging this sticker...",
    "Hey that's a nice sticker!\nMind if I kang?!..",
    "hehe me stel ur sticker\nhehe.",
    "Ay look over there (☉｡☉)!→\nWhile I kang this...",
    "Roses are red violets are blue, kanging this sticker so cool",
    "Imprisoning this sticker...",
    "Mr.Steal Your Sticker is stealing this sticker... ",
]


async def KangHandler(args):
    """ For .kang command, kangs stickers or creates new ones. """
    client = args.client
    user = await client.get_me()
    if not user.username:
        user.username = user.first_name
    message = await args.get_reply_message()
    # photo = None
    emojiByPass = False
    is_anim = False
    emoji = None

    if message and message.media:
        if isinstance(message.media, MessageMediaPhoto):
            await args.edit(f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            photo = await client.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split("/"):
            await args.edit(f"`{random.choice(KANGING_STR)}`")
            photo = io.BytesIO()
            await client.download_file(message.media.document, photo)
            if (
                    DocumentAttributeFilename(file_name="sticker.webp")
                    in message.media.document.attributes
            ):
                emoji = message.media.document.attributes[1].alt
                emojiByPass = True
        elif "tgsticker" in message.media.document.mime_type:
            await args.edit(f"`{random.choice(KANGING_STR)}`")
            await client.download_file(message.media.document, "AnimatedSticker.tgs")

            attributes = message.media.document.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt

            emojiByPass = True
            is_anim = True
            photo = 1
        else:
            await args.edit("`Unsupported File!`")
            await asyncio.sleep(2)
            await args.delete()
            return
    else:
        await args.edit("`I can't kang that...`")
        await asyncio.sleep(2)
        await args.delete()
        return

    if photo:
        splat = args.text.split()
        if not emojiByPass:
            emoji = random.choice(
                ['😏', '😉', '😁', '😮', '😈', '😇', '😱', '😳', '😜', ''])
        pack = 1
        logging.warn(splat)
        if len(splat) == 2:
            emoji = splat[-1]  # User sent client
        if len(splat) == 3:
            pack = splat[1]
            emoji = splat[-1]

        packName = f"pack_by_{user.username}_{pack}"
        packNick = f"@{user.username} pack {pack}"
        cmd = "/newpack"
        file = io.BytesIO()

        if not is_anim:
            image = await resize_photo(photo)
            file.name = "sticker.png"
            image.save(file, "PNG")
        else:
            packName += "_anim"
            packNick += " (Animated)"
            cmd = "/newanimated"

        response = urllib.request.urlopen(
            urllib.request.Request(f"http://t.me/addstickers/{packName}")
        )
        htmlStr = response.read().decode("utf8").split("\n")

        if (
                "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
                not in htmlStr
        ):
            async with client.conversation("Stickers") as conv:
                await conv.send_message("/addsticker")
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await client.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packName)
                x = await conv.get_response()
                while "120" in x.text:
                    pack += 1
                    packName = f"pack_by_{user.username}_{pack}"
                    packNick = f"@{user.username} pack {pack}"
                    await args.edit(
                        "`Switching to Pack "
                        + str(pack)
                        + " due to insufficient space`"
                    )
                    await conv.send_message(packName)
                    x = await conv.get_response()
                    if x.text == "Invalid pack selected.":
                        await conv.send_message(cmd)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await client.send_read_acknowledge(conv.chat_id)
                        await conv.send_message(packNick)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await client.send_read_acknowledge(conv.chat_id)
                        if is_anim:
                            await conv.send_file("AnimatedSticker.tgs")
                            remove("AnimatedSticker.tgs")
                        else:
                            file.seek(0)
                            await conv.send_file(file, force_document=True)
                        await conv.get_response()
                        await conv.send_message(emoji)
                        # Ensure user doesn't get spamming notifications
                        await client.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response()
                            await conv.send_message(f"<{packNick}>")
                        # Ensure user doesn't get spamming notifications
                        await conv.get_response()
                        await client.send_read_acknowledge(conv.chat_id)
                        await conv.send_message("/skip")
                        # Ensure user doesn't get spamming notifications
                        await client.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message(packName)
                        # Ensure user doesn't get spamming notifications
                        await client.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await client.send_read_acknowledge(conv.chat_id)
                        await args.edit(
                            f"`Sticker added in a Different Pack`\nThis Pack is Newly created!\nYour pack can be "
                            f"found [here](t.me/addstickers/{packName})",
                            parse_mode="md",
                        )
                        return
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    await args.edit(
                        "`Failed to add sticker, use` @Stickers `client to add the sticker manually.`"
                    )
                    return
                await conv.send_message(emoji)
                # Ensure user doesn't get spamming notifications
                await client.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/done")
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await client.send_read_acknowledge(conv.chat_id)
        else:
            await args.edit("`Brewing a new Pack...`")
            async with client.conversation("Stickers") as conv:
                await conv.send_message(cmd)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await client.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packNick)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await client.send_read_acknowledge(conv.chat_id)
                if is_anim:
                    await conv.send_file("AnimatedSticker.tgs")
                    remove("AnimatedSticker.tgs")
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                rsp = await conv.get_response()
                if "Sorry, the file type is invalid." in rsp.text:
                    await args.edit(
                        "`Failed to add sticker, use` @Stickers `client to add the sticker manually.`"
                    )
                    return
                await conv.send_message(emoji)
                # Ensure user doesn't get spamming notifications
                await client.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response()
                    await conv.send_message(f"<{packNick}>")
                # Ensure user doesn't get spamming notifications
                await conv.get_response()
                await client.send_read_acknowledge(conv.chat_id)
                await conv.send_message("/skip")
                # Ensure user doesn't get spamming notifications
                await client.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message(packName)
                # Ensure user doesn't get spamming notifications
                await client.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await client.send_read_acknowledge(conv.chat_id)

        await args.edit(
            f"`Sticker kanged successfully!`\nPack can be found [here](t.me/addstickers/{packName})",
            parse_mode="md",
        )


async def resize_photo(photo):
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizeNew = (size1new, size2new)
        image = image.resize(sizeNew)
    else:
        image.thumbnail(maxsize)

    return image


async def GetPackInfoHandler(event):
    client = event.client
    if not event.is_reply:
        await event.edit("`I can't fetch info from nothing, can I ?!`")
        await asyncio.sleep(2)
        await event.delete()
        return

    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        await event.edit("`Reply to a sticker to get the pack details`")
        await asyncio.sleep(2)
        await event.delete()
        return

    try:
        stickerSetAttr = rep_msg.document.attributes[1]
        await event.edit("`Fetching details of the sticker pack, please wait..`")
    except BaseException as e:
        logging.critical(e)
        await event.edit("`This is not a sticker. Reply to a sticker.`")
        await asyncio.sleep(2)
        await event.delete()
        return

    if not isinstance(stickerSetAttr, DocumentAttributeSticker):
        await event.edit("`This is not a sticker. Reply to a sticker.`")
        await asyncio.sleep(2)
        await event.delete()
        return

    getStickerSet = await client(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerSetAttr.stickerset.id,
                access_hash=stickerSetAttr.stickerset.access_hash,
            )
        )
    )
    pack_emojis = []
    for document_sticker in getStickerSet.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)

    OUTPUT = (
        f"**Sticker Title:** `{getStickerSet.set.title}\n`"
        f"**Sticker Short Name:** `{getStickerSet.set.short_name}`\n"
        f"**Official:** `{getStickerSet.set.official}`\n"
        f"**Archived:** `{getStickerSet.set.archived}`\n"
        f"**Stickers In Pack:** `{len(getStickerSet.packs)}`\n"
        f"**Emojis In Pack:**\n{' '.join(pack_emojis)}"
    )

    await event.edit(OUTPUT)
