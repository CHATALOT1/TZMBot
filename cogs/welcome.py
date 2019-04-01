from discord.ext import commands

class Welcoming(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass #TODO: messages for when members join

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        pass #TODO: messages for when members leave

def setup(client):
    client.add_cog(Welcoming(client))