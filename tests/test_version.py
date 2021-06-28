import brython
from bddcli import when, stdout, status, stderr

import brythoncli


def test_version(app):
    with app():
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
