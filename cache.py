import json
import os
import urllib.error
import urllib.request

from utils import url_split


def mkdir(path, root="."):
    """
    Makes directory (and parents) if it does not exist
    """
    current = root
    for folder in path.split("/"):
        current = os.path.join(current, folder)
        if not os.path.exists(current):
            os.mkdir(current)
    return current


def get_cached(key, func, directory=".cache"):
    directory = mkdir(directory)
    path = os.path.join(directory, key)
    if not os.path.exists(path):
        content = func()
        with open(path, "w") as f:
            f.write(content)
            print("wrote cached file", path)
    with open(path, "r") as f:
        return f.read()


def curl_cached(url, key=None):
    domain, path = url_split(url)
    if key is None:
        key = path.replace("/", "__")
    if len(key) > 255:
        key = key[:255]  # max wilename length is 255

    def get():
        req = urllib.request.Request(url)
        r = urllib.request.urlopen(req)
        return r.read().decode()

    return get_cached(key, get, os.path.join(".cache", domain))


class JsonCache(dict):
    """
    A dictionary that is stored to the file system.
    """

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._path = os.path.join(".cache", name + ".json")
        if os.path.exists(self._path):
            with open(self._path, "r") as f:
                self.update(json.loads(f.read()))

    def __setitem__(self, *args):
        super().__setitem__(*args)
        self._save()

    def _save(self):
        with open(self._path, "w") as f:
            f.write(json.dumps(self, indent=2))


class JsonCacheSetter(JsonCache):
    """
    A cached dictionary which takes a function instead of a dictionary value.
    If the key is not set, the function is evaluated.
    Useful when the takes a long time to compute (eg fetching a url).
    """

    def __setitem__(self, key, func):
        if key not in self:
            super().__setitem(key, func())
