from pyanoled.event.Events import KeyEvent
from pyanoled.visualizer.color_schemes.Scheme import Scheme

from typing import Tuple


class KeyScheme(Scheme):
    """
    two colors mapped to black and white keys
    """

    def get_color(self, key: KeyEvent) -> Tuple:
        if key.normalized_note < 3:
            # first 3 keys sequenced as:
            # white-black-white
            if key.normalized_note == 1:
                return self._getBlackKeyColor()
            else:
                return self._getWhiteKeyColor()
        elif 3 <= key.normalized_note < 87:
            # keys after 3rd and before 88th are sequenced as 12-keys repeated as:
            # white-black-white-black-white white-black-white-black-white-black-white
            r = (key.normalized_note - 3) % 12
            if (r <= 4 and r % 2 == 1) or (r > 4 and r % 2 == 0):
                return self._getBlackKeyColor()
            else:
                return self._getWhiteKeyColor()
        else:
            # last key is white
            return self._getWhiteKeyColor()

    def _getWhiteKeyColor(self):
        return (0, 0, 128)

    def _getBlackKeyColor(self):
        return (255, 215, 0)
