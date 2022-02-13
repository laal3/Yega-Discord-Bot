import re
from youtube_dl import YoutubeDL
import random

ytdl_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
}

ytdl = YoutubeDL(ytdl_options)

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
        if remove_param.startswith('http'):
            try:
                self.queue.pop(self.queue.index(remove_param))
            except:
                self.context.channel.send("Invalid argument")
        elif isinstance(remove_param, int):
            try:
                self.queue.pop(remove_param)
            except:
                self.context.channel.send("Invalid argument")
        elif remove_param == re("[0-9]+-[0-9]"):
            try:
                remove_range = remove_param.split("-")

                if(remove_range[0] > remove[1]):
                    return false

                for i in range(remove_range[0], remove_range[1]):
                    self.queue.pop(i)
            except:
               self.context.channel.send("Invalid argument") 
        else: 
            return false
            
    def disconnect():
        pass

    async def player_loop():
        while self.queue:
            if not self.voice_client.is_connected():
                self.context.channel.send("Not connected")
                return

            if not self.channel.members:
                self.voice_client.disconnect()

            source_string = ""
            if self.shuffle:
                source_string = self.queue.pop(random.randint(0, len(self.queue)))
            else:
                source_string = self.queue.pop()


            