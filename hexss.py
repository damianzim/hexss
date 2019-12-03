#!/usr/bin/python3

from sys import argv
from typing import List

LINE_LEN = 16

def print_line(offset: int, _bytes: List[int]) -> None:
    assert 0 <= offset < 2 ** 32, "The input stream is too large."
    n_bytes = len(_bytes)

    # Adds a zero offset that doesn't exist.
    _bytes += [] if n_bytes == LINE_LEN else [0] * (LINE_LEN - n_bytes)

    print(
        '0x{:08X}'.format(offset),
        #'0x%08X' % offset,
        '|',
        ''.join('{:02X} '.format(byte)  for byte in _bytes) + '|',
        ''.join(chr(byte) + ' ' if chr(byte).isprintable() else '  ' for byte in _bytes) + '|'
        )

def read_stream(path: str) -> None:
    try:
        with open(path, 'rb') as f:
            print(
                'Offset'.ljust(10, ' '),
                ' ',
                ''.join(str(num).rjust(2, ' ') + ' ' for num in range(1, LINE_LEN + 1))
                )
            offset = 0
            while True:
                buf = f.read(LINE_LEN)
                if not buf:
                    break
                print_line(offset, list(buf))
                offset += LINE_LEN
    except OSError as err:
        print(err)


def hexss():
    if len(argv) == 1:
        print('There is no path to file. (second arg)')
        return -1
    path = argv[1]
    read_stream(path)

if __name__ == '__main__':
    exit(hexss())

