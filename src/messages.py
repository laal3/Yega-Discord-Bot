import re
from youtube_dl import YoutubeDL
import discord
from utils import getEstimatedTimeToPlay

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
}
ytdl = YoutubeDL(YTDL_OPTIONS)

async def sendPlayMessage(context, title, duration, url, queue):
    expression = "^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*"
    
    embed = discord.Embed(title=title, url=url)
    embed.set_thumbnail(url=f"https://i.ytimg.com/vi/{re.search(expression, url)[0]}/maxresdefault.jpg")
    embed.add_field(name="Song duration:", value=duration, inline=True)

    if queue:
        embed.add_field(name="Position in queue:", value=len(queue), inline=True)
        youtube_info = ytdl.extract_info(queue[0], download=False)
        embed.add_field(name="Next:", value=youtube_info['title'], inline=True)
    else:
        embed.add_field(name="Position in queue:", value="Current", inline=True)
        embed.add_field(name="Next:", value="This is the last song :(", inline=True)
    
    
    
    estimated_time = getEstimatedTimeToPlay(queue)
    embed.add_field(name="Estimated time until playing:", value=f"{estimated_time//3600}:{estimated_time//60}:{estimated_time%60}", inline=True)

    bot_message = await context.channel.send(embed=embed)

    pause = "⏸"
    play = "▶"
    skip = "⏩"
    shuffle = "🔀"
    repeat = "🔁"
    stop = "⛔"

    await bot_message.add_reaction(pause)
    await bot_message.add_reaction(play)
    await bot_message.add_reaction(skip)
    await bot_message.add_reaction(shuffle)
    await bot_message.add_reaction(repeat)
    await bot_message.add_reaction(stop)


async def writeMessage(context, *args):
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

    ms = await channel.send(" ".join(message[2:]))