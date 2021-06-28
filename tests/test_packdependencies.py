from os import path

from bddcli import status, stdout, stderr


def test_packdependencies_simple(app, tempstruct, here, sortlines):
    temproot = tempstruct(**{
        'foo': {
            '__init__.py': 'i = 10',
            'baz.py': 'i = 11',
        },
        'brython_stdlib.js': open(path.join(here, 'stuff/brython_stdlib.js'))
    })
    outfile = path.join(temproot, 'brython_modules.js')

    with app(f'-C {temproot} pack-deps'):
        assert stderr == ''
        assert status == 0
        assert sortlines(stdout) == sortlines('''\
Create brython_modules.js with all the modules used by the application
Finding packages...
Searching brython_stdlib.js...
''')
        assert path.exists(outfile)


def test_packdependencies_outputdirextory(app, tempstruct, here, sortlines):
    temproot = tempstruct(**{
        'foo': {
            '__init__.py': 'i = 10',
            'baz.py': 'i = 11',
        },
        'brython_stdlib.js': open(path.join(here, 'stuff/brython_stdlib.js'))
    })
    destdir = tempstruct()
    outfile = path.join(destdir, 'brython_modules.js')

    with app(f'-C {temproot} pack-deps --output {destdir}'):
        assert stderr == ''
        assert status == 0
        assert sortlines(stdout) == sortlines('''\
Create brython_modules.js with all the modules used by the application
Finding packages...
Searching brython_stdlib.js...
''')
        assert path.exists(outfile)


def test_packdependencies_filename(app, tempstruct, here, sortlines):
    temproot = tempstruct(**{
        'foo': {
            '__init__.py': 'i = 10',
            'baz.py': 'i = 11',
        },
        'brython_stdlib.js': open(path.join(here, 'stuff/brython_stdlib.js'))
    })
    outfile = path.join(temproot, 'libs.js')

    with app(f'-C {temproot} pack-deps --filename libs.js'):
        assert stderr == ''
        assert status == 0
        assert sortlines(stdout) == sortlines('''\
Create brython_modules.js with all the modules used by the application
Finding packages...
Searching brython_stdlib.js...
''')
        assert path.exists(outfile)


def test_packdependencies_searchdirectory(app, tempstruct, here, sortlines):
    temproot = tempstruct(**{
        'foo': {
            '__init__.py': 'i = 10',
            'baz.py': 'i = 11',
        },
        'brython_stdlib.js': open(path.join(here, 'stuff/brython_stdlib.js'))
    })
    destdir = tempstruct()
    outfile = path.join(destdir, 'brython_modules.js')
    stdlib = temproot
    with app(f'-C {destdir} deps --search {temproot}/foo --stdlib {stdlib}'):
        assert stderr == ''
        assert status == 0
        assert sortlines(stdout) == sortlines('''\
Create brython_modules.js with all the modules used by the application
Finding packages...
Searching brython_stdlib.js...
''')
        assert path.exists(outfile)
