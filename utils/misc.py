import sys
from discord import Message, Emoji, PartialEmoji
from typing import Union, Any


async def react_for(msg: Message, *reactions: Union[Emoji, PartialEmoji, str]) -> None:
    for reaction in reactions:
        await msg.add_reaction(reaction)


def progress_bar(percent, per_pct=5):
    built = "*|"
    built += "#"*round(percent/per_pct)
    built += " "*round((100-percent)/per_pct)
    built += "|*"
    return built


class BarHelper:
    def __init__(self, total, *, pct=5, one_line=False):
        self.total = total
        self.cnt = 0
        self.pct = pct
        self.ol = one_line
    
    def progress(self, *args, no=1, **kwargs):
        self.cnt += no
        self.print(*args, **kwargs)
    
    def print(self, *, start=None, end=None):
        sys.stdout.write((("\r" if self.ol else "") if start is None else start) +
                         progress_bar(self.cnt/self.total*100) +
                         (("" if self.ol else "\n") if end is None else end))


class Interpolate:
    def __init__(self, *points: (Any, float)):
        point_z, _ = zip(*points)
        sum(point_z)
        self.points = points

    def get_val(self, part: float):
        prev_point, prev_val = self.points[0]
        for point, val in self.points[0:]:
            if prev_val < part <= val:
                percentage = (part - prev_val)/(val - prev_val)
                return percentage*prev_point + (1-percentage)*point
            prev_point = point
        return prev_point
