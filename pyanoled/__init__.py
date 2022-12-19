import os

Praspiano_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_conf_path(filename: str):
    return os.path.join(Praspiano_ROOT, 'conf', filename)
