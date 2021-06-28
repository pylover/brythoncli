from os import path

from bddcli import status, stdout, stderr


def test_packdependencies(app, tempstruct, here, sortlines):
    temproot = tempstruct(**{
        'foo': {
            '__init__.py': 'i = 10',
            'baz.py': 'i = 11',
        },
        'brython_stdlib.js': open(path.join(here, 'stuff/brython_stdlib.js'))
    })
    outfile = path.join(temproot, 'brython_module.js')

    with app(f' -C{temproot} pack-deps'):
        assert stderr == ''
        assert status == 0
        assert sortlines(stdout) == sortlines('''\
Create brython_modules.js with all the modules used by the application
Finding packages...
Searching brython_stdlib.js...
''')
        assert not path.exists(outfile)
