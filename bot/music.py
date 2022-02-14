import re
from youtube_dl import YoutubeDL
import random

FFMPEG_OPTIONS = {}

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
}

ytdl = YoutubeDL(YTDL_OPTIONS)

class Music(bot):
    def __init__(self, context):
        self.context = context
        self.channel = context.message.author.voice.channel
        self.queue = []
        self.shuffle = false
        self.voice_client = context.voice_client

    def play(url):
        if not self.channel:
            self.context.channel.send("No channel to join.")

        if not self.voice_client.is_connected():
            self.channel.connect()

        if self.context.voice_client.is_playing():
            self.queue.append(self.url)
        else:
            self.player_loop(url)
            

    def pause():
        pass

    def resume():
        pass

    def skip():
        pass

    def stop():
        pass

    def shuffle_toggle():
        self.shuffle != self.shuffle

    def get_queue():
        return self.queue

    def force_play():
        pass

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

            if(remove_range[0] > remove[1]):
                    return false

            for i in range(remove_range[0], remove_range[1]):
                self.queue.pop(i)

            #TODO: Message
        else:
            #TODO: Messgae

            
    def disconnect():
        pass

    async def player_loop():
        while self.queue:
            if not self.voice_client.is_connected():
                self.context.channel.send("Not connected")
                #TODO: better message
                return

            if not self.channel.members:
                self.voice_client.disconnect()
                return

            url = ""
            if self.shuffle:
                url = self.queue.pop(random.randint(0, len(self.queue)))
            else:
                url = self.queue.pop()

            youtube_info = ytdl.extract_info(url, download=false)
            audio_source = youtube_info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(I_URL, **FFMPEG_OPTIONS)
            self.voice_client.play(source)
            
            #TODO: Message