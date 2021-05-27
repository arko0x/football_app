import re


def extract_integer_from_string_or_return_zero(_str):
    integers = re.findall(r"\d+", _str)
    if len(integers) == 0:
        return 0
    else:
        return int(integers[0])
