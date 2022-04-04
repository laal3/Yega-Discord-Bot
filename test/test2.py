from discord.ext import commands
import discord
import random
import os
from youtube_dl import YoutubeDL
from youtube_dl import YoutubeDL

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
    }

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
}

ytdl = YoutubeDL(YTDL_OPTIONS)

class Music:
    def __init__(self, context):
        self.context = context
        self.voice_channel = context.message.author.voice.channel
        self.voice_client = discord.utils.get(context.bot.voice_clients, guild=context.guild)
        self.queue = []
        self.shuffle = False
        self.repeat = False
        self.force = False
        self.youtube_info = None
        

    async def play(self, url):
        if not self.voice_channel:
            await self.context.channel.send("No channel to join." + self.voice_channel)
            return

        if self.voice_client == None:
            self.voice_client = await self.voice_channel.connect()
            print(self.voice_client)

        self.queue.append(url)
        if self.context.voice_client.is_playing():
            return

        await self.player_loop()
        
        #await sendPlayMessage(self.context, self.youtube_info["title"], self.youtube_info["duration"], self.youtube_info["bot_url"], self.queue)

    async def player_loop(self):
        if not self.queue:
            return

        #not connected
        if self.voice_client == None or not self.voice_client.is_connected():
            await self.context.channel.send("Not connected")
            #TODO: better message
            return

        #empty channel
        if not self.voice_channel.members:
            await self.voice_client.disconnect()
            return

        url = ""
        if self.shuffle and not self.force_play:
            url = self.queue.pop(random.randint(0, len(self.queue)))
            self.force_play = False
        elif self.repeat and not self.force_play:
            url = self.queue[0]
        else:
            url = self.queue.pop(0)

        self.youtube_info = ytdl.extract_info(url, download=False)
        self.youtube_info["bot_url"] = url
        audio_source = self.youtube_info['formats'][0]['url']
        source = discord.FFmpegPCMAudio(audio_source, **FFMPEG_OPTIONS)
        self.voice_client.play(source, after=self.player_loop)



bot = commands.Bot(command_prefix='~')
voice_list = {}
CLIENT_SECRET = ""#os.getenv("CLIENT_SECRET")

#ignore own messages
@bot.listen('on_message')
async def on_message(message):
    if message.author == bot.user:
        return
    if isinstance(message.channel, discord.DMChannel):
        return

@bot.command()
async def play(context, *args):
    if not context.message.author.voice:
        return



    channel = context.message.author.voice.channel
    if not channel in voice_list:
        music = Music(context)
        voice_list[channel] = music

bot.run(CLIENT_SECRET)




