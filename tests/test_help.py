from bddcli import when, stdout, status, stderr


EXPECTED_HELP = '''\
usage: brython [-h] [-V] [-C CHANGE_DIRECTORY]
               {pack,p,serve,s,pack-dependencies,pack-deps,deps,completion}
               ...

Brython command line interface

optional arguments:
  -h, --help            show this help message and exit
  -V, --version
  -C CHANGE_DIRECTORY, --change-directory CHANGE_DIRECTORY
                        Change the current working directory before executing,
                        default: ".".

Sub commands:
  {pack,p,serve,s,pack-dependencies,pack-deps,deps,completion}
    pack (p)            Creates name.brython.js file.
    serve (s)           Start Brython development server.
    pack-dependencies (pack-deps, deps)
                        Create brython_modules.js with all the modules used by
                        the application
    completion          Bash auto completion using argcomplete python package.
'''


def test_help(app):
    with app():
        assert status == 1
        assert stderr == ''
        assert stdout == EXPECTED_HELP

        when('-h')
        assert status == 0
        assert stdout == EXPECTED_HELP

        when('--help')
        assert status == 0
        assert stdout == EXPECTED_HELP
