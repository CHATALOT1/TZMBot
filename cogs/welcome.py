from discord.ext import commands

class Welcoming(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.welcome_channel = None
        self.client.loop.create_task(self.async_setup())

    async def async_setup(self):
        await self.client.wait_until_ready()
        self.welcome_channel = self.client.get_channel(self.client.config.welcome_channel_ID)

    async def welcome_goodbye(self, member, message):
        if member.guild.id == self.welcome_channel.guild.id:
            await self.welcome_channel.send(message.format(member=member))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.welcome_goodbye(member, self.client.config.welcome_message)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await self.welcome_goodbye(member, self.client.config.goodbye_message)

def setup(client):
    client.add_cog(Welcoming(client))