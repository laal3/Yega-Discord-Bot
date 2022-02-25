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
        self.voice_client = context.Voice_client
        self.voice_channel = context.message.author.voice.channel
        self.player = None
        self.queue = []
        self.shuffle = False
        self.repeat = False
        self.force_play = False

        
    def play(self, url):
        if not self.voice_channel:
            self.context.channel.send("No channel to join.")

        if not self.voice_client.is_connected():
            self.voice_channel.connect()

        if self.context.voice_client.is_playing():
            self.queue.append(url)
        else:
           self.player = asyncio.create_task(self.player_loop())
        
        self.context.channel.send("Added")
        
            
    def pause(self):
        if not self.voice_client.is_playing:
            return

        self.voice_client.pause()
        self.context.channel.send("Paused")
        #TODO: Message

    def resume(self):
        if self.voice_client.is_playing:
            return

        self.voice_client.resume()
        self.context.channel.send("Resumed")
        #TODO: Message

    #Cancels the player loop and restarts it to skip the current song
    def skip(self):
        if not self.player:
            return
        
        self.player.cancel()
        self.player = asyncio.create_task(self.player_loop())

    def stop(self):
        if not self.voice_client.is_playing():
            return

        self.voice_client.stop()
        self.queue = []
        self.context.channel.send("Skiped")
        #TODO: Message:

    def force_play(self, url):
        if not self.player:
            return

        self.player.cancel()
        self.queue.insert(0, url)
        self.force_play = True
        self.player = asyncio.create_task(self.player_loop())
        self.context.channel.send("Playing with force")   

    def repeat_toggle(self):
        if self.repeat:
            self.queue.pop()

        self.repeat = not self.repeat

        if self.repeat:
            self.context.channel.send("Repeat on")
        self.context.channel.send("Repeat off")

    def shuffle_toggle(self):
        self.shuffle = not self.shuffle

        if self.shuffle:
            self.context.channel.send("Shuffle on")
        self.context.channel.send("Shuffle off")

    def get_queue(self):
        return self.queue
        #TODO: Message

    def drop_queue(self):
        self.queue = []
        self.context.channel.send("Deleted queue")

    def remove_from_queue(self, remove_param):
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

            self.context.channel.send("Removed")
        else:
            self.context.channel.send("Not removed")
            #TODO: Messgae
            
            
    def disconnect(self):
        self.voice_client.stop()
        self.player.cancel()
        self.voice_client.disconnect()
        self.queue = []
        self.context.channel.send("Disconnected")

    async def player_loop(self):
        while self.queue:
            #not connected
            if not self.voice_client.is_connected():
                self.context.channel.send("Not connected")
                #TODO: better message
                return

            #empty channel
            if not self.voice_channel.members:
                self.voice_client.disconnect()
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
            self.voice_client.play(source)
            #TODO: Message