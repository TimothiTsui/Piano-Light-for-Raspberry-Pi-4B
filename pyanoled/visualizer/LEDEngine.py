from pyanoled.Configuration import Configuration
from pyanoled.event.EventQueue import EventQueue
from pyanoled.event.Events import KeyEvent, PedalEvent
from pyanoled.State import State
from pyanoled.visualizer.color_schemes.Scheme import Scheme
from pyanoled.visualizer.effects.Effect import Effect

from logging import Logger
from rpi_ws281x.rpi_ws281x import Color, PixelStrip
from typing import Type, Tuple

import importlib
import math
import time


DEFAULT_COLOR_SCHEME = 'Mono'
DEFAULT_EFFECT = 'Light'

class LEDEngine(object):
    def __init__(self, l: Logger, c: Configuration, state: State,  event_queue: EventQueue):
        self._l = l
        self._c = c
        self._state = state
        self._event_queue = event_queue

        self._l.info('initializing led visualizer...')
        self._pixelstrip = PixelStrip(
            self._c.get('visualizer.strip.count'),
            self._c.get('visualizer.strip.gpio_pin'),
            freq_hz=self._c.get('visualizer.strip.frequency'),
            dma=self._c.get('visualizer.strip.dma'),
            invert=self._c.get('visualizer.strip.invert'),
            brightness=self._c.get('visualizer.strip.brightness'),
            channel=self._c.get('visualizer.strip.channel')
        )
        self._pixelstrip.begin()

        self._l.info('loading color scheme...')
        self._color_scheme = self._get_color_scheme(self._c.get('visualizer.color_scheme.value'))

        self._l.info('loading effect...')
        self._effect = self._get_effect(self._c.get('visualizer.led_effect.value'))
        self._effect.set_pixelstrip(self._pixelstrip)

    def _get_color_scheme(self, scheme: str) -> Type[Scheme]:
        try:
            if not scheme.strip():
                scheme = DEFAULT_COLOR_SCHEME
            name = '{s}Scheme'.format(s=scheme.strip())
            self._l.info('loading {s} color scheme...'.format(s=name))
            module = importlib.import_module('pyanoled.visualizer.color_schemes.{s}'.format(s=name))
        except ImportError as e:
            self._l.warning('invalid color scheme [{s}]. using default color scheme!'.format(s=scheme))
            name = '{s}Scheme'.format(s=DEFAULT_COLOR_SCHEME)
            module = importlib.import_module('pyanoled.visualizer.color_schemes.{s}'.format(s=name))

        clss = getattr(module, name)
        return clss(self._l, self._c)

    def _get_effect(self, effect: str) -> Type[Effect]:
        try:
            if not effect.strip():
                effect = DEFAULT_EFFECT
            name = '{s}Effect'.format(s=effect.strip())
            self._l.info('loading {s} effect...'.format(s=name))
            module = importlib.import_module('pyanoled.visualizer.effects.{s}'.format(s=name))
        except ImportError as e:
            self._l.warning('invalid effect [{s}]. using default effect!'.format(s=effect))
            name = '{s}Effect'.format(s=DEFAULT_EFFECT)
            module = importlib.import_module('pyanoled.visualizer.effects.{s}'.format(s=name))

        clss = getattr(module, name)
        return clss(self._l, self._c)

    def _calculate_led_index(self, event: KeyEvent) -> int:
        """
        calculates the led index for the given note number
        led index starts at 0
        :param event: note key event
        :return: led index
        """
        if event.normalized_note < 3:
            # first 3 keys align with led positions 1 to 1
            return event.normalized_note
        elif 3 <= event.normalized_note < 87:
            # for keys that repeat the 12-key pattern, recalibrate the led alignment
            start = event.normalized_note - 3
            # flat offset is used for fine-tune alignment of c-key to the led
            flat_offset = (5 - int(math.floor(start / 24) * self._c.get('visualizer.octave_alignment_drift')))
            # octave offset is for general alignment of c-key octavces to the led
            octave_offset = int(math.floor(start / 12) * 24)
            # key offset is for individual key alignment to the led relative to c-key octave
            key_offset = int(math.floor(start % 12) * 2)

            return flat_offset + octave_offset + key_offset
        else:
            # last key so use last led
            return self._c.get('visualizer.strip.count') - 1

    def _adjust_brightness(self, event: KeyEvent, color: Tuple) -> Tuple:
        """
        calculates the brightness of the color based on key velocity
        :param event: note key event
        :return: brightness percentage
        """
        if self._c.get('visualizer.brightness.force_brightness'):
            # brightness is always highest
            return color
        else:
            # velocity of 127 is high brightness and 0 is no brightness. to make led brightness difference more
            # noticeable, group the velocity into:
            # soft press : brightness reduced by 90%
            # normal press : brightness reduced by 50%
            # hard press : brightness at 100%
            if event.intensity <= self._c.get('visualizer.brightness.keypress_soft_velocity'):
                # soft press
                return tuple(map(lambda c: int(math.floor(c * self._c.get('visualizer.brightness.keypress_soft_multiplier'))), color))
            if self._c.get('visualizer.brightness.keypress_soft_velocity') < event.intensity < self._c.get('visualizer.brightness.keypress_hard_velocity'):
                # normal press
                return tuple(map(lambda c: int(math.floor(c * self._c.get('visualizer.brightness.keypress_normal_multiplier'))), color))
            else:
                # hard press
                return color

    def run(self) -> None:
        """
        main thread for lighting the led strip. reads events off of the event queue and performs:
        - determine led color
        - determine led intensity
        - enable/disable led
        :return:
        """
        self._l.info('starting led visualizer...')

        try:
            for i in range(self._c.get('visualizer.strip.count')):
                self._pixelstrip.setPixelColor(i, Color(255, 255, 255))
                self._pixelstrip.show()
                time.sleep(.01)
            for i in range(self._c.get('visualizer.strip.count')):
                self._pixelstrip.setPixelColor(i, Color(0, 0, 0))
            self._pixelstrip.show()

            while self._state.is_on():
                self._effect.pre()

                for event in self._event_queue.pop_event(1000):
                    self._l.debug('processing {n} event : {s}'.format(n=type(event).__name__, s=str(vars(event))))

                    if isinstance(event, PedalEvent):
                        if event.is_pressed:
                            self._effect.pedal_on()
                        else:
                            self._effect.pedal_off()

                    if isinstance(event, KeyEvent):
                        # translate the note number to led number
                        led_index = self._calculate_led_index(event)
                        if event.is_pressed:
                            self._l.debug('key pressed for led {l} -> note {n}'.format(l=led_index, n=event.normalized_note))
                            self._effect.key_on(led_index, self._adjust_brightness(event, self._color_scheme.get_color(event)))
                        else:
                            self._l.debug('key lifted for led {l} -> note {n}'.format(l=led_index, n=event.normalized_note))
                            self._effect.key_off(led_index, (0, 0, 0))

                self._effect.post()

                if self._effect.changed():
                    self._pixelstrip.show()
        except:
            self._l.exception('led engine error!')
            self._state.error()

        self._l.info('ending led visualizer...')
        for i in range(self._c.get('visualizer.strip.count')):
            self._pixelstrip.setPixelColor(i, Color(0, 0, 0))
        self._pixelstrip.show()
