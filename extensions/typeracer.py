import discord
from discord.ext import commands
from discord import embeds

import heapq

# Heap structure holding racers stats in tuple form
# (discord_id, words_per_min)
racer_stats = []


# Load Type racer stats and push them to a heap
def loadLeaderboard():
    with open("racerstats.txt", "r") as fo:
        for line in fo:
            print(line)

            token = str.split(line, ':', maxsplit=1)

            heapq.heappush(racer_stats, (int(token[0]), int(token[1])))


# Save Type racer Stats into text file.
def saveLeaderboard():
    with open("racerstats.txt", "w") as fo:
        for i in range(len(racer_stats)):
            fo.write(f'{racer_stats[i][0]}:{racer_stats[i][1]}\n')


@commands.command()
async def startTypingTest(ctx):
    pass


# Shows Top 10 racers
@commands.command()
async def showLeaderboard(ctx):
    top_ten = heapq.nlargest(10, racer_stats, lambda racer: racer[1])

    main_embed = discord.Embed(colour=discord.Colour.from_rgb(241, 196, 15))
    main_embed.set_author(name='TOP 10 Type Racer', url='https://github.com/MicaelOps/CSOC-DiscordBot')
    main_embed.set_footer(text='Understanding this embed shit.')

    main_embed.insert_field_at(0, name='top10', value='omg it works')
    main_embed.insert_field_at(3, name='top1011', value='omg it works')

    await ctx.channel.send(embed=main_embed)

    # for i in range(10):
    #    ctx.bot.get_user(top_ten[0])


# Extension init required as per documentation
# https://discordpy.readthedocs.io/en/stable/ext/commands/extensions.html
async def setup(bot):
    print('Type racer extension loaded')

    loadLeaderboard()

    bot.add_command(startTypingTest)
    bot.add_command(showLeaderboard)


# Extension stop as per documentation
# https://discordpy.readthedocs.io/en/stable/ext/commands/extensions.html
async def teardown(bot):
    print('Type racer extension unloaded')

    saveLeaderboard()
