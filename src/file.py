import time


class LoadPrefs:
    def __init__(self, name):
        self.name = name

    def load(self):
        try:
            conf = open('settings.conf', 'r')
            args = conf.readlines()
            conf.close()
            settings = {}
            try:
                for arg in [x for x in args if x != '\n']:
                    temp = arg.rstrip().split('=')
                    if len(temp[1].split(',')) > 1:
                        settings[temp[0]] = temp[1].split(',')
                    else:
                        settings[temp[0]] = temp[1]
                return settings
            except (IndexError, ValueError):
                print('Settings not found, did you fill out the settings.conf?')
                return {}
        except (IOError):
            conf = open('settings.conf', 'wb')
            conf.write(bytes('host=\nport=\nnick=\nusername=\nident=\nrealname=\nowners=\nchanlist=\nssl='))
            raise SettingsFileNotFoundError


class Logger():
    def __init__(self, name, log_file):
        self.name = name
        self.logfile = log_file

    def log(self, channel, sender, message):
        outstr = bytes('[{0}][{1}] {2}: {3}\r\n'.format(time.asctime(time.localtime()), channel, sender, message))
        try:
            f = open(self.logfile, 'ab')
            f.write(outstr)
            f.close()
        except IOError:
            f = open(self.logfile, 'wb')
            f.write(outstr)
            f.close()

    def get_target(self):
        return self.logfile

    def get_name(self):
        return self.name


class SettingsFileNotFoundError(BaseException):
    pass