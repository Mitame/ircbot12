from irc.bot import SingleServerIRCBot

class Bot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def add_listener(self, message_type, function, priority=0):
        self.reactor.add_global_handler(message_type, function, priority)

    def on(self, message_type):
        def f(function):
            self.add_listener(message_type, function)
        return f
