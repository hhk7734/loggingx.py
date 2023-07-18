from logging import *

from loggingx.context import CtxRecord as _CtxRecord
from loggingx.context import addFields
from loggingx.formatter import JSONFormatter

setLogRecordFactory(_CtxRecord)
addLevelName(CRITICAL, "fatal")
addLevelName(ERROR, "error")
addLevelName(WARNING, "warn")
addLevelName(INFO, "info")
addLevelName(DEBUG, "debug")
addLevelName(NOTSET, "notset")
