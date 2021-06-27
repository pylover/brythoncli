import brython
from bddcli import Given, when, stdout, status, stderr, Application

import brythoncli


app = Application('brythoncli', 'brythoncli:Brython.quickstart')


def test_version():
    with Given(app):
        assert status == 1
        assert stderr == ''

        when('-V')
        assert status == 0
        assert stdout == \
            f'Brython: {brython.__version__}\n' \
            f'Brythoncli: {brythoncli.__version__}\n'

        when('--version')
        assert status == 0
        assert stdout == \
            f'Brython: {brython.__version__}\n' \
            f'Brythoncli: {brythoncli.__version__}\n'
