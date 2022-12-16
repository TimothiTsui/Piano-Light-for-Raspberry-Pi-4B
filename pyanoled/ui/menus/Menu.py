from __future__ import annotations

from pyanoled.Configuration import Configuration
from pyanoled.ui.displays.Display import Display
from pyanoled.ui.menus.SelectionItem import SelectionItem
from pyanoled.State import State

from abc import ABC, abstractmethod
from logging import Logger
from PIL import Image, ImageDraw
from typing import Optional, Tuple, Type


class Menu(ABC, SelectionItem):
    def __init__(self, l: Logger, c: Configuration, d: Type[Display], state: State, parent:Optional[Type[Menu]]):
        SelectionItem.__init__(self, '', '')

        self._l = l
        self._c = c
        self._display = d
        self._state = state
        self._parent = parent

        self._selected = 0
        self._selections = ()

    def _multiline_split(self, s: str, n: int = 2) -> Tuple:
        """
        splits s into max of n lines based on display's character width
        :param s: string to split
        :param n: max number of lines
        :return:
        """
        lines = []
        t = ''
        for p in s.split(' '):
            if len(t + ' ' +p) < self._display.character_width:
                # can fit in current line
                t += ' ' + p
            else:
                # need new line
                if len(lines) < n - 1:
                    # max lines not reached
                    lines.append(t.strip())
                    t = p
                else:
                    # max line reached...truncate
                    t = (t + ' '  + p)[:(self._display.character_width - 5)] + '...'
                    break

        if t and len(lines) < n:
            lines.append(t.strip())

        return lines

    def _draw_header(self, draw: ImageDraw) -> None:
        y = 1
        draw.text((1, y), self.title, fill=(255, 255, 255))
        y += self._display.character_height
        draw.line([(0, y), (self._display.width, y)], fill=(255, 255, 255), width=1)
        y += 1

    def _draw_footer(self, draw: ImageDraw) -> None:
        y = self._display.height - self._display.character_height * 2 - 1
        draw.line([(0, y), (self._display.width, y)], fill=(255, 255, 255), width=1)
        y += 1
        for l in self._multiline_split(self._selections[self._selected].description, 2):
            draw.text((1, y), l, fill=(255, 255, 255))
            y += self._display.character_height

    def _draw_selections(self, draw: ImageDraw) -> None:
        y = 2 + self._display.character_height
        for i, v in enumerate(self._selections):
            # only show items that fit
            if y < (self._display.height - self._display.character_height * 3):
                # has room still
                if self._selected == i:
                    draw.rectangle([(0, y), (self._display.width, y + self._display.character_height)], fill=(255, 0, 0))
                draw.text((1, y), v.title, fill=(255, 255, 255))
                y += self._display.character_height

    def _get_selected(self) -> SelectionItem:
        return self._selections[self._selected] or None

    def action_up(self) -> None:
        """
        moves current selected selection up one
        :return:
        """
        if self._selections:
            if self._selected > 0:
                # can move down still
                self._selected -= 1
            else:
                # wrap around
                self._selected = len(self._selections) - 1

    def action_down(self) -> None:
        """
        moves current selected selection down one
        :return:
        """
        if self._selections:
            if self._selected < len(self._selections) - 1:
                # can move down still
                self._selected += 1
            else:
                # wrap around
                self._selected = 0

    def action_left(self) -> None:
        return None

    def action_right(self) -> None:
        return None

    def action_in(self) -> None:
        return None

    def action_confirm(self) -> Optional[Type[Menu]]:
        return None

    def action_cancel(self) -> None:
        return None

    def action_back(self) -> Optional[Type[Menu]]:
        return self._parent

    def show(self) -> None:
        """
        draw menu based on current path and selection
        :return:
        """
        image = Image.new('RGB', (self._display.height, self._display.width), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        self._draw_header(draw)
        self._draw_selections(draw)
        self._draw_footer(draw)
        self._display.show(image)
