from pyhocon import ConfigFactory, ConfigTree
from typing import Any, Dict


class Configuration(object):
    def __init__(self, file: str):
        self._file = file
        self._c = ConfigFactory.parse_file(self._file)
        self._m = {}

    @property
    def log_configuration(self) -> ConfigTree:
        return self._c['log']

    def get(self, key: str) -> Any:
        if key not in self._m:
            self._m[key] = self._c[key]

        return self._m[key]

    def set(self, key: str, value: Any) -> None:
        if key not in self._m:
            raise Exception('invalid key {k}'.format(k=key))

        self._m[key] = value