from pyanoled.event.Events import KeyEvent
from pyanoled.visualizer.color_schemes.Scheme import Scheme

from random import randint
from typing import Tuple


class ChaosScheme(Scheme):
    """
    random colors every time
    """

    def get_color(self, key: KeyEvent) -> Tuple:
        return (randint(0, 255), randint(0, 255), randint(0, 255))