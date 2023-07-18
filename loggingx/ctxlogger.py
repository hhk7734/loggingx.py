import inspect
import json
import logging
from contextlib import contextmanager
from contextvars import ContextVar
from logging import LogRecord
from typing import Any, Generator

_ctx = ContextVar[dict[str, Any]]("ctxLoggerContext", default={})


def setCtxRecord() -> None:
    logging._srcfile = None  # pylint: disable=protected-access
    logging.setLogRecordFactory(CtxRecord)


@contextmanager
def addFields(reset: bool = True, **fields: Any) -> Generator[None, Any, None]:
    token = _ctx.set({**_ctx.get(), **fields})
    try:
        yield
    finally:
        if reset:
            _ctx.reset(token)


class CtxRecord(LogRecord):
    def __init__(
        self, name, level, pathname, lineno, msg, args, exc_info, func=None, sinfo=None, **kwargs
    ):
        frames = inspect.getouterframes(inspect.currentframe())
        depth = 4
        while frames[depth].filename.endswith("logging/__init__.py"):
            depth += 1

        frame = frames[depth]
        pathname = frame.filename
        lineno = frame.lineno
        func = frame.function

        # TODO: if stack_info == True, use traceback.print_stack(frame, file=sio)
        sinfo = None

        self.caller = "/".join(pathname.split("/")[-2:]) + f":{lineno}"
        self.ctxFields = _ctx.get()

        super().__init__(name, level, pathname, lineno, msg, args, exc_info, func, sinfo, **kwargs)

    def __repr__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)
