import re
from itertools import cycle
from typing import Iterator

from bs4 import BeautifulSoup
from bs4.element import (NavigableString, PreformattedString,
                         Stylesheet, Script, TemplateString)

from settings import EMOJI


class Parser:
    """A helper class which is written in the sake of isolating business logic"""

    pattern = r'(\b[a-zA-Zа-яА-Я]{6})([.,\/#!$%\^&\*;:{}=\-_`~()«»<>\s]|$)'
    compiled = re.compile(pattern)

    @classmethod
    def _add_emoji(cls, content: str, emoji_cycle: Iterator) -> str:

        def callback(match):
            return f'{match.group(1)}{next(emoji_cycle)}{match.group(2)}'

        return cls.compiled.sub(callback, content)

    @classmethod
    def process(cls, string: bytes) -> bytes:
        emoji_cycle = cycle(EMOJI)
        exclude = (PreformattedString, Stylesheet, Script, TemplateString)

        soup = BeautifulSoup(string, 'html.parser')
        for child in soup.descendants:
            if hasattr(child, 'contents'):
                for content in child.contents:
                    if isinstance(content, NavigableString) and not isinstance(content, exclude):
                        content.replace_with(cls._add_emoji(content.string, emoji_cycle))
        return soup.prettify().encode()
