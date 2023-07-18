import json
from contextlib import contextmanager
from contextvars import ContextVar
from logging import LogRecord
from types import TracebackType
from typing import Any, Generator, Mapping, TypeAlias

_SysExcInfoType: TypeAlias = (
    tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None]
)
_ArgsType: TypeAlias = tuple[object, ...] | Mapping[str, object]


_ctx = ContextVar[dict[str, Any]]("loggingxCtx", default={})


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
        self,
        name: str,
        level: int,
        pathname: str,
        lineno: int,
        msg: object,
        args: _ArgsType | None,
        exc_info: _SysExcInfoType | None,
        func: str | None = None,
        sinfo: str | None = None,
        **kwargs,
    ):
        super().__init__(
            name,
            level,
            pathname,
            lineno,
            msg,
            args,
            exc_info,
            func,
            sinfo,
            **kwargs,
        )
        self.caller = "/".join(pathname.split("/")[-2:]) + f":{lineno}"
        self.ctxFields = _ctx.get()

    def __repr__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)
