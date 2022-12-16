from pyanoled.Configuration import Configuration
from pyanoled.event.Events import KeyEvent, PedalEvent
from pyanoled.event.EventQueue import EventQueue
from pyanoled.State import State

from logging import Logger

import mido


class MIDIReader(object):
    def __init__(self, l: Logger, c: Configuration, state: State, event_queue: EventQueue):
        self._l = l
        self._c = c
        self._state = state
        self._event_queue = event_queue

        self._l.info('initializing midi listener...')

        # open input port based on information from config
        self._input_port = mido.open_input([s for s in mido.get_input_names() if s.startswith(self._c.get('midi.piano_port_name'))][0])

    def run(self):
        """
        main thread for reading piano events from midi port. continuously listens on the input midi port for messages
        and:
        - filters out the pertinent events
        - converts to event instances
        - adds to event queue
        :return:
        """
        self._l.info('starting midi listener...')

        try:
            while self._state.is_on():
                # listen on input port for messages and extract out the pertinent ones
                pending = []
                for m in self._input_port.iter_pending():
                    if m.type == 'note_on' and KeyEvent.MIN_NOTE <= m.note <= KeyEvent.MAX_NOTE:
                        self._l.debug('key event : {s}'.format(s=str(vars(m))))
                        pending.append(KeyEvent(m))
                    elif m.type == 'control_change' and m.control == PedalEvent.PEDAL_VAL:
                        self._l.debug('pedal event : {s}'.format(s=str(vars(m))))
                        pending.append(PedalEvent(m))

                # append events to queue...rinse and repeat
                if len(pending):
                    self._event_queue.push_event(pending)
        except:
            self._l.exception('midi reader error!')
            self._state.error()

        self._l.info('ending midi listener...')
        self._input_port.close()