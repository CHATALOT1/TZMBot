import discord
from discord.ext import commands
import textwrap
import traceback
import io
from contextlib import redirect_stdout


class DevTools(commands.Cog, name="Developer-Only Commands"):
    def __init__(self, client):
        self.client = client
        self.last_eval_result = None

    async def cog_check(self, ctx):
        return ctx.author.id in self.client.config.dev_IDs

    @commands.command(name="eval", help="evaluate python code, developer only")
    async def _eval(self, ctx, *, body: str):
        env = {
            "client": self.client,
            "config": self.client.config,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "__lr": self.last_eval_result,
        }

        env.update(globals())

        if body.startswith("```") and body.endswith("```"):
            body = "\n".join(body.split("\n")[1:-1])

        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "    ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")

        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction("\u2705")
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f"```py\n{value}\n```")
            else:
                self.last_eval_result = ret
                await ctx.send(f"```py\n{value}{ret}\n```")

    @commands.command(
        help="essentially echo, deletes triggering message if pos, developer only"
    )
    async def say(self, ctx, *, message):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        await ctx.send(message)


def setup(client):
    client.add_cog(DevTools(client))
