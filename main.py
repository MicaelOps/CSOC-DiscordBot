import discord
import os
import asyncio
import urllib.request
import urllib.error

from discord import app_commands
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
    await asyncio.gather(*(discord_handler.load_extension(f'extensions.{ext}') for ext in getAllExtensions()))


# Unloads all the extensions from extensions folder
async def unloadAllExtensions():
    await asyncio.gather(*(discord_handler.unload_extension(f'extensions.{ext}') for ext in getAllExtensions()))


# Unload command to disable an extension
@discord_handler.tree.command()
async def unloadextension(interaction: discord.Interaction, name: str):
    if name is None:
        await interaction.response.send_message.send('Input the correct name of extension')
        return

    await interaction.response.send_message(f'Unloading {name}...')

    await discord_handler.unload_extension(f'extensions.{name}')


# Update Extension command to  create or update extension by checking the latest version on github.
@discord_handler.tree.command()
@app_commands.describe(
    name='Name of the extension',
)
async def updateextension(interaction: discord.Interaction, name: str):
    # Check if first command parameter exists
    if name is None:
        await interaction.response.send_message('Input the correct name of extension')
        return

    await interaction.response.send_message(f'Fetching {name} from repository...')

    try:

        # Retrieve the code from Repository and Update Extension python file
        updateExtensionFile(name, retrieveExtensionCode(name))

        # Checking if extension has already been loaded
        if f'extensions.{name}' in discord_handler.extensions:
            await interaction.response.send_message(f'Reloading extension {name}...')
            await discord_handler.reload_extension(f'extensions.{name}')
        else:
            await interaction.response.send_message(f'Creating new extension {name}...')
            await discord_handler.load_extension(f'extensions.{name}')

        await interaction.response.send_message('Done!')

    except urllib.error.HTTPError:
        await interaction.response.send_message(f'File {name} not found on repository')
    except ExtensionFailed:
        await interaction.response.send_message('Something went wrong while loading the extension')


# Fetches code from github repository
def retrieveExtensionCode(name):
    # Headers specified as per documentation.
    # https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#get-repository-content
    git_headers = {
        "Accept": "application/vnd.github.raw+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # More info https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#get-repository-content
    git_request = urllib.request.Request(
        url=f'https://api.github.com/repos/MicaelOps/CSOC-DiscordBot/contents/extensions/{name}.py?ref=master',
        headers=git_headers)

    urlcon = urllib.request.urlopen(git_request)
    return urlcon.read().decode('utf-8')


# Rewrites the extension file code
def updateExtensionFile(name, code):
    with open(f'extensions/{name}.py', "w") as fo:
        fo.write(code)


# Starts up the Discord bot and extensions
def loadBot():
    asyncio.run(loadAllExtensions())

    # This is ugly asf but i cba to do the correct way
    discord_handler.tree.remove_command('updateextension')
    discord_handler.tree.remove_command('unloadextension')

    discord_handler.tree.add_command(updateextension)
    discord_handler.tree.add_command(unloadextension)

    discord_handler.run(readDiscordToken())

    asyncio.run(discord_handler.tree.sync())

    print('Bot loaded successfully!')


# Reads the 72 character token from file
def readDiscordToken():
    with open(TOKEN_FILE, "r") as fo:
        token = fo.read(72)
        fo.close()

        return token


if __name__ == '__main__':
    loadBot()
