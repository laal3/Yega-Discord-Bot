from youtube_dl import YoutubeDL

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
}

ytdl = YoutubeDL(YTDL_OPTIONS)

def getEstimatedTimeToPlay(queue):
    estimated_time = 0
    for i in queue:
        youtube_info = ytdl.extract_info(i, download=False)
        estimated_time += youtube_info['duration']

    return estimated_time
