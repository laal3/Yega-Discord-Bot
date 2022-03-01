import multiprocessing
import discord
from youtube_dl import YoutubeDL
import random
import asyncio
import re

FFMPEG_OPTIONS = {}

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
        self.player = None
        self.queue = []
        self.shuffle = False
        self.repeat = False
        self.force = False
        

    async def play(self, url):
        if not self.voice_channel:
            await context.channel.send("No channel to join." + self.voice_channel)
            return

        if self.voice_client == None:
            await self.voice_channel.connect()

        if self.context.voice_client.is_playing():
            self.queue.append(url)
        else:
            self.player = multiprocessing.Process(target=self.player_loop())
            self.player.start()
        
        await self.context.channel.send("Added")
        
            
    async def pause(self):
        if self.voice_client == None or not self.voice_client.is_playing:
            return

        await self.voice_client.pause()
        await self.context.channel.send("Paused")
        #TODO: Message

    async def resume(self):
        if self.voice_client == None or self.voice_client.is_playing:
            return

        await self.voice_client.resume()
        await self.context.channel.send("Resumed")
        #TODO: Message

    #Cancels the player loop and restarts it to skip the current song
    async def skip(self):
        if not self.player:
            return
        
        self.player.terminate()
        self.player = multiprocessing.Process(target=self.player_loop())
        self.player.start()
        await self.context.channel.send("Skiped")

    async def stop(self):
        if self.voice_client == None or not self.voice_client.is_playing():
            return

        await self.voice_client.stop()
        self.queue = []
        await self.context.channel.send("Stoped")
        #TODO: Message:

    async def force_play(self, url):
        if not self.player:
            return

        self.player.terminate()
        self.queue.insert(0, url)
        self.force = True
        self.player = multiprocessing.Process(target=self.player_loop())
        self.player.start()
        await self.context.channel.send("Playing with force")   

    async def repeat_toggle(self):
        if self.repeat:
            self.queue.pop()

        self.repeat = not self.repeat

        if self.repeat:
            await self.context.channel.send("Repeat on")
        await self.context.channel.send("Repeat off")

    async def shuffle_toggle(self):
        self.shuffle = not self.shuffle

        if self.shuffle:
            await self.context.channel.send("Shuffle on")
        await self.context.channel.send("Shuffle off")

    def get_queue(self):
        return self.queue
        #TODO: Message

    async def drop_queue(self):
        self.queue = []
        await self.context.channel.send("Deleted queue")

    async def remove_from_queue(self, remove_param):
        if remove_param.startswith('http') and remove_param in self.queue:
            self.queue.pop(self.queue.index(remove_param))
            #TODO: Message
        elif isinstance(remove_param, int) and remove_param - 1 > 0 and remove_param - 1 <= len(self.queue):
            self.queue.pop(remove_param)
            #TODO: Message
        elif remove_param == re("[0-9]+-[0-9]"):
            remove_range = remove_param.split("-")

            start = min(remove_range[0], remove_range[1])
            end = max(remove_range[0], remove_range[1])

            if start - 1 < 0 or max > len(self.queue):
                    return False

            for i in range(start - 1, end - 1):
                self.queue.pop(i)

            await self.context.channel.send("Removed")
        else:
            await self.context.channel.send("Not removed")
            #TODO: Messgae
            
            
    async def disconnect(self):
        if self.voice_client == None or not self.voice_client.is_connected():
            return
        
        await self.voice_client.stop()
        self.player.terminate()
        await self.voice_client.disconnect()
        self.queue = []
        await self.context.channel.send("Disconnected")

    async def player_loop(self):
        while self.queue:
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
            

            youtube_info = ytdl.extract_info(url, download=False)
            audio_source = youtube_info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(audio_source, **FFMPEG_OPTIONS)
            await self.voice_client.play(source)
            #TODO: Message