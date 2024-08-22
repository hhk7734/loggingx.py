import logging
import re
from datetime import datetime
from enum import Enum
from logging import Formatter
from typing import List, Union

from . import json
from .context import CtxRecord

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

_LEVEL_TO_UPPER_NAME = {k: v.upper() for k, v in _LEVEL_TO_LOWER_NAME.items()}


class Information(str, Enum):
    NAME = "name"
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
        self._key_map = {x.value: re.sub(r"(?<!^)(?=[A-Z])", "_", x.value).lower() for x in additional_infos}

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

        return json.dumps(msg_dict)


_RESET = "\033[0m"
_RED_BG = "\033[30;41m"
_GREEN_BG = "\033[30;42m"
_YELLOW_BG = "\033[30;43m"


class ConsoleFormatter(Formatter):
    def __init__(
        self,
        additional_infos: Union[Information, List[Information], None] = None,
        color: bool = True,
    ) -> None:
        super().__init__()
        if additional_infos is None:
            additional_infos = []
        elif isinstance(additional_infos, Information):
            additional_infos = [additional_infos]

        self._excludes = {x.value for x in Information if x not in additional_infos}
        self._key_map = {x.value: re.sub(r"(?<!^)(?=[A-Z])", "_", x.value).lower() for x in additional_infos}

        self._color = color

    def format(self, record: CtxRecord) -> str:  # type: ignore[override]
        rfc3339 = datetime.fromtimestamp(record.created).astimezone().isoformat(sep="T", timespec="milliseconds")

        extra = {}
        for k, v in record.ctxFields.items():
            extra[k] = v

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
            extra[k] = v

        color = ""
        reset = ""
        if self._color:
            if record.levelno >= logging.ERROR:
                color = _RED_BG
            elif record.levelno >= logging.WARNING:
                color = _YELLOW_BG
            elif record.levelno >= logging.INFO:
                color = _GREEN_BG

            if record.levelno >= logging.INFO:
                reset = _RESET

        # Set ensure_ascii to False to output the message as it is typed.
        msg = f"{rfc3339} {color}{_LEVEL_TO_UPPER_NAME[record.levelno]:<6}{reset} {record.caller}\t{record.getMessage()} {json.dumps(extra)}"

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            msg += f"\n{record.exc_text}"

        if record.stack_info:
            msg += f"\n{self.formatStack(record.stack_info)}"

        return msg
