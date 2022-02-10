from discord.ext import commands
import os
from './function' import write_message

bot = commands.Bot(command_prefix='~')
my_secret = os.environ['token']

@bot.event
async def on_ready():
  print("Beep Boop")

@bot.listen('on_message')
async def on_message(message):
  if message.author == bot.user:
    return

#repeats your message in your choosen text channel
#~write <channel name> <message>
@bot.command()
async def write(context, *args):

  response = write_message(context, *args)

  #TODO:

  message = str(context.message.content).split()

  if not len(message) > 2:
    await context.channel.send(f"There is no message.")
    return

  channel = None
  for _channel in context.guild.channels:
    if _channel.name == args[0]:
      channel = _channel
      break

  if not channel:
    await context.channel.send(f"There's no channel named \"{args[0]}\".")
    return

  await channel.send(" ".join(message[2:]))


@bot.command()
async def play(context, *args):
  


bot.run(my_secret)