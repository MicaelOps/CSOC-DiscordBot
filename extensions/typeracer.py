import heapq
import random

import discord
import traceback

from discord.ext import commands

# Heap structure holding racers stats in tuple form
# (discord_id, words_per_min)
racer_stats = []

# Fastest typist in the world
FASTEST_TYPIST_WPM = 262


class TypingModal(discord.ui.Modal, title='Typing Test'):

    name = discord.ui.TextInput(
        label='Test',
        placeholder='Your text here',
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Thanks for your feedback, {self.name.value}!', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)


# Generates random text by picking a piece of text from a file with length of
# the fastest typist (yes, it assumes that there isn't anyone capable of going over that
# in the Computing Society).
def generateRandomText():
    with open('bigtext.txt', 'r', encoding='UTF-8') as fo:
        fo.seek(random.randint(0, FASTEST_TYPIST_WPM))

        return fo.read(FASTEST_TYPIST_WPM)


# Load Type racer stats and push them to a heap
def loadLeaderboard():
    with open('racerstats.txt', 'r+') as fo:
        for line in fo:
            token = str.split(line, ':', maxsplit=1)

            heapq.heappush(racer_stats, (int(token[0]), int(token[1])))


# Save Type racer Stats into text file.
def saveLeaderboard():
    with open('racerstats.txt', 'w') as fo:
        for i in range(len(racer_stats)):
            fo.write(f'{racer_stats[i][0]}:{racer_stats[i][1]}\n')


@commands.command()
async def startTypingTest(interaction: discord.Interaction):
    modal = TypingModal()
    await interaction.response.send_modal(modal)


# Shows Top 10 racers
@commands.command()
async def showLeaderboard(ctx):
    top_ten = heapq.nlargest(10, racer_stats, lambda racer: racer[1])

    main_embed = discord.Embed(colour=discord.Colour.from_rgb(241, 196, 15))
    main_embed.set_author(name='CSOC Discord bot', url='https://github.com/MicaelOps/CSOC-DiscordBot')

    top_ten_text = '\n  \n \n'
    filled_positions = 0

    for racer_index in range(len(top_ten)):
        top_ten_text = top_ten_text + f'TOP{racer_index + 1} {top_ten[racer_index][0]} - {top_ten[racer_index][1]} WPM \n'
        filled_positions = filled_positions + 1

    # Fill the remainder positions in the Top 10
    for racer_position in range(filled_positions, 10):
        top_ten_text = top_ten_text + f'TOP {racer_position + 1}  ######## - 0 WPM \n'

    main_embed.add_field(name='Top 10 Type racer', value=top_ten_text, inline=True)

    # Avoid mention of top 10 usernames from becoming a notification
    await ctx.channel.send(silent=True, embed=main_embed)

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
