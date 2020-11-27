"""MeerTEC -- Python implemenation of the MeCom interface for Meerstetter TECs."""

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

from .meer_tec import XPort, TEC
