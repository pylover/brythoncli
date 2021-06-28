[![Build](https://github.com/pylover/brythoncli/actions/workflows/build.yml/badge.svg)](https://github.com/pylover/brythoncli/actions/workflows/build.yml)
[![Coverage Status](https://coveralls.io/repos/github/pylover/brythoncli/badge.svg?branch=master)](https://coveralls.io/github/pylover/brythoncli?branch=master)
[![Linux](https://img.shields.io/badge/Linux-%3E%3D%203.19-blue?logo=linux&logoColor=white)](https://kernel.org)


# brythoncli

## Install

```bash
pip install brythoncli
```

Or, from the source:

```bash
cd path/to/brythoncli
pip install .
```

## Usage

```bash
barython pack --help
barython serve --help
barython deps --help
```

Checkout the `Makefile` at the root of https://github.com/dobisel/dial
for more info.

## Contribution

```bash
cd path/to/brythoncli
pip install -r requirements-dev.txt
pip install -e .
make test
make cover
```



