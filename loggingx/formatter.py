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
    def format(self, record: CtxRecord) -> str:  # type: ignore[override]
        msg_dict = {
            "time": record.created,
            "level": _LEVEL_TO_LOWER_NAME[record.levelno],
        }

        msg_dict["caller"] = record.caller
        msg_dict["msg"] = record.getMessage()
        for k, v in record.ctxFields.items():
            msg_dict[k] = v

        # extra
        for k, v in record.__dict__.items():
            if k not in _DEFAULT_KEYS and not k.startswith("_"):
                msg_dict[k] = v

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            msg_dict["exc_info"] = record.exc_text

        if record.stack_info:
            msg_dict["stack_info"] = self.formatStack(record.stack_info)

        # Set ensure_ascii to False to output the message as it is typed.
        return json.dumps(msg_dict, ensure_ascii=False)
