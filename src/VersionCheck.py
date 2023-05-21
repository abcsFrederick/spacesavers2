import sys

global __version__
__version__ = 'v0.4'

def version_check():
    # version check
    # glob.iglob requires 3.11 for using "include_hidden=True"
    MIN_PYTHON = (3, 11)
    try:
        assert sys.version_info >= MIN_PYTHON
    except AssertionError:
        exit(f"{sys.argv[0]} requires Python {'.'.join([str(n) for n in MIN_PYTHON])} or newer")

