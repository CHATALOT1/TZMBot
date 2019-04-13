from discord.ext import commands
from importlib import reload


class LoadUnloadReload(commands.Cog):
    def __init__(self, client):
        self.client = client

    def cog_check(self, ctx):
        return ctx.author.id in self.client.config.dev_IDs

    async def loading_behaviour(self, ctx, meth, ext, success_message):
        try:
            meth(ext)
        except (commands.ExtensionNotFound, commands.ExtensionNotLoaded):
            try:
                meth(f"{self.client.config.relative_cogs_dir}.{ext}")
            except (commands.ExtensionNotFound, commands.ExtensionNotLoaded):
                return await ctx.send(
                    "The extension could not be found in either the current working directory or relative "
                    "cogs directory"
                )
        await ctx.send(success_message)

    @commands.command(help="load the given extension, developer only")
    async def load(self, ctx, ext):
        await self.loading_behaviour(
            ctx, self.client.load_extension, ext, f"{ext} loaded"
        )

    @commands.command(help="unload the given extension, developer only")
    async def unload(self, ctx, ext):
        await self.loading_behaviour(
            ctx, self.client.unload_extension, ext, f"{ext} unloaded"
        )

    @commands.command(help="reload the given extension, developer only")
    async def reload(self, ctx, ext):
        await self.loading_behaviour(
            ctx, self.client.reload_extension, ext, f"{ext} reloaded"
        )

    @commands.command(
        name="creload",
        aliases=["reloadc", "ureload", "reloadu"],
        help="reload the config and utils, developer only",
    )
    async def reload_config_utils(self, ctx):
        reload(self.client.config)
        reload(self.client.utils)
        await ctx.send("config and utils reloaded")


def setup(client):
    client.add_cog(LoadUnloadReload(client))
