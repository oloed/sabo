__all__ = ["fix_message_encoding"]


def fix_message_encoding(message):
    fixed = dict(map(lambda v: (v[0].encode("UTF-8"), v[1]), message.items()))

    if "channels" in fixed:
        fixed["channels"] = map(lambda x: x.encode("UTF-8"), fixed["channels"])
    if "users" in fixed:
        fixed["users"] = map(lambda x: x.encode("UTF-8"), fixed["users"])

    return fixed

# vim: ts=4 sw=4 ai et   
