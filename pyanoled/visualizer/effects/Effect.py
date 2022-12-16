from pyanoled.Configuration import Configuration

from abc import ABC, abstractmethod
from logging import Logger
from rpi_ws281x.rpi_ws281x import Color, PixelStrip
from typing import Tuple

class Effect(ABC):
    """
    base abstract class defining the interface that all effect scheme subclasses needs to implement
    """

    def __init__(self, l: Logger, c: Configuration):
        self._l = l
        self._c = c
        self._changed = False
        self._pixelstrip = None

    def set_pixelstrip(self, pixel_strip: PixelStrip):
        self._pixelstrip = pixel_strip

    def changed(self) -> bool:
        """
        returns true if led effect states have been updated and needs to be shown on the led strip. false otherwise
        :return:
        """
        return self._changed

    @abstractmethod
    def pre(self) -> None:
        """
        method invoked at the start of an event loop iteration
        :return:
        """
        pass

    @abstractmethod
    def post(self) -> None:
        """
        method invoked at the end of an event loop iteration (prior to sending signal to led strip to show)
        :return:
        """
        pass

    @abstractmethod
    def pedal_on(self) -> None:
        """
        method invoked when pedal is pressed
        :return:
        """
        pass

    @abstractmethod
    def pedal_off(self) -> None:
        """
        method invoked when pedal is lifted
        :return:
        """
        pass

    @abstractmethod
    def key_on(self, led_index: int, color: Tuple) -> None:
        """
        method invoked when key is pressed
        :param led_index:
        :param color:
        :return:
        """
        pass

    @abstractmethod
    def key_off(self, led_index: int, color: Tuple) -> None:
        """
        method invoked when key is lifted
        :param led_index:
        :param color:
        :return:
        """
        pass
