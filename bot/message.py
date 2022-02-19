import imp
from music import ytdl
import discord
from utils import getEstimatedTimeToPlay

async def sendPlayMessage(context, title, duration, url, queue, next_URL):
    expression = "^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*"
    
    embed = discord.Embed(title=title, url=url)
    embed.set_thumbnail(url=f"https://i.ytimg.com/vi/{re.search(expression, url)[0]}/maxresdefault.jpg")
    embed.add_field(name="Song duration:", value=duration, inline=True)
    embed.add_field(name="Position in queue:", value=len(queue), inline=True)

    youtube_info = ytdl.extract_info(next_URL, download=False)
    embed.add_field(name="Next:", value=youtube_info['title'], inline=True)
    
    estimated_time = getEstimatedTimeToPlay(queue)
    embed.add_field(name="Estimated time until playing:", value=f"{estimated_time//3600}:{estimated_time//60}:{estimated_time%60}", inline=True)

    bot_message = await context.channel.send(embed=embed)
    bot_message.add_reaction()