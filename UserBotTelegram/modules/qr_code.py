from MyQR import myqr
import logging
import asyncio
import os
import ffmpeg
import uuid

logging.basicConfig(
    format="%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.INFO,
)


class Counter:
    counter = uuid.uuid4().hex

    def __init__(self):
        self.__class__.counter = uuid.uuid4().hex

    def get(self):
        return self.__class__.counter


async def CreateQrCodeHandler(event):
    args = event.raw_text.split(' ', maxsplit=1)
    try:
        if not event.is_reply:
            name = f'qr{Counter().get()}.png'
            if args[-1] != ':qrcode':
                text = args[-1]
            else:
                text = 'https://github.com/Reglament989'
            await event.edit('`Create qrcode..`')
            myqr.run(level='H', words=text, save_name=name)
            upload = await event.client.upload_file(name)
            await event.client.send_file(event.chat_id, upload)
            await event.delete()
            os.remove(name)
        else:
            await event.edit('Process...')
            message = await event.get_reply_message()
            if message.photo or message.gif:
                img = await message.download_media()
                logging.error(img)
                if message.photo:
                    name = f'qr{Counter().get()}.png'
                else:
                    gif = ffmpeg.input(img)
                    name = f'qr{Counter().get()}.gif'
                    current_counter = Counter().get()
                    out = ffmpeg.output(gif, f'input_gif{current_counter}.gif')
                    await event.edit('`Found gif, starting ffmpeg task..`')
                    try:
                        ffmpeg.run(out, cmd='ffmpeg')
                    except Exception as e:
                        logging.critical(e)
                        ffmpeg.run(out, cmd='./ffmpeg')
                    os.remove(img)
                    img = f'input_gif{current_counter}.gif'
                if args[-1] == ':qrcode':
                    text = 'https://github.com/Reglament989'
                else:
                    text = args[-1]
                await asyncio.sleep(1.25)
                await event.edit('`Last step, create qrcode..`')
                myqr.run(level='H', picture=img, words=text,
                         colorized=True, save_name=name)
                await event.edit('`Upload...`')
                upload = await event.client.upload_file(name)
                await event.client.send_file(event.chat_id, upload)
                await event.delete()
                os.remove(img)
                os.remove(name)
            else:
                await event.edit('I cant work for this, try photo or gif')
                await asyncio.sleep(2)
                await event.delete()
    except Exception as e:
        logging.error(e)
        current_dir = os.listdir()
        for i in current_dir:
            if i.endswith(('.png', '.gif', '.mp4')):
                os.remove(i)
