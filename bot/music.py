import re
from youtube_dl import YoutubeDL
import random
import asyncio

FFMPEG_OPTIONS = {}

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
}

ytdl = YoutubeDL(YTDL_OPTIONS)

class Music(bot):
    def __init__(self, context):
        self.context = context
        self.voice_client = context.voice_client
        self.channel = context.message.author.voice.channel
        self.player = None
        self.queue = []
        self.shuffle = false
        self.repeat = false
        self.force_play = false

        
    def play(url):
        if not self.channel:
            self.context.channel.send("No channel to join.")

        if not self.voice_client.is_connected():
            self.channel.connect()

        if self.context.voice_client.is_playing():
            self.queue.append(self.url)
        else:
           player = asyncio.create_task(self.player_loop())
            
    def pause():
        if not self.voice_client.is_playing:
            return

        await self.voice_client.pause()
        #TODO: Message

    def resume():
        if self.voice_client.is_playing:
            return

        await self.voice_client.resume()
        #TODO: Message

    #Cancels the player loop and restarts it to skip the current song
    def skip():
        if not self.player
            return
        
        self.player.cancel()
        self.player = asyncio.create_task(self.player_loop())

    def stop():
        if not self.voice_client.is_playing():
            return

        await self.voice_client.stop()
        self.queue = []
        #TODO: Message:

    def force_play(url):
        if not self.player
            return

        player.cancel()
        self.queue.insert(0, url)
        self.force_play = True
        self.player = asyncio.create_task(self.player_loop())     

    def repeat_toggle():
        if self.repeat:
            self.queue.pop()

        self.repeat = !self.repeat

    def shuffle_toggle():
        self.shuffle = !self.shuffle

    def get_queue():
        return self.queue

    def drop_queue():
        self.queue = []

    def remove_from_queue(remove_param):
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
                    return false

            for i in range(start - 1, end - 1):
                self.queue.pop(i)

            #TODO: Message
        else:
            #TODO: Messgae
            pass
            
    def disconnect():
        await self.voice_client.stop()
        self.player.cancel()
        await self.voice_client.disconnect()
        self.queue = []

    async def player_loop():
        while self.queue:
            #not connected
            if not self.voice_client.is_connected():
                self.context.channel.send("Not connected")
                #TODO: better message
                return

            #empty channel
            if not self.channel.members:
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
            

            youtube_info = ytdl.extract_info(url, download=false)
            audio_source = youtube_info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(I_URL, **FFMPEG_OPTIONS)
            self.voice_client.play(source)
            #TODO: Message