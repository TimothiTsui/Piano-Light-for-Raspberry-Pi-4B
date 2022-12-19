from pyanoled.ui.displays.Display import Display
from pyanoled.ui.displays import LCD_1in44, LCD_Config

from logging import Logger
from typing import Dict

from PIL import Image


class Adafruit2088Display(Display):

    def __init__(self, l: Logger):
        Display.__init__(self, l)
        self._lcd = LCD_1in44.LCD()
        self._lcd_scandir = LCD_1in44.SCAN_DIR_DFT
        self._lcd.LCD_Init(self._lcd_scandir)
        self._lcd.LCD_Clear()

    @property
    def width(self) -> int:
        return 128

    @property
    def height(self) -> int:
        return 128

    @property
    def character_width(self) -> int:
        return 22

    @property
    def character_height(self) -> int:
        return 12

    def show(self, i: Image) -> None:
        self._lcd.LCD_ShowImage(i, 0, 0)

    def clear(self) -> None:
        self._lcd.LCD_Clear()
