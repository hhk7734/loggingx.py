import inspect
import json
import logging
from logging import Formatter, LogRecord

logging._srcfile = None  # pylint: disable=protected-access

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

        frames = inspect.getouterframes(inspect.currentframe())
        depth = 7
        while frames[depth].filename.endswith("logging/__init__.py"):
            depth += 1

        msg_dict["caller"] = (
            "/".join(frames[depth].filename.split("/")[-2:]) + f":{frames[depth].lineno}"
        )

        msg_dict["msg"] = record.getMessage()

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
