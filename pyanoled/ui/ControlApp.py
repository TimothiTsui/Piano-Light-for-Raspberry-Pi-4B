from pyanoled.Configuration import Configuration
from pyanoled.State import State
from pyanoled.ui.displays.Display import Display
from pyanoled.ui.menus.MainMenu import MainMenu

from logging import Logger
from PIL import Image, ImageDraw
from typing import Type

import importlib
import RPi.GPIO as GPIO
import time


DEFAULT_DISPLAY = 'LCD_1in3'

class ControlApp(object):
    def __init__(self, l: Logger, c: Configuration, state: State):
        self._l = l
        self._c = c
        self._state = state

        self._l.info('initializing displays...')
        self._display = self._get_display(self._c.get('ui.display'))
        self._menu = MainMenu(self._l, self._c, self._display, self._state, None)

        # key press to channel #
        self._dpad_up = 6
        self._dpad_down = 19
        self._dpad_left = 5
        self._dpad_right = 26
        self._dpad_press = 13
        self._button_a = 21
        self._button_b = 20
        self._button_c = 16

        # init gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._dpad_up, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self._dpad_down, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self._dpad_left, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self._dpad_right, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self._dpad_press, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self._button_a, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self._button_b, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self._button_c, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(self._dpad_up, GPIO.RISING)
        GPIO.add_event_detect(self._dpad_down, GPIO.RISING)
        GPIO.add_event_detect(self._dpad_left, GPIO.RISING)
        GPIO.add_event_detect(self._dpad_right, GPIO.RISING)
        GPIO.add_event_detect(self._dpad_press, GPIO.RISING)
        GPIO.add_event_detect(self._button_a, GPIO.RISING)
        GPIO.add_event_detect(self._button_b, GPIO.RISING)
        GPIO.add_event_detect(self._button_c, GPIO.RISING)

    def _get_display(self, display: str) -> Type[Display]:
        try:
            if not display.strip():
                name = DEFAULT_DISPLAY
            name = '{s}Display'.format(s=display.strip())
            self._l.info('loading {s} displays...'.format(s=name))
            module = importlib.import_module('pyanoled.ui.displays.{s}'.format(s=name))
        except ImportError as e:
            self._l.warning('invalid displays {s}. using default displays!'.format(s=name))
            name = '{s}Display'.format(s=DEFAULT_DISPLAY)
            module = importlib.import_module('pyanoled.ui.displays.{s}'.format(s=name))

        clss = getattr(module, name)
        return clss(self._l)

    def run(self) -> None:
        self._l.info('starting control menu...')

        try:
            str_disp = 'Starting control menu...'

            self._display.show(str_disp)
            time.sleep(2)

            self._menu.show()

            while self._state.is_on():
                if GPIO.event_detected(self._dpad_up):
                    self._l.debug('dpad up pressed')
                    self._menu.action_up()
                    self._menu.show()
                if GPIO.event_detected(self._dpad_down):
                    self._l.debug('dpad down pressed')
                    self._menu.action_down()
                    self._menu.show()
                if GPIO.event_detected(self._dpad_left):
                    self._l.debug('dpad left pressed')
                    pass
                if GPIO.event_detected(self._dpad_right):
                    self._l.debug('dpad right pressed')
                    pass
                if GPIO.event_detected(self._dpad_press):
                    self._l.debug('dpad pressed')
                    pass
                if GPIO.event_detected(self._button_a):
                    self._l.debug('button a pressed')
                    m = self._menu.action_confirm()
                    if m:
                        self._menu = m
                        self._menu.show()
                if GPIO.event_detected(self._button_b):
                    self._l.debug('button b pressed')
                    pass
                if GPIO.event_detected(self._button_c):
                    self._l.debug('button c pressed')
                    m = self._menu.action_back()
                    if m:
                        self._menu = m
                        self._menu.show()
                    pass

                time.sleep(.01)
        except:
            self._l.exception('control menu error!')
            self._state.error()

        self._l.info('ending control menu...')
        self._display.clear()
        GPIO.cleanup()
