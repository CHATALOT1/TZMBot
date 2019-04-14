from discord.ext import commands
from datetime import datetime
import config
from config import bot_config
import utils
import os
import logging

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
handler.setLevel(logging.WARNING)
logger.addHandler(handler)

handler = logging.FileHandler(filename="debug.log", encoding="utf-8", mode="a")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

client = commands.Bot(command_prefix="!")
client.config = bot_config
client.utils = utils


@client.event
async def on_ready():
    logger.info(f"Bot running on {client.user} (ID: {client.user.id})")
    logger.info(f"Took {datetime.now()-launch_time}, Time now {datetime.now()}")


if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            try:
                client.load_extension(f"{'cogs'}.{filename[:-3]}")
                logger.debug(f"-\tCog extension {filename} loaded successfully")
            except Exception as e:
                logger.debug(f"-\tCog extension {filename} could not be loaded: {e}")

    launch_time = datetime.now()
    logger.info(f"Attempting to run bot at {launch_time}")
    client.run(config.token)
