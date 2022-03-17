from http import client
from discord.ext import commands
import discord
import os
from utils import writeMessage
from music import Music
from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix='~')
voice_list = {}
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
  if not context.message.author.voice:
    return

  channel = str(context.message.author.voice.channel)
  if not channel in voice_list:
    music = Music(context)
    voice_list[channel] = music

  await voice_list[channel].play(url=args[0])

@bot.command()
async def forceplay(context, *args):
  if not context.message.author.voice:
    return

  channel = str(context.message.author.voice.channel)
  if channel in voice_list:
    await voice_list[channel].force_play(url=args[0])
    return

  music = Music(context)
  voice_list[channel] = music
  await voice_list[channel].force_play(url=args[0])

@bot.command()
async def pause(context, *args):
  if not context.message.author.voice:
    return

  channel = str(context.message.author.voice.channel)
  if channel in voice_list:
    await voice_list[channel].pause()
  else:
    await context.channel.send(f"I'm not playing yet. Please start a song first")
  
@bot.command()
async def resume(context, *args):
  if not context.message.author.voice:
    return

  channel = str(context.message.author.voice.channel)
  if channel in voice_list:
    await voice_list[channel].resume()
  else:
    await context.channel.send(f"I'm not playing yet. Please start a song first")

@bot.command()
async def stop(context, *args):
  if not context.message.author.voice:
    return

  channel = str(context.message.author.voice.channel)
  if channel in voice_list:
    await voice_list[channel].stop()
  else:
    await context.channel.send(f"I'm not playing yet. Please start a song first")

@bot.command()
async def skip(context, *args):
  if not context.message.author.voice:
    return

  channel = str(context.message.author.voice.channel)
  if channel in voice_list:
    await voice_list[channel].skip()
  else:
    await context.channel.send(f"I'm not playing yet. Please start a song first")

@bot.command()
async def repeat(context, *args):
  if not context.message.author.voice:
    return

  channel = str(context.message.author.voice.channel)
  if channel in voice_list:
    await voice_list[channel].repeat_toggle()
  else:
    await context.channel.send(f"I'm not playing yet. Please start a song first")

@bot.command()
async def shuffle(context, *args):
  if not context.message.author.voice:
    return

  channel = str(context.message.author.voice.channel)
  if channel in voice_list:
    await voice_list[channel].shuffle_toggle()
  else:
    await context.channel.send(f"I'm not playing yet. Please start a song first")

@bot.command()
async def dropQueue(context, *args):
  if not context.message.author.voice:
    return
    
  channel = str(context.message.author.voice.channel)
  if channel in voice_list:
    await voice_list[channel].drop_queue()
  else:
    await context.channel.send(f"I'm not playing yet. Please start a song first")

@bot.command()
async def removeFromQueue(context, *args):
  if not context.message.author.voice:
    return

  channel = str(context.message.author.voice.channel)
  if channel in voice_list:
    await voice_list[channel].remove_from_queue(args[0])
  else:
    await context.channel.send(f"I'm not playing yet. Please start a song first")

@bot.command()
async def disconnect(context, *args):
  if not context.message.author.voice:
    return

  channel = str(context.message.author.voice.channel)
  if channel in voice_list:
    await voice_list[channel].disconnect()
  else:
    await context.channel.send(f"I'm not playing yet. Please start a song first")


@bot.event
async def on_reaction_add(reaction, user):
  if user == bot.user:
    return

  if not user.voice:
    return

  channel = str(user.voice.channel)
  if not channel in voice_list:
    return

  if reaction.emoji == "⏸":
    await voice_list[channel].pause()
  elif reaction.emoji == "▶":
    await voice_list[channel].resume()
  elif reaction.emoji == "⏩":
    await voice_list[channel].skip()
  elif reaction.emoji == "🔀":
    await voice_list[channel].shuffle_toggle()
  elif reaction.emoji == "🔁":
    await voice_list[channel].repeat_toggle()
  elif reaction.emoji == "⛔":
    await voice_list[channel].stop()
  else:
    await reaction.remove(user)

@bot.event
async def on_voice_state_update(member, before, after):
  if member == bot and before.channel and not after.channel:
    voice_list.pop(str(before.channel))
  

bot.run(CLIENT_SECRET)