import multiprocessing
import socket
import traceback
from src import irc, file, message, plugin_manager


class IRCBot:
    def __init__(self, host, port, nick, username, ident, realname, owners,
                 chanlist):
        self.HOST = host
        self.PORT = port
        self.NICK = nick
        self.USERNAME = username
        self.IDENT = ident
        self.REALNAME = realname
        self.OWNER = owners
        self.CHANLIST = chanlist
        self.ACTIVE = True
        self.IDENTIFIED = False
        self.ERROR = 'I feel a disturbance in the force.'
        self.QUEUE = []
        self.THREADPOOL = multiprocessing.Pool()
        self.SCRIPTS = []
        self.LOGGER = [file.Logger('Error', 'log/Error.log')]
        self.USERLIST = {}
        self.PLUGINMANAGER = plugin_manager.PluginManager(self)
        self.PLUGINMANAGER.loadPlugins()
        self.SERVERNAME = ''
        self.JOINED = False
        for channel in self.CHANLIST:
            self.LOGGER.append(file.Logger(channel, 'log/' + channel + '.log'))
            self.USERLIST[channel] = []

        s = socket.socket()
        s.connect((self.HOST, self.PORT))
        self.identify(s)
        try:
            while self.ACTIVE:
                self.listen(s)
        except:
            trace = traceback.format_exc()
            print trace
            irc.qUIT('Bye~')
            print('{0}Bailing out!'.format(self.ERROR + ' '))
            self.ACTIVE = False
            try:
                self.THREADPOOL.terminate()
            except:
                pass

    def listen(self, socket):
        line = socket.recv(2048)
        line = str(line).rstrip()

        print(line)
        args = line.split()

        if self.SERVERNAME == '':
            self.SERVERNAME = args[0]
        if not line.find('376') == -1 and not self.JOINED:
            self.join(socket)

        if (args[0] == 'PING'):
            pong = irc.pONG(args[1])
            socket.send(bytes(pong))
            print(pong.rstrip())
            if not self.JOINED:
                self.join(socket)

        if (args[0] == 'ERROR'):
            self.ERROR = line.rstrip()
            raise KeyboardInterrupt

        if (args[0] != 'PING' and args[0] != 'ERROR'):
            p = multiprocessing.Process(None, message.process, None, (line, self))
            p.run()

        while (len(self.QUEUE) > 0):
            command = self.QUEUE.pop(0)
            socket.send(bytes(command))
            print(command)

    def identify(self, socket):
        socket.send(bytes(irc.nICK(self.NICK)))
        socket.send(bytes(irc.uSER(self.USERNAME, self.IDENT, self.REALNAME)))
        self.IDENTIFIED = True

    def join(self, socket):
        for channel in self.CHANLIST:
            socket.send(bytes(irc.jOIN(channel)))

    def addToQueue(self, string):
        self.QUEUE.append(string)

    def addScript(self, obj):
        self.SCRIPTS.append(obj)

    def getLogger(self, name):
        for logger in self.LOGGER:
            if (logger.getName() == name):
                return True, logger
        return False, None

    def updateUserList(self, channel, userList):
        if channel in self.USERLIST:
            self.USERLIST[channel] = userList
            return True
        else:
            return False

    def getUserList(self, channel):
        if channel in self.USERLIST:
            return self.USERLIST[channel]
        else:
            return []

    def isOwner(self, nick):
        for x in self.OWNER:
            if (nick == x):
                return True
        return False

try:
    args = file.loadPrefs('loader').load()
    try:
        t = IRCBot(args[0], args[1], args[2], args[3], args[4], args[5],
                   args[6], args[7])
    except IndexError:
        pass
except file.SettingsFileNotFoundError:
    print('Settings file not found, making one for you now.')
