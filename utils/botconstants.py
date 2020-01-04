import json

try:
    config = json.load(open("config/config.json", "r"))
except FileNotFoundError:
    raise FileNotFoundError("Please create and fill in /config/config.json")

"""
config.json needs to be filled in:
{
  "TOKEN": "<token>",
  "PREFIX_RAW": "<prefix>",
  "PREFIX_ARRAY": ["<prefix>", "<prefix_alias_1>", "<prefix_alias_2>", ...]
  "POLL_CHAN": <channel_id of poll buffer>
}
"""

try:
    TOKEN = config["TOKEN"]
    PREFIX_RAW = config["PREFIX_RAW"]
    PREFIX_LEN = len(PREFIX_RAW)
    PREFIX = config["PREFIX_ARRAY"]
    POLL_CHAN = config["POLL_CHAN"]
except KeyError as e:
    raise KeyError("Your config.json file is filled in incorrectly." +
                   "Missing: {}".format(e))

try:
    POLL_BUFF = int(open("config/poll_msg.id", "r").readline())
except FileNotFoundError:
    POLL_BUFF = None
except ValueError:
    print("poll_msg.id is not an integer, resetting.")
    POLL_BUFF = None

VOTING_CHANNELS = set((614242269758881816, 609818815634735104,
                       605524587597529089, 607225987838509068))
PIN_REACTIONS_MIN = 3
MEE6_ID = 159985870458322944
EMOJI = json.load(open("config/emoji.json", "r"))
