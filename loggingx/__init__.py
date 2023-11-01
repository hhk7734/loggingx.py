from importlib.metadata import PackageNotFoundError, version
from logging import *

from loggingx.context import CtxRecord as _CtxRecord
from loggingx.context import addFields
from loggingx.formatter import Information, JSONFormatter

try:
    __version__ = version("loggingx-py")

except PackageNotFoundError:
    pass


setLogRecordFactory(_CtxRecord)
