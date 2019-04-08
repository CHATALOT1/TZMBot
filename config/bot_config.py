from discord.ext import commands

relative_cogs_dir = 'cogs'

dev_IDs = [353574266236567556, 328976083145981962, 333945749803106306]

error_dict = {
    commands.CheckFailure: None,
    commands.CommandNotFound: None,
    commands.DisabledCommand: None,
    commands.MissingRequiredArgument: "`{exc.param.name}` is a required argument that is missing.",
    commands.BadArgument: "One of the arguments you entered is invalid, try {ctx.prefix}help {ctx.command} for "
                          "information on how to use this command",
    commands.BadUnionArgument: "One of the arguments you entered is invalid, try {ctx..prefix}help {ctx.command} for "
                               "information on how to use this command",
    commands.NoPrivateMessage: "This command cannot be run in DMs, please try again in a server channel",
    commands.TooManyArguments: "Too many arguments were passed into this command",
    commands.CommandOnCooldown: "This command is on cooldown, try again in {exc.retry_after} seconds.",
    commands.NotOwner: "Only the owner of the bot can use this command",
    commands.MissingPermissions: "You're missing the required permission(s) in this server to use this command:\n"
                                 "{exc.missing_perms}",
    commands.BotMissingPermissions: "I'm missing the required permission(s) in this server to use this command:\n"
                                    "{exc.missing_perms}\nPlease give me those permissions or the Administrator permission",
    commands.CommandInvokeError: "An unexpected error occurred, please report it to `CHATALOT1#0707`"
}

welcome_message = "{member.mention} just joined. welcome!"
goodbye_message = "{member.mention} ({member}) just left. goodbye!"

# MUST BE CHANGED TO THE IDS OF CHANNELS THAT YOUR INSTANCE HAS ACCESS TO:
err_channel_ID = 564885281782890497
welcome_channel_ID = 564885319527432202

