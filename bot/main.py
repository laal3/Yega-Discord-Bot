from http import client
from discord.ext import commands
import discord
import os
from utils import writeMessage
import music
from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix='~')
music = music.Music(bot)
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


@bot.event
async def on_ready():
  print("Beep Boop")

#make sure the bot don't crashes because of his own messages or dm messages
@bot.listen('on_message')
async def on_message(message):
  if message.author == bot.user:
    return
  if isinstance(message.channel, discord.DMChannel):
    return

#repeats your message in your choosen text channel
#~write <channel name> <message>
@bot.command()
async def write(context, *args):
  await writeMessage(context, *args)
  

@bot.command()
async def play(context, *args):
  music.play(args[0])

@bot.command()
async def forceplay(context, *args):
  music.force_play(args[0])

@bot.command()
async def pause(context, *args):
  music.pause()

@bot.command()
async def resume(context, *args):
  music.resume(args[0])

@bot.command()
async def stop(context, *args):
  music.stop()

@bot.command()
async def skip(context, *args):
  music.skip()

@bot.command()
async def repeat(context, *args):
  music.repeat_toggle() 

@bot.command()
async def shuffle(context, *args):
  music.shuffle_toggle()

@bot.command()
async def dropQueue(context, *args):
  music.drop_queue()

@bot.command()
async def removeFromQueue(context, *args):
  music.remove_from_queue(args[0])

@bot.command()
async def disconnect(context, *args):
  music.disconnect()


@bot.event
async def on_reaction_add(reaction, user):
  if user == client.user:
    return

  await reaction.message.edit(".")


bot.run(CLIENT_SECRET)