from abc import ABC, abstractmethod
from logging import Logger
from PIL import Image
from typing import Dict

class Display(ABC):
    """
    base abstract class defining the interface that all displays class implement
    """

    def __init__(self, l: Logger):
        self._l = l

    @property
    @abstractmethod
    def width(self) -> int:
        pass

    @property
    @abstractmethod
    def height(self) -> int:
        pass

    @property
    @abstractmethod
    def character_width(self) -> int:
        pass

    @property
    @abstractmethod
    def character_height(self) -> int:
        pass

    @abstractmethod
    def show(self, i: str) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
