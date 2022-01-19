from bs4 import BeautifulSoup
from collections import defaultdict
import json
import logging
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

def mkdir(path, root='.'):
    """
    Makes directory (and parents) if it does not exist
    """
    current = root
    for folder in path.split('/'):
        current = os.path.join(current, folder)
        if not os.path.exists(current):
            os.mkdir(current)
    return current


def get_cached(key, func, directory='.cache'):
    directory = mkdir(directory)
    path = os.path.join(directory, key)
    if not os.path.exists(path):
        content = func()
        with open(path, 'w') as f:
            f.write(content)
            print('wrote cached file', path)
    with open(path, 'r') as f:
        return f.read()


class JsonCache(dict):
    """
    A dictionary that is stored to the file system.
    """
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._path = os.path.join('.cache', name+'.json')
        if os.path.exists(self._path):
            with open(self._path, 'r') as f:
                self.update(json.loads(f.read()))
    def __setitem__(self, *args):
        super().__setitem__(*args)
        self._save()
    def _save(self):
        with open(self._path, 'w') as f:
            f.write(json.dumps(self, indent=2))


class JsonCacheSetter(JsonCache):
    """
    A cached dictionary which takes a function to evaluate instead of a dictionary value.
    If the key is not set, the function is evaluated.
    Useful when the takes a long time to compute (eg fetching a url).
    """
    def __setitem__(self, key, func):
        if key not in self:
            super().__setitem(key, func())
