import importlib.util
import os

from traceback import print_exc

class NotAllowed(BaseException):
    pass

class CommandHandler:
    OWNER = 10
    OP = 9
    ADMIN = 8
    MOD = 7
    NONE = 0
    def __init__(self, bot, folder="./commands", command_flag="!", case_sensitive=False, permissions={}):
        self.bot = bot

        self.folder = folder
        self.command_flag = command_flag
        self.case_sensitive = case_sensitive
        self.permissions = permissions

        self.commands = {}
        self.tested_users = {}

        self.load_all_from_dir(self.folder, recurse=0)



        bot.add_listener("pubmsg", self.on_message)
        bot.add_listener("privmsg", self.on_message)

    def set_permission(self, nick, level):
        self.permissions[nick] = level

    def is_authed(self, c, nick):

        #TODO: make this check nickserv or something
        return True

    def require_perm(self, c, e, level):
        if self.is_authed(c, e.source.nick):
            try:
                if self.permissions[e.source.nick.lower()] >= level:
                    return
            except KeyError:
                pass
        raise NotAllowed()

    def load_command(self, path):
        base_name = ".".join(os.path.split(path)[-1].split(".")[0:-1])

        # load in the module
        try:
            spec = importlib.util.spec_from_file_location(base_name, path)
            command_mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(command_mod)
        except:
            print("Could not load '%s'" % path)
            print("-" * 60)
            print_exc()
            print("-" * 60)


        for key in dir(command_mod):
            value = getattr(command_mod, key)
            if callable(value) and not key.startswith("_"):
                if not self.case_sensitive:
                    key = key.lower()
                self.commands[key] = value

    def load_all_from_dir(self, path, recurse=0):
        for root, dirs, files in os.walk(path):
            for f in files:
                if f.endswith(".py"):
                    self.load_command(os.path.join(root, f))
            if recurse:
                for d in dirs:
                    load_all_from_dir(os.path.join(root, d), recurse - 1)


    def on_message(self, c, e):
        if e.type == "privmsg":
            def reply(message):
                c.privmsg(e.source.nick, message)
        elif e.type == "pubmsg":
            def reply(message):
                c.privmsg(e.target, message)
        else:
            def reply(message):
                print("Can't reply. Don't know message type '%s'." % e.type)

        message = e.arguments[0]
        if message.startswith(self.command_flag):
            self.on_command(c, e, reply)

    def on_command(self, c, e, reply):
        message = e.arguments[0].lstrip(self.command_flag).split(" ")
        cmd = message[0]
        args = message[1:]

        if not self.case_sensitive:
            cmd = cmd.lower()

        if cmd in self.commands:
            try:
                self.commands[cmd](args, reply, c, e, self)
            except NotAllowed:
                reply("You do not have permission to run this command.")
            except:
                print("Exception raised in '%s'" % c)
                print("-" * 60)
                print_exc()
                print("-" * 60)
                reply("An error occurred while running '%s'. Please contact your system Administrator." % cmd)
        else:
            reply("Command '%s' was not recognised." % cmd)
