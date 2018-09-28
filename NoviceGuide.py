#Project imports
import discord
import traceback
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='*')
bot.remove_command('help')

#setup the error handler
#TODO: setup error handling

#setup the command listeners
@bot.command()
async def info(ctx):
    embed = discord.Embed(title='Novice Guide - FFXIV', description='I am a guide designed to answer basic questions about the game and it''s mechanics.\n\nQuestions? message Hunter.', author='Hunter James @ihunthunters7', colour=0x00FF00)

    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    await ctx.send(getHelpDescription())

@bot.command()
async def mechanics(ctx, *args):
    target_mechanic = ""

    for val in args:
        target_mechanic += (val + ' ')

    video_link = getMechanicVideo(str.strip(target_mechanic.lower()))

    if video_link != 'nothing':
        bot_respone = ("Here is a video to help with %s: \n%s" % (target_mechanic, video_link))
    else:
        bot_respone = ("Sorry, I could not find anything helpful for %s.  Maybe you meant to lookup something else?" % target_mechanic)

    await ctx.send(bot_respone)

def getHelpDescription():
    return '```General \n\n info \n\treturns info about me. \n\n mechanics {{dungeon_name}} \n\t returns information about the requested dungeon/raid/duty/boss```'

def getMechanicVideo(arg):
    video_links = {
        "sastasha": "https://www.youtube.com/watch?v=tT3-1Yb787w",
        "tam-tara deepcroft": "https://www.youtube.com/watch?v=_8xWuLi7iVM",
        "copperbell Mines": "https://www.youtube.com/watch?v=cNKaKd1CBnw",
        "halatali": "https://www.youtube.com/watch?v=Lukm-U8aaOw",
        "thousand maws of toto-rak": "https://www.youtube.com/watch?v=LQ2ZlkAEbM4",
        "haukke manor": "https://www.youtube.com/watch?v=n8KhwmjBKII",
        "brayflox's longstop": "https://www.youtube.com/watch?v=1n8mJ7GeXQ0",
        "sunken temple of qarn": "https://www.youtube.com/watch?v=q4GS1N9pMcI"
    }
    return video_links.get(arg, "nothing")

bot.run("token")