# mikro-napari

[![codecov](https://codecov.io/gh/jhnnsrs/mikro-napari/branch/master/graph/badge.svg?token=UGXEA2THBV)](https://codecov.io/gh/jhnnsrs/mikro-napari)
[![PyPI version](https://badge.fury.io/py/mikro-napari.svg)](https://pypi.org/project/mikro-napari/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://pypi.org/project/mikro-napari/)
![Maintainer](https://img.shields.io/badge/maintainer-jhnnsrs-blue)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/mikro-napari.svg)](https://pypi.python.org/pypi/mikro-napari/)
[![PyPI status](https://img.shields.io/pypi/status/mikro-napari.svg)](https://pypi.python.org/pypi/mikro-napari/)

mikro napari enables napari on the mikro/arkitekt platform


## Idea

This is a napari plugin, that provides a simple user interface to use napari with mikro you can view and annotate
data on the mikro platform (synchronised between all of your napari instances) and use napari within arkitekt workflows
(can be extended with other plugins)

## Install

This plugin is available on the napari plugin-manager, where you can install it through
the UI.Login with your local mikro/arkitekt platform and start using it in workflows

You can also install mikro-napari directly in your enviroment 

```bash
pip install mikro-napari napari[pyqt5]
```

## Usage

If you want to start the plugin from the command line, you can use the following command

```bash
mikro-napari
```

This  starts napari with the mikro-napari plugin enabled by default.

For more information on how to use mikro-napari check out the [documentation](https://arkitekt.live)


## Development

If you want to contribute to this project, you can clone the repository and install the package in development mode

```bash
git clone
cd mikro-napari
poetry install --all-extras
```

This will install the package in development mode and install all dependencies.


