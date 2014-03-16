class plugin():
    def callback(self):
        return {'type': 'PRIVMSG', 'help': self.hlp}

    def hlp(self, typ, channel, sender, message, ircBot):
        hlp = ['A smiple module managment system.',
               '1. "!plugin list" || a list of all plugins and their current states.',
               '2. "!plugin (enable|disable) [plugin name]" || Change the state of a loaded plugin.',
               '3. "!plugin reload" || Reloads all plugins']
        return {'type': 'privmsglist', 'target': channel, 'list': hlp}

    def run(self, typ, channel, sender, message, irc_bot):
        if message is not None:
            if irc_bot.is_owner(sender['Nick']):
                if not message.find('!plugin') == - 1:
                    if not message.find('list') == - 1:
                        lst = irc_bot.plugin_manager.get_plugins()
                        outstr = ''
                        for x in lst:
                            if x['enabled']:
                                status = 'Enabled'
                            else:
                                status = 'Disabled'
                            outstr = outstr + x['name'] + ': ' + status + ', '
                        return True, {'type': 'irc_privmsg', 'target': channel, 'message': outstr}

                    if not message.find('enable') == -1 or not message.find('disable') == -1:
                        args = message.split()
                        lst = irc_bot.plugin_manager.get_plugins()
                        for x in lst:
                            if args[2] == x['name']:
                                if args[1] == "enable":
                                    x['enabled'] = True
                                    return True, {'type': 'irc_privmsg', 'target': channel, 'message': x['name'] +
                                                  ' Enabled!'}
                                if args[1] == "disable":
                                    x['enabled'] = False
                                    return True, {'type': 'irc_privmsg', 'target': channel, 'message': x['name'] +
                                                  ' Disabled!'}

                    if not message.find('reload') == -1:
                        print('reloading plugins. Ordered by ' + sender['Nick'])
                        irc_bot.plugin_manager.load_plugins()
                        return True, {'type': 'irc_privmsg', 'target': channel, 'message': 'Plugins reloaded!'}

                return False, {}

            return False, {}