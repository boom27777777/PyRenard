import os
import irc
import traceback


class PluginManager:
    def __init__(self, ircBot):
        self.ATTACHED = ircBot
        self.PLUGINS = []

    def loadPlugins(self):
        self.PLUGINS = None
        pl = []
        lst = os.listdir('plugins')
        pls = []
        for f in lst:
            if (f != "__init__.py"):
                if (not f.split('.py')[1]):
                    pls.append(f.split('.py')[0])

        for f in pls:
            temp = None
            try:
                temp = __import__("plugins." + f, globals(), locals(), ['plugin'], -1)
                obj = temp.plugin()
                pl.append({'name': f, 'plugin': obj, 'enabled': True, 'callbacks': obj.callback()})
                print("loaded plugin " + f)
            except AttributeError:
                print("!!!Failed to load plugin " + f)
                trace = traceback.format_exc()
                e, logger = self.ATTACHED.getLogger('Error')
                logger.log('PluginManager', '', trace)
                print(trace)
        self.PLUGINS = pl

    def runPlugins(self, typ, channel, sender, message):
        global pl
        try:
            for pl in self.PLUGINS:
                if pl['enabled'] and pl['callbacks']['type'] == typ:
                    status, results = pl['plugin'].run(typ, channel, sender, message, self.ATTACHED)
                    if status:
                        if (results['type'] == 'privmsg'):
                            self.ATTACHED.addToQueue(irc.pRIVMSG(results['target'],
                                                                 results['message']))
                        if (results['type'] == 'privmsglist'):
                            for x in results['list']:
                                self.ATTACHED.addToQueue(irc.pRIVMSG(results['target'], x))
        except:
            trace = traceback.format_exc()
            print("!!!Error raised in Plugin: " + pl['name'] + "\r\n" + trace)
            e, logger = self.ATTACHED.getLogger('Error')
            logger.log('PluginManager', pl['name'], trace)

    def getPlugins(self):
        return self.PLUGINS