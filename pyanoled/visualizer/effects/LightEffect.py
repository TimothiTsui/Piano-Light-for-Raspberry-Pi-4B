from pyanoled.visualizer.effects.Effect import Effect

from rpi_ws281x.rpi_ws281x import Color
from typing import Tuple

class LightEffect(Effect):
    """
    default light effect that lights up led when key is pressed and shuts led off when key is lifted
    """

    def pre(self) -> None:
        self._changed = False

    def post(self) -> None:
        pass

    def pedal_on(self) -> None:
        pass

    def pedal_off(self) -> None:
        pass

    def key_on(self, led_index: int, color: Tuple) -> None:
        self._l.debug('lighting up led {l}'.format(l=led_index))
        self._pixelstrip.setPixelColor(led_index, Color(*color))
        self._changed = True

    def key_off(self, led_index: int, color: Tuple) -> None:
        self._l.debug('shutting down led {l}'.format(l=led_index))
        self._pixelstrip.setPixelColor(led_index, Color(*color))
        self._changed = True