def irc_nick(new_nick):
    return 'NICK {0}\r\n'.format(new_nick)


def irc_user(user_name, ident, real_name):
    return 'USER {0} 0 {1} : {2}\r\n'.format(user_name, ident, real_name)


def irc_pong(challenge):
    return 'PONG {0}\r\n'.format(challenge)


def irc_join(channel):
    return 'JOIN {0}\r\n'.format(channel)


def irc_part(channel, reason=''):
    return 'PART {0} :{1}\r\n'.format(channel, reason)


def irc_privmsg(target, message=''):
    return 'PRIVMSG {0} :{1}\r\n'.format(target, message)


def irc_quit(reason=''):
    return 'QUIT :{0}\r\n'.format(reason)


def irc_kick(channel, users, reason=''):
    li = ''
    for usr in users:
        li = li + ' ' + usr
    return 'KICK {0} {1} :{2}\r\n'.format(channel, li, reason)

