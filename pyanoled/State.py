from threading import Lock


class State(object):
    STATE_ON = 'on'
    STATE_OFF = 'off'
    STATE_RELOAD = 'reload'
    STATE_ERROR = 'error'

    def __init__(self):
        self._state = self.STATE_ON
        self._lock = Lock()

    def is_on(self):
        with self._lock:
            return self._state == self.STATE_ON

    def is_reload(self):
        with self._lock:
            return self._state == self.STATE_RELOAD

    def is_off(self):
        with self._lock:
            return self._state == self.STATE_OFF

    def is_error(self):
        with self._lock:
            return self._state == self.STATE_ERROR

    def on(self):
        with self._lock:
            self._state = self.STATE_ON

    def off(self):
        with self._lock:
            self._state = self.STATE_OFF

    def reload(self):
        with self._lock:
            self._state = self.STATE_RELOAD

    def error(self):
        with self._lock:
            self._state = self.STATE_ERROR