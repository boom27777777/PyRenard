class plugin():
    def callback(self):
        return {'type': 'PRIVMSG', 'help': self.hlp}

    def hlp(self, typ, channel, sender, message, irc_bot):
        return {'type': 'irc_privmsg', 'target': channel, 'message':
                        'What can I help you with? (Ex. !help [plugin])'}

    def run(self, typ, channel, sender, message, irc_bot):
        plugins = irc_bot.plugin_manager.get_plugins()
        if not message.find('!help'):
            message = message.strip('!help').rstrip()
            if message != '':
                try:
                    for pl in plugins:
                        if pl['name'] == message.replace(' ', ''):
                            try:
                                if pl['callbacks']['help']:
                                    hlp = pl['plugin'].callback()['help']
                                    resp = hlp(typ, channel, sender, message, irc_bot)
                                    return True, resp
                            except (KeyError, ValueError):
                                return True, {'type': 'irc_privmsg', 'target': channel,
                                              'message': 'The plugin ' + pl['name'] +
                                                         ' does not have a help callback'}
                    return True, {'type': 'irc_privmsg', 'target': channel,
                                  'message': 'Plugin not found'}
                except:
                    return True, {'type': 'irc_privmsg', 'target': channel, 'message':
                                  'What can I help you with? (Ex. !help [plugin])'}
            else:
                return True, {'type': 'irc_privmsg', 'target': channel, 'message':
                              'What can I help you with? (Ex. !help [plugin])'}
        return False, {}