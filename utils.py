import discord


async def strikethrough(message: discord.Message, new_message: str = ""):
    await message.edit(content=f"~~{message.content}~~ {new_message}")
    try:
        await message.clear_reactions()
    except discord.Forbidden:
        pass
