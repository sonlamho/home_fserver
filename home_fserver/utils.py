"""
utils.py
"""
import sys
import os
import re
from typing import List
from functools import lru_cache
from getpass import getpass
from werkzeug import generate_password_hash
DIR = os.path.realpath(os.path.dirname(__file__))

PSWD_HASH_PATH = os.path.join(DIR, 'password_hash.txt')
INSTANCE_PATH = os.path.realpath(os.path.join(DIR, '../instance'))
CONFIG_PATH = os.path.join(INSTANCE_PATH, 'config.py')
if not os.path.exists(INSTANCE_PATH):
    os.mkdir(INSTANCE_PATH)


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


def generate_secret_key() -> None:
    print(f'new key will be at\n {CONFIG_PATH}')
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'x') as f:
            f.write('\n')
    with open(CONFIG_PATH, 'r') as f:
        lines = f.readlines()
    pos = -1
    for i, line in enumerate(lines):
        if re.match(r'SECRET_KEY *=.*', line):
            pos = i
    new_line = f'SECRET_KEY = {str(os.urandom(16))}\n'
    if pos < 0:
        lines.append(new_line)
    else:
        lines[pos] = new_line
    with open(CONFIG_PATH, 'w') as f:
        f.writelines(lines)


def get_secret_key_hex() -> str:
    p = os.path.dirname(CONFIG_PATH)
    sys.path.append(p)
    try:
        from config import SECRET_KEY  # type: ignore
    except ImportError:
        generate_secret_key()
        from config import SECRET_KEY  # type: ignore
    sys.path.remove(p)
    return SECRET_KEY.hex()


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

    def get_folder_items(self, relpath: str) -> List:
        """returns list of tuples (is_folder, fname, size)"""
        items = []
        for fname in os.listdir(self.full_path(relpath)):
            fpath = os.path.join(self.full_path(relpath), fname)
            is_folder = os.path.isdir(fpath)
            size = 0 if is_folder else os.path.getsize(fpath)
            items.append((is_folder, fname, SizeOnDisk(size)))
        sorted(items, key=lambda r: r[1])  # sort by fname
        return items

    def get_dotdot(self, relpath: str) -> str:
        up1 = re.sub(r'/[^/]+$', '', '/' + relpath.strip('/'), count=1)
        return up1.strip('/')


# This object will be available in jinja templates to get file system data
NAV = Navigator()

if __name__ == '__main__':
    if '--help' in sys.argv:
        print("""
        - Run this file with --set-pass to set the password
        - Or run with --generate-key to generate secrey key and save in
          config.py
        """)
    elif '--set-pass' in sys.argv:
        set_password()
    elif '--generate-key' in sys.argv:
        generate_secret_key()
