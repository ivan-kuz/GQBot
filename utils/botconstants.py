import json

config = json.load(open("config/config.json", "r"))

"""
config.json needs to be filled in:
{
  "TOKEN": "<token>",
  "PREFIX_RAW": "<prefix>",
  "PREFIX_ARRAY": [<prefix>, <prefix_alias_1>, <prefix_alias_2>, ...]
}
"""

TOKEN = config["TOKEN"]
PREFIX_RAW = config["PREFIX_RAW"]
PREFIX_LEN = len(PREFIX_RAW)
PREFIX = config["PREFIX_ARRAY"]
MEE6_ID = 159985870458322944
EMOJI = json.load(open("config/emoji.json", "r"))