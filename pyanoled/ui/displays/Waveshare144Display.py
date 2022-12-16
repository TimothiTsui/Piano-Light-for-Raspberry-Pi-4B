from pyanoled.ui.displays.Display import Display
from pyanoled.ui.displays import LCD_1in3, LCD_Config

from logging import Logger
from typing import Dict


class LCD_1in3Display(Display):
    def __init__(self, l: Logger):
        Display.__init__(self, l)
        self._lcd = LCD_1in3.LCD(self)
        self._lcd.LCD_Clear()

    @property
    def width(self) -> int:
        return 16

    @property
    def height(self) -> int:
        return 2

    @property
    def character_width(self) -> int:
        return 22

    @property
    def character_height(self) -> int:
        return 12

    def show(self, i: str) -> None:
        self._lcd.lcd_string(i, 0, 0)

    def clear(self) -> None:
        self._lcd.LCD_Clear()
