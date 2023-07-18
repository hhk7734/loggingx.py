from logging import *

from loggingx.context import CtxRecord as _CtxRecord
from loggingx.context import addFields
from loggingx.formatter import JSONFormatter

setLogRecordFactory(_CtxRecord)
