from pyanoled.event.Events import KeyEvent
from pyanoled.visualizer.color_schemes.Scheme import Scheme

from typing import Tuple


class MonoScheme(Scheme):
    """
    one color for all keys
    """

    def get_color(self, key: KeyEvent) -> Tuple:
        return (255, 255, 255)