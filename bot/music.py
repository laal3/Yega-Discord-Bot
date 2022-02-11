import re

class Music(bot):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.shuffle = false

    def play(url:str):
        pass

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
            pass
        elif isinstance(remove_param, int):
            pass
        elif remove_param == re("[0-9]+-[0-9]"):
            remove_range = remove_param.split("-")

            if(remove_range[0] > remove[1]):
                return false

            for i in range(remove_range[0], remove_range[1]):
               self.queue.pop(i)



    def connect():
        pass

    def disconnect():
        pass


class Player():
    def play(url:str):
        pass