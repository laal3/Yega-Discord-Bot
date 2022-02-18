import re
import discord

async def write_message(context, *args):
    message = str(context.message.content).split()

    if not len(message) > 2:
        await context.channel.send(f"There's no channel named {args[0]}.")
        return

    channel = None
    for _channel in context.guild.channels:
        if _channel.name == args[0]:
            channel = _channel
            break

    if not channel:
        await context.channel.send(f"There is no message.")
        return

    await channel.send(" ".join(message[2:]))

def music_embed(title, duration, url, queue_length, next)
    expression = "^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*"
    
    embed = discord.Embed(title=title)
    embed.set_thumbnail(url=f"https://i.ytimg.com/vi/{re.search(expression, url)[0]}/maxresdefault.jpg)
    