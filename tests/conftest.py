import os
import socket
import tempfile
import shutil
from os import path

import pytest


@pytest.fixture
def changedir():
    backup = path.abspath(os.curdir)

    def _ch(d):
        os.chdir(d)

    yield _ch
    os.chdir(backup)


@pytest.fixture
def tempstruct():
    temp_directories = []

    def create_nodes(root, **kw):
        for k, v in kw.items():
            name = path.join(root, k)

            if isinstance(v, dict):
                os.mkdir(name)
                create_nodes(name, **v)
                continue

            with open(name, 'w') as f:
                f.write(v)

    def _make_temp_directory(**kw):
        """Structure example: {'a.html': 'Hello', 'b': {}}."""
        root = tempfile.mkdtemp()
        temp_directories.append(root)
        create_nodes(root, **kw)
        return root

    yield _make_temp_directory

    for d in temp_directories:
        shutil.rmtree(d)


@pytest.fixture
def freeport():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((socket.gethostname(), 0))
        return s.getsockname()[1]
    finally:
        s.close()
