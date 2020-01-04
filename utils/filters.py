class Filter:
    """Always True."""
    def check_msg(self, message, emoji, *_, **kwargs):
        return True
    
    def __call__(self, reaction):
        return True


class Default(Filter):
    def __call__(self, react):
        return react.me


