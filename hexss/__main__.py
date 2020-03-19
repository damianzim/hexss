#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from argparse import (
    ArgumentParser,
    Namespace,
)

from hexss.Formatter import Formatter

STREAM_LIMIT = 2 ** 32

# Default size of output bytes.
# Mainly for the --head and --tail
DEFAULT_RESOLUTION = 1024


def parse_args() -> Namespace:
    parser = ArgumentParser(description='Hex Stream Scan')

    parser.add_argument(
        'file',
        type=str,
        help='Path to the file to be scanned.',
    )

    parser.add_argument(
        '-n', '--lines',
        action='store',
        default=-1,
        type=int,
        help='The number of lines.',
    )

    parser.add_argument(
        '-l', '--len',
        action='store',
        default=16,
        type=int,
        choices=[4, 8, 16, 32, 64, 128],
        help='Number of bytes to print per line.',
        dest='line_len',
    )

    unicode_representation = parser.add_mutually_exclusive_group()

    unicode_representation.add_argument(
        '-c', '--compact',
        action='store_true',
        help='Print compact unicode representation.',
        dest='compact_unicode',
    )

    unicode_representation.add_argument(
        '-d',
        action='store_false',
        help='Disable bytes representation in Unicode.',
        dest='unicode',
    )

    parser.add_argument(
        '-D',
        action='store_true',
        help='Hide header.',
        dest='hide_header',
    )

    parser.add_argument(
        '-O',
        action='store_false',
        help='Do not print the offset.',
        dest='is_offset',
    )

    section = parser.add_mutually_exclusive_group()
    section.add_argument('-T', '--tail', action='store_true')
    section.add_argument('-H', '--head', action='store_true')

    parser.add_argument(
        '-f', '--fill-empty',
        action='store_true',
        help='Fill the empty offset with zeros.',
    )

    parser.add_argument(
        '-p',
        action='store_false',
        help='Do not color the output.',
        dest='coloring',
    )

    return parser.parse_args()


def read_stream(path: str, formatter: Formatter) -> None:
    try:
        file_size = os.path.getsize(path)
    except OSError as err:
        print(err)
        raise

    try:
        with open(path, 'rb') as f:
            offset = 0

            # Only with -n, --head or --tail
            output_resolution = DEFAULT_RESOLUTION
            use_resolution = formatter.tail | formatter.head

            if formatter.lines != -1:
                assert formatter.lines > 0, 'Nothing to print, because lines,\
 aka -n = {}'.format(formatter.lines)

                output_resolution = formatter.line_len * formatter.lines
                use_resolution = True

            if formatter.tail and file_size > output_resolution:
                tail_complementing = (
                    formatter.line_len - file_size % formatter.line_len
                ) % formatter.line_len

                offset = file_size + tail_complementing - output_resolution
                f.seek(offset)

            if formatter.header:
                print(formatter.get_header_line())

            while True:
                # TODO: Is it good to read the stream every few bytes?
                buf = f.read(
                    formatter.line_len
                    if file_size - offset > formatter.line_len
                    else max(0, file_size - offset)
                )

                if not buf:
                    break

                formatter.load(offset, list(buf))
                print(formatter)

                offset += formatter.line_len
                if use_resolution and offset >= (
                    file_size if formatter.tail else output_resolution
                ):
                    break

                assert 0 <= offset < STREAM_LIMIT, \
                    'The input stream is too large.'

    except OSError as err:
        print(err)


def hexss(args: Namespace) -> int:
    read_stream(args.file, Formatter(args))
    return 0


if __name__ == '__main__':
    exit(hexss(parse_args()))

