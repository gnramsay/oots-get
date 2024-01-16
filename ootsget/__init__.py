"""Get the version of the package."""
from importlib.metadata import (
    PackageNotFoundError,
    version,
)

try:
    # Change here if project is renamed and does not equal the package name
    __version__ = version("oots-get")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError
