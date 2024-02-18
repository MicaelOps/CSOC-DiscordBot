import discord

TOKEN_FILE = "token.txt"

intents = discord.Intents.default()
intents.message_content = True

discord_handler = discord.Client(intents=intents)


# Reads the token from file
def readDiscordToken():

    fo = open(TOKEN_FILE, "r")
    token = fo.read(72)
    fo.close()

    return token


def loadBot():
    discord_handler.run(readDiscordToken())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    loadBot()
