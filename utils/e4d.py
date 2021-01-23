import logging
from collections import namedtuple
from functools import reduce
from typing import List, Optional

Abbr = namedtuple("Abbr", "first_letter length last_letter")

try:
    with open("/usr/share/dict/words") as words_file:
        SYSTEM_WORDS_LIST = [line.strip() for line in words_file]
except FileNotFoundError:
    logging.getLogger("e4d").warning(
        "Could not find system dictionary, e4d disabled")
    SYSTEM_WORDS_LIST = None


def parse_abbr(abbr_str: str) -> Optional[Abbr]:
    try:
        first_letter, last_letter = abbr_str[0].lower(), abbr_str[-1].lower()
        assert first_letter.isalpha() and last_letter.isalpha()
        return Abbr(first_letter=first_letter,
                    last_letter=last_letter,
                    length=int(abbr_str[1:-1]))
    except (ValueError, IndexError, AssertionError):
        return


def match_abbr(abbr: Abbr) -> List[str]:
    return [w for w in SYSTEM_WORDS_LIST
            if w[0].lower() == abbr.first_letter
            and w[-1].lower() == abbr.last_letter
            and len(w) == abbr.length + 2]


def to_output_line(input_word: str, matches: Optional[List[str]]) -> str:
    if matches is None:
        result_str = "<Invalid input>"
    elif not matches:
        result_str = "<No matches>"
    else:
        result_str = "_{}_".format(", ".join(matches))
    return f"**{input_word}**: {result_str}"


def to_output_messages(output_lines: List[str]) -> List[str]:
    def combine(a: List[str], x: str):
        if not a or len(a[-1]) + len(x) > 2000 - 1:
            a.append(x)
        else:
            a[-1] = a[-1] + f"\n{x}"
        return a
    messages = reduce(combine, output_lines, [])
    if len(messages) == 1:
        return messages
    return [messages]
