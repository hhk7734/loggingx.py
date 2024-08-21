import logging as _logging
from importlib.metadata import PackageNotFoundError, version
from logging import *  # noqa: F403

from .context import CtxRecord as _CtxRecord
from .context import addFields
from .formatter import ConsoleFormatter, Information, JSONFormatter

try:
    __version__ = version("loggingx-py")

except PackageNotFoundError:
    pass

__all__ = _logging.__all__.copy()
__all__ += ["addFields", "Information", "JSONFormatter", "ConsoleFormatter"]


setLogRecordFactory(_CtxRecord)  # noqa: F405
