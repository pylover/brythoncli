import os
import socket
import tempfile
import functools
import shutil
from os import path

import pytest
from bddcli import Given, Application


cliapp = Application('brython', 'brythoncli:Brython.quickstart')
GivenApp = functools.partial(Given, cliapp)


@pytest.fixture
def app():
    return GivenApp


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

            if hasattr(v, 'read'):
                f = v
                v = f.read()
                f.close()

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


@pytest.fixture
def here():
    return path.abspath(path.dirname(__file__))


@pytest.fixture
def sortlines():
    def sorter(s):
        return '\n'.join(sorted(s.splitlines()))
    return sorter
