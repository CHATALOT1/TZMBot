from discord.ext import commands
import asyncio
import traceback
import sys


class ErrorHandling(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.error_channel = None
        self.client.loop.create_task(self.async_setup())

    async def async_setup(self):
        self.error_channel = self.client.get_channel(self.client.config.err_channel_ID)

    async def err_reporting(self, ctx, err):
        report_confirmation = await ctx.send(
            "An unexpected error occurred, would you like to report it? "
            "You must decide within 30 seconds"
        )
        await report_confirmation.add_reaction(
            "\U0001f1fe"
        )  # regional_indicator_y emoji
        await report_confirmation.add_reaction(
            "\U0001f1f3"
        )  # regional_indicator_n emoji

        try:
            response, user = await self.client.wait_for(
                "reaction_add",
                check=lambda r, u: u.id == ctx.author.id
                and r.emoji in ["\U0001f1fe", "\U0001f1f3"],
                timeout=30,
            )

        except asyncio.TimeoutError:  # 30 seconds passes without response
            await self.client.utils.strikethrough(report_confirmation, "Time's up!")
            return

        if response.emoji == "\U0001f1fe":  # response is yes
            report = "".join(
                traceback.format_exception(type(err), err, err.__traceback__)
            )
            await self.error_channel.send(
                f"Exception raised in command {ctx.command} in cog {ctx.command.cog_name} "
                f"by user {ctx.author}: ```py\n{report}\n```"
            )

        else:  # response is no
            await self.client.utils.strikethrough(
                report_confirmation, "You chose not to report the error"
            )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc):
        if isinstance(exc, commands.CommandInvokeError):
            if ctx.author.id in self.client.config.dev_IDs:
                print(
                    f"Ignoring exception in command {ctx.command} in cog {ctx.command.cog_name}:",
                    file=sys.stderr,
                )
                traceback.print_exception(
                    type(exc), exc, exc.__traceback__, file=sys.stderr
                )

                return await ctx.send("Unexpected error, traceback printed to console")

            return await self.err_reporting(ctx, exc)

        response = self.client.error_dict[type(exc)]

        if response is None:
            return

        await ctx.send(response.format(exc=exc, ctx=ctx))


def setup(client):
    client.add_cog(ErrorHandling(client))
