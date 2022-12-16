from pyanoled.Configuration import Configuration
from pyanoled.visualizer.effects.Effect import Effect

from logging import Logger
from rpi_ws281x.rpi_ws281x import Color
from typing import Tuple

import math


class FadeEffect(Effect):
    """
    light effect that does not turn led off immediately on key lift but fades it to 0
    """
    def __init__(self, l: Logger, c: Configuration):
        Effect.__init__(self, l, c)

        # tracks leds that are fading
        self._leds = {}

    def pre(self) -> None:
        self._changed = False

    def post(self) -> None:
        if self._leds:
            percentage = (95 - (math.floor(len(self._leds) / 6)) * 3) / 100
            fading_leds = {}
            for led_index, color in self._leds.items():
                # fade it
                color = tuple(map(lambda c: int(math.floor(c * percentage)), color))
                self._pixelstrip.setPixelColor(int(led_index), Color(*color))

                if color != (0, 0, 0):
                    # can still fade so add it back to dictionary
                    fading_leds[led_index] = color
            self._leds = fading_leds
            self._changed = True

    def pedal_on(self) -> None:
        pass

    def pedal_off(self) -> None:
        pass

    def key_on(self, led_index: int, color: Tuple) -> None:
        self._l.debug('lighting up led {l}'.format(l=led_index))

        # add it to led registry to start fading
        self._leds[str(led_index)] = color

    def key_off(self, led_index: int, color: Tuple) -> None:
        pass
