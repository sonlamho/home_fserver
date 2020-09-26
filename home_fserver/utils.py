
import os
from typing import List
DIR = os.path.realpath(os.path.dirname(__file__))


class Navigator(object):
    BASE_DIR = os.path.join(DIR, 'www')

    def __init__(self) -> None:
        pass

    def full_path(self, relpath: str) -> str:
        return os.path.join(self.BASE_DIR, relpath.strip(' /'))

    def is_folder(self, relpath: str) -> bool:
        return os.path.isdir(self.full_path(relpath))

    def get_folder_items(self, relpath) -> List:
        """returns list of tuples (is_folder, fname, size)"""
        items = []
        for fname in os.listdir(self.full_path(relpath)):
            fpath = os.path.join(self.full_path(relpath), fname)
            is_folder = os.path.isdir(fpath)
            size = 0 if is_folder else os.path.getsize(fpath)
            items.append((is_folder, fname, size))
        sorted(items, key=lambda r: r[1])  # sort by fname
        return items


NAV = Navigator()
