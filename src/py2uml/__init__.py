from ._version import get_versions
from . import core


__version__ = get_versions()['version']
del get_versions


if __name__ == "__main__":
    core.cli()
