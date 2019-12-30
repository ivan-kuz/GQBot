from utils import BarHelper

COG_COUNT = 8
_bh = BarHelper(COG_COUNT, one_line=True)

print("Importing cogs...")
_bh.print()
from .basic import BasicCog
_bh.progress()
from .role import RoleCog
_bh.progress()
from .games import GamesCog
_bh.progress()
from .help import HelpCog
_bh.progress()
from .error_handler import ErrorHandlerCog
_bh.progress()
from .voting import VotingCog
_bh.progress()
from .conversation import ConvoCog
_bh.progress()
from .chance import ChanceCog
_bh.progress(end="\n")

COGS = [BasicCog, ChanceCog, RoleCog,
        GamesCog, HelpCog, ErrorHandlerCog,
        VotingCog, ConvoCog]
