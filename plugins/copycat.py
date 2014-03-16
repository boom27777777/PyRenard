class plugin():

    def callback(self):
        return {'type': 'PRIVMSG', 'help': self.hlp}

    def hlp(self, typ, channel, sender, message, ircBot):
        return {'type': 'irc_privmsg', 'target': channel, 'message':
                        '!help copycat, I\'m just being a smartass'}

    def run(self, typ, channel, sender, message, ircBot):
        if (sender['Nick'] != ircBot.nick and channel != ircBot.nick and
                sender['Nick'] != ircBot.server_name):
            return True, {'type': "irc_privmsg", 'target': channel, 'message': message}
        if (sender['Nick'] != ircBot.nick and channel == ircBot.nick and
                sender['Nick'] != ircBot.server_name):
            return True, {'type': "irc_privmsg", 'target': sender['Nick'], 'message': message}
        return False, {}