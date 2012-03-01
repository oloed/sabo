# -*- mode: python -*-

from yaml import load as yaml_load
from twisted.python import log
import re
import codecs

__all__ = ["setting", "reload", "init"]

setting = None
yaml = None

class ConfigError(Exception):
    pass


def _compile_regex(v):
    if isinstance(v[0], str) and v[0].startswith("match_"):
        return (v[0], re.compile(v[1]))
    else:
        return v


def reload():
    global setting
    log.msg("reloading configuration: %s" % yaml)
    setting = _init(yaml)
    return setting

def init(_yaml):
    return _init(_yaml)


def _init(_yaml):
    global yaml

    yaml = _yaml
    _setting = None

    with codecs.open(yaml, "r", encoding="utf-8") as f:
        _setting = yaml_load(f.read())

    # rearrange servers' data structure
    try:
        servers = dict()
        for item in yaml_load(_setting["servers"]):
            servers[item["name"]] = item
        _setting["servers"] = servers
    except Exception as e:
        raise ConfigError("malformed server configuration: %s" % str(e))

    # rearrange channels' data structure
    try:
        channels = dict()
        for item in yaml_load(_setting["channels"]):
            index = (item["server"], item["name"])
            channels[index] = item
        _setting["channels"] = channels
    except Exception as e:
        raise ConfigError("malformed channel configuration: %s" % str(e))

    # rearrange handlers' data structure
    try:
        h = dict(privmsg=list(), user_joined=list(), joined=list())
        for item in list(yaml_load(_setting["handlers"])):
            if item["type"] in h:
                data = dict(map(_compile_regex, item.items()))
                h[item["type"]].append(data)
            else:
                log.msg("invalid message type: %s" % item["type"])

        _setting["handlers"] = h
    except Exception as e:
        raise ConfigError("malformed handler configuration: %s" % str(e))

    # rearrange handlers' data structure
    try:
        encodings = list()
        for item in yaml_load(_setting["encodings"]):
            data = dict(map(_compile_regex, item.items()))
            encodings.append(data)
        _setting["encodings"] = encodings
    except Exception as e:
        raise ConfigError("malformed encoding configuration: %s" % str(e))

    global setting
    setting = _setting
    return _setting
