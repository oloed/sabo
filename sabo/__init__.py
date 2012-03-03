from sabo.setting import init as init_setting
from sabo.ircclient import IRCClientFactory
from sabo.service import MessageService
from twisted.web import resource, server
from twisted.internet import reactor
from twisted.python import log

def start(yaml):
    init_setting(yaml)

    from sabo.setting import setting

    # setup clients
    siblings = dict()
    for name in setting["servers"].keys():
        siblings[name] = f = IRCClientFactory(name, siblings)
        log.msg("Connecting to %s:%s" % (f.host, f.port))
        reactor.connectTCP(f.host, f.port, f)

    # setup controlling server
    root = resource.Resource()
    root.putChild("message", MessageService(siblings))
    site = server.Site(root)

    reactor.listenTCP(setting["controller"]["port"], site)
    reactor.run()
