import traceback


def process(line, irc_bot):
    try:
        line.rstrip()
        args = line.split()
        user = {"Ident": args[0], "Nick": args[0].split('!')[0].replace(":", "")}
        typ = args[1]
        channel = args[2]
        message = line.rstrip().split(':')[2]
        irc_bot.plugin_manager.run_plugins(typ, channel,  user, message)

        logger_exists, logger = irc_bot.get_logger(channel)
        if logger_exists:
            logger.log(channel, user['Nick'], message)
    except:
        trace = traceback.format_exc()
        print trace