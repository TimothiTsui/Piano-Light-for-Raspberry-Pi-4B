from pyanoled.Configuration import Configuration
from pyanoled.ui.displays.Display import Display
from pyanoled.ui.menus.Menu import Menu
from pyanoled.ui.menus.SelectionItem import SelectionItem
from pyanoled.State import State

from logging import Logger
from typing import Optional, Type


class EffectMenu(Menu):
    def __init__(self, l: Logger, c: Configuration, d: Type[Display], state: State, parent:Optional[Type[Menu]]):
        super().__init__(l, c, d, state, parent)

        self._title = 'Effect'
        self._description = 'LED effect to show on key/pedal press'
        self._selections = [
            SelectionItem('Fade', 'Lights and fades over time'),
            SelectionItem('Hold', 'Lights and stays on if pedal pressed'),
            SelectionItem('Light', 'Lights on/off based on key pressed'),
        ]

    def action_confirm(self) -> Optional[Type[Menu]]:
        self._c.set('visualizer.led_effect.value', self._get_selected().title)
        self._state.reload()
