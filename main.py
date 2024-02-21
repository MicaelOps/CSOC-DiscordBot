import discord
import os

from discord.ext import commands

# File where it contains private Discord Token
TOKEN_FILE = "token.txt"

intents = discord.Intents.default()
intents.message_content = True

discord_handler = commands.Bot(command_prefix="/", intents=intents)


# Reads the 72 character token from file
def readDiscordToken():
    fo = open(TOKEN_FILE, "r")
    token = fo.read(72)
    fo.close()

    return token


# Looks through all the files in
# the extensions folder and returns the list of python files.
def getAllExtensions():
    return filter(lambda files: files.endswith('.py'), os.listdir('./extensions'))


# Loads all the extensions from extensions folder
def loadAllExtensions():
    for ext in getAllExtensions():
        discord_handler.load_extension(f'extensions.{ext[:-3]}')


# Unloads all the extensions from extensions folder
def unloadAllExtensions():
    for ext in getAllExtensions():
        discord_handler.unload_extension(f'extensions.{ext[:-3]}')


# Starts up the Discord bot and extensions
def loadBot():
    discord_handler.run(readDiscordToken())

    loadAllExtensions()

    print('Bot loaded successfully!')


if __name__ == '__main__':
    loadBot()
