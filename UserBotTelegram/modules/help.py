import logging

logging.basicConfig(
    format=u"%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.INFO,
)

help_response = """The simple help message
`Admin tools`:
  :[u]ban - <@Nickname> or reply message
  :[u]mute - <@Nickname> or reply message
  :promote <Rank(label)> - Use for promote user to admin
  :demote - Use for remove admin rights
`URL shooter`:
  :surl - <url>
  :dropurls - Clear all urls from heroku
`Translate`:
  :tr - Reply message, translate to your lang
  :settolang <lang> - Set your lang, must be a google format - en, de, pl, ru
  :tolang <lang> <text> - Translate input text to input lang
`Notes`:
  :note - <Note name>
  :save - <Body note>
  :allnotes - Your all notes
  :resetnotes - Drop your db notes
  :delnote - <Note name>
`Spam`:
  :spam - <[int] Count> <Message>
  :sspam - <Message> 
`Purge`:
  :purge - Reply message
  :tpurge - <Time on minuts> and reply message | `:tpurge N` - purge after passing N minuts
  :statspurge - Give you all tpurges timers
  :ffpurges - Fast end for all yours tpurges
  :ccpurges - Cancel all your tpurges
`Kang`:
  :kang - Sticker or photo or gif
  :packinfo - Pack info
`Other`:
  :tagall - Tag all from chat
  :figlet - <Text>
  :type - <Text> pastiche typing
  :qrcode <text> - Reply any media or simple put text
"""


async def HelpHandler(event):
    on_command = event.raw_text.split(' ', maxsplit=1)[-1]
    if not on_command == ':help':
        pass
    else:
        await event.edit(help_response)
