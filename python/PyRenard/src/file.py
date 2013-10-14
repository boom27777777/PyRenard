import time


class loadPrefs:
    def __init__(self, name):
        self.name = name

    def load(self):
        try:
            conf = open('settings.conf', 'r')
            args = conf.readlines()
            conf.close()
            try:
                args[0] = str(args[0]).replace('host=', '').rstrip()
                args[1] = int(str(args[1].replace('port=', '').rstrip()))
                args[2] = str(args[2]).replace('nick=', '').rstrip()
                args[3] = str(args[3]).replace('username=', '').rstrip()
                args[4] = str(args[4]).replace('ident=', '').rstrip()
                args[5] = str(args[5]).replace('realname=', '').rstrip()
                args[6] = str(args[6]).replace('owners=', '').rstrip().split(',')
                args[7] = str(args[7]).replace('chanlist=', '').rstrip().split(',')
                return args
            except (IndexError, ValueError):
                print('Settings not found, did you fill out the settings.conf?')
                return []
        except (IOError):
            conf = open('settings.conf', 'wb')
            conf.write(bytes('host=\nport=\nnick=\nusername=\nident=\nrealname=\nowners=\nchanlist='))
            raise SettingsFileNotFoundError


class Logger():
    def __init__(self, name, logFile):
        self.NAME = name
        self.LOGFILE = logFile

    def log(self, channel, sender, message):
        outstr = bytes('[{0}][{1}] {2}: {3}\r\n'.format(time.asctime(time.localtime()), channel, sender, message))
        try:
            f = open(self.LOGFILE, 'ab')
            f.write(outstr)
            f.close()
        except IOError:
            f = open(self.LOGFILE, 'wb')
            f.write(outstr)
            f.close()

    def getTarget(self):
        return self.LOGFILE

    def getName(self):
        return self.NAME


class SettingsFileNotFoundError(BaseException):
    pass