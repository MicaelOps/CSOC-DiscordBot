import discord
import os
import asyncio
import urllib.request
import urllib.error

from discord.ext import commands
from discord.ext.commands import ExtensionFailed

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


# Unload command to disable an extension
@commands.command()
async def unloadExtension(ctx, arg1):
    if arg1 is None:
        await ctx.send('Input the correct name of extension')
        return

    await ctx.send(f'Unloading {arg1}...')

    await discord_handler.unload_extension(f'extensions.{arg1}')


# Update Extension command to  create or update extension by checking the latest version on github.
@commands.command()
async def updateExtension(ctx, name=None):
    if name is None:
        await ctx.send('Input the correct name of extension')
        return

    await ctx.send(f'Fetching {name} from repository...')

    try:

        updateExtensionFile(name, retriveExtensionCode(name))

        if f'extensions.{name}' in discord_handler.extensions:
            await ctx.send(f'Reloading extension {name}...')
            await discord_handler.reload_extension(f'extensions.{name}')
        else:
            await ctx.send(f'Creating new extension {name}...')
            await discord_handler.load_extension(f'extensions.{name}')

        await ctx.send('Done!')

    except urllib.error.HTTPError:
        await ctx.send(f'File {name} not found on repository')
    except ExtensionFailed:
        await ctx.send('Something went wrong while loading the extension')

# Fetches code from github repository
def retriveExtensionCode(name):

    # Headers specified as per documentation.
    # https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#get-repository-content
    git_headers = {
        "Accept": "application/vnd.github.raw+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    git_request = urllib.request.Request(
        url=f'https://api.github.com/repos/MicaelOps/CSOC-DiscordBot/contents/extensions/{name}.py?ref=master',
        headers=git_headers)

    urlcon = urllib.request.urlopen(git_request)
    return urlcon.read().decode('utf-8')

# Rewrites the extension file code
def updateExtensionFile(name, code):
    fo = open(f'extensions/{name}.py', "w")
    fo.write(code)

    # Close opened file
    fo.close()


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
