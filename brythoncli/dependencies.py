from os import path

from brython import list_modules


def pack(outdir, filename):
    print(
        'Create brython_modules.js with all the modules used by the '
        'application'
    )

    print('Searching brython_stdlib.js...')
    stdlib_dir, stdlib = list_modules.load_stdlib_sitepackages()

    print('Finding packages...')
    user_modules = list_modules.load_user_modules()
    finder = list_modules.ModulesFinder(
        stdlib=stdlib,
        user_modules=user_modules
    )
    finder.inspect()
    outfilename = path.join(outdir, filename)
    finder.make_brython_modules(outfilename)
