from os import path

from bddcli import Given, status, stdout, stderr, Application


app = Application('brythoncli', 'brythoncli:Brython.quickstart')


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
        assert stdout == '''\
Generating package foo
Adding bar.baz module.
Adding bar.bar module.
Adding foo package.
3 files
'''


# def test_pack_minimum_argument():
# def test_help():
