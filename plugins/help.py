class plugin():
    def callback(self):
        return {'type': 'PRIVMSG', 'help': self.hlp}

    def hlp(self, typ, channel, sender, message, ircBot):
        return {'type': 'privmsg', 'target': channel, 'message':
                        'What can I help you with? (Ex. !help [plugin])'}

    def run(self, typ, channel, sender, message, ircBot):
        plugins = ircBot.PLUGINMANAGER.getPlugins()
        if not message.find('!help'):
            message = message.strip('!help').rstrip()
            if message != '':
                try:
                    for plugin in plugins:
                        if plugin['name'] == message:
                            try:
                                if plugin['callbacks']['help']:
                                    hlp = plugin['plugin'].callback()['help']
                                    resp = hlp(typ, channel, sender, message, ircBot)
                                    return True, resp
                            except (KeyError, ValueError):
                                return True, {'type': 'privmsg', 'target': channel,
                                              'message': 'The plugin ' + plugin['name'] +
                                                         ' does not have a help callback'}
                        return {'type': 'privmsg', 'target': channel,
                                'message': 'Plugin not found'}
                except:
                    return {'type': 'privmsg', 'target': channel, 'message':
                            'What can I help you with? (Ex. !help [plugin])'}
            else:
                return {'type': 'privmsg', 'target': channel, 'message':
                        'What can I help you with? (Ex. !help [plugin])'}
        return False, {}