import os
from UserBotTelegram.mongo import Mongo


def test_falsetest():
    print('hi')


async def Wtest_mongo():
    try:
        import motor
    except:
        raise Exception('Cannot import motor, try add "motor" to requirements.txt.')
    from UserBotTelegram.mongo import Mongo

    try:
        await Mongo.Config()
    except Exception as error:
        raise Exception(f"Database has not connection.\n{error}")


async def Wtest_bot():
    try:
        import telethon
    except:
        raise Exception(
            'Cannot import telethon, try add "telethon" to requirements.txt.'
        )
    name: str = "bot"
    api_id, api_hash, _ = await Mongo.Config()
    client = telethon.TelegramClient(name, api_id, api_hash)
    async with client:
        client.loop.run_until_complete()


async def bot_getme(client):
    await client.get_me()


async def Wtest_telethon():
    try:
        import telethon
    except:
        raise Exception(
            'Cannot import telethon, try add "telethon" to requirements.txt.'
        )
    name: str = "test"
    session: bool = False
    for file in os.listdir():
        # print(file)
        if file == name + ".session":
            session = True
            break
    # if session:
    try:
        api_id, api_hash, _ = await Mongo.Config()
        client = telethon.TelegramClient(name, api_id, api_hash)
        async with client:
            client.loop.run_until_complete(Telethon(client))
    except Exception as e:
        raise e
    # else:
    #     raise Exception("Where your *.session? first step auth in telethon")


async def Wtest_Shoot_util():
    from UserBotTelegram.utils import Shoooot

    urls = ["https://www.example.com", "https://who.is", "https://start.duckduckgo.com"]
    for url in urls:
        r = await Shoooot(url)
        if r == "Your href is not avalible!":
            raise Exception(
                "util shooter not working, raise your href is not avalible."
            )
        else:
            pass


async def Telethon(client):
    from telethon import TelegramClient
    from UserBotTelegram.modules.purge import _purge
    from UserBotTelegram.modules.spam import _spam
    from UserBotTelegram.modules.spam import _spell_spam
    from UserBotTelegram.modules.destroy_chat import _delallusers
    from UserBotTelegram.modules.notes import (
        _notes,
        _note,
        _save_note,
        _reset_notes,
        _del_note,
    )
    from UserBotTelegram.modules.kang import _kang, _get_pack_info
    from UserBotTelegram.modules.love import _love_is, _sleep
    from UserBotTelegram.modules.type import _typecmd
    from UserBotTelegram.modules.url import _surl, _clearurls
    from UserBotTelegram.modules.tagall import _tagall
    from UserBotTelegram.modules.figlet import _figlet
    from UserBotTelegram.modules.admin_tools import _ban_unban, _mute_unmute

    import asyncio

    start_msg = await client.send_message("me", "Start Testing")
    spam_msg = await client.send_message("me", "$spam 5 test")
    await _spam(spam_msg)

    await asyncio.sleep(3)

    spel_msg = await client.send_message("me", "$sspam test")
    await _spell_spam(spel_msg)

    await asyncio.sleep(3)

    type_msg = await client.send_message("me", "$type Test")
    await _typecmd(type_msg)

    await asyncio.sleep(3)

    note_msg = await client.send_message("me", "$save test TestComplite")
    await _save_note(note_msg)

    await asyncio.sleep(3)

    getnote_msg = await client.send_message("me", "$note test")
    await _note(getnote_msg)

    await asyncio.sleep(3)

    allnotes_msg = await client.send_message("me", "$allnotes")
    await _notes(allnotes_msg)

    await asyncio.sleep(3)

    removenote_msg = await client.send_message("me", "$delnote test")
    await _del_note(removenote_msg)

    await asyncio.sleep(3)

    tagall_msg = await client.send_message("me", "$tagall")
    await _tagall(tagall_msg)

    await asyncio.sleep(3)

    figlet_msg = await client.send_message("me", "$figlet Test")
    await _figlet(figlet_msg)

    await asyncio.sleep(3)

    purge_msg = await client.send_message("me", "$purge", reply_to=start_msg)
    await _purge(purge_msg)

    await asyncio.sleep(3)

    complite_msg = await client.send_message("me", "Testing complite")
    await asyncio.sleep(3)
    await complite_msg.delete()
