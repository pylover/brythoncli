from os import path

from bddcli import Given, status, stdout, stderr, Application, when, given


app = Application('brythoncli', 'brythoncli:Brython.quickstart')


# def test_help():
def sortlines(s):
    return '\n'.join(sorted(s.splitlines()))


def test_pack_exclude(tempstruct, changedir):
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

    with Given(app, 'pack foo'):
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


def test_pack_simple(tempstruct, changedir):
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
    with Given(app, 'pack foo'):
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


def test_pack_packagedirectory(tempstruct):
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

    with Given(app, f'pack -d{temproot} -o{outroot} foo'):
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
