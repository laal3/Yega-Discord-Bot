def write_message(context, *arg):
    message = str(context.message.content).split()

    if not len(message) > 2:
        return "There is no message."

    channel = None
    for _channel in context.guild.channels:
        if _channel.name == args[0]:
        channel = _channel
        break

    if not channel:
        return f"There's no channel named \"{args[0]}\"."