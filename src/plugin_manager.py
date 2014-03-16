import os
import irc
import traceback


class PluginManager:
    def __init__(self, irc_bot):
        self.attached = irc_bot
        self.plugins = []

    def load_plugins(self):
        self.plugins = None
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
                print("!!!Failed to load plugin " + f + "!!!")
                trace = traceback.format_exc()
                e, logger = self.attached.get_logger('Error')
                logger.log('PluginManager', '', trace)
                print(trace)
        self.plugins = pl

    def run_plugins(self, typ, channel, sender, message):
        current_plugin = None
        try:
            for pl in self.plugins:
                current_plugin = pl
                if pl['enabled'] and pl['callbacks']['type'] == typ:
                    status, results = pl['plugin'].run(typ, channel, sender, message, self.attached)
                    if status:
                        if (results['type'] == 'irc_privmsg'):
                            self.attached.add_to_queue(irc.irc_privmsg(results['target'],
                                                       results['message']))
                        if (results['type'] == 'privmsglist'):
                            for x in results['list']:
                                self.attached.add_to_queue(irc.irc_privmsg(results['target'], x))
        except:
            trace = traceback.format_exc()
            print("!!!Error raised in Plugin: " + current_plugin['name'] + "!!!\r\n" + trace)
            e, logger = self.attached.get_logger('Error')
            logger.log('PluginManager', current_plugin['name'], trace)

    def get_plugins(self):
        return self.plugins