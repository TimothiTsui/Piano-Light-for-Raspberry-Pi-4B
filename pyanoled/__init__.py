import os

PYANOLED_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_conf_path(filename: str):
    return os.path.join(PYANOLED_ROOT, 'conf', filename)
