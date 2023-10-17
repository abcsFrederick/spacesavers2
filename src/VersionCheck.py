import sys
import os

global __version__
current_path = os.path.dirname(os.path.abspath(__file__))
vfile = open(os.path.join(current_path, "VERSION"), "r")
__version__ = "v" + vfile.read()
__version__ = __version__.strip()
vfile.close()


def version_check():
    # version check
    # glob.iglob requires 3.11 for using "include_hidden=True"
    MIN_PYTHON = (3, 11)
    try:
        assert sys.version_info >= MIN_PYTHON
    except AssertionError:
        exit(
            f"{sys.argv[0]} requires Python {'.'.join([str(n) for n in MIN_PYTHON])} or newer"
        )


def version_print():
    exit(f"version: {__version__}")
