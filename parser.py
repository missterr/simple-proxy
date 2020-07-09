import re
from functools import partial
from itertools import cycle

from bs4 import BeautifulSoup
from bs4.element import NavigableString, PreformattedString, Stylesheet, Script, TemplateString

from settings import EMOJI


class Parser:
    """ A helper class which is written in the sake of isolating business logic """

    @staticmethod
    def _add_emoji(content: str) -> str:
        pattern = r'(\b[a-zA-Zа-яА-Я]{6})([.,\/#!$%\^&\*;:{}=\-_`~()«»<>\s]|$)'
        compiled = re.compile(pattern)

        def callback(match, emoji):
            return f'{match.group(1)}{next(emoji)}{match.group(2)}'

        callback = partial(callback, emoji=cycle(EMOJI))
        return compiled.sub(callback, content)

    @classmethod
    def process(cls, string: bytes) -> bytes:
        exclude = (PreformattedString, Stylesheet, Script, TemplateString)

        soup = BeautifulSoup(string, 'html.parser')
        for child in soup.descendants:
            if hasattr(child, 'contents'):
                for content in child.contents:
                    if isinstance(content, NavigableString) and not isinstance(content, exclude):
                        content.replace_with(cls._add_emoji(content.string))
        return soup.prettify().encode()
