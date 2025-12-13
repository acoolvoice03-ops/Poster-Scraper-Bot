# ruff: noqa: E402

from datetime import datetime
from logging import Formatter
from asyncio import gather

from pytz import timezone
from pyrogram import idle

from config import Config
from . import LOGGER, bot_loop
from .core.EchoClient import EchoBot
from .core.plugs import add_plugs
from .helper.utils.db import database
from .helper.utils.bot_cmds import _get_bot_commands


async def main():
    await database._load_all()

    def changetz(*args):
        return datetime.now(timezone(Config.TIMEZONE)).timetuple()

    Formatter.converter = changetz

    await gather(
        EchoBot.start(),
    )
    await EchoBot.bot.set_bot_commands(_get_bot_commands())

    add_plugs()

    LOGGER.info("All EchoBot Services started")

    await idle()

    await EchoBot.stop()


bot_loop.run_until_complete(main())
bot_loop.run_forever()
