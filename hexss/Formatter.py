#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = ['Formatter']

from argparse import Namespace
from typing import List, Callable

from hexss.Color import *

class Formatter(object):

	MIDDLE_DOT = 0xB7

	def __init__(self, args: Namespace):
		self.__offset = 0
		self.__data = List[int]

		self.line_len = args.line_len
		self.lines = args.lines

		self.coloring = args.coloring

		self._fill_empty = args.fill_empty
		self._unicode = args.unicode
		self._is_offset = args.is_offset
		self.header = not args.hide_header

		self.head = args.head
		self.tail = args.tail

		self.__buffer = []

		self.__accent_offset_every = 1024       # Bytes (pow of 2)

	def __str__(self) -> str:
		return self.get_formatted_line()

	def load(self, offset: int, data: List[int]):
		self.__buffer = []
		self.__offset = offset
		self.__data = data

	def get_header_line(self) -> str:
		offset_label = True
		_line = ''
		if self._is_offset:
			if offset_label:
				_line += 'Offset'
			_line = _line.ljust(10, ' ') + ' '*5

		numbers = ''.join(
			str(num).rjust(2, ' ') + ' '
			if 0 <= self.line_len < 100
			else '{:02X} '.format(num)
			if num < 256
			else '00 '
			for num
			in range(1, self.line_len + 1)
		)

		_line += numbers if not self.coloring else color(
			Colors.BRIGHT_WHITE,
			Foreground,
			numbers
		)

		return _line

	def __format_offset(self, offset: int) -> str:
		if not self._is_offset:
			return ''
		formatted = '0x{:08X}'.format(offset)
		if not self.coloring or offset % self.__accent_offset_every:
			return formatted
		return color(Colors.BRIGHT_BLUE, Foreground, formatted)

	def __get_separator(
		self,
		left_padding: int = 0,
		right_padding: int = 0) -> str:

		_separator = ' '
		if self.coloring:
			_separator = color(
				Colors.GREY
				if self.__offset % self.__accent_offset_every
				else Colors.BRIGHT_BLUE,
				Background,
				_separator,
			)

		_separator = ' '*left_padding + _separator + ' '*right_padding
		return _separator

	def __conditional_coloring(
			self,
			data: str,
			_color: ColorType,
			space: Callable = Foreground) -> str:

		if not self.coloring:
			return data

		return color(_color, space, data)

	def get_formatted_line(self) -> str:
		n_data = len(self.__data)

		# Complement the line with zeros or spaces.
		self.__data += [] if n_data == self.line_len \
			else [0 if self._fill_empty else '  '] * (self.line_len - n_data)

		# Check if the line is already formatted.
		if self.__buffer:
			return ''.join(self.__buffer)

		# TODO: Is there a faster way to do this?
		self.__buffer = [
			self.__format_offset(self.__offset),
			self.__get_separator(2, 2) if self._is_offset else '',
			''.join(
				byte + ' '
				if type(byte) == str
				else '{:02X} '.format(byte)
				if chr(byte).isprintable()
				else self.__conditional_coloring(
					'{:02X} '.format(byte),
					Colors.GREY if not byte else Colors.BRIGHT_RED,
				)
				for byte in self.__data
			),
		]

		if self._unicode:
			self.__buffer.append(self.__get_separator(1, 2))
			self.__buffer.append(
				''.join(
					byte
					if type(byte) == str
					else chr(byte) + ' '
					if chr(byte).isprintable()
					else self.__conditional_coloring(
						chr(self.MIDDLE_DOT) + ' ',
						Colors.GREY if not byte else Colors.BRIGHT_RED,
					)
					for byte in self.__data
				)
			)

		self.__buffer.append(self.__get_separator(1, 3))
		return ''.join(self.__buffer)

