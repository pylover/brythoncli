from os import path

from bddcli import status, stdout, stderr, when, given


def test_pack_emptydirectory(app, tempstruct, changedir, sortlines):
    temproot = tempstruct(**{
        '.foo': {
            '__init__.py': 'i = 10',
            'baz.py': 'i = 11',
        }
    })
    changedir(temproot)
    outfile = path.join(temproot, 'bar.brython.js')

    with app('pack bar'):
        assert stderr == ''
        assert status == 0
        assert sortlines(stdout) == sortlines('''\
Generating package bar
No file to create package.
''')
        assert not path.exists(outfile)


def test_pack_pypackage(app, tempstruct, changedir, sortlines):
    temproot = tempstruct(**{
        'foo': {
            '__init__.py': 'i = 10',
            'baz.py': 'i = 11',
        }
    })
    changedir(temproot)
    outfile = path.join(temproot, 'bar.brython.js')

    with app(f'pack -d{temproot}/foo bar'):
        assert stderr == ''
        assert status == 0
        assert sortlines(stdout) == sortlines('''\
Generating package bar
Adding bar package.
Adding bar.baz module.
2 files
''')
        assert path.exists(outfile)


def test_pack_systemfiles(app, tempstruct, changedir, sortlines):
    temproot = tempstruct(**{
        '.foo': {
            '__init__.py': 'i = 10',
        },
        '.bar': {
            'baz.py': 'i = 21',
        },
        'qux': {
            '.bar.py': 'i = 31',
            'thud.py': 'i = 32',
        },
        '_fred': {
            'baz.py': 'i = 41',
        }
    })
    changedir(temproot)
    outfile = path.join(temproot, 'foo.brython.js')

    with app('pack foo'):
        assert stderr == ''
        assert status == 0
        assert sortlines(stdout) == sortlines('''\
Generating package foo
Adding qux.thud module.
1 files
''')
        assert path.exists(outfile)


def test_pack_exclude(app, tempstruct, changedir, sortlines):
    temproot = tempstruct(
        foo={
            '__init__.py': 'i = 10',
        },
        bar={
            'bar.py': 'i = 21',
            'baz.py': 'i = 22',
        }
    )
    changedir(temproot)
    outfile = path.join(temproot, 'foo.brython.js')

    with app('pack foo'):
        assert stderr == ''
        assert status == 0
        assert sortlines(stdout) == sortlines('''\
Generating package foo
Adding bar.baz module.
Adding bar.bar module.
Adding foo package.
3 files
''')
        assert path.exists(outfile)

        when(given + '-ebaz')
        assert stderr == ''
        assert status == 0
        assert path.exists(outfile)
        assert sortlines(stdout) == sortlines('''\
Generating package foo
Adding bar.bar module.
Adding foo package.
2 files
''')

        when(given + '-ebar')
        assert stderr == ''
        assert status == 0
        assert path.exists(outfile)
        assert sortlines(stdout) == sortlines('''\
Generating package foo
Adding foo package.
1 files
''')


def test_pack_simple(app, tempstruct, changedir, sortlines):
    temproot = tempstruct(
        foo={
            '__init__.py': 'i = 10',
        },
        bar={
            'bar.py': 'i = 21',
            'baz.py': 'i = 22',
        }
    )
    outfile = path.join(temproot, 'foo.brython.js')

    changedir(temproot)
    with app('pack foo'):
        assert status == 0
        assert path.exists(outfile)
        assert stderr == ''
        assert sortlines(stdout) == sortlines('''\
Generating package foo
Adding bar.baz module.
Adding bar.bar module.
Adding foo package.
3 files
''')


def test_pack_packagedirectory(app, tempstruct, sortlines):
    temproot = tempstruct(
        foo={
            '__init__.py': 'i = 10',
        },
        bar={
            'bar.py': 'i = 21',
            'baz.py': 'i = 22',
        }
    )
    outroot = tempstruct()
    outfile = path.join(outroot, 'foo.brython.js')

    with app(f'pack -d{temproot} -o{outroot} foo'):
        assert stderr == ''
        assert status == 0
        assert path.exists(outfile)
        assert sortlines(stdout) == sortlines('''\
Generating package foo
Adding bar.baz module.
Adding bar.bar module.
Adding foo package.
3 files
''')
