import signal
import time

from bddcli import Given, stdout, status, stderr, Application
from requests import get


app = Application('brythoncli', 'brythoncli:Brython.quickstart')


def test_serve(freeport):
    with Given(app, f'serve -p{freeport}', nowait=True) as s:
        url = f'http://localhost:{freeport}'
        time.sleep(.5)
        resp = get(url)
        assert resp.status_code == 200

        resp = get(f'{url}/cpython_site_packages/brython/__main__.py')
        assert resp.status_code == 200

        resp = get(f'{url}/cpython_site_packages/brython/data/brython.js')
        assert resp.status_code == 200
        s.kill(signal.SIGINT)
        s.wait()
        assert status == -2
        assert stdout == f'''\
Brython development server. Not meant to be used in production.
Press CTRL+C to Quit.
Serving HTTP on 0.0.0.0 port {freeport} (http://0.0.0.0:{freeport}/) ...

Keyboard interrupt received, exiting.
'''
        assert len(stderr.splitlines()) == 3
