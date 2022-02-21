from .mongo import DB


class Config:
    async def get_config(self):
        self.__class__.api_id, self.__class__.api_hash, self.__class__.secret = await DB.Config()

    token = ""  # ""
    cuttly_key = ""
    api_key_rebrandly = ""
    api_key_shorte = ""
    DEBUG = True
