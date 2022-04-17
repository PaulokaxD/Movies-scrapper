"""
Provides some repetitive functionalities
"""


def format_list(text: str, separator: str) -> list:
    """Takes a comma separated string of items and returns
    a list with those"""
    return list(map(lambda x: x.strip().replace("'", ""), text.split(separator)))
