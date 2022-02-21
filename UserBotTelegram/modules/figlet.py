import asyncio
import logging
import pyfiglet
import random

logging.basicConfig(
    format="%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] %(message)s",
    level=logging.INFO,
)


async def FigletHandler(event):
    text = event.raw_text.split(" ", maxsplit=1).pop(-1)
    if text != "$figlet":
        styles = ["utopiab", "tinker-toy", "c_consen", "kik_star", "helv"]
        mode = random.choice(styles)
        fig = pyfiglet.Figlet(font=mode, width=30)
        figlet_text = "`" + fig.renderText(text) + "`"
        await event.edit(figlet_text)
    else:
        await event.edit("Nothing edit")
        await asyncio.sleep(1)
        await event.delete()
