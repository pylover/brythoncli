from easycli import Root, Argument, SubCommand


EXIT_SUCCESS = 0
EXIT_FAILURE = 1


class Serve(SubCommand):
    __command__ = 'serve'
    __aliases__ = ['s']
    __help__ = 'Start Brython development server.'
    __arguments__ = [
        Argument(
            '-p', '--port',
            default=8080,
            type=int,
            help='The TCP port to bind. default: 8080.'
        ),
    ]

    def __call__(self, args):
        from .httpserver import start
        start(args.port)


class Pack(SubCommand):
    __command__ = 'pack'
    __aliases__ = ['p']
    __help__ = 'Creates name.brython.js file.'
    __arguments__ = [
        Argument('name', help='Name for newly generated package.'),
        Argument(
            '-d', '--package-directory',
            default='.',
            help='The directory to search for the package, default: ".".'
        ),
        Argument(
            '-o', '--output-directory',
            default='.',
            help='The directory to generate the brython package, default: ".".'
        ),
        Argument(
            '-e', '--exclude',
            action='append',
            help='Package name to exclude. this option can be specified '
                 'multiple times.'
        )
    ]

    def __call__(self, args):
        from .pack import create_package
        create_package(
            args.name,
            args.package_directory,
            excludes=args.exclude,
            outpath=args.output_directory
        )


class Brython(Root):
    __completion__ = True
    __help__ = 'Brython command line interface'
    __arguments__ = [
        Argument('-V', '--version', action='store_true'),
        Pack,
        Serve,
    ]

    def __call__(self, args):
        if args.version:
            import brythoncli
            import brython
            print(f'Brython: {brython.__version__}')
            print(f'Brythoncli: {brythoncli.__version__}')
            return

        self._parser.print_help()
        return EXIT_FAILURE
