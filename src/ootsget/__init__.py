import sys

if sys.version_info[:2] >= (3, 8):
    from importlib.metadata import (
        PackageNotFoundError,
        version,
    )  # pragma: no cover
else:
    from importlib_metadata import (
        PackageNotFoundError,
        version,
    )  # pragma: no cover

try:
    # Change here if project is renamed and does not equal the package name
    __version__ = version("oots-get")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
