import json
import logging
import re
from enum import Enum
from logging import Formatter
from typing import List, Union

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
    "relativeCreated",
    "stack_info",
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


class Information(str, Enum):
    THREAD = "thread"
    THREAD_NAME = "threadName"
    PROCESS = "process"
    PROCESS_NAME = "processName"


class JSONFormatter(Formatter):
    def __init__(
        self,
        additional_infos: Union[Information, List[Information], None] = None,
    ) -> None:
        super().__init__()
        if additional_infos is None:
            additional_infos = []
        elif isinstance(additional_infos, Information):
            additional_infos = [additional_infos]

        self._excludes = {x.value for x in Information if x not in additional_infos}
        self._key_map = {
            x.value: re.sub(r"(?<!^)(?=[A-Z])", "_", x.value).lower() for x in additional_infos
        }

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
            if k in _DEFAULT_KEYS:
                continue
            if k.startswith("_"):
                continue
            if k in self._excludes:
                continue
            if k in self._key_map:
                k = self._key_map[k]
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
