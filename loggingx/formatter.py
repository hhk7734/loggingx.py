import json
import logging
from logging import Formatter, LogRecord

from loggingx.logxrecord import LogxRecord

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
)

_LEVEL_TO_LOWER_NAME = {
    logging.CRITICAL: "fatal",
    logging.ERROR: "error",
    logging.WARNING: "warn",
    logging.INFO: "info",
    logging.DEBUG: "debug",
}


class JSONFormatter(Formatter):
    def format(self, record: LogRecord) -> str:
        msg_dict = {
            "time": record.created,
            "level": _LEVEL_TO_LOWER_NAME[record.levelno],
        }

        msg_dict["msg"] = record.getMessage()

        if isinstance(record, LogxRecord):
            msg_dict["caller"] = record.caller
        else:
            msg_dict["caller"] = "/".join(record.pathname.split("/")[-2:]) + f":{record.lineno}"

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
