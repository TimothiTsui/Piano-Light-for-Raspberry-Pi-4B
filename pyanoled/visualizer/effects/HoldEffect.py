from pyanoled.Configuration import Configuration
from pyanoled.visualizer.effects.Effect import Effect

from logging import Logger
from rpi_ws281x.rpi_ws281x import Color
from typing import Tuple


class HoldEffect(Effect):
    """
    light effect that leave led lit when pedal is pressed
    """
    def __init__(self, l: Logger,  c: Configuration):
        Effect.__init__(self, l, c)

        # tracks state of pedal press
        self._pedal = False

        # tracks leds that are held on
        self._leds = {}

    def pre(self) -> None:
        self._changed = False

    def post(self) -> None:
        pass

    def pedal_on(self) -> None:
        self._pedal = True
        self._changed = True

    def pedal_off(self) -> None:
        self._pedal = False

        # pedal is lifted, so convert any led that was in held state to off state
        for led_index in self._leds.keys():
            self._pixelstrip.setPixelColor(int(led_index), Color(0, 0, 0))
        self._leds = {}
        self._changed = True

    def key_on(self, led_index: int, color: Tuple) -> None:
        self._l.debug('lighting up led {l}'.format(l=led_index))
        self._pixelstrip.setPixelColor(led_index, Color(*color))
        self._changed = True

    def key_off(self, led_index: int, color: Tuple) -> None:
        if self._pedal:
            # pedal is pressed so keep led on as held state
            self._l.debug('holding led {l}'.format(l=led_index))
            self._leds[str(led_index)] = self._pixelstrip.getPixelColor(led_index)
        else:
            self._l.debug('shutting down led {l}'.format(l=led_index))
            self._pixelstrip.setPixelColor(led_index, Color(0, 0, 0))
        self._changed = True
