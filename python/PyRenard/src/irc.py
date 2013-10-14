def nICK(newNick):
    return 'NICK {0}\r\n'.format(newNick)


def uSER(userName, ident, realName):
    return 'USER {0} 0 {1} : {2}\r\n'.format(userName, ident, realName)


def pONG(challenge):
    return 'PONG {0}\r\n'.format(challenge)


def jOIN(channel):
    return 'JOIN {0}\r\n'.format(channel)


def pART(channel, reason=''):
    return 'PART {0} :{1}\r\n'.format(channel, reason)


def pRIVMSG(target, message=''):
    return 'PRIVMSG {0} :{1}\r\n'.format(target, message)


def qUIT(reason=''):
    return 'QUIT :{0}\r\n'.format(reason)


def kICK(channel, users, reason=''):
    li = ''
    for user in users:
        li = li + ' ' + user
    return 'KICK {0} {1} :{2}\r\n'.format(channel, li, reason)

