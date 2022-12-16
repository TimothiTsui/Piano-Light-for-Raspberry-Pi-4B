from pyanoled import get_conf_path
from pyanoled.Configuration import Configuration
from pyanoled.device.MIDIReader import MIDIReader
from pyanoled.event.EventQueue import EventQueue
from pyanoled.State import State
from pyanoled.ui.ControlApp import ControlApp
from pyanoled.visualizer.LEDEngine import LEDEngine
from logging import config, getLogger, Logger

import concurrent.futures
import re
import subprocess


class PyanoLED(object):
    def __init__(self, l: Logger, c: Configuration):
        self._l = l
        self._c = c
        self._port_regex = re.compile(r"^client (\d+): '(.*)'", re.IGNORECASE | re.ASCII)

    def _unlink_ports(self) -> None:
        subprocess.call('aconnect -x', shell=True)
        self._l.info('ports unlinked...')

    def _link_ports(self) -> None:
        piano_port = None
        rpi_port = None

        response = subprocess.run('aconnect -l', shell=True, capture_output=True)
        for l in response.stdout.decode('utf-8').split('\n'):
            found = self._port_regex.findall(l)
            if found:
                if found[0][1] == self._c.get('midi.piano_port_name'):
                    self._l.info(f"piano port identified as: {found[0][0]}")
                    piano_port = found[0][0]
                if found[0][1] == self._c.get('midi.rpi_port_name'):
                    self._l.info(f"rpi port identified as: {found[0][0]}")
                    rpi_port = found[0][0]

        if piano_port and rpi_port and piano_port != rpi_port:
            subprocess.call(f"aconnect {piano_port}:0 {rpi_port}:0", shell=True)
            self._l.info('ports linked...')

    def run(self):
        self._l.info('================================== PYANOLED START ==================================')

        event_queue = EventQueue()
        state = State()

        self._unlink_ports()
        self._link_ports()

        while state.is_on() or state.is_reload():
            if state.is_reload():
                self._l.info('reloading pyanoled...')
                self._unlink_ports()
                self._link_ports()
                state.on()

            ui_thread = ControlApp(getLogger('ui'), self._c, state)
            visualizer_thread = LEDEngine(getLogger('visualizer'), self._c, state, event_queue)
            midi_thread = MIDIReader(getLogger('midi'), self._c, state, event_queue)
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                executor.submit(ui_thread.run)
                executor.submit(visualizer_thread.run)
                executor.submit(midi_thread.run)

        self._l.info('================================== PYANOLED END ==================================')

        if state.is_off():
            self._unlink_ports()
            subprocess.call("sudo shutdown -h now", shell=True)

def main():
    c = Configuration(get_conf_path('cse467s.conf'))
    config.dictConfig(c.log_configuration)

    app = PyanoLED(getLogger('pyanoled'), c)
    app.run()

if __name__ == "__main__":
    main()
