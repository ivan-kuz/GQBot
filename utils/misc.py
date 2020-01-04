import sys



def progress_bar(percent, per_pct=5):
    hits = round(100/per_pct)
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
                         progress_bar(self.cnt/self.total*100)+
                         (("" if self.ol else "\n") if end is None else end))
