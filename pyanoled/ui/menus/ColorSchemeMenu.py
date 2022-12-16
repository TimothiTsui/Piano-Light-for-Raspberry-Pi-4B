from pyanoled.Configuration import Configuration
from pyanoled.ui.displays.Display import Display
from pyanoled.ui.menus.Menu import Menu
from pyanoled.ui.menus.SelectionItem import SelectionItem
from pyanoled.State import State

from logging import Logger
from typing import Optional, Type


class ColorSchemeMenu(Menu):
    def __init__(self, l: Logger, c: Configuration, d: Type[Display], state: State, parent:Optional[Type[Menu]]):
        super().__init__(l, c, d, state, parent)

        self._title = 'Color Scheme'
        self._description = 'LED color to show on key press'
        self._selections = [
            SelectionItem('Chaos', 'Random color everytime'),
            SelectionItem('Divided', '2 colors split on middle C'),
            SelectionItem('Key', '2 colors for key color'),
            SelectionItem('Mono', '1 color for all')
        ]

    def action_confirm(self) -> Optional[Type[Menu]]:
        self._c.set('visualizer.color_scheme.value', self._get_selected().title)
        self._state.reload()
