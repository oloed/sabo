# -*- mode: python -*-

from yaml import load as yaml_load
from twisted.python import log
import re
import codecs

__all__ = ["setting", "reload_setting"]

setting, yaml = None, None


class ConfigError(Exception):
    pass


def _compile_regex(v):
    if isinstance(v[0], str) and v[0].startswith("match_"):
        return (v[0], re.compile(v[1]))
    else:
        return v


def compile_regex(v):
    return dict(map(_compile_regex, v.items()))


def reload_setting():
    global setting
    log.msg("reloading configuration: %s" % yaml)
    setting = _init(yaml)
    return setting


def init(_yaml):
    global setting, yaml
    yaml = _yaml
    setting = _init(_yaml)
    return setting


def _init(_yaml):
    _setting = dict()

    with codecs.open(yaml, "r", encoding="utf-8") as f:
        _setting = yaml_load(f.read())

    _setting["servers"] = dict(map(lambda x: (x["name"], x),
                                   _setting["servers"]))

    _setting["channels"] = dict(
        map(lambda x: ((x["server"], x["name"]), x), _setting["channels"]))

    if "encodings" in _setting:
        _setting["encodings"] = map(compile_regex, _setting["encodings"])
    else:
        _setting["encodings"] = list()

    # rearrange handlers' data structure
    try:
        h = dict(privmsg=list(), user_joined=list(), joined=list())
        for item in _setting["handlers"]:
            if item["type"] in h:
                data = dict(map(_compile_regex, item.items()))
                h[item["type"]].append(data)
            else:
                log.msg("invalid message type: %s" % item["type"])

        _setting["handlers"] = h
    except Exception as e:
        raise ConfigError("malformed handler configuration: %s" % str(e))

    return _setting
