from youtube_dl import YoutubeDL

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
}

ytdl = YoutubeDL(YTDL_OPTIONS)

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

    await channel.send(" ".join(message[2:]))
    


def getEstimatedTimeToPlay(queue):
    estimated_time = 0
    for i in queue:
        youtube_info = ytdl.extract_info(i, download=False)
        estimated_time += youtube_info['duration']

    return estimated_time
