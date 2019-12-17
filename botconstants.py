import json

config = json.load(open("config.json", "r"))

TOKEN = config["TOKEN"]
PREFIX_RAW = config["PREFIX_RAW"]
PREFIX_LEN = len(PREFIX_RAW)
PREFIX = config["PREFIX_ARRAY"]


def format_doc(func):
    func.__doc__ = func.__doc__.format(PREFIX_RAW)
    return func
