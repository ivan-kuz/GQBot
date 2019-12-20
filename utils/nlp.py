from typing import List


def sentence_case(sentence):
    try:
        return sentence[0].upper() + sentence[1:]
    except IndexError:
        return sentence.upper()


def list_values(values: List[str]):
    if len(values) <= 2:
        return "".join(values)
    else:
        return ", ".join(values[:-1]) + " and " + values[-1]
