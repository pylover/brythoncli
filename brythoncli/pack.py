import os
import ast
import time
import json


from brython import make_package, python_minifier


def create_package(package_name, package_path, exclude_dirs=None,
                   output_path=None):
    if not package_name:
        raise ValueError("package name is not specified")
    print("Generating package {}".format(package_name))
    VFS = {"$timestamp": int(1000 * time.time())}
    has_init = os.path.exists(os.path.join(package_path, "__init__.py"))
    nb = 0
    if exclude_dirs is None:
        exclude_dirs = []
    for dirpath, dirnames, filenames in os.walk(package_path):
        # TODO: Remove it, not used, reported by pyflake.
        # flag = False
        root_elts = dirpath.split(os.sep)
        for exclude in exclude_dirs:
            if exclude in root_elts:
                continue
        if '__pycache__' in dirnames:
            dirnames.remove("__pycache__")

        if dirpath == package_path:
            package = []
        else:
            package = dirpath[len(package_path) + 1:].split(os.sep)
        if has_init:
            package.insert(0, package_name)

        for filename in filenames:
            name, ext = os.path.splitext(filename)
            if ext != '.py':
                continue
            is_package = name.endswith('__init__')
            if is_package:
                mod_name = '.'.join(package)
            else:
                mod_name = '.'.join(package + [name])

            nb += 1
            absname = os.path.join(dirpath, filename)
            with open(absname, encoding='utf-8') as f:
                data = f.read()

            data = python_minifier.minify(data, preserve_lines=True)
            path_elts = package[:]
            if os.path.basename(filename) != "__init__.py":
                path_elts.append(os.path.basename(filename)[:-3])

            # TODO: Remove it, not used, reported by pyflake.
            # fqname = ".".join(path_elts)
            with open(absname, encoding="utf-8") as f:
                tree = ast.parse(f.read())
                visitor = make_package.Visitor(package_path, package)
                visitor.visit(tree)
                imports = sorted(list(visitor.imports))

            if is_package:
                VFS[mod_name] = [ext, data, imports, 1]
            else:
                VFS[mod_name] = [ext, data, imports]

            print(
                f'Adding {mod_name} {"package" if is_package else "module"}.')

    if nb == 0:
        print("No Python file found in current directory")
    else:
        print('{} files'.format(nb))

        output_path = output_path or os.path.join(
            package_path,
            package_name + ".brython.js"
        )
        with open(output_path, "w", encoding="utf-8") as out:
            out.write('__BRYTHON__.use_VFS = true;\n')
            out.write('var scripts = {}\n'.format(json.dumps(VFS)))
            out.write('__BRYTHON__.update_VFS(scripts)\n')
