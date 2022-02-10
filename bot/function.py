import youtube_dl as yt

async def write_message(context, *args):
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

async def download_song(url):
    pass