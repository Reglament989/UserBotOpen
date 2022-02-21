from telethon import TelegramClient, events

from UserBotTelegram.modules.translate import TranslateHandler, TranslateToHandler, SetLanguageHandler
from UserBotTelegram.mongo import DB

from UserBotTelegram.modules.purge import PurgeHandler
from UserBotTelegram.modules.purge import TimePurgeHandler
from UserBotTelegram.modules.purge import GetTPurgesHandler
from UserBotTelegram.modules.purge import AdvancedTimePurgeHandler

from UserBotTelegram.modules.spam import SpamHandler
from UserBotTelegram.modules.spam import SpellSpamHandler

from UserBotTelegram.modules.destroy_chat import DeleteAllUsersHandler

from UserBotTelegram.modules.notes import NotesHandler, GetNoteHandler, SaveNoteHandler, ResetNotesHandler
from UserBotTelegram.modules.notes import DeleteNoteHandler

from UserBotTelegram.modules.kang import KangHandler, GetPackInfoHandler
from UserBotTelegram.modules.type import TypeCmdHandler
from UserBotTelegram.modules.url import SurlHandler, ClearUrlsHandler
from UserBotTelegram.modules.tagall import TagAllHandler
from UserBotTelegram.modules.figlet import FigletHandler

from UserBotTelegram.modules.admin_tools import BanOrUnbanHandler, MuteOrUnmuteHandler
from UserBotTelegram.modules.admin_tools import PromoteOrDemoteToAdminChatHandler

from UserBotTelegram.modules.help import HelpHandler
from UserBotTelegram.modules.no_pm import DeleteWhiteListHandler, ShowWhiteListHandler, AddToWhiteListHandler
from UserBotTelegram.modules.qr_code import CreateQrCodeHandler

import UserBotTelegram.telegram_bot

import os
import pyfiglet
import logging
import platform
import time

logging.basicConfig(
    format="%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.INFO,
)

# https://t.me/proxy?server=telegram.n-1.mtproxy.me&port=3000&secret=736273c1efdf6cc547c768405777f22c

# client = TelegramClient('anon', '', '')
client = TelegramClient('anon', '', '')


async def main():
    me = await client.get_me()
    await StartedApp(me)


async def StartedApp(me):
    arch = platform.architecture()
    if arch[0] == "64bit" and arch[-1] != "":
        os.system("clear")
    else:
        pass
    print(
        """\n\n\n-------------------------------------------------------------------------------
"""
    )
    print(pyfiglet.figlet_format(
        f"App started with:\n{me.username}", font="doom"))
    print("(Press Ctrl+C to stop this)")
    print(
        """\n-------------------------------------------------------------------------------
"""
    )


# @client.on(events.NewMessage(incoming=True))
# async def NoPm(event):
#     await NoPmHandler(event)

@client.on(events.NewMessage(outgoing=True, pattern=r':tolang'))
async def TranslateTo(event):
    await TranslateToHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r':settolang'))
async def SetLanguage(event):
    await SetLanguageHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r':tr'))
async def Translate(event):
    await TranslateHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r'\:promote'))
async def PromoteOrDemoteToAdminChat(event):
    await PromoteOrDemoteToAdminChatHandler(event, promote=True)


@client.on(events.NewMessage(outgoing=True, pattern=r'\:demote'))
async def PromoteOrDemoteToAdminChat(event):
    await PromoteOrDemoteToAdminChatHandler(event, promote=False)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:addwh"))
async def AppendToWhitelist(event):
    await AddToWhiteListHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:qrcode"))
async def QrCode(event):
    await CreateQrCodeHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:delwh"))
async def RemoveForWhitelist(event):
    await DeleteWhiteListHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:listwh"))
async def ShowWhiteList(event):
    await ShowWhiteListHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:ping"))
async def Ping(event):
    await event.edit("Pong")


@client.on(events.NewMessage(outgoing=True, pattern=r"\:dbping"))
async def PingDb(event):
    t0 = time.time()
    _, _, _ = await DB.Config()
    t1 = time.time()
    await event.edit(f"Pong - {t1-t0} seconds.")


@client.on(events.NewMessage(outgoing=True, pattern=r"\:statspurge"))
async def GetTPurge(event):
    await GetTPurgesHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:ffpurges"))
async def AdvancePurge(event):
    await AdvancedTimePurgeHandler(event, ff=True)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:ccpurges"))
async def CancelPurge(event):
    await AdvancedTimePurgeHandler(event, ff=False)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:help"))
async def HelpCmd(event):
    await HelpHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:purge"))
async def purge(event):
    await PurgeHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:tpurge"))
async def tpurge(event):
    await TimePurgeHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:spam"))
async def spam(event):
    await SpamHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:sspam"))
async def spell_spam(event):
    await SpellSpamHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:destroy"))
async def DeleteAllUsers(event):
    await DeleteAllUsersHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:allnotes"))
async def notes(event):
    await NotesHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:note"))
async def note(event):
    await GetNoteHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:save"))
async def save_note(event):
    await SaveNoteHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:resetnotes"))
async def reset_notes(event):
    await ResetNotesHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:delnote"))
async def del_note(event):
    await DeleteNoteHandler(event)


# @client.on(events.NewMessage(outgoing=True, pattern=r"\:sleep"))
# async def sleep(event):
#     await _sleep(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:kang"))
async def kang(args):
    await KangHandler(args)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:packinfo"))
async def get_pack_info(event):
    await GetPackInfoHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:type"))
async def TypeCmd(event):
    await TypeCmdHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:surl"))
async def surl(event):
    await SurlHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:dropurls"))
async def ClearUrl(event):
    await ClearUrlsHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:tagall"))
async def tagall(event):
    await TagAllHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:figlet"))
async def figlet(event):
    await FigletHandler(event)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:ban"))
async def ban(event):
    await BanOrUnbanHandler(event, True)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:uban"))
async def unban(event):
    await BanOrUnbanHandler(event, False)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:mute"))
async def mute_unmute(event):
    await MuteOrUnmuteHandler(event, False)


@client.on(events.NewMessage(outgoing=True, pattern=r"\:umute"))
async def mute_unmute(event):
    await MuteOrUnmuteHandler(event, True)
