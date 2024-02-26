from discord.ext import commands
from discord.ext.commands import bot


@commands.command()
async def hello(ctx):
    await ctx.send(f'Hello 2.0 {ctx.author.display_name}.')


async def nsfw_message_listener(message):
    message.edit('none')


# Extension init required as per documentation
# https://discordpy.readthedocs.io/en/stable/ext/commands/extensions.html
async def setup(bot):
    print('NSFW extension loaded.')

    bot.add_command(hello)

    bot.add_listener(nsfw_message_listener, 'on_message')
