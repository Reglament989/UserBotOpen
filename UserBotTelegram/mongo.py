import asyncio
# import os
import logging

import telethon
# import ujson
import pydantic
import json
from telethon.tl.functions.channels import CreateChannelRequest


class Note(pydantic.BaseModel):
    name: str
    data: str
    type_note: str


# sha = SHA256.new(data=os.getenv('TG_API_ID').encode())
# sha.update(os.getenv('TG_API_HASH').encode())
# sha.update(os.getenv('TG_NUMBER_PHONE').encode())
# key = sha.digest()
#
# cipher = AES.new(key, AES.MODE_EAX)
# nonce = cipher.nonce


class DB:
    async def getDB(self):
        msgs = await self.__class__.client.get_messages(self.__class__.db_data_name)
        msg = msgs[-1]
        db = json.loads(msg.raw_text)
        return msg, db

    async def found_dbs(self):
        db_data = None
        db_assets = None
        async for dialog in self.__class__.client.iter_dialogs():
            if dialog.name == self.__class__.db_data_name:
                logging.debug('Found db_data!')
                db_data = dialog.entity
            elif dialog.name == self.__class__.db_assets_name:
                logging.debug('Found db_assets!')
                db_assets = dialog.entity
        return db_data, db_assets

    async def init(self, client):
        
        try:
            self.__class__.client = client
            data, assets = self.found_dbs()
            if not data or not assets:
                self.__class__.me = await self.__class__.client.get_me()
                self.__class__.db_data_name = f"data-{self.__class__.me.id}"
                self.__class__.db_assets_name = f'assets-{self.__class__.me.id}'
                self.__class__.db_data_name, self.__class__.db_assets_name = await self._make_channel()
        except Exception as e:
            logging.critical(e)

    async def _make_channel(self):
        dataChat = await self.__class__.client(CreateChannelRequest(self.__class__.db_data_name,
                                                                    "// Don't touch", megagroup=True))
        await self.__class__.client.send_message(dataChat.chats[-1],
                                                 json.dumps({'main': {'notes': [],
                                                                      'delayedPurge': [],
                                                                      'whiteList': [],
                                                                      'language': 'en'}}))
        await asyncio.sleep(6)
        assetChat = await self.__class__.client(CreateChannelRequest(self.__class__.db_assets_name,
                                                                     "// Don't touch", megagroup=True))
        return dataChat.chats[-1], assetChat.chats[-1]

    async def GetNotes(self, db=None):
        if not db:
            msgs = await self.__class__.client.get_messages(self.__class__.db_data_name)
            db = json.loads(msgs[-1].raw_text)
        notes = []
        for note in db['main']['notes']:
            if note['type_note'] == 'media':
                note['data'] = f'[File](https://t.me/c/1200422376/{note["data"]})'
            notes.append(Note(**note))
        return notes

    async def GetNote(self, name, db=None):
        try:
            if not db:
                msgs = await self.__class__.client.get_messages(self.__class__.db_data_name)
                db = json.loads(msgs[-1].raw_text)
            for note in db['main']['notes']:
                if note['name'] == name:
                    return Note(**note)
            return False
        except Exception as e:
            logging.critical(e)
            return False

    async def CreateNote(self, name, data, type_note):
        try:
            msgs = await self.__class__.client.get_messages(self.__class__.db_data_name)
            msg = msgs[-1]
            db = json.loads(msg.raw_text)
            exists = await self.GetNote(name, db=db)
            if exists:
                logging.warning('Delete prev note')
                db = await self.RemoveNotes(name=name, back=True)
            db['main']['notes'].append(
                Note(name=name, data=data, type_note=type_note).dict())
            await self.__class__.client.edit_message(self.__class__.db_data_name, msg, json.dumps(db))
            return True
        except Exception as e:
            logging.critical(e)
            return False

    async def SaveAsset(self, name, reply_message, type_note):
        msg, db = await self.getDB()
        sender_msg = await self.__class__.client.send_message(self.__class__.db_assets_name, reply_message)
        db['main']['notes'].append(Note(
            name=name, data=sender_msg.id, type_note=type_note
        ).dict())
        await self.__class__.client.edit_message(self.__class__.db_data_name, msg, json.dumps(db))

    async def GetAsset(self, msg_id):
        msgs = await self.__class__.client.get_messages(self.__class__.db_assets_name)
        for msg in msgs:
            if str(msg.id) == msg_id:
                return msg
        return False

    async def ClearAssets(self):
        msgs = []
        iter_msg = self.__class__.client.iter_messages(
            self.__class__.db_assets_name)
        async for msg in iter_msg:
            msgs.append(msg)
            if len(msgs) == 100:
                await self.__class__.client.delete_messages(self.__class__.db_assets_name, msgs)
                msgs = []
        await self.__class__.client.delete_messages(self.__class__.db_assets_name, msgs)

    async def RemoveNotes(self, name=None, hard=False, back=False):
        msg, db = await self.getDB()
        pack = []
        if not hard:
            notes = await self.GetNotes(db=db)
            for note in notes:
                if note.name == name:
                    continue
                pack.append(note.dict())
        if hard:
            await self.ClearAssets()
        db['main']['notes'] = pack
        try:
            await self.__class__.client.edit_message(self.__class__.db_data_name, msg, json.dumps(db))
        except telethon.errors.rpcerrorlist.MessageNotModifiedError:
            pass
        if back:
            return db
        return True

    async def Append_DelayPurge(self, data):
        msg, db = await self.getDB()
        db['main']['delayedPurge'].append(data)
        await self.__class__.client.edit_message(self.__class__.db_data_name, msg, json.dumps(db))

    async def Remove_DelayPurge(self, data):
        msg, db = await self.getDB()
        pack = []
        for purge in db['main']['delayedPurge']:
            if purge == data:
                continue
            pack.append(purge)
        db['main']['delayedPurge'] = pack
        await self.__class__.client.edit_message(self.__class__.db_data_name, msg, json.dumps(db))

    async def Get_DelayPurge(self):
        msgs = await self.__class__.client.get_messages(self.__class__.db_data_name)
        db = json.loads(msgs[-1].raw_text)
        return db['main']['delayedPurge']

    async def get_whitelist(self):
        msgs = await self.__class__.client.get_messages(self.__class__.db_data_name)
        db = json.loads(msgs[-1].raw_text)
        return db['main']['whiteList']

    async def append_to_whitelist(self, id):
        msg, db = await self.getDB()
        db['main']['whiteList'].append(id)
        await self.__class__.client.edit_message(self.__class__.db_data_name, msg, json.dumps(db))

    async def remove_for_whitelist(self, id):
        msg, db = await self.getDB()
        pack = []
        for _id in db['main']['whiteList']:
            if _id == id:
                continue
            pack.append(_id)
        db['main']['whiteList'] = pack
        await self.__class__.client.edit_message(self.__class__.db_data_name, msg, json.dumps(db))

    async def GetLanguage(self):
        _, db = await self.getDB()
        return db['main']['language']

    async def SetLanguage(self, lang):
        msg, db = await self.getDB()
        db['main']['language'] = lang
        await self.__class__.client.edit_message(self.__class__.db_data_name, msg, json.dumps(db))
