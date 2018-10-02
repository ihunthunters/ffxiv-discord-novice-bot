#Project imports
import discord
import traceback
import json
import os
import logging
from textblob import TextBlob
from discord.ext import commands

#logging setup
logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='novice_bot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#basic bot setup
bot = commands.Bot(command_prefix='*')
bot.remove_command('help')

def getAuthToken():
    with open('settings.json') as f:
        data = json.load(f)

    return data["authToken"]

#setup the error handling
@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(title='An Error Has Occured', description='Sorry, something wen''t wrong.  I will log the error and have Hunter fix it later.', colour=0xFF0000)

    await ctx.send(embed=embed)    

#setup the command listeners
@bot.command()
async def info(ctx):
    embed = discord.Embed(title='Novice Guide - FFXIV', description='I am a guide designed to answer basic questions about the game and it''s mechanics.\n\nQuestions? message Hunter.', author='Hunter James @ihunthunters7', colour=0x00FF00)

    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    description = getHelpDescription()
    embed = discord.Embed(title='Commands Help', description=description, author='Hunter James', colour=0x00FF00)
    
    await ctx.send(embed=embed)

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
async def jobs(ctx, *args):
    target_job = ""

    for val in args:
        target_job += (val + ' ')

    overview_link = getJobDetails(str.strip(target_job.lower()))

    if overview_link != 'nothing':
        bot_response = ("Here is a link to help with %s: \n%s" % (target_job, overview_link))
    else:
        bot_response = ("Sorry, I could not find anything helpful for %s.  Maybe you meant to lookup something else?" % target_job)
    
    await ctx.send(bot_response)

@bot.command()
async def hunting_logs(ctx, *args):
    args_list = [arg for arg in args]
    target_job = ''.join(args_list)

    log_link = getHuntingLogs(str.strip(target_job.lower()))

    if log_link != 'nothing':
        bot_response = ("Here is a link to help with %s: \n%s" % (target_job, log_link))
    else:
        bot_response = ("Sorry, I could not find anything helpful for %s.  Maybe you meant to lookup something else?" % target_job)
 
    await ctx.send(bot_response)        

def getHelpDescription():
    return '---------- General ----------\n\n info \n\treturns info about me. \n\n mechanics {{dungeon_name}} \n\t returns information about the requested dungeon/raid \n\n jobs {{job_name}} \n\t returns information about the requested job/class \n\n hunting_logs {{job_name}} \n\treturns information about that classes hunting logs \n\n ---------- In Development ----------\n\n professions {{job_name}} \n\treturns information about a specific profession'

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

def getHuntingLogs(arg):
    log_links = {
        "lancer": "lancer",
        "rogue": "rogue",
        "archer": "archer",
        "gladiator": "gladiator",
        "pugilist": "pugilist",
        "marauder": "marauder",
        "conjurer": "conjurer",
        "thaumaturge": "thaumaturge",
        "arcanist": "archanist",
    }

    if arg in log_links:
        log_link = "https://ffxiv.consolegameswiki.com/wiki/%s_Hunting_Log" % log_links.get(arg)
    else:
        log_link = "nothing"

    return log_link





#setup basic message processing
@bot.event
async def on_message(message):
    print(message.content)

    #blob out the content of the message
    blob = TextBlob(message.content)
    processMessage(blob)

    '''TODO: 
        1) Parse message.
        2) Determine if the message is directed to the bot or the channel.
        3) Determine if the message is a question.
        4) Determine what the subject of the question is.
        5) ???
        6) Profit.
    '''

def processMessage(blob):
    #pull the subject out of the message
    subjects = [tag for tag in blob.tags if tag[1] == 'PRP']
    print('\nSubject ->')
    print(subjects)

def isQuestion(input):
    #TODO: There are other ways to tell if its a question.
    if input.ends_with('?'):
        return True
    else:
        return False


bot.run(getAuthToken())