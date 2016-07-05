def join(args, reply, c, e, cmd):
    for channel in args:
        c.join(channel)

def die(args, reply, c, e, cmd):
    c.quit(" ".join(args))

def setflag(args, reply, c, e, cmd):
    cmd.require_perm(c, e, cmd.OWNER)
    cmd.command_flag = args[0]
    reply("Command flag set to '%s'. You should now run commands with `%scommand <args>'" % (cmd.command_flag, cmd.command_flag))

def addowner(args, reply, c, e, cmd):
    for x in cmd:
        cmd.set_permission(x, cmd.OWNER)

def error(args, reply, c, e, cmd):
    assert 1 == 2

def who(args, reply, c, e, cmd):
    reply(c.who(args[0]))
