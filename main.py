import discord
import os
import asyncio
import urllib.request

from discord.ext import commands

# File where it contains private Discord Token
TOKEN_FILE = "token.txt"

intents = discord.Intents.all()

discord_handler = commands.Bot(command_prefix="/", intents=intents)


# Looks through all the files in
# the extensions folder and returns the list of python files.
def getAllExtensions():
    return [x[:-3] for x in os.listdir('./extensions') if x.endswith('.py')]


# Loads all the extensions from extensions folder
async def loadAllExtensions():
    for ext in getAllExtensions():
        await discord_handler.load_extension(f'extensions.{ext}')


# Unloads all the extensions from extensions folder
async def unloadAllExtensions():
    for ext in getAllExtensions():
        await discord_handler.unload_extension(f'extensions.{ext}')


@commands.command()
async def unloadExtension(ctx, arg1):
    if arg1 is None:
        await ctx.send('Input the correct name of extension')
        return

    await ctx.send(f'Unloading {arg1}...')

    await discord_handler.unload_extension(f'extensions.{arg1}')


# Update Extension command
# Fetches Extension code from github (raw content raw.github) and
# Unloads extension and rewrites the file with new code
@commands.command()
async def updateExtension(ctx, name=None):
    if name is None:
        await ctx.send('Input the correct name of extension')
        return

    await ctx.send(f'Fetching {name} from repository...')

    contents = urllib.request.urlopen(
        f'https://raw.githubusercontent.com/MicaelOps/CSOC-DiscordBot/master/extensions/{name}.py').read()

    print(contents)


# Starts up the Discord bot and extensions
def loadBot():
    asyncio.run(loadAllExtensions())

    discord_handler.add_command(unloadExtension)
    discord_handler.add_command(updateExtension)

    discord_handler.run(readDiscordToken())

    print('Bot loaded successfully!')


# Reads the 72 character token from file
def readDiscordToken():
    fo = open(TOKEN_FILE, "r")
    token = fo.read(72)
    fo.close()

    return token


if __name__ == '__main__':
    loadBot()


