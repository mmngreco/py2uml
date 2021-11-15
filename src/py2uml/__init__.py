from ._version import get_versions
from .core import cli

__version__ = get_versions()['version']
del get_versions


if __name__ == "__main__":
    cli()
