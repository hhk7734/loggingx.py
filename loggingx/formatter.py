import json
import logging
from logging import Formatter

from loggingx.context import CtxRecord

# https://docs.python.org/3/library/logging.html#logrecord-attributes
_DEFAULT_KEYS = (
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    # CtxRecord
    "caller",
    "ctxFields",
)

_LEVEL_TO_LOWER_NAME = {
    logging.CRITICAL: "fatal",
    logging.ERROR: "error",
    logging.WARNING: "warn",
    logging.INFO: "info",
    logging.DEBUG: "debug",
    logging.NOTSET: "notset",
}


class JSONFormatter(Formatter):
    def format(self, record: CtxRecord) -> str:
        msg_dict = {
            "time": record.created,
            "level": _LEVEL_TO_LOWER_NAME[record.levelno],
        }

        msg_dict["caller"] = record.caller
        msg_dict["msg"] = record.getMessage()
        for k, v in record.ctxFields.items():
            msg_dict[k] = v

        # TODO: record.exc_info
        # TODO: record.exc_text
        # TODO: record.stack_info

        # extra
        if (extra := record.__dict__.get("extra", None)) is None:
            extra = record.__dict__
        for k, v in extra.items():
            if k not in _DEFAULT_KEYS and not k.startswith("_"):
                msg_dict[k] = v

        # Set ensure_ascii to False to output the message as it is typed.
        return json.dumps(msg_dict, ensure_ascii=False)
