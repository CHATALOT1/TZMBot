import discord
from discord.ext import commands


class Activity(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        pass  # TODO: Activity detection functionality


def setup(client):
    client.add_cog(Activity(client))
