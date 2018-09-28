#Project imports
import discord
import traceback
import json
import os
from discord.ext import commands

#basic bot setup
bot = commands.Bot(command_prefix='*')
bot.remove_command('help')

def getAuthToken():
    with open('settings.json') as f:
        data = json.load(f)

    return data["authToken"]

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

@bot.command()
async def job(ctx, *args):
    target_job = ""

    for val in args:
        target_job += (val + ' ')

    overview_link = getJobDetails(str.strip(target_job.lower()))

    if overview_link != 'nothing':
        bot_respone = ("Here is a link to help with %s: \n%s" % (target_job, overview_link))
    else:
        bot_respone = ("Sorry, I could not find anything helpful for %s.  Maybe you meant to lookup something else?" % target_job)
    
    await ctx.send(bot_respone)

def getHelpDescription():
    return '```General \n\n info \n\treturns info about me. \n\n mechanics {{dungeon_name}} \n\t returns information about the requested dungeon/raid \n\n jobs {{job_name}} \n\t returns information about the requested job/class```'

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

def getJobDetails(arg):
    wiki_links = {
        "lancer": "lancer",
        "rogue": "rogue",
        "archer": "archer",
        "gladiator": "gladiator",
        "pugilist": "pugilist",
        "marauder": "marauder",
        "conjurer": "conjurer",
        "thaumaturge": "thaumaturge",
        "arcanist": "archanist",
        "warrior": "warrior",
        "paladin": "paladin",
        "monk": "monk",
        "dragoon": "dragoon",
        "bard": "bard",
        "white mage": "white_mage",
        "black mage": "black_mage",
        "summoner": "summoner",
        "scholar": "scholar",
        "ninja": "ninja",
        "dark knight": "dark_knight",
        "astrologian": "astrologian",
        "machinist": "machinist",
        "samurai": "samurai",
        "red mage": "red_mage"
    }

    if arg in wiki_links:
        wiki_link = "https://ffxiv.consolegameswiki.com/wiki/%s" % wiki_links.get(arg)
    else:
        wiki_link = "nothing"

    return wiki_link

bot.run(getAuthToken())