from dabot.setting import init as init_setting
from dabot.ircclient import IRCClientFactory
from dabot.service import MessageService
from twisted.web import resource, server
from twisted.internet import reactor


def start(yaml):
    init_setting(yaml)

    from dabot.setting import setting

    # setup clients
    siblings = dict()
    for name in setting["servers"].keys():
        siblings[name] = f = IRCClientFactory(name, siblings)
        reactor.connectTCP(f.host, f.port, f)

    # setup controlling server
    root = resource.Resource()
    root.putChild("message", MessageService(siblings))
    site = server.Site(root)

    reactor.listenTCP(setting["backend"]["port"], site)
    reactor.run()
