import traceback


def process(line, ircBot):
    try:
        line.rstrip()
        args = line.split()
        user = {"Ident": args[0], "Nick": args[0].split('!')[0].replace(":", "")}
        typ = args[1]
        channel = args[2]
        message = line.rstrip().split(':')[2]
        ircBot.PLUGINMANAGER.runPlugins(typ, channel,  user, message)

        loggerExists, logger = ircBot.getLogger(channel)
        if loggerExists:
            logger.log(channel, user['Nick'], message)
    except:
        trace = traceback.format_exc()
        print trace