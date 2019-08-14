TOKEN = "<token>"
PREFIX_RAW = "<PREFIX>"
PREFIXLEN = len(PREFIX_RAW)
PREFIX = <string, iterable or function>

def formatdoc(func):
    func.__doc__ = func.__doc__.format(PREFIX_RAW)
    return func
