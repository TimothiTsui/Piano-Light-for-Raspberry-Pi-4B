from pyanoled.event.Events import KeyEvent
from pyanoled.visualizer.color_schemes.Scheme import Scheme

from typing import Tuple


class DividedScheme(Scheme):
    """
    divided into two colors
    """

    def get_color(self, key: KeyEvent) -> Tuple:
        if key.note < 60:
            return (255, 0, 0)
        else:
            return (0, 0, 255)
