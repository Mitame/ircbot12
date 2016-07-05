
def echo(args, reply, c, e, cmd):
    cmd.require_perm(c, e, cmd.OWNER)
    reply(" ".join(args))
