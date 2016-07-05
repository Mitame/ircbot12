import irk
from irk import commands
from pprint import pprint
b = irk.Bot("##MitameTest", "MitameBot", "irc.freenode.net")


@b.on("all_events")
def on_any(c, e):
    if e.type != "all_raw_messages":
        print(e.type, e.arguments)

@b.on("welcome")
def on_welcome(c, e):
    print("We were welcomed!")
    c.join("##MitameTest")

@b.on("privmsg")
def on_privmsg(c, e):
    print("Got a message from '%s':" % e.source.nick)
    print(e.arguments[0])

c = commands.CommandHandler(b, "./commands", permissions={"mitame": 10})

b.start()
