
import sys
import os
from typing import List
from functools import lru_cache
from getpass import getpass
from werkzeug import generate_password_hash
DIR = os.path.realpath(os.path.dirname(__file__))

PSWD_HASH_PATH = os.path.join(DIR, 'password_hash.txt')


def set_password() -> None:
    print('Set your password.')
    p = getpass()
    print('Enter the same password again to confirm.')
    p2 = getpass()
    if p != p2:
        print('Confirmation failed. Password not set.')
    else:
        with open(PSWD_HASH_PATH, 'w') as f:
            f.write(generate_password_hash(p))
        print(f'Password hash successfully saved at {PSWD_HASH_PATH}')
    return None


class SizeOnDisk(object):
    def __init__(self, size: int):
        self.s = size

    @lru_cache()
    def __repr__(self) -> str:
        if self.s < (1 << 10):
            return f'{self.s} B'
        elif self.s < (1 << 20):
            return f'{round(self.s / (1 << 10), 2)} KB'
        elif self.s < (1 << 30):
            return f'{round(self.s / (1 << 20), 2)} MB'
        elif self.s < (1 << 40):
            return f'{round(self.s / (1 << 30), 2)} GB'
        return str(self.s)

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other) -> bool:
        return self.s == other.s

    def __lt__(self, other) -> bool:
        return self.s < other.s

    def __hash__(self) -> int:
        return hash(self.s)


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
            items.append((is_folder, fname, SizeOnDisk(size)))
        sorted(items, key=lambda r: r[1])  # sort by fname
        return items


NAV = Navigator()

if __name__ == '__main__':
    if '--help' in sys.argv:
        print("Run this file with --set-pass to set the password")
    if '--set-pass' in sys.argv:
        set_password()
