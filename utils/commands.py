from utils.botconstants import PREFIX_RAW


def format_doc(func):
    func.__doc__ = func.__doc__.format(PREFIX_RAW)
    return func
