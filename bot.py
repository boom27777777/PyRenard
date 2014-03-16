import multiprocessing
import socket
import traceback
from src import irc, file, message, plugin_manager


class IRCBot:
    def __init__(self, host, port, nick, username, ident, realname, owners,
                 chanlist):
        self.host = host
        self.port = port
        self.nick = nick
        self.username = username
        self.ident = ident
        self.realname = realname
        self.owner = owners
        self.chanlist = chanlist
        self.active = True
        self.identified = False
        self.error = 'I feel a disturbance in the force.'
        self.queue = []
        self.threadpool = multiprocessing.Pool()
        self.scripts = []
        self.logger = [file.Logger('Error', 'log/Error.log')]
        self.userlist = {}
        self.plugin_manager = plugin_manager.PluginManager(self)
        self.plugin_manager.load_plugins()
        self.server_name = None
        self.joined = False
        for channel in self.chanlist:
            self.logger.append(file.Logger(channel, 'log/' + channel + '.log'))
            self.userlist[channel] = []

        s = socket.socket()
        s.connect((self.host, self.port))
        self.identify(s)
        try:
            while self.active:
                self.listen(s)
        except:
            trace = traceback.format_exc()
            print trace
            s.send(irc.irc_quit('Bye~'))
            print('{0}Bailing out!'.format(self.error + ' '))
            self.active = False
            try:
                self.threadpool.terminate()
            except:
                pass

    def listen(self, sock):
        line = sock.recv(2048)
        line = str(line).rstrip()

        print(line)
        temp = line.split()

        if self.server_name is None:
            self.server_name = temp[0]
        if not line.find('376') == -1 and not self.joined:
            self.join(sock)

        if (temp[0] == 'PING'):
            pong = irc.irc_pong(temp[1])
            sock.send(bytes(pong))
            print(pong.rstrip())
            if not self.joined:
                self.join(sock)

        if (temp[0] == 'ERROR'):
            self.error = line.rstrip()
            raise KeyboardInterrupt

        if (temp[0] != 'PING' and temp[0] != 'ERROR'):
            p = multiprocessing.Process(None, message.process, None, (line, self))
            p.run()

        while (len(self.queue) > 0):
            command = self.queue.pop(0)
            sock.send(bytes(command))
            print(command)

    def identify(self, sock):
        sock.send(bytes(irc.irc_nick(self.nick)))
        sock.send(bytes(irc.irc_user(self.username, self.ident, self.realname)))
        self.identified = True

    def join(self, sock):
        for channel in self.chanlist:
            sock.send(bytes(irc.irc_join(channel)))

    def add_to_queue(self, string):
        self.queue.append(string)

    def add_script(self, obj):
        self.scripts.append(obj)

    def get_logger(self, name):
        for logger in self.logger:
            if (logger.get_name() == name):
                return True, logger
        return False, None

    def update_user_list(self, channel, user_list):
        if channel in self.userlist:
            self.userlist[channel] = user_list
            return True
        else:
            return False

    def get_user_list(self, channel):
        if channel in self.userlist:
            return self.userlist[channel]
        else:
            return []

    def is_owner(self, nick):
        for x in self.owner:
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
