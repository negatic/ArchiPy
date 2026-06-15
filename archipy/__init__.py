"""ArchiPy - Architecture + Python framework for structured design."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("archipy")
except PackageNotFoundError:
    __version__ = "0.0.0"
