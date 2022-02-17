from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
load_dotenv()
from function import write_message

bot = commands.Bot(command_prefix='~')
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

print("." + CLIENT_SECRET + ".")

@bot.event
async def on_ready():
  print("Beep Boop")

@bot.listen('on_message')
async def on_message(message):
  if message.author == bot.user:
    return
  if discord.ChannelType.private:
    return
  

#repeats your message in your choosen text channel
#~write <channel name> <message>
@bot.command()
async def write(context, *args):
  await write_message(context, *args)
  

@bot.command()
async def play(context, *args):
  pass


bot.run(CLIENT_SECRET)