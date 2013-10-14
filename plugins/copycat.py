class plugin():

    def callback(self):
        return {'type': 'PRIVMSG'}

    def hlp(self):
        pass

    def run(self, typ, channel, sender, message, ircBot):
        if (sender['Nick'] != ircBot.NICK and channel != ircBot.NICK and
                sender['Nick'] != ircBot.SERVERNAME):
            return True, {'type': "privmsg", 'target': channel, 'message': message}
        if (sender['Nick'] != ircBot.NICK and channel == ircBot.NICK and
                sender['Nick'] != ircBot.SERVERNAME):
            return True, {'type': "privmsg", 'target': sender['Nick'], 'message': message}
        return False, {}