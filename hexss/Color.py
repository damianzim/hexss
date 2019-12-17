#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Callable, TypeVar

ColorType = TypeVar('ColorType', str, int)


def Background(_color: ColorType) -> str:
    __b = u'\u001b[48;5;'
    return __b + str(_color) + u'm'


def Foreground(_color: ColorType) -> str:
    __b = u'\u001b[38;5;'
    return __b + str(_color) + u'm'


@dataclass(frozen=True)
class Colors(object):

    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    MAGENTA = 5
    CYAN = 6
    WHITE = 7
    GREY = 8
    BRIGHT_RED = 9
    BRIGHT_GREEN = 10
    BRIGHT_YELLOW = 11
    BRIGHT_BLUE = 12
    BRIGHT_MAGENTA = 13
    BRIGHT_CYAN = 14
    BRIGHT_WHITE = 15

    RESET = u'\u001b[0m'
    ANY = ''


def reset() -> str:
    return Colors.RESET


def color(_color: ColorType, space: Callable, text: str = None) -> str:
    if text is not None and len(text) == 0:
        return ''
    response = space(_color)
    if text:
        response += text + reset()
    return response


"""
# Examples

print(Background(Colors.BLUE) + 'simple text' + reset())

print(color(Colors.BRIGHT_BLUE, Foreground, 'simple text'))

# Text and background at the same time.

print(color(Colors.RED, Background) + color(Colors.YELLOW, Foreground) +\
        'simple text' + reset())

print(color(Colors.BRIGHT_BLUE, Foreground,
        color(Colors.BRIGHT_WHITE, Background, 'simple text')))
"""
