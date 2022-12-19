from pyanoled.Configuration import Configuration
from pyanoled.ui.displays.Display import Display
from pyanoled.ui.menus.Menu import Menu
from pyanoled.ui.menus.SelectionItem import SelectionItem
from pyanoled.State import State

from logging import Logger
from typing import Optional, Type


class LearnMenu(Menu):
    def __init__(self, l: Logger, c: Configuration, d: Type[Display], state: State, parent:Optional[Type[Menu]]):
        super().__init__(l, c, d, state, parent)

        self._title = 'Midi Learn'
        self._description = 'LED effect to show on key/pedal press'
        self._selections = [
            SelectionItem('Twinkle Twinkle', 'Learn this song'),
            SelectionItem('CSE467s Main Theme', 'Learn this song'),
        ]

    def action_confirm(self) -> Optional[Type[Menu]]:
        self._c.set('visualizer.learn_midi.value', self._get_selected().title)
        self._state.reload()
